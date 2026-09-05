# Outside the Lines — working notes

Read this before touching anything. It covers what we are trying to make, why
the code is shaped the way it is, and the two things that are currently broken.

---

## 1. What we are generating

A **print-ready US-Letter PDF colouring book for kids** (`book/outside-the-lines.pdf`).

The gimmick: **every page is a double image.** The line art reads as one
ordinary object — a house, an umbrella, a flower. Colour it by number and a
completely different, more detailed picture appears — an owl, a jellyfish, a
butterfly. Same contours, two readings. Inspired by Rob Gonsalves' shared-contour
magic realism.

The book also teaches one rule, which is the whole pedagogical point:

> **Thick line = a colour stops. Thin line = colour straight over it.**
> *The lines are not the boss of you.*

Thin lines are decoration (shingles, planks, veins, scales). They look like
boundaries and are deliberately not. A kid who obeys every line gets a muddled
picture; a kid who reads which lines actually matter gets the reveal.

### The six pages in the book

| # | module | looks like | is secretly |
|---|--------|-----------|-------------|
| 1 | `p1_owl` | the house | an owl |
| 2 | `p2_jellyfish` | the umbrella | a jellyfish |
| 3 | `p3_butterfly` | the flower | a butterfly |
| 4 | `p4_fish` | the sailboat | a fish |
| 5 | `p6_elephant` | the tree | an elephant |
| 6 | `p7_city` | the bookshelf | a city at night |

`p5_balloon` (the teacup → a hot air balloon) **exists but is not in the book.**
It is excluded from `MODS` in `book.py` and kept only in `sheet.py`. Add it back
to `book.py`'s `MODS` if wanted — note the PDF layout assumes an even page
count split 4 + rest across two answer pages, so check `build()` if you change
the count.

Module numbering does not match book order — `p5_balloon` is skipped, so
`p6_elephant` is book page 5. Don't "fix" this by renaming files.

### PDF structure

cover → how-it-works → 6 colouring pages → 2 answer pages (4 reveals + 2 reveals).

---

## 2. Known breakage — fix this first

Both entry points write to a **sandbox path from the machine that built this**,
which does not exist anywhere else:

- `book.py:92` → `build('/sessions/modest-charming-curie/mnt/outputs/outside-the-lines.pdf')`
- `sheet.py:24` → `s.write_to_png('/sessions/modest-charming-curie/mnt/outputs/_sheet.png')`

Both crash immediately on any other computer. The README claims output lands in
`book/outside-the-lines.pdf` — that is where it *should* go. Change them to
repo-relative paths (`book/outside-the-lines.pdf` and `_sheet.png`, matching
`.gitignore`, which already ignores `_sheet.png`). Create `book/` if missing.

Also worth knowing: there is **no `requirements.txt`** in this repo despite the
README implying a dependency list. See setup below.

---

## 3. Setup and build

Needs **Python 3** with **numpy**, **Pillow**, **pycairo**.

pycairo needs the native cairo library present first:

```bash
# macOS
brew install cairo pkg-config
# Debian/Ubuntu
sudo apt install libcairo2-dev pkg-config python3-dev
```

