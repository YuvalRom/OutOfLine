# Recovery provenance

## Starting point

The reconstruction started from repository commit `d5e53e2`, whose history also
contained `22b53c5` (initial book) and `68594f9` (later illustration revisions).
The owner supplied two prototype contact sheets, now preserved as:

- [Prototype 1](references/prototype-1.png): house, umbrella, flower, sailboat.
- [Prototype 2](references/prototype-2.png): teacup, tree, bookshelf.

The available Git history did not contain exact generating code for every
screenshot. The work is a mixture of preserved geometry and editable vector
reconstruction, not a claim that all lost code was recovered.

## What was recovered or reconstructed

- House and umbrella: based directly on saved modules. The owl remains intact.
- Teacup: restored brown tea and removed sugar-cube outlines.
- Bookshelf: restored a simpler case, grids, cooler palette and illuminated path.
- Flower: reconstructed wing proportions and markings with saved primitives.
- Fish and elephant: rebuilt approximately from the supplied visual references.

The original `pages/` modules remain unchanged. `--saved-geometry` renders them
through the current layout without reconstruction or cleanup. The historical
Cairo scripts and older artwork remain accessible through Git history.

## Subsequent owner-directed changes

1. Removed the owl reveal from the cover to avoid spoiling a puzzle.
2. Removed nonessential detail from the umbrella, flower, fish and elephant;
   clipped retained details and hid overlapped outlines.
3. Restored rain, reinforced the thin mast, and added sparse tree cues.
4. Selected the paper-airplane cover for now, using the subtitle
   "The lines are not the boss of me!".
5. Joined the elephant's legs/feet and shortened its trunk and tusks.

The current implementation and review state are described in
[design-status.md](docs/design-status.md). This file records provenance rather
than serving as an evolving to-do list.
