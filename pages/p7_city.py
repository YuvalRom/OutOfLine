"""THE BOOKSHELF  ->  a city at night."""
from engine import *
import math

BASE = 868          # top face of the shelf board -> street level

# ------------------------------------------------------------ local helpers
def tw(bx0, bx1, tx0, tx1, ty):
    """A standing book: returns f(y) -> (left, right) so it may lean."""
    def at(y):
        t = (BASE - y) / float(BASE - ty)
        return (bx0 + (tx0-bx0)*t, bx1 + (tx1-bx1)*t)
    at.top = ty
    return at

def body(at):
    l0, r0 = at(at.top); l1, r1 = at(BASE)
    return [(l0, at.top), (r0, at.top), (r1, BASE), (l1, BASE)]

def band(at, y0, y1):
    l0, r0 = at(y0); l1, r1 = at(y1)
    return [(l0, y0), (r0, y0), (r1, y1), (l1, y1)]

def band_grid(at, y0, y1):
    """Thin ruled lines inside a title band -> a lit window grid."""
    out = []
    rows = max(1, int((y1-y0)/46))
    for i in range(1, rows+1):
        y = y0 + (y1-y0)*i/(rows+1)
        l, r = at(y)
        out.append([(l+10, y), (r-10, y)])
    for f in (0.22, 0.42, 0.62, 0.82):
        p = []
        yy = y0 + 8
        while yy <= y1 - 6:
            l, r = at(yy)
            p.append((l + (r-l)*f, yy))
            yy += 18
        out.append(p)
    return out

def ribs(at, bands, step=112):
    """Raised bands on a dark spine -> faint floor lines on a tower."""
    out = []
    y = at.top + 78
    while y < BASE - 56:
        if not any(b0-20 <= y <= b1+26 for b0, b1, _ in bands):
            for dy in (0, 12):
                l, r = at(y+dy)
                out.append([(l+8, y+dy), (r-8, y+dy)])
        y += step
    return out

def wave(x0, x1, y, amp=7, per=150, n=40):
    return [(x0 + (x1-x0)*i/n, y + amp*math.sin(6.0*(x0+(x1-x0)*i/n)/per))
            for i in range(n+1)]

# --------------------------------------------------------------- the books
#        bx0  bx1  tx0  tx1  top   colour   title bands (thick)
BOOKS = [
    (tw( 50, 152,  50, 152, 520), 2, [(798, BASE, 5)]),
    (tw(152, 262, 166, 276, 250), 3, [(250, 322, 5)]),
    (tw(262, 360, 262, 360, 600), 4, [(680, 744, 5), (806, BASE, 5)]),
    (tw(360, 478, 360, 478, 160), 2, [(392, 468, 5), (700, BASE, 7)]),
    (tw(478, 586, 446, 554, 372), 3, [(372, 442, 5)]),
    (tw(586, 702, 586, 702, 108), 4, [(300, 372, 5)]),
    (tw(702, 820, 688, 806, 430), 2, [(798, BASE, 5)]),
]

shapes = []
# back panel of the case -> night sky
shapes.append((rect(44, 54, 956, BASE), 1))
# shelf board and its front edge -> the street
shapes.append((rect(44, 866, 956, 974), 6))
# the bookcase itself: top board, both uprights and a little centre crest,
# all one piece -> it vanishes into the night sky
shapes.append(([(8, 18), (992, 18), (992, 974), (956, 974), (956, 54),
                (532, 54), (532, 86), (468, 86), (468, 54),
                (44, 54), (44, 974), (8, 974)], 1))
# plate propped at the back of the shelf -> the moon
shapes.append((circle(146, 196, 86), 7))
# the books -> tower blocks
for at, col, bands in BOOKS:
    shapes.append((body(at), col))
    for y0, y1, bc in bands:
        shapes.append((band(at, y0, y1), bc))
