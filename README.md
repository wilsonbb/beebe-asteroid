# (20220) Beebe

A public-astronomy field journal: real ZTF cutouts, a controllable image player, an evolving archive, and approachable science about asteroid Beebe.

The frontend exports ordinary HTML, CSS, JavaScript and WebP/GIF files. Python does the upstream work on a schedule. Visitors never trigger slow telescope-archive requests. The site can be hosted on GitHub Pages without a running backend; the accompanying Sites deployment is an owner-only review copy.

## What is here

- Real common-WCS image sequences and individual exposure/source links.
- Play/pause, frame stepping, scrubbing, speed selection and a predicted-position overlay.
- Archive filters by year, band and availability, with static pagination and permanent image-night pages.
- Verified discovery/naming content, JPL orbital elements and caveats, a size/reflectivity explainer, and dated Horizons predictions.
- Incremental MOST discovery, bounded IBE downloads, retry states, cache validation, media provenance and source freshness.
- Recorded-source tests, geometry tests, failure tests, a static-link checker, and GitHub CI/Pages workflows.

The implementation uses the generated Vinext/React starter with static export, rather than the brief's suggested Jinja templates. The hosting model stays the same: no Worker or server is required in production. Generated Shadcn components are retained and composed for controls. Astronomy pixels are processed locally, not sent to an image-generation service.

## Quick start

Requirements: Node 24 or a compatible newer version, Python 3.12, Git.

```bash
npm ci
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm run dev
```

Open the local URL printed by the development server. Committed data and media make the site work without contacting astronomy services.

```bash
npm run typecheck
npm run lint
npm run test:unit
.venv/bin/python -m pytest tests -q
.venv/bin/python -m pipeline.cli validate
npm run build
python3 scripts/check_static.py
```

`npm run build` prepares public JSON downloads, exports to `dist/client`, then adds directory index copies for plain static hosts. To inspect exactly those files:

```bash
python3 -m http.server 4173 --directory dist/client
```

Some sandboxes require permission to start the temporary local server used by static prerendering. This is not a production-server dependency.

## Refresh the journal

```bash
.venv/bin/python -m pipeline.cli refresh --mode fast
.venv/bin/python -m pipeline.cli refresh --mode images --max-downloads 100 --budget-seconds 1200
.venv/bin/python -m pipeline.cli refresh --mode all --max-downloads 12 --budget-seconds 300
.venv/bin/python -m pipeline.cli refresh --mode images --reconcile
```

- `fast`: JPL facts, current MPC primary records, and 30 days of daily geocentric Horizons predictions.
- `images`: incremental MOST coverage search plus a persistent image queue. Newest and oldest due nights alternate so historical work gets a share of the budget.
- `all`: both sets of sources.
- `--reconcile`: one historical calendar year per invocation, advancing a durable year cursor. The quarterly workflow invokes it.

A refresh can validly find no new images. Upstream failures are recorded in `data/status.json`; that source's previous valid content remains. Fatal validation errors return nonzero and prevent publishing. Standard output includes GitHub warning annotations for upstream failures, and the workflow writes a summary. No service credentials are needed for public images.

**Do not run `seed` on an established archive.** It is an explicit bootstrap/recovery utility using dated fixtures. If starting from scratch with the original local source directory available:

```bash
.venv/bin/python -m pipeline.cli seed --source /path/to/beebe_asteroid
```

Original supplied inputs remain unmodified under `archive/original`. They include the earlier plan for historical context; `docs/BUILD_PLAN.md` records its audited replacement. Neither is a live source of current values.

## Enable GitHub Pages and scheduled updates

A destination GitHub repository must be selected by the owner. The Sites source repository is a separate version store and does not execute GitHub Actions. The checked-in schedules are **not active merely because the review site is deployed**.

