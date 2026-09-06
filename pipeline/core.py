"""Pure normalization and durable JSON operations. No upstream calls on import."""

from __future__ import annotations
import csv
import hashlib
import io
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
STATIONS = {
    "C57": "TESS",
    "T05": "ATLAS, Haleakalā",
    "T08": "ATLAS, Mauna Loa",
    "703": "Catalina Sky Survey",
    "704": "LINEAR, Socorro",
    "F51": "Pan-STARRS 1",
    "F52": "Pan-STARRS 2",
    "G96": "Mt. Lemmon Survey",
    "809": "La Silla",
}


def now():
    return (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )


def load(path, default=None):
    return json.loads(Path(path).read_text()) if Path(path).exists() else default


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (
        json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
        + "\n"
    )
    if path.exists() and path.read_text() == raw:
        return False
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(raw)
    tmp.replace(path)
    return True


def digest(data):
    return hashlib.sha256(data).hexdigest()


def mpc_date(value):
    year, month, day = value.split()
    value = float(day)
    dt = datetime(int(year), int(month), int(value), tzinfo=timezone.utc) + timedelta(
        days=value - int(value)
    )
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def normalize_mpc(payload, retrieved_at):
    lines = payload[0]["OBS80"].splitlines()
    if not lines:
        raise ValueError("Empty MPC response")
    observations = []
    continuation = 0
    previous = None
    for line in lines:
        if len(line) != 80:
            raise ValueError("MPC record must have 80 columns")
        if line[:5].strip() != "20220":
            raise ValueError("Wrong MPC target")
        code = line[14]
        if code in "srv":
            if (
                previous is None
                or previous[14] != code.upper()
                or any(
                    previous[a:b] != line[a:b] for a, b in [(0, 12), (15, 32), (77, 80)]
                )
            ):
                raise ValueError("Unpaired MPC continuation")
            observations[-1]["continuation"] = line
            continuation += 1
            previous = None
            continue
        if previous and previous[14] in "SRV":
            raise ValueError("Missing MPC continuation")
        if code not in " CSPcBTAeMHnNDEO":
            raise ValueError(f"Unsupported MPC record type {code!r}")
        if code == "R":
            raise ValueError("Radar needs a separate parser")
        mag = line[65:70].strip()
        observations.append(
            {
                "id": digest(line.encode())[:20],
                "observed_at": mpc_date(line[15:32]),
                "ra": line[32:44].strip(),
                "dec": line[44:56].strip(),
                "magnitude": float(mag) if mag else None,
                "band": line[70].strip() or None,
                "station": line[77:80],
                "raw": line,
            }
        )
        previous = line
    if previous and previous[14] in "SRV":
        raise ValueError("Missing final continuation")
    records = sorted(
        {r["id"]: r for r in observations}.values(), key=lambda r: r["observed_at"]
    )
    stations = Counter(r["station"] for r in records)
    return {
        "schema_version": 1,
        "retrieved_at": retrieved_at,
        "source": "https://data.minorplanetcenter.net/api/get-obs",
        "record_count": len(lines),
        "continuation_count": continuation,
        "count": len(records),
        "first": records[0]["observed_at"],
        "last": records[-1]["observed_at"],
        "stations": [
            {"code": k, "name": STATIONS.get(k, k), "count": v}
            for k, v in stations.most_common()
        ],
        "by_year": dict(sorted(Counter(r["observed_at"][:4] for r in records).items())),
        "recent": records[-20:][::-1],
        "records": records,
    }


def normalize_sbdb(raw, retrieved_at):
    if raw["object"]["spkid"] != "20020220":
        raise ValueError("Wrong SBDB target")
    orbit = raw["orbit"]
    elements = {
        e["name"]: {
            **e,
            "value": float(e["value"]),
            "sigma": float(e["sigma"]) if e["sigma"] else None,
        }
        for e in orbit["elements"]
    }
    return {
        "schema_version": 1,
        "retrieved_at": retrieved_at,
        "identity": raw["object"],
        "discovery": raw["discovery"],
        "orbit": {**orbit, "elements": elements},
        "physical": raw.get("phys_par", []),
        "source": "https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=20220&discovery=1&phys-par=1&full-prec=1",
    }


def normalize_horizons(raw, retrieved_at):
    if raw.get("error"):
        raise ValueError(raw["error"])
    text = raw["result"]
    if "20220 Beebe" not in text or "$$SOE" not in text or "$$EOE" not in text:
        raise ValueError("Invalid Horizons target/output")
    # Fixed requested quantities are guarded by actual header labels.
    before = text.split("$$SOE")[0]
    for label in ["R.A.", "DEC", "delta", "S-O-T", "1-way_down_LT"]:
        if label not in before:
            raise ValueError(f"Missing Horizons column {label}")
    samples = []
    for row in csv.reader(io.StringIO(text.split("$$SOE")[1].split("$$EOE")[0])):
        if not row or not row[0].strip():
            continue
        r = [x.strip() for x in row]
        dt = datetime.strptime(r[0], "%Y-%b-%d %H:%M").replace(tzinfo=timezone.utc)
        samples.append(
            {
                "at": dt.isoformat().replace("+00:00", "Z"),
                "ra": r[3],
                "dec": r[4],
                "v_mag": float(r[5]),
                "sun_distance_au": float(r[7]),
                "earth_distance_au": float(r[9]),
                "light_minutes": float(r[11]),
                "elongation_deg": float(r[12]),
            }
        )
    if not samples:
        raise ValueError("No Horizons samples")
    return {
        "schema_version": 1,
        "retrieved_at": retrieved_at,
        "observer": "Earth center (500@399)",
        "frame": "ICRF astrometric RA/Dec",
        "time_scale": "UTC",
        "valid_from": samples[0]["at"],
        "valid_until": (
            datetime.fromisoformat(samples[-1]["at"].replace("Z", "+00:00"))
            + timedelta(days=1)
        )
        .isoformat()
        .replace("+00:00", "Z"),
        "samples": samples,
        "source": "https://ssd.jpl.nasa.gov/horizons/",
    }


def import_candidates(table, timestamp, existing=None):
    from astropy.time import Time

    by_id = {r["id"]: r for r in (existing or [])}
    for row in table:
        ident = str(row["Image_ID"])
        url = str(row["image_url"])
        if not ident.startswith("ztf_") or not url.startswith(
            "https://irsa.ipac.caltech.edu/ibe/data/ztf/"
        ):
            raise ValueError("Unexpected ZTF source")
        if ident in by_id:
            continue
        by_id[ident] = {
            "id": ident,
            "survey": "ZTF",
            "observed_at": Time(float(row["mjd_obs"]), format="mjd").isot + "Z",
            "mjd": float(row["mjd_obs"]),
            "night": str(row["date_obs"]),
            "band": next((b for b in ["g", "r", "i"] if f"_z{b}_" in ident), "?"),
            "ra": float(row["ra_obj"]),
            "dec": float(row["dec_obj"]),
            "source_url": url,
            "availability": "untried",
            "quality": "unprocessed",
            "visibility": "unreviewed",
            "first_seen_at": timestamp,
            "published_at": None,
            "assets": None,
            "attempts": 0,
            "next_retry_at": None,
        }
    return sorted(by_id.values(), key=lambda r: r["observed_at"])
