"""Fail before publishing corrupt manifests or missing/altered media."""

from pathlib import Path
from PIL import Image
from jsonschema import Draft202012Validator, FormatChecker
from .core import ROOT, load, digest


def validate(root=ROOT):
    root = Path(root)
    o = load(root / "data/object.json")
    obs = load(root / "data/observations.json")
    ep = load(root / "data/ephemeris.json")
    assert o["identity"]["spkid"] == "20020220", "Object identity"
    assert obs["count"] == len(obs["records"]), "Observation count"
    assert obs["record_count"] >= obs["count"] + obs["continuation_count"], (
        "Record accounting"
    )
    assert ep["samples"] and ep["valid_from"] < ep["valid_until"], "Prediction interval"
    for name in ["frames", "animations"]:
        Draft202012Validator(
            load(ROOT / f"schemas/{name}.schema.json"), format_checker=FormatChecker()
        ).validate(load(root / f"data/{name}.json"))
    frames = load(root / "data/frames.json")
    ids = [f["id"] for f in frames]
    assert len(ids) == len(set(ids)), "Duplicate frame IDs"
    checked = set()

    def check(a):
        if not a:
            return
        p = (root / "public" / a["url"].lstrip("/")).resolve()
        assert p.is_relative_to((root / "public/media").resolve()), (
            "Asset outside public media"
        )
        if p in checked:
            return
        assert p.is_file(), f"Missing asset {p}"
        assert digest(p.read_bytes()) == a["sha256"], f"Asset hash mismatch {p}"
        with Image.open(p) as im:
            assert im.size == (a["width"], a["height"]), "Asset dimensions"
            im.verify()
        checked.add(p)

    seqs = load(root / "data/animations.json")
    assert seqs, "No image sequences"
    for seq in seqs:
        assert seq["n_frames"] == len(seq["frames"]) > 0, "Sequence count"
        assert len({f["id"] for f in seq["frames"]}) == len(seq["frames"]), (
            "Duplicate exposure"
        )
        assert [f["at"] for f in seq["frames"]] == sorted(
            f["at"] for f in seq["frames"]
        ), "Exposure ordering"
        for frame in seq["frames"]:
            assert frame["id"] in ids, "Sequence references unknown exposure"
            assert 0 <= frame["marker"]["x"] <= 1 and 0 <= frame["marker"]["y"] <= 1, (
                "Marker outside image"
            )
            check(frame["asset"])
        check(seq["poster"])
        check(seq["gif"])
    for f in frames:
        if f["assets"]:
            check(f["assets"])
    print(
        f"Validated {len(frames)} candidate exposures, {len(seqs)} nights, {len(checked)} media assets."
    )
