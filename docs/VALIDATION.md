# Validation record

This file records checks actually performed; it does not claim future scheduled runs have happened.

## Data and live services

- Original local inputs preserved in `archive/original` and compared during planning.
- JPL identity/orbit/physical normalization and geocentric Horizons prediction retrieval exercised against live public endpoints.
- MPC GET-with-JSON-body exercised. Recorded fixture: 5,066 text records, 750 paired satellite continuations, 4,316 primary observations; the latest reported brightness band remains `w`.
- MOST Regular search tested against the real service. Its HTML wrapper and separate fixed-width results table are handled explicitly.
- A live `all` refresh with a 12-cutout budget found 84 additional candidate exposures, grew the index from 1,003 to 1,087, published three older cutouts and marked nine public files pending. No source errors were reported. These are results from that run, not evergreen counts.
- Ten nights currently have usable rendered products, including three multi-frame GIF sequences. Reprojection checks and source hashes are retained. Source visibility remains labeled unreviewed.

## Automated checks

- 15 Python tests cover MPC paired-record accounting and orphan rejection, source identity, Horizons columns, RA wrap, reprojection, deterministic rendering, marker motion, invalid FITS, 404/403 distinction, Retry-After, trusted MOST result links, deduplication, schemas, outage preservation, queue behavior, and a pending-to-published transition that is idempotent on rerun.
- Five TypeScript unit tests cover independent publication/observing-date sort order, combined filters and empty results.
- TypeScript checks include the retained UI catalog. Application lint excludes vendored starter components and documents the pipeline-optimized `<img>` exception.
- Manifest validation checks identity, counts, ordering, marker coordinates, referenced assets, hashes and image dimensions before publishing.
- The production static-link checker verifies exported local page, image, script and stylesheet links, including directory indexes and configured base paths.

## Browser checks

The local preview was inspected with the in-app browser. Frame stepping changed the exposure timestamp, playback changed the Play/Pause state, and the marker switch changed its checked state. Archive year/band/availability filters and the zero-results state worked. At a 390px viewport the page and archive had no horizontal overflow. Browser error logs were empty during those checks.

The player defaults to a poster, so reduced-motion visitors encounter no autoplay. Keyboard-operable native controls and the accessible component primitives are used, with explicit labels and visible focus. This is not a claim of a formal WCAG certification or an independent screen-reader audit.

## Dependency and build notes

The initial generated scaffold reported 11 dependency vulnerabilities. Compatible patched versions of React/RSC, Vinext, Vite and Cloudflare development packages were installed together; npm reported zero vulnerabilities afterward. Installation respected package-manager resolution without `--force` or legacy-peer bypasses.

The earlier Vinext export configuration redirected trailing-slash routes during prerendering. Exporting without `trailingSlash` and generating directory index copies in `scripts/finalize.mjs` supports ordinary static hosts while retaining the site's slash-terminated public links. The output directory is `dist/client`. A `/beebe` base-path export was also checked; the finalizer flattens Vinext’s nested base-path output so GitHub Pages can mount the artifact at the repository path.

## Deliberate limits

Scheduled refresh and GitHub Pages deployment need the owner's destination repository and Actions configuration. The separately deployed Sites copy is an owner-only review snapshot. Current quality filtering validates pixels and common sky coverage; it does not automatically identify the asteroid, measure a lightcurve, or certify astrometric registration accuracy. Seasonal opposition predictions and other survey integrations remain deferred as in the build brief.