1. Create or choose the intended repository, push this repository's `main` branch, and enable Actions. A public repository on GitHub Free is the default no-hosting-charge path.
2. In **Settings → Pages**, select **GitHub Actions** as the build source.
3. In **Settings → Secrets and variables → Actions → Variables**, set `PAGES_BASE_PATH` to `/repository-name` for project Pages. Leave it empty for an `owner.github.io` repository or a custom domain.
4. Permit the refresh workflow to commit to `main`. If branch protection requires a PR, adapt the documented generated-data write step to your approved branch/PR process before enabling the schedule. Do not weaken unrelated repository protections.
5. In Actions, run **Refresh and publish Beebe** with `mode: publish` to test the current snapshot, then `all` for a bounded live refresh. Confirm both the commit and the Pages deployment in that same run.
6. Verify schedules are enabled: fast sources daily at 09:23 UTC; images Tuesday/Friday at 10:41 UTC; one historical reconciliation at 11:17 UTC on the first day of each quarter. GitHub timing is best effort.

Production image updates then publish to **GitHub Pages**. The owner-only Sites review copy remains a saved snapshot unless separately redeployed; it is not secretly wired to a second hosting platform.

The refresh workflow shares a concurrency group, does not cancel an in-progress write, validates before committing, and deploys directly after its own commit. It does not rely on a bot push triggering another workflow. If a human pushes concurrently, `git push` fails safely; rerun from the latest `main` rather than force-pushing.

For a local subpath validation matching Pages:

```bash
BASE_PATH=/beebe NEXT_PUBLIC_BASE_PATH=/beebe npm run build
BASE_PATH=/beebe python3 scripts/check_static.py
```

Both variables must match. The first controls exported framework paths; the second controls application-owned links and media. Rebuild without those variables for root hosting.

## Scientific interpretation

- MOST means predicted image coverage, not confirmed detection.
- A circle marks an ephemeris prediction. New images are labeled unreviewed; the pipeline does not claim automatic source detection.
- MPC satellite continuation lines are paired with their observations. Text-line counts, primary observation counts and JPL's fit count are separate.
- Reported magnitude bands stay attached to measurements. Horizons V magnitudes are predictions.
- Orbital elements retain their solution, epoch, frame and source sigmas.
- The diameter slider is conditional on assumed reflectivity, not a measured size or confidence interval. The approximate three-hour spin has a documented large uncertainty.
- All animation frames are real exposures. Reprojection and background normalization aid viewing; displayed brightness is not calibrated photometry.

See [operations](docs/OPERATIONS.md), [validation](docs/VALIDATION.md), and the website's Sources page for details.

## Repository map

| Path | Purpose |
|---|---|
| `app/`, `components/`, `lib/` | Static-export pages and browser interactions |
| `pipeline/` | Normalizers, public clients, rendering, refresh orchestration and validation |
| `data/` | Durable current manifests, source status and queue/watermark state |
| `public/media/` | Immutable compressed image assets and GIFs |
| `.cache/fits/` | Disposable local/Actions cache; never the only durable state |
| `tests/fixtures/` | Recorded public JPL, MPC and Horizons responses |
| `schemas/` | Published frame and sequence contracts |
| `archive/original/` | Byte-preserved supplied inputs |
| `.github/workflows/` | Offline CI and optional scheduled refresh/Pages deployment |

## Costs and maintenance

Static hosting and standard public-repository Actions runners can be free under the providers' current limits; domain registration is separate. Monitor output and repository size in the workflow logs. FITS caches may be evicted; the manifests and published images survive. Source files can change upstream, so cached input hashes and requests are provenance, not a guarantee of indefinite bit-for-bit reproduction.

Pinned direct Python dependencies are in `requirements.txt`; npm dependencies have exact direct versions and a lockfile. The vendored UI catalog is excluded from application linting; it is still typechecked. The `nextjs/no-img-element` rule is disabled intentionally because the pipeline already produces optimized, dimensioned images for static hosting. Dependencies should be reviewed periodically with `npm audit` and tested before updating. See the validation log for the audit performed on this version.

Dataset acknowledgments and scientific citations are displayed on `/sources/`. Original archive data keep their source provenance. No license for the user's original work has been invented.
