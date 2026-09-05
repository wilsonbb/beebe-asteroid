# Beebe — a small world, still coming into view

Implementation brief for the next agent · 5 September 2026

## 1. The assignment

Build a beautiful public website about **(20220) Beebe**, with real telescope imagery that grows as new public data become available. A curious 12-year-old should understand the story; a scientifically minded adult should find quantities, uncertainties, and original sources without hunting through another site.

The signature experience is **watching a faint dot move through a field of stars**. Put that experience near the top, give it excellent playback controls, and explain what the visitor is seeing. The discovery and naming story makes the dot meaningful. The evolving archive gives people a reason to return.

Recommended implementation: **Python data pipeline + Jinja-generated static HTML + small TypeScript/JavaScript modules + GitHub Actions + GitHub Pages**. No public backend, login, database service, or visitor-triggered archive queries are needed. The site is interactive in the browser and refreshed by scheduled computation.

This is a replacement brief. It incorporates the useful ideas in `/Users/wbeebe/claude/beebe_asteroid/BUILD_PLAN.md`, with corrections below. The original files were not modified. Do not treat that earlier document's “verified” label as a substitute for source checks.

Deliver the working website, automated refresh pipeline, source fixtures, meaningful tests, deployment workflow, and a short operator README. This planning task has not created a repository, deployed a website, or activated a schedule.

## 2. Start with the material already available

Source directory: `/Users/wbeebe/claude/beebe_asteroid`.

| Existing material | What was inspected | Use |
|---|---|---|
| `make_cutouts.py` | Requests IBE FITS cutouts, applies ZScale, projects a green marker using WCS, creates selected GIFs | Refactor useful functions; replace fragile caching and selection logic |
| `ztf_matches.ecsv` | 1,003 unique image IDs; 2018-08-31 through 2026-07-03 | Seed the archive and avoid a full historical query at every run |
| `Beebe.txt` | 5,038 80-column records; ends 2025-09-24 | Historical snapshot, not the current observation count |
| `animations/` | Three GIFs: 2021-08-20, 2022-10-30, 2022-11-16 | Immediate candidate sequences for the first designed page |
| `cutouts/png/`, `cutouts/fits/` | Existing rendered frames and source cutouts | Reuse validated inputs; regenerate website presentation from FITS |

There are **110 UTC dates with at least three matches** in the ECSV. This is a candidate pool, not a promise of 110 usable animations: availability, overlapping exposures, motion, image quality, and band differences still need checking. The source script's hardcoded nights do not reproduce all files currently present.

Copy the original inputs into an immutable `archive/original/` folder inside the implementation repository. Preserve their bytes and record checksums. Do not move or overwrite the user's source files. The accompanying `reference/local-inputs.json` records their current checksums.

## 3. Scientific ground truth and editorial boundaries

### Identity, discovery, and naming