Then:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install numpy Pillow pycairo
```

Build:

```bash
python3 book.py                        # the full PDF
python3 sheet.py                       # contact sheet of ALL pages -> _sheet.png
python3 sheet.py p3_butterfly p7_city  # just these pages, much faster
```

Run both from the repo root — they do `sys.path.insert(0,'pages')`, so a
different working directory breaks the imports.

**`sheet.py` is the iteration loop.** It renders line art and coloured reveal
side by side with the number count in the caption. Use it constantly; only
build the PDF once a page looks right.

Font: both scripts ask for `"DejaVu Sans"`. If it is missing, cairo silently
substitutes something else and the layout shifts — worth checking if text looks
off.

---

## 4. How the engine works

Coordinate space is **0..1000 × 0..1000, y pointing DOWN**. Everything scales
from there.

A page module defines a `PAGE` dict:

```python
PAGE = dict(
    key="owl", title="THE HOUSE", answer="an owl",
    prompt="This looks like a house.",   # "  Or is it?" is appended by book.py
    ncolors=7,                           # how many swatch boxes to print
    shapes=shapes, thin=thin,
    colors={1:(r,g,b), ...},             # answer-key render ONLY
)
```

### `shapes` — the load-bearing part

An **ordered** list of `(polygon, colour_number)`. Painted like a stack: later
shapes overwrite earlier ones. These are simultaneously the **thick drawn
lines** and the **colour regions**. Order is everything — reordering changes the
picture.

### `thin` — decoration

A list of polylines, stroked hairline (2.4 vs 7.0 line width), never closed,
never a colour boundary, never numbered. This is where the teaching trick lives.

### `colors`

Used **only** for the answer-key reveal. The kid picks their own palette; the
how-to page says so explicitly. Any colour works for any number as long as
different numbers differ. Don't treat these values as prescriptive.

### Number placement is automatic

`label_page()` does it — do not hand-place numbers:

1. Rasterise shapes to a label image, knock out the thick lines.
2. Flood-fill each enclosed region.
3. Find the pole of inaccessibility by repeated erosion — the deepest interior
   point, so the digit sits where there is room.
4. Place up to `MAXLBL=6` labels per region, pushed apart by `SPREAD=3.1`
   radii, skipping regions thinner than `MINR=16`.

Font size scales with region depth, clamped to 21–42pt. Tuning knobs are the
constants at the top of the labelling section in `engine.py`.

### Primitives

`circle`, `ellipse`, `rect`, `arch`, `blob`, `arc`, `scallop_row`, `quoin_edge`,
`mirror`, `poly`. All return plain point lists — compose them with list
concatenation. `mirror(pts, axis=500)` reflects across the vertical centreline,
which is how bilateral pages (owl, butterfly, elephant) stay symmetric: build
the left half, mirror it.

`p5_balloon.py` additionally defines a local `smooth()` (Catmull–Rom) for curvy
organic outlines. It is **not** in `engine.py` — copy it if a new page needs it,
or promote it to the engine.

---

## 5. Design rules for a new or edited page

This is the hard part; the code is easy by comparison.

1. **The ordinary object must win the first glance.** If it reads as the hidden
   thing straight away, the page has failed.
2. **Hide giveaway features as plausible object detail.** In `p1_owl` the owl's
   eyes are window panes, the beak is a gable vent, the toes are stoop posts,
   the tail is the front door. Every hidden feature has an innocent job.
3. **Use decoy shapes.** Paint a shape the same colour as its surroundings so it
   is visible as a line but vanishes in the reveal — e.g. the owl's gable vent
   circle, colour 1 on a colour 1 roof. Sells the ordinary reading at zero cost
   to the hidden one.
4. **Push texture into `thin`.** Shingles, siding, planks, muntins. It makes the
   object convincing and, because colour runs straight over it, costs the
   reveal nothing. This is also the rule the book is teaching, so pages should
   demonstrate it generously.
5. **Keep `ncolors` at 7.** Every current page uses 7; the swatch row in
   `book.py` is laid out for that. More will overflow the row.
6. **Watch region size.** Anything thinner than `MINR=16` gets no number and is
   uncolourable. Check the label count in the `sheet.py` caption.

Workflow for a new page: copy the closest existing `pages/pN_*.py`, design the
double image, then add the module name to `MODS` in **both** `book.py` and
`sheet.py`.

---

## 6. Repo map

```
engine.py        primitives, automatic number placement, cairo drawing
book.py          PDF assembly: cover, how-to, colouring pages, answer pages
sheet.py         contact sheet for reviewing pages — the iteration loop
pages/pN_*.py    one page each, geometry only, exports PAGE
book/            output PDF (committed)
```

`p4_fish` and `p6_elephant` are noted in their docstrings as *reconstructions of
the first-run pages* — earlier versions were lost and rebuilt. If they look
rougher than the others, that is why.

## 7. Voice

The book talks to kids without talking down. Lowercase, dry, a bit conspiratorial
("colours: your call", "your colours will be different — that is allowed", "Or
is it?"). The how-to page is split "For the grown-up" / "For the kid". Match that
register in any new copy. British spelling of *colour* throughout.