# small book lying flat on the tallest one -> roof water tank
shapes.append((rect(590, 72, 700, 108), 4))
# book lying flat on the short dark one -> decoy: vanishes into the block below
shapes.append((rect(254, 544, 372, 600), 4))
# potted plant at the end of the row -> a tree in the street
shapes.append((blob(886, 728, 78, 0.13, seed=4), 4))
shapes.append(([(848, 802), (932, 802), (920, 866), (860, 866)], 6))

# ------------------------------------------------------------------- thin
thin = []
for sx, sy, sr in ((250,150,7),(420,120,6),(560,72,5),(762,140,7),(884,96,6)):
    thin.append(circle(sx, sy, sr) + [circle(sx, sy, sr)[0]])   # panel dots -> stars
for at, col, bands in BOOKS:
    # head and tail bands of the binding
    l, r = at(at.top + 24)
    thin.append([(l+7, at.top+24), (r-7, at.top+24)])
    l, r = at(BASE - 24)
    thin.append([(l+7, BASE-24), (r-7, BASE-24)])
    # author rules near the head
    for dy in (52, 66):
        l, r = at(at.top + dy)
        w = r - l
        thin.append([(l + w*0.22, at.top+dy), (r - w*0.22, at.top+dy)])
    # ruled lines over the lit title bands only -> window grids
    for y0, y1, bc in bands:
        if bc in (5, 7):
            thin += band_grid(at, y0, y1)
    # ribbed spines on the two dark books only
    if col == 4:
        thin += ribs(at, bands)
# publisher mark at the spine foot of a few books
for at in (BOOKS[0][0], BOOKS[3][0], BOOKS[6][0]):
    l, r = at(BASE - 52)
    thin.append(circle((l+r)/2.0, BASE-52, 9, 24))
# title panels pasted on two spines
for x0, x1, y0, y1 in ((596, 692, 400, 500), (166, 246, 500, 596)):
    thin.append(rect(x0, y0, x1, y1) + [(x0, y0)])
    for i in range(1, 4):
        thin.append([(x0+12, y0 + (y1-y0)*i/4.0), (x1-12, y0 + (y1-y0)*i/4.0)])
# page edges on the two lying books
thin.append([(598, 94), (692, 94)])
thin.append([(680, 78), (680, 104)])
thin.append([(262, 572), (364, 572)])
thin.append([(352, 550), (352, 596)])
# wood grain on the case frame + shelf-pin holes up the uprights
thin.append(wave(16, 984, 40, 2.5, 420))
for x in (28, 972):
    thin.append([(x, 78), (x, 858)])
    for y in range(180, 820, 130):
        thin.append(circle(x, y, 6, 16))
# grain on the back panel -> thin clouds
for x0, x1, y, a in ((60, 566, 80, 6), (690, 938, 66, 5), (60, 352, 212, 7),
                     (700, 940, 258, 6), (474, 588, 306, 4), (60, 148, 404, 5)):
    thin.append(wave(x0, x1, y, a))
# clock ticks on the plate -> light round the moon
for i in range(12):
    a = math.radians(i*30)
    thin.append([(146 + 68*math.cos(a), 196 + 68*math.sin(a)),
                 (146 + 80*math.cos(a), 196 + 80*math.sin(a))])
thin.append(circle(146, 196, 26))
# shelf lip and board grain -> kerb and lane markings
thin.append([(44, 902), (956, 902)])
thin.append(wave(56, 944, 946, 4, 260))
for x in range(80, 930, 96):
    thin.append([(x, 928), (x+52, 928)])
# leaves on the plant -> the tree in the street
for a in range(0, 360, 40):
    r = math.radians(a)
    thin.append([(886, 728), (886 + 64*math.cos(r), 728 + 64*math.sin(r))])
thin.append([(886, 792), (886, 812)])

PAGE = dict(
    key="city", title="THE BOOKSHELF", answer="a city at night",
    prompt="This looks like a shelf of books.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1: (0.10, 0.14, 0.30), 2: (0.30, 0.38, 0.55), 3: (0.44, 0.33, 0.29),
            4: (0.13, 0.14, 0.22), 5: (0.99, 0.83, 0.34), 6: (0.34, 0.35, 0.39),
            7: (0.98, 0.96, 0.86)},
)