Beebe is numbered **20220**, previously designated **1997 GA40**, and JPL identifies it as a main-belt asteroid. It was discovered **7 April 1997**, by **E. W. Elst**, at **La Silla**, observatory code **809**. Its name was published **9 July 2026**, in *WGSBN Bulletin* **6**, no. **11**, page **10**. These details agree between the bulletin and the JPL response retrieved for this brief. [WGSBN bulletin](https://www.wgsbn-iau.org/files/Bulletins/V006/WGSBNBull_V006_011.pdf#page=10), [JPL object record](https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=20220&discovery=1&phys-par=1&full-prec=1).

Suggested introductory copy:

> A small world between Mars and Jupiter. Discovered in 1997. Named Beebe in 2026. Follow its journey through real telescope images.

Explain that the name honors Wilson Beebe's work developing software to find faint objects beyond Neptune using survey images. **Beebe itself is in the main asteroid belt**, not a trans-Neptunian object. Explain shift-and-stack as aligning images along a possible object's motion so its faint light adds up. A blinking animation illustrates motion; it is not itself shift-and-stack discovery.

Use the official naming citation from the original supplied plan/JPL `discovery.citation`, attributed and linked to the bulletin. Preserve the historical wording, including the observatory's full name and Unicode punctuation. A brief paraphrase should precede the citation so the story remains readable. Do not invent who proposed the name, a ceremony, or a personal relationship with the discoverer. The publication is the documented naming circumstance.

The earliest observation in the retrieved records is **7 April 1992**, five years before discovery. Explain an earlier observation later associated with the asteroid as a *precovery*. Do not invent when or by whom the association was made. Current ZTF frames are not discovery photographs.

A short “Named alongside other researchers” link or expandable note is optional. The earlier plan's large cohort section is not essential to launch and should not displace Beebe's imagery or imply a jointly organized naming event.

### Orbit: use one source and one epoch together

The earlier plan's detailed element table uses IRSA values while labeling them as JPL values. Replace it. This brief's saved JPL response gives the following baseline; fetch again during implementation and preserve the complete source fields:

| Quantity | JPL snapshot | Friendly display |
|---|---:|---|
| Semimajor axis | 2.739979966751602 au | About 2.74 times Earth's orbital scale |
| Eccentricity | 0.09661896778481198 | A gently oval orbit |
| Inclination | 13.5289060143888° | Tilted about 13.5° to Earth's orbital plane |
| Perihelion | 2.475245930612999 au | Closest to the Sun: 2.48 au |
| Aphelion | 3.004714002890205 au | Farthest from the Sun: 3.00 au |
| Orbital period | 1656.607060994303 days | One orbit takes about 4.54 Earth years |
| Earth MOID | 1.47919 au | The current orbital paths remain widely separated |

Snapshot metadata: solution **60**, solution date **2026-03-12 15:25:58**, element epoch **JD 2461200.5**, equinox **J2000**; **4,729** observations used in the fit; arc **1992-04-07 → 2025-09-24**; condition code **0**; fit RMS **0.43671 arcsec**. Retain returned sigmas and their source interpretation in the technical panel. [JPL SBDB API and field definitions](https://ssd-api.jpl.nasa.gov/doc/sbdb.html).

Semimajor axis is the orbit's characteristic size, not precisely the time-averaged distance. MOID is a distance between orbital paths, not today's Earth–asteroid distance. Use “JPL classifies Beebe as a main-belt asteroid, not a near-Earth asteroid.” Do not promise it can *never* approach Earth, or turn fit RMS into a guarantee of positional precision decades into the future. Any future position uncertainty needs an actual propagated estimate.

### Size, spin, and honest unknowns

JPL currently lists absolute magnitude **H = 13.87** and a synodic rotation period of **2.99603 hours**. The rotation entry includes a warning that incomplete coverage could leave the period wrong by roughly **30%**. Display “Possibly about 3 hours — uncertain,” with the detailed source note available immediately beside it. The current response has no diameter, albedo, or spectral-type entry; that means **not listed in this source**, not proof nobody has ever measured them. [JPL physical-parameter response](https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=20220&discovery=1&phys-par=1&full-prec=1).

Use `D_km = 1329 × 10^(-H/5) / sqrt(p_V)` for an explicitly assumption-based size illustration. At H = 13.87, an assumed reflectivity range of 0.057–0.25 gives approximately **4.5–9.4 km**. Say “If its reflectivity lies in this illustrative range, Beebe would be about 4.5–9.4 km across.” This is neither a measured size nor a statistical confidence interval.

A compact reflectivity slider can teach the idea: **“The same amount of light could come from a small bright surface or a larger dark one.”** Default to the range explanation; label the slider “Assumed reflectivity.” Moving it changes the inferred diameter and a flat circle, not a supposedly accurate asteroid model. Keep the formula and assumptions in a details panel. Never depict an invented resolved surface as Beebe.

### Observation counts: repair the earlier plan's parser

The live MPC response retrieved for this brief has **5,066 text records**, including **750 lowercase `s` satellite-position continuation records**. It has **4,316 unique primary observation records**, and **738 primary C57 records**, not 1,476 TESS sightings. The historical local file has 4,288 primary records. These are snapshot audit results, not constants to hardcode.

Parse full fractional UTC dates using columns 16–32 (Python `[15:32]`), and pair satellite continuation records with their primary records. Support record types explicitly; do not infer counts by counting lines. Preserve the magnitude's band: the latest retrieved F52 record reports **18.60 in `w`**, not V. Keep JPL's fit count separate; its source selection/count semantics do not match this retrieval, and the difference is unresolved here. [MPC observation format](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/mpc1992-format/).

The saved Horizons example, **2026-09-05 00:00 UTC**, predicts RA **01h 46m 57.23s**, Dec **+09° 05′ 59.4″**, V **18.767**, Earth distance **2.20445 au**, and one-way light time **18.3339 min**. Label these as predictions for the specified time and observer. Do not attach today's light time to a historical photograph. [Horizons reference](https://ssd.jpl.nasa.gov/horizons/manual.html).

## 4. Visual direction: an observatory field journal

Make the page feel carefully edited, spacious, and intimate. Real grainy telescope images should feel valuable. The design should help someone notice a tiny moving point without pretending it is a close-up photograph.

| Element | Direction |
|---|---|
| Background | Deep blue-black `#0B1117`; raised surfaces `#141E27` |
| Main text | Warm white `#F2F0E8` |
| Secondary text | Blue-gray `#AAB9C4`; verify contrast in context |
| Accent | Existing marker mint `#00E5A0`, used sparingly |
| Pending state | Amber `#E9BB6A`, always with text/icon |
| Display type | A restrained editorial serif, e.g. locally bundled Newsreader, with license |
| Body type | System sans-serif; 18px desktop, 16–18px mobile, line height 1.6 |
| Numbers | Tabular numerals; system monospace for coordinates and timestamps |
| Width | 1,180px overall; reading text limited to about 65 characters |
| Shape | Thin dividers, mostly flat surfaces, 8–12px corners on image viewers |

Avoid decorative starfields, glowing dashboard gauges, parallax, excessive cards, and stock asteroid art. The mint circle already belongs to the existing imagery and can become the visual signature. Use whitespace, strong type hierarchy, and image scale for drama.

### Page composition

1. **Header:** `(20220) BEEBE`, anchor links `Watch · Story · Science · Archive`, one unobtrusive data-updated timestamp. Sticky only if it does not crowd mobile.
2. **Hero:** large “A small world. A story still moving.” On desktop, a short introduction takes roughly 40% of the row and a real sequence takes 60%. On phones: title, one sentence, viewer, facts. The viewer caption says **Featured sequence · [actual historical date]**; never “live.” A text link leads to the newest available sequence.
3. **Small fact strip:** `Main asteroid belt`, `4.54-year orbit`, `Named 9 July 2026`. A separate small panel says **Predicted position today**, with its actual UTC sample time. Keep RA/Dec expandable.
4. **What's new:** up to three meaningful additions, using publication-on-this-site dates. Distinguish a newly available older image from a newly taken observation. If nothing new arrived, show the latest available date and when the archive was last successfully checked.
5. **The story:** three dates—earliest associated observation, discovery, naming—with concise prose and the official citation in an expandable source block. No unsupported biographical flourishes.
6. **A place in the Solar System:** an accessible SVG orbit schematic, then the size/reflectivity explainer. The orbital diagram identifies the Sun, Earth, Mars, Beebe's orbit, and Jupiter; label orbital distances and state the view/projection. Planet/body sizes are exaggerated for legibility. Do not mark “Beebe now” unless using computed vectors at a matching epoch.
7. **Image archive:** a featured sequence row followed by a compact, paginated grid of nights. Year, band, and availability filters; sort by `Recently added` or `Date observed`. Each night opens a permanent detail page.
8. **Scientific details:** accessible disclosure sections for orbital elements, physical entries, observation history, methods, and sources. A year histogram is optional for the first release; data tables remain available.
9. **Footer:** project purpose, source code, dataset attribution, update cadence, source freshness, and workflow status link.

The hero needs to work at 390px wide with the moving dot visible. Use the strongest verified sequence there, not automatically the newest noisy exposure. Maintain a small curated featured list alongside the automated chronological archive.

### Sequence viewer—the main interaction

Use individual WebP frames in a lightweight controllable player. Provide **Play/Pause**, previous/next frame, a labeled scrubber, speed (0.5×/1×/2×), **Show predicted position**, and a link to the observation detail page. Default to a static poster and user-initiated playback; this also honors reduced-motion preferences. Pause when the viewer is offscreen or the tab is hidden.

Put actual exposure time, band, `Frame 3 of 6`, elapsed observing span, and playback compression outside the pixels. A 700ms frame interval is an initial design choice, not the real sampling cadence. Scrubbing must update the timestamp and marker. Do not interpolate synthetic images between exposures.

The marker initially identifies the **predicted** location. A reviewer can mark a sequence “motion visually verified” with review date and evidence. Unreviewed products remain clearly labeled. Provide a simple “What am I looking at?” explanation: stars should stay in place while Beebe moves; seeing and noise change between exposures.

Provide downloadable GIFs for sharing, but keep the interactive frame player as the primary experience. An animated WebP export is optional. A poster and ordinary image links must remain usable without JavaScript; native video/GIF playback alone is insufficient for precise frame stepping and marker toggles.

### Accessibility and performance

Target WCAG 2.2 AA. Use semantic headings, visible focus, 44px touch targets, keyboard-operable controls and filters, captions, informative alt text, and non-color state labels. Provide a frame text summary rather than announcing every autoplay frame through an ARIA live region. Test 200% zoom, keyboard-only navigation, reduced motion, and a screen reader.

Render the story, facts, latest poster, and archive links in HTML. Paginate archive pages at roughly 24 nights; load frame sequences only on interaction. Target initial transfer below 600KB, initial JS below 60KB compressed, and no layout shift from image loading. These are implementation budgets to measure, not current results. Generate responsive images at useful resolutions without pretending upsampling increases telescope detail.

## 5. Data architecture and refresh policy

```text
MPC observations ──┐
JPL SBDB ──────────┼── Python adapters → validated data + freshness metadata ──┐
JPL Horizons ──────┘                                                         │
                                                                            ├→ static build → Pages
IRSA MOST → candidate exposure index → IBE public cutouts → FITS QA           │
                                            → common sky grid → WebP/GIF ───┘
```

All upstream requests occur in an operator/CI job. Visitors download published files only. Keep each source independently refreshable; upstream failure should leave its last valid snapshot visible with an honest timestamp.

### What “new data” means

MOST finds images intersecting the asteroid's **predicted path**; that does not establish that the asteroid was detected in an image. Separate exposure coverage, file availability, and visual confirmation. [IRSA MOST tutorial](https://caltech-ipac.github.io/irsa-tutorials/most-queries/).

ZTF's current published policy describes public science images released on a **60-day sliding window**, with proprietary images after approximately **550 days**. The earlier plan's universal “two-month batches” interpretation is not the published policy. Availability can still lag or vary. Say **“Public images generally follow observations by about two months; availability varies.”** Never promise a pending file will arrive on a particular date. [ZTF release policy](https://www.ztf.caltech.edu/ztf-public-releases.html).

Use separate fields, not one overloaded “detected” flag:

| Dimension | Values / meaning |
|---|---|
| Coverage | `predicted_match`; optional explicit MPC association |
| Pixel availability | `untried`, `available`, `pending`, `restricted`, `retryable_error`, `invalid` |
| Render quality | `unprocessed`, `passed`, `rejected`, with reason |
| Visibility evidence | `unreviewed`, `visually_confirmed`, `unclear` |

Public labels: **Image available**, **Archive match—image not yet available**, **Observation reported to MPC**, **Object visibility unconfirmed**. An MPC report and a ZTF frame can coexist for one night; a night cannot have only one mutually exclusive global state.

Track `observed_at`, `first_seen_at`, `pixels_available_at` (when our pipeline first obtained them), `published_at`, and `updated_at`. Lead “What's new” with `published_at`, so backfilled older observations appear. Re-encoding the same sequence should not masquerade as a new observation.

### Source adapters

**SBDB:** request `sstr=20220&discovery=1&phys-par=1&full-prec=1`. Validate designation and SPK ID, response shape, and units. Preserve raw response, request, retrieval timestamp, solution date, element epoch, covariance epoch, and reference frame. Content editing must not silently overwrite a newer upstream physical entry. Refresh weekly; monthly would also suffice.

**MPC:** the following exact request succeeded during planning:

```bash
curl -X GET 'https://data.minorplanetcenter.net/api/get-obs' \
  -H 'Content-Type: application/json' \
  -d '{"desigs":["20220"],"output_format":["OBS80"]}'
```

This GET-with-body belongs in the backend job. Validate actual records rather than accepting a successful HTTP response alone. Prefer a supported structured observation representation if verified; otherwise use a tested MPC1992 parser with paired record handling. Preserve raw payloads for audit. Refresh daily, deduplicate observations, and retain revisions/retractions explicitly. Fetch station-name metadata from MPC; show the code when unknown.

**Horizons:** use an explicit small-body selection such as `COMMAND='20220;'`, then assert the returned identity. The supplied fixture used `CENTER='500@399'`, observer ephemerides, `CSV_FORMAT='YES'`, and quantities `1,9,19,20,21,23,43`. Parse the returned header and the block between `$$SOE` and `$$EOE`; reject error/ambiguity output even at HTTP 200. Verify observer, coordinate system, time scale, and column definitions. Respect service rate limits and make JPL requests serially. [Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html).

For v1, publish daily UTC samples for the coming 30 days and choose the current day's sample in the browser. Display “Prediction for 00:00 UTC on [date]”; do not label it instantaneous. On expiry, show the last date and “Prediction needs an update.” Refresh daily. An hourly/interpolated version is optional and must handle RA wrap correctly.

The old opposition date is not independently reverified in this brief. Do not hardcode it or assert opposition, minimum Earth distance, and maximum brightness are the same event. If adding seasonal predictions, calculate each separately over a stated interval, refine extrema, identify the opposition definition, and allow `null` when no event falls in the window. This is optional after the image experience works.

**MOST:** prefer Regular output and the documented Astroquery adapter if it handles ZTF correctly. Otherwise isolate direct HTTP parsing behind the same interface. Use robust IPAC parsing, not whitespace splitting. Keep returned stable image IDs and image URLs; temporary workspace/region URLs are not durable provenance links. Initial source: existing ECSV. Thereafter query the last successful coverage end minus a configurable **90-day overlap**, through today. Commit the watermark only after complete parsing and merging. Run a broader reconciliation in bounded yearly chunks quarterly, so very late metadata are discoverable. Persist pending IDs independently of the query window.

**IBE:** derive URLs from verified metadata when needed, using the official ZTF schema. Prefer returned image URLs. Cutout parameters from the source script—`center=ra,dec&size=Narcsec&gzip=false`—are a starting point to smoke-test with one known exposure. Confirm current behavior before large backfill. [ZTF API](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_api.html).

### Schedule and resource limits

Recommended defaults: daily fast sources; **twice-weekly image discovery/download/render**. A weekly image cadence is acceptable if compute is tighter. Use off-hour-boundary schedules and manual dispatch with `fast`, `images`, `all`, and bounded `backfill` modes. Schedule timing is approximate; never promise observations immediately after acquisition.

Initial operational budget: 20-minute imaging work budget inside a 30-minute job; no more than 100 cutout downloads per run; at most two concurrent IRSA image requests; separate sequential MOST queries with generous timeouts. Check current service guidance before enabling concurrency. Stop cleanly at the budget and checkpoint remaining work. Prioritize selected seed nights, newly available frames, and a fair share of old pending frames so old work cannot starve.

404 → `pending` with `last_http_status` and next retry; it can mean not released or a bad/missing URL, so retain diagnostics. 401/403 → `restricted`, do not repeatedly authenticate or treat as an ordinary missing file. 429 → honor Retry-After; timeout/5xx → bounded exponential backoff. Repeated old 404s get slower retries and operator review, not permanent deletion. Validate a known accessible control image when an entire batch suddenly fails.

## 6. Cutouts and animations that are scientifically believable

The original function uses the same requested center for a night's cutouts. That is useful but **does not ensure common pixel coordinates, orientation, distortion, or scale**. Different WCS headers still need handling.

1. Group by explicit UTC date and band initially, then by compatible field overlap and exposure sequence. Keep observation instants in UTC. The old `floor(mjd + 0.5)` rounds around UTC noon; do not silently treat it as a calendar date. Deduplicate overlapping detections of the same exposure before playback.
2. Choose the common center with spherical coordinates, not an arithmetic RA average across 0/360°. Size the field from the full predicted track plus background and edge margins. Start around 180–480 arcsec as appropriate; split sequences if a bounded frame cannot contain the track.
3. Download to a temporary file, open as FITS, validate celestial WCS, dimensionality, finite pixels, and footprint, then atomically rename into the cache. An existing filename alone is not proof of a valid cutout.
4. Cache by stable exposure ID **plus cutout geometry** and source product identity. Cache render products by input hashes, destination WCS, band grouping, stretch settings, and renderer version. The source script's index-based filenames can reuse the wrong pixels after selection changes.
5. Reproject every frame to one north-up, east-left tangent-plane WCS and identical pixel shape. Use a common footprint/crop, or clearly mark missing areas. [`reproject`](https://reproject.readthedocs.io/en/stable/) resamples according to WCS; it does not repair incorrect astrometry. Check bright background-star alignment; reject or separately flag sequences with residual jumps.
6. Keep ZScale as an available stretch. For animations, use a consistent robust background/noise normalization and shared display stretch within the band group, masking invalid regions and extreme artifacts. State that display processing is for visibility, not calibrated photometry. Band/seeing changes must not be sold as asteroid brightness changes.
7. Export image pixels without Matplotlib's white page, repeated axes, or baked-in title. Render a marker-free image and return predicted marker coordinates in the common output grid. Place the thin mint ring as a browser overlay; never obscure the dot. Include an orientation indicator and angular scale outside/over the viewer. Offer a scientific annotated export separately if useful.
8. Quality-check target footprint coverage, masks, elongation/artifacts, and background alignment. Start with at least **three distinct usable exposures** for an animation and meaningful visible displacement; show one/two frames as stills or a labeled comparison. Blank sky at the prediction is not a confirmed detection.
9. Update only affected night/band sequences when frames arrive, using immutable asset names. Commit a manifest only after all referenced files exist and decode. Keep rejected frames with reasons for operator inspection.

Curated launch QA: manually inspect the three existing sequences, choose the clearest, and verify the moving source tracks the predictions. Automated quality gates can publish neutral archive cutouts; **automatic confirmation of detections is not required for v1**. Keep visual review independent of refresh operation, so newly available cutouts still appear without pretending certainty.

## 7. Data contracts and repository shape

Use versioned JSON schemas and consistent UTC ISO timestamps. Preserve source precision in JSON; round only in presentation. Use `null` for missing information, not zero, empty strings, or “unknown” numbers.

```text
archive/original/          immutable supplied inputs
pipeline/sources/         sbdb.py, horizons.py, mpc.py, most.py, ibe.py
pipeline/                 ingest.py, quality.py, render.py, publish.py, cli.py
templates/                base, home, archive, night, sources
frontend/                 CSS, viewer module, archive filters, size explainer
content/                  reviewed prose and featured-sequence choices
data/                     committed normalized manifests and source status
public/media/             immutable WebP posters/frames, GIF downloads
schemas/                  versioned JSON schemas
tests/fixtures/           small recorded responses and representative FITS
.cache/fits/               disposable, gitignored cache
.github/workflows/        refresh and build/deploy
dist/                     generated, gitignored website
README.md                 local use, refresh, repair, deployment
```

Required contracts:

| File | Required content |
|---|---|
| `object.json` | Identity, discovery/naming, source-linked physical entries, orbit elements + sigmas + epochs/frame, separately labeled derivations |
| `observations.json` | Normalized primary records/count, raw record count, continuation count, time extent, station/year aggregates, original band; JPL fit count separate |
| `ephemeris.json` | Observer, frame, time scale, generation time, validity interval, dated prediction samples, optional independently defined seasonal events |
| `frames.json` | Stable ID, survey/product, exact UTC time, band, source URL, predicted position/method, geometry, availability, quality, visibility evidence, publication timestamps, asset metadata |
| `animations.json` | Stable sequence ID, ordered frame IDs, night/band, actual observing span, output WCS/shape, timing policy, poster/GIF, revision hash, review status |
| `status.json` | Last attempted/successful refresh per source, last coverage interval, counts, pending budget, errors, build time and code revision |
| `state.json` | Durable query watermarks, retries, next-attempt dates, hashes, work queue; not dependent on cache survival |

Asset metadata includes URL, MIME type, width, height, bytes, SHA-256, and marker position in the declared image coordinates. Page URLs should be stable, e.g. `/archive/2022-11-16/`, with optional band/frame query parameters. Honor the configured GitHub Pages base path throughout.

Make all adapters return a common result wrapper with request metadata, retrieval time, coverage, records, and diagnostics. This allows future survey adapters without redesigning the player. Defer Rubin credentials/access-policy decisions until that integration is actually commissioned; credentials would belong in CI secrets, not public browser code. Do not assume either universal access or unavoidable expensive hosting.

## 8. Cheap hosting, persistence, and failure recovery

**Default: public GitHub repository, standard Linux GitHub Actions runners, GitHub Pages.** This can run with no hosting charge under current public-repository provisions; a custom domain is optional and separately paid. Private repositories, larger runners, retained build artifacts, and overages can change costs. [Pages eligibility and limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits), [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

Keep normalized manifests and compressed website media in Git initially; keep bulk FITS in an expendable Actions/local cache. Cache eviction must only make a subsequent job slower. Retain a small FITS test fixture and the request/processing provenance needed to rebuild products; remote archives can change, so do not promise bit-for-bit reconstruction unless source bytes are retained. Content-addressed names prevent needless binary rewrites.

Budget using measurements from the first 50 processed frames. Illustrative assumptions: 1,000 frames at 100KB each plus 110 GIFs at 1MB each is roughly 210MB before extra resolutions. At 200 additional frames and 30 GIFs annually, roughly 50MB/year follows from those assumptions. This is a sizing scenario, not a measured compression/cadence forecast. Generate large downloads only where useful. Set warnings around 500MB site output and 750MB repository size; Pages has a 1GB published-site limit. If growth warrants it, migrate immutable media to an object store/CDN behind a configurable asset base URL and recheck that provider's pricing.

Run commit + static build + Pages artifact deployment in the **same refresh workflow**, or explicitly call a reusable deploy workflow. Do not rely on a commit made by `GITHUB_TOKEN` triggering another push workflow. [GitHub token behavior](https://docs.github.com/en/actions/concepts/security/github_token).

Use minimal job permissions, pinned dependencies and action revisions, workflow concurrency, and guarded writes so fast and imaging jobs cannot overwrite each other's state. Pull/reconcile before publishing; avoid partially updating manifests on failure. Branch protection may require a dedicated generated-data branch or an approved update path: document the chosen setup rather than depending on direct default-branch writes.

Generate into staging, validate schemas/assets/links, then publish one consistent snapshot. If SBDB/MPC/MOST fails, keep that source's last good values and timestamp. If the prediction interval expires, render the dated stale state and suppress “today.” Schema errors or incomplete artifacts fail the deployment; the last live site remains intact. Upstream failures should produce a clear operator summary while allowing independently valid updates where practical.

GitHub schedules can be delayed and public-repository schedules can disable after 60 days without repository activity. Include a README recovery step, status dates visible to visitors, and workflow-failure notifications through GitHub's existing settings. Do not add an external monitoring subscription by default. [Schedule behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

## 9. Build order and completion gates

### A. Prove one complete image path

Create the implementation repository, copy inputs, install a pinned Python environment, and choose one existing sequence. Ingest its metadata, validate cached FITS, fetch one known public cutout, reproject, render, and write a schema-valid sequence manifest. Keep offline source fixtures. Confirm a missing/new cutout produces a pending record without destroying good imagery.

**Gate:** one traceable, well-aligned real sequence with distinct exposure timestamps and reversible marker overlay. This is the central product; do not defer it until after a fact-only launch.

### B. Design the page around that sequence

Implement hero, player, story, core science, and one archive detail page. Use the existing mint marker as the accent. Add the reflectivity explainer after the core player works. Check 390px, 768px, and 1440px layouts, typography, keyboard use, reduced motion, and accessible reading order.

**Gate:** a coherent usable page with actual imagery, no invented facts, and no decorative placeholder asteroid.

### C. Turn the prototype into a growing archive

Implement normalized source adapters, candidate/pixel/quality states, overlap searches, persistent retries, common-grid rendering, pagination, stable detail pages, and a newly-published feed. Seed at least three good historical sequences where available, plus representative stills and pending states. Process remaining historical candidates in bounded resumable batches.

**Gate:** a previously pending fixture becomes a published cutout and updates the relevant sequence exactly once; an unchanged rerun produces identical scientific/media output. Refresh timestamps may change, but no duplicate discovery items appear.

### D. Automate and deploy

Implement manual and scheduled refresh, cache restore, safe state merge, static build, and direct Pages deployment. Document repository visibility, permissions, branch rules, base path, and domain configuration. Select the owner's destination repository during implementation; none was supplied for this planning task.

**Gate:** a manually dispatched refresh obtains current data, produces a valid artifact, deploys it, and demonstrates the pending-to-available case with a deterministic fixture when live data do not change. Verify that schedules are enabled. A one-time manual run alone does not prove future scheduled execution.

### E. Finish the science and operational review

Review copy against sources, retain uncertainty caveats, check the official citation, inspect charts/diagram labels, audit downloadable media and provenance, and measure page/asset sizes. Apply current ZTF dataset acknowledgments and IRSA acknowledgment/DOI guidance rather than copying possibly stale boilerplate. [IRSA acknowledgment guidance](https://irsa.ipac.caltech.edu/ack.html).

**Gate:** the finished website passes the acceptance checks below, and the operator README can recover from an interrupted refresh or lost cache.

## 10. Focused acceptance tests

- Scientific content: discovery/naming dates match sources; orbit values share their stated source/epoch; size is explicitly inferred; spin is explicitly uncertain; predictions and observations are visibly distinguished.
- MPC fixture: 5,066 records → 4,316 primary observations + 750 continuation records; C57 primary count 738; fractional date survives; latest `w` band remains `w`. Verify proper record pairing rather than merely dropping lowercase rows.
- FITS safety: corrupt cached FITS and HTML returned with HTTP 200 are rejected; partial writes do not become valid cache entries.
- Geometry: use a synthetic WCS test with rotated/scaled inputs and a 0/360° RA case; fixed stars agree within the documented display tolerance after reprojection, while the predicted asteroid marker moves. Confirm visually with real seed data.
- Update semantics: repeated candidates deduplicate; out-of-order older metadata is ingested; a two-month-old newly obtained image leads the recent-additions feed; one new frame rebuilds only its affected sequences.
- Failure behavior: all recent cutouts 404, MOST timeout, 429 Retry-After, expired predictions, and lost cache all preserve a usable truthful site; malformed publish artifacts never replace a good deployment.
- Player: play/pause, frame step, scrub, speed, marker toggle, time/band labels, keyboard and reduced motion work on desktop and phone; the visual target is not cropped out.
- Archive: filters and deep links work under a repository subpath; empty states make sense; static pages remain useful without JS.
- Delivery: no broken internal assets, no console errors, accessible contrast/focus, initial performance budget measured, and actual workflow deployment demonstrated.

Do not require that a real-time run find new exposures: upstream archives may legitimately have nothing new. Test the state transition with a recorded fixture and show the live run's actual result separately.

## 11. Handoff evidence and unresolved checks

This brief includes raw snapshots in `reference/sbdb.json`, `reference/horizons.json`, and `reference/mpc.json`, retrieved during planning on 2026-09-05. Treat them as dated fixtures, not live content. The Horizons request covers 2026-09-05 through 2026-09-06, daily, geocentric, observer quantities 1/9/19/20/21/23/43. `reference/local-inputs.json` identifies the local files inspected.

Independently checked: official discovery/naming record, JPL facts and caveats, one Horizons ephemeris request, MPC GET response and record structure, local ECSV counts, source code, a rendered seed frame, current MOST documentation, ZTF release policy, and GitHub deployment/cost constraints.

Still to prove during implementation: live MOST query performance/output for this target, fresh IBE availability, full real-sequence registration/visibility, exact seasonal events, independently measured size/composition literature if desired, and the owner's actual hosting configuration. Earlier claims of 103-second MOST latency, a July image-release cliff, and fixed annual media growth are historical assertions from the supplied plan, not measurements reproduced here.

The previous plan mentions `artifact-design`, `artifact-diagramming`, and `dataviz` skills not present in this session's skill catalog. They are not prerequisites. Use the implementing agent's actually available design/website tools; if it uses Sites, follow that environment's building/hosting instructions while preserving the portable pipeline and honest data states defined here.

Optional later work: Rubin or another survey adapter, calibrated photometry/lightcurves, a rigorously computed seasonal observing chart, fuller observation-history charts, or sibling asteroid pages. None should delay a polished moving-image archive for Beebe.
