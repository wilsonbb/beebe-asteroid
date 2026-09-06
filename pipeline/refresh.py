"""Independent source refreshes plus an incremental, resumable image queue."""

from __future__ import annotations
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import time
from . import sources
from .core import (
    ROOT,
    load,
    write,
    now,
    normalize_mpc,
    normalize_sbdb,
    normalize_horizons,
    import_candidates,
)
from .render import render_sequence, sky_center


def refresh(mode="fast", max_downloads=100, budget_seconds=1200, reconcile=False):
    stamp = now()
    deadline = time.monotonic() + budget_seconds
    today = datetime.now(timezone.utc).date()
    status = load(
        ROOT / "data/status.json", {"schema_version": 1, "sources": {}, "errors": []}
    )
    status["errors"] = []
    state = load(
        ROOT / "data/state.json", {"most_through": "2026-07-03", "reconcile_year": 2018}
    )
    s = sources.session()
    s.trust_env = True

    def failed(name, error):
        message = f"{name}: {type(error).__name__}: {error}"
        status["errors"].append(message)
        status["sources"].setdefault(name, {})["last_attempt"] = stamp
        status["sources"][name]["error"] = str(error)
        print(f"::warning::{message}")

    def succeeded(name):
        status["sources"][name] = {"last_attempt": stamp, "last_success": stamp}

    if mode in ["fast", "all"]:
        end = (today + timedelta(days=30)).isoformat()
        jobs = [
            ("sbdb", "object", lambda: sources.sbdb(s), normalize_sbdb),
            ("mpc", "observations", lambda: sources.mpc(s), normalize_mpc),
            (
                "horizons",
                "ephemeris",
                lambda: sources.horizons(s, today.isoformat(), end),
                normalize_horizons,
            ),
        ]
        for name, filename, fetch, normalize in jobs:
            try:
                raw = fetch()
                data = normalize(raw, stamp)
                write(
                    ROOT / f".cache/responses/{name}.json",
                    {"retrieved_at": stamp, "response": raw},
                )
                write(ROOT / f"data/{filename}.json", data)
                succeeded(name)
            except Exception as error:
                failed(name, error)
    if mode in ["images", "all"]:
        frames = load(ROOT / "data/frames.json", [])
        sequences = load(ROOT / "data/animations.json", [])
        old = {a["night"]: a for a in sequences}
        start = (
            date.fromisoformat(state["most_through"]) - timedelta(days=90)
        ).isoformat()
        end = today.isoformat()
        if reconcile:
            year = state.get("reconcile_year", 2018)
            start = f"{year}-01-01"
            end = min(f"{year}-12-31", end)
        try:
            table, text = sources.most(s, start, end, deadline)
            frames = import_candidates(table, stamp, frames)
            write(
                ROOT / ".cache/responses/most.json",
                {"start": start, "end": end, "retrieved_at": stamp, "table": text},
            )
            if reconcile:
                state["reconcile_year"] = 2018 if year >= today.year else year + 1
            else:
                state["most_through"] = end
            succeeded("most")
        except Exception as error:
            failed("most", error)
        by_night = defaultdict(list)
        for row in frames:
            by_night[row["night"]].append(row)
        paths = {}
        downloads = 0
        added = 0
        # Alternate newest and oldest pending nights to avoid permanent backlog starvation.
        due = lambda r: (
            (not r.get("assets") or r["availability"] != "available")
            and r.get("quality") != "rejected"
            and (not r.get("next_retry_at") or r["next_retry_at"] <= stamp)
        )
        dates = sorted([n for n, rs in by_night.items() if any(due(r) for r in rs)])
        ordered = []
        while dates:
            ordered.append(dates.pop())
            if dates:
                ordered.append(dates.pop(0))
        for night in ordered:
            if downloads >= max_downloads or time.monotonic() >= deadline:
                break
            rows = by_night[night]
            c = sky_center([(r["ra"], r["dec"]) for r in rows])
            center = (c.lon.deg, c.lat.deg)
            changed = False
            for row in rows:
                if downloads >= max_downloads or time.monotonic() >= deadline:
                    break
                # Rehydrate previously rendered inputs when a sequence gains a new exposure.
                if not due(row) and not row.get("assets"):
                    continue
                try:
                    result, path, code = sources.fetch_cutout(
                        s, row, center, ROOT / ".cache/fits", deadline
                    )
                    downloads += 1
                    row["attempts"] += 1
                    row["last_attempt_at"] = stamp
                    row["last_http_status"] = code
                    row["source_availability"] = result
                    row["availability"] = "available" if row.get("assets") else result
                    days = (
                        2
                        if result == "retryable_error"
                        else 14
                        if result == "restricted"
                        else min(30, 3 + row["attempts"] * 2)
                    )
                    row["next_retry_at"] = (
                        None
                        if result == "available"
                        else (datetime.now(timezone.utc) + timedelta(days=days))
                        .isoformat()
                        .replace("+00:00", "Z")
                    )
                    if path:
                        paths[row["id"]] = path
                        row["pixels_available_at"] = (
                            row.get("pixels_available_at") or stamp
                        )
                        changed = True
                except Exception as error:
                    downloads += 1
                    row["availability"] = (
                        "available" if row.get("assets") else "retryable_error"
                    )
                    row["last_error"] = str(error)
                    row["attempts"] += 1
                    row["next_retry_at"] = (
                        (datetime.now(timezone.utc) + timedelta(days=2))
                        .isoformat()
                        .replace("+00:00", "Z")
                    )
                    failed("ibe", error)
            available = [r for r in rows if r["id"] in paths]
            # Never replace a good sequence with a partial queue/budget result.
            previous = old.get(night)
            previous_ids = {f["id"] for f in previous["frames"]} if previous else set()
            if changed and previous_ids.issubset({r["id"] for r in available}):
                try:
                    sequence = render_sequence(
                        available, paths, ROOT / "public", stamp, previous
                    )
                    if previous and not previous_ids.issubset(
                        {f["id"] for f in sequence["frames"]}
                    ):
                        raise ValueError(
                            "New rendering would discard previously usable exposures"
                        )
                    old[night] = sequence
                    rendered = {f["id"]: f for f in sequence["frames"]}
                    for row in available:
                        if row["id"] in rendered:
                            if not row.get("assets"):
                                added += 1
                            row["assets"] = rendered[row["id"]]["asset"]
                            row["quality"] = "passed"
                            row["published_at"] = row.get("published_at") or stamp
                        else:
                            row["quality"] = "rejected"
                            row["quality_reason"] = "Insufficient common footprint"
                except Exception as error:
                    for row in available:
                        if not row.get("assets"):
                            row["quality"] = "rejected"
                            row["quality_reason"] = str(error)
                    failed("render", error)
        # Assets exist before references are published; CI serializes refresh/build/deploy.
        write(
            ROOT / "data/animations.json",
            sorted(old.values(), key=lambda s: s["night"], reverse=True),
        )
        write(ROOT / "data/frames.json", frames)
        state["last_imaging_run"] = stamp
        status["imaging"] = {
            "requests": downloads,
            "new_frames": added,
            "queued": sum(due(r) for r in frames),
            "pending": sum(r["availability"] == "pending" for r in frames),
        }
    status["last_run"] = stamp
    write(ROOT / "data/state.json", state)
    write(ROOT / "data/status.json", status)
    print(
        f"Refresh complete: {mode}; {len(status['errors'])} source warnings. Last valid data retained where needed."
    )
    return status
