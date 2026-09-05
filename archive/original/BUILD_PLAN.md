# Build Plan — (20220) Beebe website

**For:** the agent implementing this site.
**Working dir:** `/Users/wbeebe/claude/beebe_asteroid` (not yet a git repo).
**Plan written:** 2026-09-05. Every fact and every API behavior below was verified on that date — see §2 and §3. Re-verify anything that looks stale before relying on it.

---

## 1. What we are building

A small, beautiful, **self-refreshing** website about the asteroid **(20220) Beebe**, named on 2026 July 9.

Two things make it more than a static page:

1. **It re-renders itself.** A scheduled GitHub Action re-runs the imaging pipeline, pulls newly-released survey frames, makes new cutouts and animations, and redeploys. New telescope data shows up on the site without a human touching it.
2. **It is current to today.** Even between image releases, the front page reports last night's detections and where Beebe is right now.

**Audience: both at once.** A curious scientifically-literate adult must find real numbers, real provenance, and nothing dumbed down. A 12-year-old must be able to read the same page and understand what they're looking at. §8 specifies exactly how to serve both without writing two sites.

**Voice: third person, citation-forward.** This is a public object page about the asteroid, not a personal homepage. Quote the naming citation verbatim as the historical record. Do not narrate in first person and do not editorialize about the honoree.

**Hosting: GitHub Pages + GitHub Actions. Cost $0.**

---

## 2. Content ground truth

Use these values. They are verified against primary sources. **Do not invent, round differently in different places, or fill gaps from memory** — if you need a fact that isn't here, fetch it from the APIs in §3 and cite it.

### 2.1 Identity

| Field | Value |
|---|---|
| Designation | **(20220) Beebe** |
| Provisional designation | 1997 GA40 |
| SPK-ID | 20020220 |
| Class | Main-belt asteroid (MBA), middle belt |
| Discovery date | **1997 April 7** |
| Discoverer | **Eric Walter Elst** |
| Discovery site | **La Silla Observatory, Chile** (MPC observatory code 809) |

Note: the object was *observed* as early as **1992 April 7** (a precovery, exactly five years before discovery) — the orbit arc starts there, not at discovery. That's a nice detail; state it precisely and don't confuse it with the discovery.

### 2.2 Naming

Published in **WGSBN Bulletin, Volume 6, #11, 2026 July 9** (ISSN 2789-2603), page 10. That issue named **251** minor planets.

Citation, **verbatim** — reproduce exactly, including the em-dash-free phrasing and the full observatory name:

> Wilson Beebe (b. 1993) is an American researcher at the University of Washington, where he develops software for discovering faint trans-Neptunian objects with novel shift-and-stack techniques in large astronomical survey image data, especially the NSF-DOE Vera C. Rubin Observatory's Legacy Survey of Space and Time.

Cite as: *WGSBN Bull.* **6**, #11, 10.
PDF: `https://www.wgsbn-iau.org/files/Bulletins/V006/WGSBNBull_V006_011.pdf`

**The cohort — build a section on this.** Beebe was not named alone. The same bulletin named a cluster of people working on Rubin Observatory / LSST solar-system science, including two adjacent numbers:

| Object | Discovery | Who |
|---|---|---|
| (20087) Abbiedonaldson | 1994-08-10 / E. W. Elst / La Silla | Comet shapes; Rubin + ESA Comet Interceptor, Edinburgh |
| **(20220) Beebe** | 1997-04-07 / E. W. Elst / La Silla | Shift-and-stack TNO discovery software, UW |
| (20221) Bektešević | 1997-04-30 / LINEAR / Socorro | Shift-and-stack TNO techniques, DiRAC + UW |
| (20397) Jamierobinson | 1998-06-24 / LINEAR / Socorro | Asteroids in large surveys, ATLAS + LSST, Edinburgh |
| (20542) Maxwest | 1999-09-07 / LINEAR / Socorro | AI-assisted shift-and-stack TNO discovery, UW |

Beebe and Abbiedonaldson share a discoverer (Elst, La Silla). Beebe and Bektešević are consecutive numbers doing the same science. That is a genuinely good story: *a research community got written into the sky in one afternoon.* Pull the full citations from the bulletin PDF; do not paraphrase them.

### 2.3 Orbit

JPL SBDB solution `orbit_id 60`, computed **2026-03-12**, fit to **4729 observations** over a **12223-day (33.5-year) arc**, 1992-04-07 → 2025-09-24. Condition code **0** (the best possible — this orbit is nailed down). RMS residual **0.44″**.

