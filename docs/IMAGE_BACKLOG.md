# Image catch-up — 6 September 2026

The initial queue has been worked through. The final data contains 1,089 candidate exposures:

- 713 rendered and published images across 370 observing nights, including 62 GIF sequences.
- 335 exposures whose files were unavailable from the upstream archive. Their retry dates remain in the manifest.
- 41 exposures rejected by the image checks, with reasons retained in `quality_reason`.
- Zero untried exposures.

The catch-up added 686 images to the 27 previously published. A coverage match is still not confirmation that the asteroid is visible. Rejected images are not presented as successful detections or usable cutouts.

Successful batches:

- https://github.com/wilsonbb/beebe-asteroid/actions/runs/34045496224 — 100 requests, 34 new images.
- https://github.com/wilsonbb/beebe-asteroid/actions/runs/34045970756 — 500 requests, 383 new images.
- https://github.com/wilsonbb/beebe-asteroid/actions/runs/34062066468 — 488 requests, 269 new images.

One earlier batch stopped at typechecking when a first-time source error lacked a `last_success` field. The Sources page now handles that case. The completed deployments passed their validation and build checks.

Quality-rejected frames are excluded from automatic retries. After investigating and correcting the reason for rejection, an operator can explicitly set a frame's `quality` to `unprocessed` to return it to processing. The focused regression test verifies that rejection skips repeated fetching while fresh candidates still run, and that the explicit reset restores eligibility. All 16 Python tests passed after this change. The outage test now creates its own pending candidates so completion of the production backlog cannot invalidate the test setup.

The `family-tone` branch is a separate presentation experiment. This catch-up does not merge or deploy that design. Its original-design restore tag remains `before-family-tone`.
