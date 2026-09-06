"""Public source clients with bounded requests and source identity validation."""

from __future__ import annotations
import io
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
from astropy.table import Table
from .core import digest, now, write
from .render import read_fits


class UpstreamError(RuntimeError):
    pass


def session():
    s = requests.Session()
    s.headers["User-Agent"] = (
        "BeebeAsteroidJournal/1.0 (public archive cutouts; bounded requests)"
    )
    return s


def request(s, url, *, deadline=None, **kwargs):
    """Retry transient responses only; honor Retry-After without overrunning the job."""
    response = None
    for attempt in range(3):
        if deadline and time.monotonic() >= deadline:
            raise UpstreamError("Work budget exhausted")
        try:
            response = s.request("GET", url, **kwargs)
            if response.status_code not in [429, 500, 502, 503, 504]:
                return response
            delay = min(60.0, 2**attempt * 2.0)
            retry = response.headers.get("Retry-After")
            if retry:
                try:
                    delay = max(delay, float(retry))
                except ValueError:
                    from email.utils import parsedate_to_datetime

                    try:
                        delay = max(
                            delay,
                            (
                                parsedate_to_datetime(retry)
                                - datetime.now(timezone.utc)
                            ).total_seconds(),
                        )
                    except (ValueError, TypeError):
                        pass
        except requests.RequestException as error:
            if attempt == 2:
                raise UpstreamError(str(error)) from error
            delay = 2**attempt * 2.0
        if attempt == 2:
            break
        if delay > 60 or (deadline and time.monotonic() + delay >= deadline):
            raise UpstreamError("Upstream requested a later retry")
        time.sleep(delay)
    if response is not None:
        raise UpstreamError(f"HTTP {response.status_code}")
    raise UpstreamError("Request failed")


def sbdb(s):
    r = request(
        s,
        "https://ssd-api.jpl.nasa.gov/sbdb.api",
        params={"sstr": "20220", "discovery": "1", "phys-par": "1", "full-prec": "1"},
        timeout=(10, 45),
    )
    r.raise_for_status()
    return r.json()


def mpc(s):
    r = request(
        s,
        "https://data.minorplanetcenter.net/api/get-obs",
        json={"desigs": ["20220"], "output_format": ["OBS80"]},
        timeout=(10, 45),
    )
    r.raise_for_status()
    return r.json()


def horizons(s, start, end):
    params = {
        "format": "json",
        "COMMAND": "'20220;'",
        "OBJ_DATA": "'YES'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'OBSERVER'",
        "CENTER": "'500@399'",
        "START_TIME": f"'{start}'",
        "STOP_TIME": f"'{end}'",
        "STEP_SIZE": "'1 d'",
        "QUANTITIES": "'1,9,19,20,21,23,43'",
        "CSV_FORMAT": "'YES'",
    }
    r = request(
        s, "https://ssd.jpl.nasa.gov/api/horizons.api", params=params, timeout=(10, 45)
    )
    r.raise_for_status()
    return r.json()


def parse_most(text):
    # A genuine IPAC table is parsed with declared fixed-width columns.
    if not re.search(r"^\|", text, re.M):
        raise UpstreamError("MOST response is not an IPAC table")
    table = Table.read(text, format="ascii.ipac")
    for column in ["Image_ID", "date_obs", "mjd_obs", "ra_obj", "dec_obj", "image_url"]:
        if column not in table.colnames:
            raise UpstreamError(f"MOST missing {column}")
    return table


def most(s, start, end, deadline=None):
    r = request(
        s,
        "https://irsa.ipac.caltech.edu/cgi-bin/MOST/nph-most",
        params={
            "catalog": "ztf",
            "input_type": "name_input",
            "obj_name": "20220",
            "obs_begin": start,
            "obs_end": end,
            "output_mode": "Regular",
        },
        timeout=(15, 180),
        deadline=deadline,
    )
    r.raise_for_status()
    text = r.text
    if not re.search(r"^\|", text, re.M):
        url = most_results_url(text)
        result = request(s, url, timeout=(10, 45), deadline=deadline)
        result.raise_for_status()
        text = result.text
    return parse_most(text), text


def fetch_cutout(s, row, center, cache, deadline=None):
    url = row["source_url"]
    if not url.startswith("https://irsa.ipac.caltech.edu/ibe/data/ztf/"):
        raise ValueError("Untrusted cutout URL")
    params = {
        "center": f"{center[0]:.7f},{center[1]:.7f}",
        "size": "480arcsec",
        "gzip": "false",
    }
    key = digest((url + str(params)).encode())[:24]
    path = Path(cache) / f"{key}.fits"
    if path.exists():
        try:
            read_fits(path)
            return "available", path, None
        except Exception:
            path.unlink()
    response = request(s, url, params=params, timeout=(10, 90), deadline=deadline)
    code = response.status_code
    if code == 404:
        return "pending", None, code
    if code in (401, 403):
        return "restricted", None, code
    if code != 200:
        return "retryable_error", None, code
    if len(response.content) > 8_000_000:
        raise UpstreamError("Oversized cutout response")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(response.content)
    try:
        read_fits(tmp)
    except Exception:
        tmp.unlink(missing_ok=True)
        return "invalid", None, code
    tmp.replace(path)
    return "available", path, code


def most_results_url(html):
    from html.parser import HTMLParser

    class Links(HTMLParser):
        links = []

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                url = dict(attrs).get("href", "")
                if url.endswith("/results.tbl"):
                    self.links.append(url)

    parser = Links()
    parser.links = []
    parser.feed(html)
    allowed = [
        u
        for u in parser.links
        if u.startswith("https://irsa.ipac.caltech.edu/workspace/") and "/MOST/" in u
    ]
    if len(set(allowed)) != 1:
        raise UpstreamError("MOST did not return a unique public results table")
    return allowed[0]
