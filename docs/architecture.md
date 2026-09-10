# Architecture and reproducible builds

## Pipeline

1. `recreate.MODS` defines the seven page modules in book order.
2. Each original module exports a `PAGE` dictionary.
3. `reference_reconstruction.rebuild()` copies the dictionaries and reconstructs
   features missing from the saved history.
4. That function calls `cleanup.clean()` for the umbrella, flower, fish and
   elephant. The owl, teacup and bookshelf keep the preceding rendering rules.
5. `recreate.labels()` computes automatic label positions.
6. ReportLab writes the comparison sheets and US-Letter book. The active cover
   comes from `cover_alternative.cover()`.

`--saved-geometry` skips steps 3-4. This compares original saved geometry through
the current renderer and layout; it does not recreate every historical PDF.

## Coordinates and page data

Artwork uses a 1000 by 1000 coordinate space, y increasing downward. The book is
612 by 792 PDF points (US Letter). The renderer scales and flips artwork into
PDF coordinates. All artwork and cover graphics are vector paths; embedded fonts
come from `fonts/`, which includes their licence.

| Key | Meaning |
| --- | --- |
| `shapes` | Ordered `(polygon, colour_number)` pairs; later shapes cover earlier ones |
| `colors` | Number-to-RGB example palette |
| `thin` | Legacy global detail polylines on untouched pages |
| `occlude_outlines` | Enables shape-by-shape rendering and hidden-outline removal |
| `details` | Shape-index-to-polylines map, clipped to each owning polygon |
| `detail_widths` | Optional shape-specific detail width; mast is 4 instead of 2.4 |
| `background` | Polylines drawn before shapes, such as rain or water |
| `foreground` | Intentional detail drawn after shapes, such as flower stamens |
| `key`, `title`, `answer`, `prompt`, `ncolors` | Page metadata and text |

Structural outlines are 7 artwork units; ordinary thin detail is 2.4 units.
`details` uses integer shape indices, so reordering or inserting shapes requires
updating their detail assignments. Pay particular attention to fish body index 6,
mast index 5, and elephant legs/feet/trunk/tusks indices 5-11.

## Layering and clipping

For a cleaned page, each shape is filled (white in line art, its palette colour
in the reveal), then its clipped details and outline are drawn. Later shapes
hide the earlier shape's ink. This contains scales within the fish body and
prevents them from crossing portholes, the belly, fins and deck.

The numbering raster applies the same occlusion order to structural boundaries.
Untouched pages preserve the historical all-outlines-on-top behaviour. A small
white clearance around digits on cleaned pages keeps thin details from crossing
the printed number; reveal pages do not print numbers.

## Number placement and audit

The renderer rasterizes colour IDs and structural outlines at 1000 by 1000.
SciPy labels connected components and computes taxicab distance transforms,
matching the original erosion rule. Up to `MAXLBL=6` labels are spread through a
region, with `SPREAD=3.1`. Regions with depth below `MINR=16` are skipped.
Digit size is clamped to 21-42 artwork units before page scaling.

`region-audit.json` records placed-label counts and unlabelled component areas.
Components can be tiny raster slivers; a count is not a confirmed number of
physical colouring defects. The algorithm does not prove that every printed
region is large enough for a child or that the two visual readings succeed.

## Build and refresh committed artifacts

From the repository root with the documented environment installed:

```sh
.venv/bin/python recreate.py
.venv/bin/python cover_alternative.py --output book/recreated/outofline-cover-alternative.pdf
pdftoppm -scale-to-x 890 -scale-to-y -1 -png book/recreated/outofline-reconstruction-sheets.pdf book/recreated/recreated
pdftoppm -f 1 -l 1 -r 85 -singlefile -png book/recreated/outofline-reconstruction-book.pdf book/recreated/cover
```

The PDFs use ReportLab's invariant mode and bundled fonts. Rebuilding with the
same source and tested dependency versions should reproduce the artifacts;
font/rasterizer/library changes can still alter output. Poppler is needed for
PNG previews and the clipping regression test, not PDF generation itself.

## Verification

```sh
.venv/bin/python -m unittest test_reconstruction.py
```

The tests cover:

1. Finite geometry, seven palette IDs, coverage of all seven IDs by labels, and
   each label matching the colour ID at its position.
2. Exact equality between original and accelerated owl label positions/radii.
3. A rendered fish with scales versus a render without scales: added scale ink
   must lie in the visible body mask, allowing a 3-pixel antialiasing tolerance.
   This test is skipped if Poppler is unavailable.

After changes, inspect both number pages and reveal pages at readable size.
When a change is scoped to certain drawings, compare the content streams of
unaffected PDF pages to catch accidental changes elsewhere.

## Historical code

`engine.py` retains the original geometry primitives and label implementation.
Its Cairo import is optional so current builds do not need Cairo. Its old Cairo
preview functions still require that library if explicitly used.

`book.py` and `sheet.py` are historical entry points with old sandbox paths.
They are kept as provenance, not supported build commands. The unused
`recreate.cover()` is the earlier crayon cover; the book explicitly imports the
paper-airplane cover. Original geometry is in `pages/`; original screenshot
references are in `references/`.
