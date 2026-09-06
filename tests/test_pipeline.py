import copy
import json
from pathlib import Path
from unittest.mock import Mock
import numpy as np
import pytest
from astropy.io import fits
from astropy.table import Table
from reproject import reproject_interp
from pipeline.core import (
    normalize_mpc,
    normalize_sbdb,
    normalize_horizons,
    import_candidates,
    write,
    load,
)
from pipeline.render import output_wcs, sky_center, read_fits, render_sequence
from pipeline.sources import (
    fetch_cutout,
    request,
    UpstreamError,
    most_results_url,
    parse_most,
)
from pipeline.validate import validate

FIX = Path(__file__).parent / "fixtures"


def test_mpc_pairs_fractional_date_and_band():
    result = normalize_mpc(load(FIX / "mpc.json"), "2026-09-05T00:00:00Z")
    assert (result["record_count"], result["count"], result["continuation_count"]) == (
        5066,
        4316,
        750,
    )
    assert next(s["count"] for s in result["stations"] if s["code"] == "C57") == 738
    assert result["recent"][0]["band"] == "w"
    assert result["recent"][0]["observed_at"].startswith("2026-09-05T11:47:")
    assert sum("continuation" in r for r in result["records"]) == 750


def test_mpc_rejects_orphan_continuation():
    raw = load(FIX / "mpc.json")
    lines = raw[0]["OBS80"].splitlines()
    i = next(i for i, s in enumerate(lines) if s[14] == "s")
    lines.pop(i - 1)
    raw[0]["OBS80"] = "\n".join(lines)
    with pytest.raises(ValueError, match="Unpaired"):
        normalize_mpc(raw, "now")


def test_source_identity_and_horizons_columns():
    o = normalize_sbdb(load(FIX / "sbdb.json"), "now")
    assert o["orbit"]["elements"]["a"]["value"] == pytest.approx(2.73997996675)
    e = normalize_horizons(load(FIX / "horizons.json"), "now")
    assert e["samples"][0]["v_mag"] == 18.767
    assert e["samples"][0]["earth_distance_au"] == pytest.approx(2.20445361)
    raw = load(FIX / "horizons.json")
    raw["result"] = raw["result"].replace("20220 Beebe", "12345 Other")
    with pytest.raises(ValueError):
        normalize_horizons(raw, "now")


def test_ra_wrap_and_reprojection_preserve_stars():
    c = sky_center([(359.999, 5), (0.001, 5)])
    assert min(c.lon.deg, 360 - c.lon.deg) < 0.00001
    target = output_wcs([(1, 5)], 120, 120)
    source = target.deepcopy()
    a = np.deg2rad(15)
    source.wcs.pc = [[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]
    yy, xx = np.mgrid[:120, :120]
    ra, dec = target.pixel_to_world_values(48, 61)
    x, y = source.world_to_pixel_values(ra, dec)
    image = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * 1.5**2))
    aligned, _ = reproject_interp((image, source), target, shape_out=(120, 120))
    py, px = np.unravel_index(np.nanargmax(aligned), aligned.shape)
    assert abs(px - 48) <= 1 and abs(py - 61) <= 1


def test_render_is_idempotent_and_marker_moves(tmp_path):
    rng = np.random.default_rng(4)
    w = output_wcs([(1, 5)], 480, 480)
    data = rng.normal(100, 4, (480, 480))
    paths = {}
    rows = []
    for i in range(3):
        ra, dec = w.pixel_to_world_values(220 + i * 6, 240)
        p = tmp_path / f"{i}.fits"
        fits.writeto(p, data, w.to_header())
        paths[str(i)] = p
        rows.append(
            {
                "id": str(i),
                "ra": float(ra),
                "dec": float(dec),
                "observed_at": f"2026-01-01T01:0{i}:00Z",
                "night": "2026-01-01",
                "band": "r",
                "mjd": 61041 + i / 1440,
                "source_url": "https://example.invalid",
            }
        )
    public = tmp_path / "public"
    a = render_sequence(rows, paths, public, "2026-02-01T00:00:00Z")
    b = render_sequence(rows, paths, public, "2026-03-01T00:00:00Z", a)
    assert a == b
    assert a["frames"][0]["marker"]["x"] < a["frames"][-1]["marker"]["x"]
    assert a["gif"]
    assert a["published_at"] == "2026-02-01T00:00:00Z"


def test_invalid_fits_never_enters_cache(tmp_path):
    s = Mock()
    s.request.return_value = Mock(
        status_code=200, content=b"<html>login</html>", headers={}
    )
    result, path, code = fetch_cutout(
        s,
        {"source_url": "https://irsa.ipac.caltech.edu/ibe/data/ztf/example.fits"},
        (1, 2),
        tmp_path,
    )
    assert result == "invalid" and path is None
    assert not list(tmp_path.iterdir())