| Element | Value | Plain meaning |
|---|---|---|
| a — semi-major axis | **2.740336 AU** (409.9 million km) | average distance from the Sun |
| e — eccentricity | **0.096469** | slightly oval, nearly circular |
| i — inclination | **13.5274°** | tilt against Earth's orbital plane |
| Ω — ascending node | 188.513° | where it crosses that plane |
| ω — argument of perihelion | 350.820° | orientation of the oval |
| q — perihelion | **2.476 AU** (370.4 Mkm) | closest to the Sun |
| Q — aphelion | **3.005 AU** (449.5 Mkm) | farthest from the Sun |
| P — period | **4.54 years** (1657 d) | one Beebe year |
| n — mean motion | 0.2170 °/day | |
| Earth MOID | 1.48 AU | never comes near Earth |
| Mean orbital speed | ~18.0 km/s | |

Epoch of the published elements: JD 2461200.5. Note the ECSV in this directory carries a *different* epoch (MJD 61041 = 2026-01-01) from IRSA's own fit — that's expected, they're independent solutions of the same orbit. Present the SBDB numbers as canonical.

**Dynamical context:** a = 2.740 AU sits in the middle main belt, **outside the 3:1 Kirkwood gap (2.50 AU)** and **inside the 5:2 gap (2.82 AU)**. It is not near-Earth, not a PHA, not a Trojan. Say so plainly — "will it hit us" is the first question a 12-year-old asks. MOID 1.48 AU means the orbits never come within 220 million km of each other.

### 2.4 Physical properties — and their honest error bars

| Property | Value | Confidence |
|---|---|---|
| H — absolute magnitude | **13.87** | solid (ref E2025N01) |
| Rotation period | **2.996 hours** | **shaky — see below** |
| Diameter | **~4.5–9.4 km** | **inferred, not measured** |
| Albedo | unknown | not measured |
| Spectral type | unknown | not measured |

**Diameter is not a measurement.** No one has resolved this object or measured its thermal emission. The range comes from H = 13.87 via `D = 1329 / sqrt(p_V) × 10^(−H/5)`:

| Assumed albedo | Diameter |
|---|---|
| 0.057 (dark, C-type) | 9.37 km |
| 0.10 | 7.07 km |
| 0.20 (bright, S-type) | 5.00 km |
| 0.25 | 4.47 km |

Present it as *"somewhere between about 4.5 and 9.5 km across, and which end depends on how dark it is — which nobody has measured yet."* This is a feature, not a gap: it's a clean, honest demonstration of how inference works in astronomy, and it's exactly the kind of thing that respects an adult reader and teaches a kid something real. **Do not quote a single diameter.**

**Rotation period is provisional.** 2.99603 h, from LCDB (rev. 2023-October), originating in TESS photometry — Pál, A.; Szakáts, R.; Kiss, C.; Bódi, A.; et al. (2020), *ApJS* **247**, 26. LCDB flags it: *"Result based on less than full coverage, so that the period may be wrong by 30 percent or so."* Carry that caveat every time you show the number.

If it is right: a day on Beebe lasts **3 hours**, and it spins **8 times** for every one Earth rotation. Best kid-hook on the site — use it, with the asterisk.

### 2.5 Observation record

**5066 MPC observations, 1992-04-07 → 2026-09-05** (i.e. through *today*). Most prolific stations:

| Code | Observatory | Obs |
|---|---|---|
| C57 | TESS (space) | 1476 |
| T05 | ATLAS Haleakalā | 513 |
| T08 | ATLAS Mauna Loa | 492 |
| 703 | Catalina Sky Survey | 399 |
| 704 | LINEAR, Socorro | 382 |
| P07 | — | 241 |
| F51 | Pan-STARRS 1 | 226 |
| G96 | Mt. Lemmon | 218 |

The most recent observation as of writing: **2026-09-05, Pan-STARRS 2 (F52), V = 18.60.**

**ZTF archive:** 1003 frames in `ztf_matches.ecsv`, 2018-08-31 → 2026-07-03. A fresh MOST query on 2026-09-05 returned 171 frames in the trailing 12 months, of which **85 are newer than the existing table**.

### 2.6 Where it is right now (recompute at build time — do not hardcode)

Snapshot from Horizons on 2026-09-05 00:00 UT, for sanity-checking your implementation:

