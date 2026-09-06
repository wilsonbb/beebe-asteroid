# Family tone experiment

This branch tries a warmer, more direct version for the Beebe family, friends, and curious visitors. It keeps the original dark palette, serif headings, telescope viewer, source citations, scientific qualifications, and interactive explanations.

The emphasis is a familiar name and a chance to learn a little astronomy. It does not present this website as a scientific research project or make new claims about the asteroid.

Examples:

- “A small world. Still in motion.” becomes “An asteroid named Beebe.”
- “Far away. Remarkably knowable.” becomes “What kind of asteroid is it?”
- “Real light. Clear provenance.” becomes “Where the photos and facts come from.”
- “The observing journal” becomes “The photo collection.”

## Preservation and comparison

- Experimental branch: `family-tone`.
- Original design restore point: annotated tag `before-family-tone` (commit `5fa954b`).
- The public site continues to deploy from `main`; this branch has not been merged or deployed.
- Local branch preview: `http://localhost:3001/` while its preview server is running.
- The main checkout and this branch use separate worktrees. The image backlog job continues updating `main`.

If keeping the experiment, merge/cherry-pick its presentation changes onto current `main` so newer image data is retained. If it is later adopted and then rejected, revert that presentation commit/merge. Do not reset all of `main` to the restore tag, because that would also roll back newer image-processing results. The tag preserves the original presentation for exact comparison.

Only presentation copy, a small typography adjustment, and this note change on this branch. Pipeline behavior, archive data, and media are unchanged by the experiment.
