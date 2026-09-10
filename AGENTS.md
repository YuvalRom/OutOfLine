# OutOfLine contributor context

Read README.md, docs/design-status.md and docs/architecture.md before changes.
The user's current instructions take precedence over these project notes.

## Current pipeline

Use recreate.py, not the historical book.py or sheet.py. PAGE dictionaries from
pages/ are reconstructed by reference_reconstruction.py, refined by cleanup.py,
and rendered with ReportLab. The active cover is cover_alternative.cover().
The function recreate.cover() is an unused earlier crayon design.

## Preserve current decisions

- Target ages 4-10; encourage creative interpretation, not just rule following.
- The owner approved the owl and cleaned flower. Preserve them unless asked.
- Umbrella: sparse detail, with rain retained.
- Fish: scale detail must be clipped to its visible body. Mast centreline is
  black and 4 units wide, thinner than the 7-unit structural outlines.
- Elephant: rounded foliage and sparse leaf cues, legs and feet meeting at the
  centre, shortened trunk and tusks. Do not restore grids or scale textures.
- The paper-airplane cover is selected for now. Subtitle is exactly:
  "The lines are not the boss of me!". Do not show puzzle answers on the cover.
- Teacup: a wide cup and handle become a basket; steam forms the balloon.
  This new interpretation awaits review, especially its uncoloured first reading.
- Bookshelf: daylight palette with blue sky, yellow sun, mint, coral and lavender.

## Validate and preserve context

Run python -m unittest test_reconstruction.py. Render changed PDFs with Poppler
and inspect both uncoloured and coloured versions. Build current artifacts in
book/recreated/. Update design status when a decision changes. Keep changes
reproducible in source rather than relying on conversation memory.

Original references are in references/. The original page modules remain
available via recreate.py --saved-geometry. See RECOVERY_NOTES.md for provenance;
not every screenshot's exact generating code was recoverable from Git.