- RA 01h 46m 57.2s, Dec +09° 05′ 59″
- V = 18.77
- Heliocentric distance r = 2.994 AU; geocentric Δ = 2.204 AU
- Phase angle 14.03°
- Light travel time 18.3 minutes

**Next opposition: 2026 October 15** — Δ = 1.986 AU, elongation 175.5°, **V = 17.93**, the brightest it gets all year. That is **six weeks after this plan was written**, and ZTF will be imaging it hard through that window. Build a countdown to it; the site will be at its most interesting right as it launches. Faintest in the coming year: 2027-03-12 at V = 19.70.

At V ≈ 18.8, Beebe is about **130,000× fainter** than the faintest star a person can see unaided. It has never been seen by eye and never will be.

---

## 3. Data sources — verified behavior

**This section is the most important engineering input in the plan.** All five sources need no API key, no account, no card. But their latencies differ by two orders of magnitude, and that difference dictates the whole architecture. Measurements taken 2026-09-05.

| Source | Latency | Response time | Use it |
|---|---|---|---|
| **MPC `get-obs`** | **same day** | fast, 415 KB | build time |
| **JPL Horizons** | predictive | **0.7 s** | build time |
| **JPL SBDB** | per orbit solution | fast | build time |
| **IRSA MOST** (ZTF frame search) | metadata ~1 day | **103 seconds** | **cron only** |
| **IRSA IBE** (image cutouts) | **~2 months, batched** | ~1 s/cutout | cron only |

### 3.1 The critical finding: metadata runs two months ahead of pixels

MOST will tell you Beebe was photographed **yesterday**. The actual image file for that night **is not downloadable yet**.

Probed one frame per available night, 2026-06-25 → 2026-09-04:

```
2026-06-25  200      2026-07-15  404      2026-08-15  404
2026-06-29  200      2026-07-21  404      2026-08-24  404
2026-07-03  200      2026-08-02  404      2026-09-03  404
            ↑                                          
   last fetchable image           everything after: 404
```

Clean cliff at 2026-07-03. Note that the existing `ztf_matches.ecsv` was generated 2026-07-14 and also ends at 2026-07-03 — **nothing new has become fetchable in the two months since.** IRSA releases ZTF science images in batches, not continuously.

**Three consequences, all mandatory:**

1. **The site must distinguish *detected* from *imaged*.** These are different states and conflating them will make the site look broken or lying. Model every night as one of: `imaged` (cutout exists) · `detected, image pending` (MOST knows, IBE 404s) · `observed by others` (MPC astrometry only, no ZTF frame).
2. **404 is a normal outcome, not an error.** The pipeline must record the frame, mark it pending, and retry on later runs. It must never crash, never write a placeholder image, and never log an alarming failure for this case.
3. **Cutouts backfill in bursts.** A run may add nothing for six weeks and then 80 frames at once. The "what's new" logic must key on *when the asset was created*, not on observation date, or a two-month-old night that just became available will be silently buried down the page.

This is also *good content*. A small honest line — "ZTF photographed Beebe on 4 September; the image files reach the public archive about two months later, so this cutout is still pending" — teaches a real fact about how survey astronomy works, and it means the site is never empty-handed.

### 3.2 Endpoints

**MPC observations** — note it is `GET` *with a JSON body*. POST returns 405.

```bash
curl -X GET "https://data.minorplanetcenter.net/api/get-obs" \
  -H "Content-Type: application/json" \
  -d '{"desigs":["20220"],"output_format":["OBS80"]}'
```

Returns a JSON list; `[0]["OBS80"]` is a single newline-joined string of 80-column records (5066 lines). Also offers `ADES_DF`, `OBS_DF`, `XML`. Parse OBS80 by fixed column: date `[15:25]`, RA `[32:44]`, Dec `[44:56]`, mag `[65:70]`, band `[70]`, station code `[77:80]`.

**JPL Horizons** — observer ephemeris:

```bash
curl -G "https://ssd.jpl.nasa.gov/api/horizons.api" \
  --data-urlencode "format=text" --data-urlencode "COMMAND='20220'" \
  --data-urlencode "OBJ_DATA='NO'" --data-urlencode "MAKE_EPHEM='YES'" \
  --data-urlencode "EPHEM_TYPE='OBSERVER'" --data-urlencode "CENTER='500@399'" \
  --data-urlencode "START_TIME='2026-09-05'" --data-urlencode "STOP_TIME='2027-09-05'" \
  --data-urlencode "STEP_SIZE='2 d'" --data-urlencode "QUANTITIES='9,20,23'"
```

