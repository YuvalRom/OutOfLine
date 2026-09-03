# Outside the Lines

A kids' colouring book where every page is a double image: one simple line
drawing (a house, an umbrella, a teacup...) whose contours, coloured by
number, reveal a completely different, more detailed picture (an owl, a
jellyfish, a hot air balloon...). Inspired by Rob Gonsalves' shared-contour
magic realism.

The rule the book teaches: **thick line = a colour stops, thin line = colour
straight over it.** The lines are not the boss of you.

## Pages

| # | looks like | is secretly |
|---|-----------|-------------|
| 1 | the house | an owl |
| 2 | the umbrella | a jellyfish |
| 3 | the flower | a butterfly |
| 4 | the sailboat | a fish |
| 5 | the tree | an elephant |
| 6 | the bookshelf | a city at night |

(, a teacup/hot-air-balloon page, is kept in the tree
but not included in the book - add it back via MODS in book.py if wanted.)

## How it works

- `engine.py` - all the machinery. A page is a dict with:
  - `shapes`: ordered `(polygon, colour_number)` list, painted like a stack
    (later shapes overwrite earlier ones). These are the THICK lines and the
    colour regions. Numbers are placed automatically (rasterise, flood-fill
    each region, pole-of-inaccessibility via erosion, several labels spread
    through big regions).
  - `thin`: polylines drawn hairline; pure decoration, never a colour
    boundary, never numbered.
  - `colors`: number -> RGB, used only for the answer-key render.
  Coordinate space is 0..1000 x 0..1000, y down. Primitives: circle, ellipse,
  rect, arch, blob, arc, scallop_row, quoin_edge, mirror.
- `pages/pN_*.py` - one file per page, geometry only.
- `sheet.py p3_butterfly p5_balloon ...` - contact sheet (line art + reveal)
  to `_sheet.png` for reviewing pages.
- `book.py` - assembles the print-ready US-Letter PDF (cover, instructions,
  6 colouring pages, 2 answer pages).

## Build

Needs Python 3 with numpy, Pillow, pycairo.

    python3 book.py        # writes the PDF
    python3 sheet.py       # contact sheet of every page

## Adding a page

Copy any `pages/pN_*.py`, design the double image (the simple object must win
the first glance; hide giveaway features as plausible object detail; add a
decoy shape painted the same colour as its surroundings so it vanishes in the
reveal), then add the module name to `MODS` in `book.py` and `sheet.py`.

Output: `book/outside-the-lines.pdf`
