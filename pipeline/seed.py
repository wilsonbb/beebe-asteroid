"""Import the supplied archive without relying on index-based FITS filenames."""

from pathlib import Path
from astropy.table import Table
from astropy.io import fits
from .core import (
    ROOT,
    load,
    write,
    normalize_mpc,
    normalize_sbdb,
    normalize_horizons,
    import_candidates,
    now,
)
from .render import render_sequence


def seed(source=None):
    stamp = now()
    fixtures = ROOT / "tests/fixtures"
    for name, normalizer in [
        ("object", normalize_sbdb),
        ("observations", normalize_mpc),
        ("ephemeris", normalize_horizons),
    ]:
        file = {"object": "sbdb", "observations": "mpc", "ephemeris": "horizons"}[name]
        write(
            ROOT / f"data/{name}.json",
            normalizer(load(fixtures / f"{file}.json"), "2026-09-05T22:00:00Z"),
        )
    frames = import_candidates(
        Table.read(ROOT / "archive/original/ztf_matches.ecsv"),
        "2026-07-14T15:28:01Z",
        load(ROOT / "data/frames.json", []),
    )
    animations = load(ROOT / "data/animations.json", [])
    old = {s["night"]: s for s in animations}
    paths = {}
    if source:
        for p in (Path(source) / "cutouts/fits").glob("*.fits"):
            h = fits.getheader(p)
            mjd = h.get("OBSMJD")
            band = str(h.get("FILTER", ""))[-1:]
            matches = [
                r for r in frames if abs(r["mjd"] - mjd) < 2e-7 and r["band"] == band
            ]
            if len(matches) == 1:
                import shutil

                cache = ROOT / ".cache/fits" / matches[0]["id"]
                cache.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(p, cache)
                paths[matches[0]["id"]] = cache
    for night in sorted({r["night"] for r in frames if r["id"] in paths}):
        rows = [r for r in frames if r["night"] == night and r["id"] in paths]
        try:
            sequence = render_sequence(
                rows, paths, ROOT / "public", stamp, old.get(night)
            )
        except ValueError as error:
            for row in rows:
                row.update(
                    availability="available",
                    quality="rejected",
                    quality_reason=str(error),
                )
            continue
        old[night] = sequence
        usable = {f["id"]: f for f in sequence["frames"]}
        for row in rows:
            row.update(
                availability="available",
                quality="passed" if row["id"] in usable else "rejected",
                pixels_available_at=row.get("pixels_available_at", stamp),
            )
            if row["id"] in usable:
                row.update(
                    assets=usable[row["id"]]["asset"],
                    published_at=row.get("published_at") or stamp,
                )
    write(ROOT / "data/frames.json", frames)
    write(
        ROOT / "data/animations.json",
        sorted(old.values(), key=lambda s: s["night"], reverse=True),
    )
    write(
        ROOT / "data/status.json",
        {
            "schema_version": 1,
            "sources": {
                "sbdb": {"last_success": "2026-09-05T22:00:00Z"},
                "mpc": {"last_success": "2026-09-05T22:00:00Z"},
                "horizons": {"last_success": "2026-09-05T22:00:00Z"},
                "most": {
                    "last_success": "2026-07-14T15:28:01Z",
                    "note": "Imported historical search; current discovery not yet run",
                },
            },
            "errors": [],
        },
    )
    write(
        ROOT / "data/state.json",
        load(
            ROOT / "data/state.json",
            {"most_through": "2026-07-03", "reconcile_year": 2018},
        ),
    )