Data sits between `$$SOE` and `$$EOE`. `CENTER='500@399'` is geocentric. Quantities: 1 = astrometric RA/Dec, 9 = visual magnitude, 19 = heliocentric range, 20 = observer range, 23 = solar elongation, 43 = phase angle.

**JPL SBDB** — elements, physical parameters, discovery + naming citation in one call. **Add `full-prec=1`**; the default output rounds `a` to `2.74`, which is useless.

```
https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=20220&discovery=1&phys-par=1&full-prec=1
```

**IRSA MOST** — which ZTF frames contain Beebe. **Takes ~103 seconds.** Never call this from a web request.

```bash
curl -G "https://irsa.ipac.caltech.edu/cgi-bin/MOST/nph-most" \
  --data-urlencode "catalog=ztf" --data-urlencode "input_type=name_input" \
  --data-urlencode "obj_name=20220" \
  --data-urlencode "obs_begin=2026-06-01" --data-urlencode "obs_end=2026-09-05" \
  --data-urlencode "output_mode=Brief"
```

Returns an IPAC fixed-width table. Parse column boundaries from the `|`-delimited header row — **do not split on whitespace**, fields can be empty. `output_mode=Regular` additionally returns ready-made `image_url` / `postcard_url` columns (that's what produced the existing ECSV); `Brief` returns the components and you build the URL. Either is fine; `Brief` is smaller and the URL construction is deterministic:

```python
url = (f"https://irsa.ipac.caltech.edu/ibe/data/ztf/products/sci/"
       f"{ffd[:4]}/{ffd[4:8]}/{ffd[8:]}/"
       f"ztf_{ffd}_{int(field):06d}_{filtercode}_c{int(ccdid):02d}_o_q{qid}_sciimg.fits")
```
where `ffd` is `filefracday`. Verified against a known-good frame.

**IRSA IBE cutout** — append to any of those image URLs:

```
?center=<ra>,<dec>&size=<n>arcsec&gzip=false
```

Returns a FITS cutout with a valid WCS. ~150 KB at 180″. Already implemented correctly in `make_cutouts.py`.

### 3.3 One data caveat

MOST reports `magnitude_parameters = 13.87 0.00`, i.e. it assumes **G = 0.00**, while the standard photometric slope is G = 0.15. Its `vmag` column is therefore slightly off, especially at large phase angles. **Use Horizons for any magnitude the site displays**; treat MOST's `vmag` only as a rough sort key for picking good frames.

---

## 4. Architecture

Static site, generated by a scheduled job. Nothing to run at request time, so there is nothing to pay for and nothing to keep alive.

```
                    ┌──────────── GitHub Actions (cron, weekly) ────────────┐
                    │                                                       │
   MPC get-obs ─────┤                                                       │
   Horizons    ─────┤──▶  pipeline/  ──▶  data/*.json  +  assets/*.webp    │
   SBDB        ─────┤        │                                     *.gif    │
   MOST (103 s) ────┤        └── FITS cutouts (cached, gitignored)          │
   IBE cutouts ─────┤                                                       │
                    │                          │                            │
                    │                          ▼                            │
                    │                   site build (static)                 │
                    └──────────────────────────┬────────────────────────────┘
                                               ▼
                                    GitHub Pages  ($0)
```

**Why this and not a server:** the only slow thing (MOST, 103 s) and the only unpredictable thing (IBE backfill) both belong on a schedule, not in a request path. Once they run on a schedule, the output is a folder of files, and a folder of files hosts for free. A server would add cost, a cold-start problem, and an uptime obligation, and would buy nothing.

**Why the repo is also the archive:** cutouts and animations are the site's real content and they accumulate slowly (§10). Keeping them in git means the history *is* the observation archive, every deploy is reproducible, and rollback is a revert. If it ever gets big, §10 has the exit.

**Storage growth is not a concern.** Current outputs: PNGs average 271 KB, GIFs 446 KB, FITS 503 KB. Ship **WebP** instead of matplotlib PNG (§6.4) and the per-frame cost drops to roughly 40 KB. At ZTF's observed cadence for this object (~170 frames/yr) that is well under 30 MB/yr including animations. Do **not** commit FITS — cache them in the Actions workspace and `.gitignore` the directory.

---

## 5. Repository layout

```
beebe-asteroid/
├─ .github/workflows/
│  ├─ refresh.yml            # weekly cron: run pipeline, commit, deploy
│  └─ deploy.yml             # build + publish to Pages on push
├─ pipeline/
│  ├─ sources/
│  │  ├─ mpc.py              # get-obs → observations.json
│  │  ├─ horizons.py         # ephemeris → ephemeris.json, opposition
│  │  ├─ sbdb.py             # elements, phys params, citation
│  │  └─ most.py             # ZTF frame search (slow; cached)
│  ├─ cutouts.py             # IBE fetch + 404/pending bookkeeping
│  ├─ render.py              # FITS → WebP frames, GIF/animated WebP
│  ├─ build.py               # orchestrator; writes data/*.json
│  └─ requirements.txt       # pinned
├─ data/                     # generated JSON, committed (§7)
├─ assets/
│  ├─ frames/                # per-frame WebP
│  ├─ animations/            # per-night animated WebP + GIF fallback
│  └─ fits/                  # .gitignore'd cache
├─ site/                     # static source → built output
├─ archive/                  # the original inputs, kept verbatim
│  ├─ Beebe.txt              # MPC 80-col, as downloaded 2026-07-14
│  └─ ztf_matches.ecsv       # MOST result, as downloaded 2026-07-14
├─ state.json                # pipeline bookkeeping (§7.5)
└─ BUILD_PLAN.md             # this file
```

**Preserve `make_cutouts.py`.** It is correct, working, hard-won code — the ZScale stretch, the fixed-sky-center trick that makes the asteroid move against fixed stars, the WCS marker placement. `pipeline/render.py` and `pipeline/cutouts.py` are a *refactor* of it, not a rewrite. Keep its logic and its docstring's explanation; change only what §6 requires.

---

## 6. Pipeline specification

`pipeline/build.py` runs five stages. **Every stage must be independently re-runnable and must degrade gracefully** — if MOST times out, the site still rebuilds with a fresh ephemeris and yesterday's detections. A failure in one source must never produce an empty or broken page.

### 6.1 Facts (SBDB)
Fetch with `full-prec=1`. Write `data/object.json`. Diff against the committed copy; if the orbit solution ID changed, note it — a new solution is itself news worth showing ("orbit refit on <date> using N observations").

### 6.2 Detections (MPC)
Fetch OBS80, parse fixed-width, write `data/observations.json`. Derive: total count, arc span, per-station tallies, per-year histogram, most recent observation. This is the same-day feed — it is what keeps the front page alive between image batches.

Note the archived `Beebe.txt` stops at 2025-09-24 while the API returns through today; treat the API as truth and keep the file as a provenance artifact.

### 6.3 Ephemeris (Horizons)
Two queries: fine steps (1 d) for the next 90 days, coarse (2 d) for 18 months. Write `data/ephemeris.json`. Compute the **next opposition** as the local minimum in Δ / maximum in elongation, and the year's brightest and faintest V. Verified reference values in §2.6 — assert against them in a test.

### 6.4 Imaging (MOST → IBE → render)

1. Query MOST for `[last_successful_query_date − 30 d, today]`. The 30-day overlap catches late metadata. Merge into a persistent frame table keyed by `filefracday` + `ccdid` + `qid`; never re-query the full 2018→now range on a routine run.
2. For each frame not yet imaged, attempt the IBE cutout.
   - **200** → save FITS to the cache, render, mark `imaged`.
   - **404** → mark `pending`, increment `attempts`, record `last_attempt`. **This is normal.** Retry on subsequent runs. After ~20 failed attempts spread over a year, mark `unavailable` and stop retrying.
   - **5xx / timeout** → transient; leave state untouched and retry next run.
3. **Render frames to WebP, not PNG.** Keep the ZScale stretch and the WCS-projected marker from `make_cutouts.py`. Target ~40 KB/frame. Emit at two widths (≈480 px and ≈960 px) and use `srcset`.
4. **Animations.** Keep the existing approach exactly: group frames by night, fix one sky center for the whole night (mean of the object positions), so background stars stay put and **Beebe is the thing that moves**. That single design decision is what makes these animations legible — do not lose it. Require ≥3 frames. Emit **animated WebP** primary + **GIF** fallback. Frame duration 700 ms, infinite loop.
5. Write `data/frames.json` and `data/animations.json`.

### 6.5 Assembly
Render the static site from the JSON. Write `state.json`. Fail the build loudly if `data/object.json` is missing or if the ephemeris is more than 30 days stale — those mean something is actually wrong, as opposed to the routine 404s.

---

## 7. Data contracts

The site reads only these files. Keep them stable; they are the seam between pipeline and presentation.

**`data/object.json`** — identity, orbit (element + value + sigma + units), physical params each with `{value, uncertainty, source, caveat}`, discovery block, naming block (verbatim citation + bulletin reference + cohort list), derived quantities (diameter range table, period in years, orbital speed).

**`data/observations.json`** — `{total, first, last, arc_days, n_used_in_fit, stations: [{code, name, count}], by_year: [{year, count}], recent: [{date, ra, dec, mag, band, station, station_name}]}`.

**`data/ephemeris.json`** — `{generated_at, now: {...}, next_opposition: {date, v_mag, delta_au, elongation_deg, days_until}, brightest, faintest, track_90d: [...], track_18mo: [...]}`.

**`data/frames.json`** — one record per known ZTF frame: `{id, obsdate, mjd, filter, ra_obj, dec_obj, v_mag, geo_dist, status: "imaged"|"pending"|"unavailable", attempts, image_url, assets: {webp_480, webp_960}, first_seen, imaged_at}`.

**`data/animations.json`** — `{night, n_frames, filter(s), span_minutes, arcsec, assets: {webp, gif, poster}, created_at}`.

**`state.json`** — `{last_run, last_most_query_through, counts: {imaged, pending, unavailable}, newest_imaged_date, newest_detection_date, errors: []}`.

`first_seen` / `imaged_at` / `created_at` are what drive "what's new" (§3.1, consequence 3). They are not optional.

---

## 8. Site specification

### 8.1 Serving a 12-year-old and a scientist on the same page

Do **not** build a kids' version and an adults' version, and do **not** add a reading-level toggle — both split the audience and double the maintenance. Instead, four rules applied everywhere:

1. **Plain sentence first, precise number second.** Every technical value is introduced by a sentence that works on its own, with the number immediately after. *"Beebe takes four and a half years to go around the Sun once — 4.54 years, or 1657 days."* The adult skims to the number; the kid reads the sentence. Neither is patronized.

2. **Every number gets a human anchor.** 2.74 AU is meaningless to almost everyone. 410 million km is worse. *"Nearly three times as far from the Sun as we are"* lands for both. Anchors to use: distance → multiples of Earth's orbit; diameter → *"about the size of a city"* (4.5–9.5 km); rotation → *"a day on Beebe lasts 3 hours; it spins 8 times while Earth turns once"*; brightness → *"130,000 times too faint to see with your eyes"*; light time → *"the light in this picture left Beebe 18 minutes ago."*

3. **Uncertainty is content, not a disclaimer.** The diameter range and the shaky rotation period are the two best teaching moments on the site. Show *why* we don't know: we know how much light it reflects, not how big or how dark it is, and those trade off. Render that as the albedo/diameter table from §2.4. An adult reads competence; a kid learns how science actually works.

4. **Never a bare jargon word.** First use of *opposition*, *albedo*, *absolute magnitude*, *ecliptic*, *arcsecond*, *shift-and-stack* gets a four-to-eight-word gloss inline or on hover. Not a glossary page nobody visits.

### 8.2 Page structure

Single scrolling page, deep-linkable sections. It should feel like an observatory object page that someone actually cared about.

**Hero — "Beebe tonight."** The live panel. Where it is right now (RA/Dec + a small sky position), current magnitude, distance, light-travel time. **Countdown to opposition on 15 October 2026**, with the plain-language line: *"the closest and brightest it gets all year — and the best chance for new pictures."* Latest detection: *"Last seen 5 September 2026 by Pan-STARRS 2 in Hawai'i."* Timestamp everything and say when the page was last rebuilt.

**The object.** What it is and where it lives — middle main belt, between the 3:1 and 5:2 Kirkwood gaps. Answer the unasked question early and directly: it will never come near Earth (MOID 1.48 AU). A belt diagram showing the orbit is worth building; keep it schematic and honest about scale.

**Discovery.** 1997 April 7, Eric Elst, La Silla. Then the precovery: images from **1992 April 7 — five years earlier to the day** — were found to contain it once the orbit was known, which is how the arc reaches 33.5 years. That's a lovely, true, easy-to-grasp idea: *we found it in pictures taken before anyone knew to look.*

**Naming.** Citation-forward. The verbatim block quote, attributed to *WGSBN Bull.* 6, #11, 2026 July 9, with a link to the PDF. Then the cohort table (§2.2) — the naming makes far more sense, and is far more interesting, once you see it was a group of colleagues named together. Note that 251 minor planets were named in that one issue.

**What we know, and how well.** Orbit table with real sigmas and the condition-code-0 story: 4729 observations over 33.5 years, 0.44″ RMS — *we know where this rock will be decades from now to within a fraction of an arcsecond.* Then the physical table, honest about the gaps: H solid, rotation shaky, diameter inferred, albedo and composition unknown. The albedo/diameter table goes here.

**Seeing it move.** *The centerpiece.* The animations. Explain the trick plainly: every frame is centered on the same patch of sky, so the stars hold still and the moving dot is the asteroid. State that this is genuinely how these objects are found — motion against fixed stars — which connects directly to the shift-and-stack work in the citation. Each animation labeled with date, telescope, filter, and time span.

**The image archive.** Browsable cutouts, newest first, filterable by year and filter band. Each with date, band, magnitude, distance, and a link to the source frame at IRSA. **Show pending nights too**, clearly marked — this is where §3.1 becomes visible content rather than a missing row.

**The observation record.** 5066 observations, 1992 → today. A timeline, per-station breakdown (TESS leading with 1476 is a nice surprise — a planet-hunting space telescope kept accidentally photographing this rock), and a per-year histogram showing the surveys switching on. **Load the `dataviz` skill before building any of these charts.**

**Colophon.** Every source named and linked: MPC, JPL SBDB, JPL Horizons, IRSA/MOST, ZTF, WGSBN. Credit ZTF and IRSA properly — see §11. State the refresh schedule and link the workflow run.

### 8.3 Design direction

**Load the `artifact-design` skill before writing any markup**, and `artifact-diagramming` for the orbit and sky-position diagrams.

Direction: an astronomical image is nearly black with a few bright points, so let the page be dark, quiet, and typographically confident, and let the data be the only thing that's loud. Restraint over decoration — no starfield backgrounds, no parallax gimmicks, nothing that competes with actual telescope images. Generous space around the cutouts; they are small, grey, and subtle, and they need room to read. A single restrained accent — the existing pipeline's marker green `#00e5a0` is already the site's signature colour, it appears on every cutout, so build the palette around it rather than inventing a new one.

Requirements: fully responsive; the animation section must work on a phone; respect `prefers-reduced-motion` by showing a static poster frame with a play control instead of auto-running the GIFs; every image needs real alt text describing what is actually visible; hit WCAG AA. Fast — no framework needed, and no CDN dependency that could outlive the site.

---

## 9. The refresh workflow

`.github/workflows/refresh.yml`:

- **Schedule: weekly.** Not nightly — §3.1 shows images arrive in ~2-month batches, so nightly runs would burn 103-second MOST queries to find nothing 95% of the time. Weekly also keeps the commit log readable.
- `workflow_dispatch` as well, so a run can be forced by hand.
- Consider a second, cheap **daily** job that refreshes *only* ephemeris + MPC detections (both fast, both same-day) and skips MOST/IBE entirely. That keeps the hero panel current every day at negligible cost. Recommended.
- Steps: checkout → Python + pinned deps → cache `assets/fits/` → run `pipeline/build.py` → commit `data/`, `assets/frames/`, `assets/animations/` if changed → deploy Pages.
- **Commit message should be informative**, since it doubles as the changelog: `data: +12 frames imaged (2026-07-15 → 2026-07-29), 4 nights animated`.
- Concurrency group so overlapping runs can't race.
- Timeout 30 min; MOST alone can take 2 minutes and a large backfill will take a while.
- **Do not fail the job on IBE 404s.** Fail only on: SBDB unreachable, malformed JSON written, or the site build erroring. Surface counts in the job summary.

---

## 10. Known risks

| Risk | Mitigation |
|---|---|
| IRSA changes MOST's output format or URL scheme | Parser is isolated in `sources/most.py`; snapshot a known response as a test fixture. Site degrades to "no new images" rather than breaking. |
| MOST 103 s query gets slower or flakier | Generous timeout, retry with backoff, cache last good result. Never blocks the fast daily job. |
| Image backfill stops entirely | Site stays current via MPC + Horizons. Pending frames stay honestly marked. |
| Repo grows past comfort | At ~30 MB/yr it takes many years to matter. Exit if needed: move `assets/` to Cloudflare R2 or a `gh-pages` orphan branch; the JSON already addresses assets by URL, so only the base path changes. |
| Horizons `COMMAND='20220'` ambiguity | Quote it exactly as `'20220'`. Assert the returned object name contains "Beebe" before writing output. |
| Someone re-runs the full 2018→now MOST query by accident | Cache the frame table; make full re-query an explicit flag, not the default. |

---

## 11. Attribution requirements

Non-negotiable, and correct scientific practice:

- **ZTF:** based on observations obtained with the Samuel Oschin Telescope 48-inch and the 60-inch Telescope at Palomar Observatory as part of the Zwicky Transient Facility project. ZTF is supported by the NSF. Use the project's current standard acknowledgement text.
- **IRSA:** this research has made use of the NASA/IPAC Infrared Science Archive, operated by JPL/Caltech under contract with NASA. Credit the **Moving Object Search Tool (MOST)** by name.
- **MPC:** observation data from the IAU Minor Planet Center.
- **JPL:** SBDB and Horizons, JPL/Caltech.
- **WGSBN:** citation reproduced from *WGSBN Bulletin* Vol. 6, #11 (ISSN 2789-2603), IAU WG Small Bodies Nomenclature.

---

## 12. Build order

1. **Repo + archive.** `git init`. Move `Beebe.txt` and `ztf_matches.ecsv` into `archive/` unmodified. `.gitignore` `assets/fits/` and `__pycache__/`. Pin `requirements.txt` (astropy, numpy, matplotlib, Pillow, requests) — note the current shell's `python3` lacks astropy/numpy; they live in the `beebe` conda env, so CI must install explicitly.
2. **Fast sources first.** `sbdb.py`, `mpc.py`, `horizons.py` → three JSON files. Assert against §2.6 reference values. **This alone is a live site** — ship it before touching imaging.
3. **Static site over that JSON.** Full content, real design. Everything in §8 except the imaging sections. Deploy to Pages. Now it is real and iterable.
4. **Imaging.** Refactor `make_cutouts.py` into `cutouts.py` + `render.py`, add the pending/404 state machine, backfill from the existing 1003-frame table, re-render existing cutouts as WebP.
5. **Animations + archive UI.** New animations from all nights with ≥3 frames — there is far more material available than the three GIFs currently built.
6. **Automate.** Weekly full refresh + daily fast refresh. Force a run and confirm it commits and deploys cleanly.
7. **Polish.** Accessibility pass, reduced-motion, alt text, Lighthouse, meta/OG tags with a good cutout as the preview image.

Steps 2–3 give a complete, correct, self-updating site. Everything after deepens it.

---

## 13. Acceptance criteria

- [ ] Loads with no console errors; passes WCAG AA; keyboard-navigable.
- [ ] Every number in §2 appears exactly once as canonical and matches this document.
- [ ] Naming citation is verbatim and correctly attributed to *WGSBN Bull.* 6, #11, 2026 July 9.
- [ ] Diameter is presented as a **range with its albedo dependence** — never a single figure.
- [ ] Rotation period always carries the "may be wrong by ~30%" caveat.
- [ ] `detected` vs `imaged` vs `pending` are visually distinct and explained in plain language.
- [ ] A 12-year-old can state, after reading: what it is, how big, where it is, why it was named that, and how we know where it is.
- [ ] An astronomer can find: elements with sigmas, epoch, solution date, observation count, arc, RMS, H, and every source link — without leaving the page.
- [ ] A forced workflow run adds new data and redeploys with no manual step.
- [ ] Pipeline exits 0 when every recent IBE request 404s.
- [ ] Site still builds correctly if MOST times out.
- [ ] Opposition countdown is correct against Horizons (2026-10-15).
- [ ] Total hosting cost: $0.

---

## 14. Deferred

- **Rubin/LSST cutouts.** The obvious thematic endgame given the citation. LSST solar-system data products carry no proprietary period, but cutout access needs Rubin Science Platform credentials, which does not fit $0 static hosting. Revisit when a public cutout API exists — and note the site would then be showing an asteroid named for shift-and-stack work, imaged by the survey that work was built for.
- **Lightcurve from archival photometry.** Enough ZTF and TESS data may exist to test the shaky 2.996 h period. Real science, out of scope here.
- **Colour from ZTF g/r/i.** The archive spans three filters; a colour index would hint at spectral type, which is currently unknown.
- **Sibling pages** for the other four cohort asteroids, sharing the pipeline.
