# Operating the Beebe journal

## State and durability

`data/state.json` stores the MOST search watermark and historical reconciliation year. `data/frames.json` stores each candidate's stable exposure identity, timestamps, source URL, availability, retry date, download attempts, quality state and published asset. `data/animations.json` links ordered exposures to immutable media. `data/status.json` records successful source refreshes independently.

A normal image run searches from the last successful watermark minus 90 days through the current UTC date. Existing candidates are retained and deduplicated by exposure identity. The watermark advances only after a complete successfully parsed search; retries outlive the overlap window. A quarterly reconciliation walks one older year per run. Use manual reconciliation repeatedly for a faster complete historical audit.

MOST currently returns an HTML wrapper linking to an IPAC results table. The adapter accepts only a unique results-table link within IRSA's workspace/MOST path, then parses fixed-width columns with Astropy. Both direct tables and this wrapper flow are supported. Temporary result links are downloaded immediately; persistent frame URLs are kept for the public provenance links.

The queue alternates newest and oldest due nights. A normal run is bounded to 100 attempted cutouts and 1,200 seconds; HTTP calls have their own bounded timeouts, so the process can finish shortly after the work deadline. GitHub's job timeout is 30 minutes. Downloads are serial and use a descriptive User-Agent. 429 responses honor Retry-After; long requested waits defer work to another run.

## Image states

| State | Action |
|---|---|
| `untried` | Candidate in the work queue |
| `available` | Valid FITS obtained; published media may already exist |
| `pending` | HTTP 404; retry with increasing delay, maximum 30 days |
| `restricted` | HTTP 401/403; wait longer; no automatic credential flow |
| `retryable_error` | Timeout, service error or rate limit; retain diagnostic and retry later |
| `invalid` | HTTP response cannot be opened as valid image/WCS data |

A published image stays available even if a later source recheck fails. The latest source result is separate. HTTP 200 alone never validates a file. Cached FITS is opened and inspected before reuse; invalid cache entries are removed and refetched. Temporary downloads become cache files only after validation.

Geometry-specific cache names include the source URL, cutout center and size. Renderer hashes include source bytes, common geometry and renderer version. Source images are reprojected onto one north-up/east-left tangent grid; the source display array is flipped for the browser's upper-left origin. A marker's coordinates are normalized to that exact output image.

Rendering currently screens for usable common footprint and finite pixels; WCS accuracy and faint-source visibility still warrant human review. The website says unreviewed, not confirmed. It is a public visualization pipeline, not an automated astrometric measurement system.

## Failure and recovery

**No new images:** expected. Inspect the latest successful MOST timestamp and pending counts. Do not manufacture an updated observation date or placeholder telescope image.

**MOST fails:** the frame list and watermark remain. Other sources can update. Retry manually once the service is healthy; inspect `.cache/responses` locally for recently successful payloads.

**Many 404s:** they may reflect release/access policy, missing products, or an archive URL change. Compare one known older exposure before drawing conclusions. Do not promise every pending image will become public.

**FITS cache disappears:** rerun the image job. Previously published images remain in Git. The current implementation may need to refetch all participating inputs before expanding an existing sequence; a small download budget can postpone that expansion. Raise the bounded budget for the affected night rather than publishing a partial replacement.

**A sequence gets another exposure:** the new manifest is accepted only if it includes all previously published frames. If rendering or the download budget would discard older usable frames, the previous sequence stays visible. New inputs remain in the queue for another run.

**A source's facts fail to refresh:** its old valid JSON remains with the old successful timestamp. If Horizons runs beyond its saved validity interval, the UI shows the last sample with an update-needed label. The client selects the current UTC day without claiming an instantaneous position.

**Validation fails:** do not publish. Repair the affected manifest or asset and rerun `python -m pipeline.cli validate`, tests and the static build. All referenced published assets must exist and match stored SHA-256/dimensions.

**Interrupted run:** inspect `git status` and rerun. Individual JSON writes use temporary files plus atomic replacement. Published assets are immutable; orphan assets from interrupted renders are harmless. The serialized workflow only builds/deploys after the whole refresh and validation steps finish. Do not run multiple local refresh writers simultaneously.

**Concurrent human push:** the workflow's normal Git push fails rather than overwriting work. Rerun it on the new head. Shared concurrency protects workflow writers, not unrelated human Git activity.

**GitHub schedule stops:** check Actions settings, workflow enablement, repository inactivity, branch protection, and GitHub status. Public schedules may disable after 60 days without repository activity. Manual dispatch can recover; do not infer success from the mere presence of a cron expression.

## Adding another survey

Create a separate adapter that emits stable exposure IDs, UTC observation times, bands, predicted coordinates, source URLs and access state. Keep credentials in CI secrets if that survey requires them. Do not assume Rubin data access or licensing from another survey's policy. Reuse common rendering/manifest contracts after validating FITS/WCS conventions, units and time scales.

## Reviewing visibility

The current release leaves visibility as `unreviewed`. Before labeling a sequence confirmed, inspect marker-free playback, compare the moving source to predictions over multiple exposures, and record reviewer/date/evidence in the manifest and source-controlled review notes. Do not infer confirmation merely from successful rendering. Do not submit astrometry or claim a discovery through this workflow.