def test_pending_and_restricted_are_distinct(tmp_path):
    s = Mock()
    r = Mock(status_code=404, headers={})
    s.request.return_value = r
    row = {"source_url": "https://irsa.ipac.caltech.edu/ibe/data/ztf/a.fits"}
    assert fetch_cutout(s, row, (1, 2), tmp_path)[0] == "pending"
    r.status_code = 403
    assert fetch_cutout(s, row, (1, 2), tmp_path)[0] == "restricted"


def test_rate_limit_respects_retry_after():
    s = Mock()
    s.request.return_value = Mock(status_code=429, headers={"Retry-After": "3600"})
    with pytest.raises(UpstreamError, match="later retry"):
        request(s, "https://example.invalid")
    assert s.request.call_count == 1


def test_most_wrapper_only_accepts_irsa():
    assert most_results_url(
        "<a href=https://irsa.ipac.caltech.edu/workspace/abc/MOST/x/results.tbl>Download</a>"
    ).endswith("/results.tbl")
    with pytest.raises(UpstreamError):
        most_results_url(
            "<a href=https://evil.example/workspace/x/MOST/results.tbl>x</a>"
        )


def test_candidates_deduplicate_and_keep_publication():
    row = {
        "Image_ID": "ztf_test_zr_a",
        "image_url": "https://irsa.ipac.caltech.edu/ibe/data/ztf/test",
        "mjd_obs": 60000.0,
        "date_obs": "2023-02-25",
        "ra_obj": 1.0,
        "dec_obj": 2.0,
    }
    t = Table(rows=[row])
    a = import_candidates(t, "first")
    a[0]["published_at"] = "later"
    b = import_candidates(t, "again", a)
    assert len(b) == 1
    assert b[0]["published_at"] == "later"


def test_manifest_validation_and_noop_write(tmp_path):
    validate()
    p = tmp_path / "a.json"
    assert write(p, {"x": 1})
    assert not write(p, {"x": 1})


def isolated_project(tmp_path):
    import shutil
    import pipeline.refresh as mod
    from pipeline.core import ROOT

    shutil.copytree(ROOT / "data", tmp_path / "data")
    (tmp_path / "public").mkdir()
    return mod


def test_failed_sources_keep_last_good_data(tmp_path, monkeypatch):
    mod = isolated_project(tmp_path)
    before = (tmp_path / "data/object.json").read_bytes()
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    def broken(*a, **kw):
        raise UpstreamError("fixture outage")

    for name in ["sbdb", "mpc", "horizons"]:
        monkeypatch.setattr(mod.sources, name, broken)
    result = mod.refresh("fast", budget_seconds=1)
    assert len(result["errors"]) == 3
    assert (tmp_path / "data/object.json").read_bytes() == before
    assert result["sources"]["sbdb"]["last_success"]


