# Family tone revision

Approved for publication on 6 September 2026, this revision uses a warmer, more direct tone for the Beebe family, friends, and curious visitors. It keeps the original dark palette, serif headings, telescope viewer, source citations, scientific qualifications, and interactive explanations.

The emphasis is a familiar name and a chance to learn a little astronomy. It does not present this website as a scientific research project or make new claims about the asteroid.

Examples:

- “A small world. Still in motion.” becomes “An asteroid named Beebe.”
- “Far away. Remarkably knowable.” becomes “What kind of asteroid is it?”
- “Real light. Clear provenance.” becomes “Where the photos and facts come from.”
- “The observing journal” becomes “The photo collection.”

## Preservation and comparison

- Experimental branch: `family-tone`.
- Original design restore point: annotated tag `before-family-tone` (commit `5fa954b`).
- The user approved this version for publication. `family-tone` was merged into `main`; GitHub Pages publishes from `main`.
- Local branch preview: `http://localhost:3001/` while its preview server is running.
- The main checkout and this branch use separate worktrees. The completed image backlog is included in both.

The presentation change is commit `f60b42c`. To restore the original design, revert its presentation changes or restore just the presentation files changed by that commit from `before-family-tone`. Do not reset all of `main` to the restore tag, because that would also roll back newer image-processing results. The tag preserves the original presentation for exact comparison.

Only presentation copy, a small typography adjustment, and this note change on this branch. Pipeline behavior, archive data, and media are unchanged by the experiment.