def test_all_404s_and_most_timeout_leave_sequences_intact(tmp_path, monkeypatch):
    mod = isolated_project(tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    before = (tmp_path / "data/animations.json").read_bytes()
    old_watermark = load(tmp_path / "data/state.json")["most_through"]
    # Keep this outage test independent of the changing production backlog.
    existing = load(tmp_path / "data/frames.json")
    for row in existing:
        row["next_retry_at"] = "9999-01-01T00:00:00Z"
    table = Table(
        rows=[
            {
                "Image_ID": f"ztf_timeout_{i}_zr",
                "image_url": f"https://irsa.ipac.caltech.edu/ibe/data/ztf/timeout_{i}.fits",
                "mjd_obs": 48000 + i / 1440,
                "date_obs": "1990-04-19",
                "ra_obj": 1.0,
                "dec_obj": 2.0,
            }
            for i in range(3)
        ]
    )
    write(tmp_path / "data/frames.json", import_candidates(table, "fixture", existing))

    def broken(*a, **kw):
        raise UpstreamError("MOST fixture timeout")

    monkeypatch.setattr(mod.sources, "most", broken)
    monkeypatch.setattr(
        mod.sources, "fetch_cutout", lambda *a, **kw: ("pending", None, 404)
    )
    result = mod.refresh("images", max_downloads=3, budget_seconds=30)
    assert result["imaging"]["requests"] == 3
    assert (tmp_path / "data/animations.json").read_bytes() == before
    assert load(tmp_path / "data/state.json")["most_through"] == old_watermark
    assert any(
        r.get("last_http_status") == 404 for r in load(tmp_path / "data/frames.json")
    )


def test_invalid_schema_is_rejected(tmp_path):
    from jsonschema import Draft202012Validator, ValidationError

    schema = load(Path(__file__).parents[1] / "schemas/frames.schema.json")
    frame = load(Path(__file__).parents[1] / "data/frames.json")[0]
    frame["availability"] = "detected"
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate([frame])


def test_pending_becomes_published_once(tmp_path, monkeypatch):
    import pipeline.refresh as mod

    monkeypatch.setattr(mod, "ROOT", tmp_path)
    w = output_wcs([(1, 5)], 480, 480)
    rng = np.random.default_rng(12)
    data = rng.normal(100, 4, (480, 480))
    paths = {}
    rows = []
    for i in range(3):
        ra, dec = w.pixel_to_world_values(235 + i * 3, 240)
        ident = f"ztf_fixture_{i}_zr"
        p = tmp_path / f"{i}.fits"
        fits.writeto(p, data, w.to_header())
        paths[ident] = p
        rows.append(
            {
                "Image_ID": ident,
                "image_url": f"https://irsa.ipac.caltech.edu/ibe/data/ztf/{i}.fits",
                "mjd_obs": 61041 + i / 1440,
                "date_obs": "2026-01-01",
                "ra_obj": float(ra),
                "dec_obj": float(dec),
            }
        )
    table = Table(rows=rows)
    frames = import_candidates(table, "2026-01-02T00:00:00Z")
    write(tmp_path / "data/frames.json", frames)
    write(tmp_path / "data/animations.json", [])
    monkeypatch.setattr(mod.sources, "most", lambda *a, **kw: (table, "fixture"))
    monkeypatch.setattr(
        mod.sources, "fetch_cutout", lambda *a, **kw: ("pending", None, 404)
    )
    mod.refresh("images", max_downloads=3, budget_seconds=30)
    frames = load(tmp_path / "data/frames.json")
    assert all(
        f["availability"] == "pending" and f["published_at"] is None for f in frames
    )
    for f in frames:
        f["next_retry_at"] = "2000-01-01T00:00:00Z"
    write(tmp_path / "data/frames.json", frames)
    monkeypatch.setattr(
        mod.sources,
        "fetch_cutout",
        lambda s, row, *a, **kw: ("available", paths[row["id"]], 200),
    )
    mod.refresh("images", max_downloads=3, budget_seconds=30)
    assert all(
        f["published_at"] and f["assets"] for f in load(tmp_path / "data/frames.json")
    )
    before = load(tmp_path / "data/animations.json")
    assert len(before) == 1 and before[0]["n_frames"] == 3 and before[0]["gif"]
    result = mod.refresh("images", max_downloads=3, budget_seconds=30)
    assert result["imaging"]["requests"] == 0
    assert load(tmp_path / "data/animations.json") == before


def test_quality_rejection_waits_for_review_but_new_frames_still_run(
    tmp_path, monkeypatch
):
    import pipeline.refresh as mod

    monkeypatch.setattr(mod, "ROOT", tmp_path)
    table = Table(
        rows=[
            {
                "Image_ID": f"ztf_review_{i}_zr",
                "image_url": f"https://irsa.ipac.caltech.edu/ibe/data/ztf/review_{i}.fits",
                "mjd_obs": 60000 + i / 1440,
                "date_obs": "2023-02-25",
                "ra_obj": 1.0,
                "dec_obj": 2.0,
            }
            for i in range(2)
        ]
    )
    frames = import_candidates(table, "2026-01-01T00:00:00Z")
    rejected = frames[0]
    rejected.update(
        availability="available",
        quality="rejected",
        quality_reason="No usable pixels at predicted positions",
        attempts=1,
    )
    write(tmp_path / "data/frames.json", frames)
    write(tmp_path / "data/animations.json", [])
    monkeypatch.setattr(mod.sources, "most", lambda *a, **kw: (table, "fixture"))
    fetch = Mock(return_value=("pending", None, 404))
    monkeypatch.setattr(mod.sources, "fetch_cutout", fetch)

    result = mod.refresh("images", max_downloads=10, budget_seconds=30)
    assert result["imaging"]["requests"] == 1
    assert result["imaging"]["queued"] == 0
    assert fetch.call_args.args[1]["id"] != rejected["id"]
    saved = load(tmp_path / "data/frames.json")
    retained = next(row for row in saved if row["id"] == rejected["id"])
    assert (
        retained["attempts"] == 1
        and retained["quality_reason"] == rejected["quality_reason"]
    )
    assert not retained["assets"]

    # An operator can explicitly return a reviewed/corrected frame to the queue.
    retained["quality"] = "unprocessed"
    write(tmp_path / "data/frames.json", saved)
    fetch.reset_mock()
    result = mod.refresh("images", max_downloads=10, budget_seconds=30)
    assert result["imaging"]["requests"] == 1
    assert fetch.call_args.args[1]["id"] == rejected["id"]
