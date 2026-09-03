"""Shared engine for the 'Outside the Lines' colouring book.

A page is ONE simple line drawing whose contours read as a second, detailed
picture once coloured (Rob Gonsalves style shared-contour double image).

    shapes : ordered [(polygon, colour_number)] - painted like a stack.
             These ARE the thick drawn lines AND the colour boundaries.
    thin   : [polyline] - decoration (shingles, planks, veins, scales...).
             Drawn hairline. Colour runs STRAIGHT OVER these; they never
             split a colour region and never get a number.

Coordinate space is 0..1000 in x and y, y pointing DOWN.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
import cairo

# ---------------------------------------------------------------- primitives
def circle(cx, cy, r, n=80):
    return [(cx + r*math.cos(2*math.pi*i/n), cy + r*math.sin(2*math.pi*i/n)) for i in range(n)]

def ellipse(cx, cy, rx, ry, rot=0.0, n=96):
    c, s = math.cos(rot), math.sin(rot)
    out = []
    for i in range(n):
        a = 2*math.pi*i/n
        x, y = rx*math.cos(a), ry*math.sin(a)
        out.append((cx + x*c - y*s, cy + x*s + y*c))
    return out

def rect(x0, y0, x1, y1):
    return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]

def arch(x0, y0, x1, y1, n=36):
    """Rectangle whose top edge (at y0) is a semicircle; bottom edge at y1."""
    cx = (x0+x1)/2.0; r = (x1-x0)/2.0
    pts = [(x0, y1), (x0, y0)]
    for i in range(n+1):
        a = math.pi - math.pi*i/n
        pts.append((cx + r*math.cos(a), y0 - r*math.sin(a)))
    return pts + [(x1, y1)]

def blob(cx, cy, r, wobble, seed=0, n=64, lobes=7):
    """Soft organic closed shape - clouds, foliage, splashes."""
    rng = np.random.RandomState(seed)
    ph = rng.uniform(0, 2*math.pi, 3)
    out = []
    for i in range(n):
        a = 2*math.pi*i/n
        rr = r*(1 + wobble*(0.6*math.sin(lobes*a+ph[0]) + 0.3*math.sin(2*a+ph[1])
                            + 0.1*math.sin(3*lobes*a+ph[2])))
        out.append((cx + rr*math.cos(a), cy + rr*math.sin(a)))
    return out

def arc(cx, cy, r, a0, a1, n=32):
    """Open arc polyline, angles in degrees, 0 = east, clockwise on screen."""
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*i/n)),
             cy + r*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]

def scallop_row(x0, x1, y, k, down=True, n=14):
    """Row of k half-circles - fish-scale shingles, feathers, waves."""
    w = (x1-x0)/k; r = w/2.0; pts = [(x0, y)]
    for i in range(k):
        cx = x0 + w*i + r
        for j in range(1, n+1):
            a = math.pi - math.pi*j/n
            pts.append((cx + r*math.cos(a), y + (r*math.sin(a) if down else -r*math.sin(a))))
    return pts

def quoin_edge(x_in, x_out, y0, y1, steps):
    """Stepped vertical edge: corner stones one way, feather edge the other."""
    pts = []; h = (y1-y0)/float(steps)
    for i in range(steps):
        x = x_out if i % 2 else x_in
        pts += [(x, y0 + h*i), (x, y0 + h*(i+1))]
    return pts

def mirror(pts, axis=500.0):
    return [(2*axis - x, y) for x, y in pts]

def poly(*pts):
    return list(pts)

# ------------------------------------------------------------- face labelling
S = 1000; LINE_W = 7; MAXLBL = 6; MINR = 16; SPREAD = 3.1

def _erode(m):
    o = m.copy()
    o[1:,:] &= m[:-1,:]; o[:-1,:] &= m[1:,:]
    o[:,1:] &= m[:,:-1]; o[:,:-1] &= m[:,1:]
    o[0,:] = o[-1,:] = False; o[:,0] = o[:,-1] = False
    return o

def label_page(page):
    lab = Image.new('L', (S,S), 0); d = ImageDraw.Draw(lab)
    for pts, num in page['shapes']:
        d.polygon([(x,y) for x,y in pts], fill=num)
    ln = Image.new('L', (S,S), 0); dl = ImageDraw.Draw(ln)
    for pts, num in page['shapes']:
        dl.line([(x,y) for x,y in pts] + [tuple(pts[0])], fill=255, width=LINE_W, joint='curve')
    work = np.array(lab); work[np.array(ln) > 0] = 0

    img = Image.fromarray(work); arr = np.array(img); out = []
    yy, xx = np.mgrid[0:S, 0:S]
    while True:
        ys, xs = np.nonzero((arr > 0) & (arr < 100))
        if len(ys) == 0: break
        seed = (int(xs[0]), int(ys[0])); num = int(arr[seed[1], seed[0]])
        ImageDraw.floodfill(img, seed, 100); arr = np.array(img)
        mask = arr == 100; remain = mask.copy()
        for _ in range(MAXLBL):
            m = remain.copy(); dt = np.zeros(mask.shape, np.int32); depth = 0
            while m.any():
                dt[m] += 1; depth += 1; m = _erode(m)
            if depth < MINR: break
            iy, ix = np.unravel_index(np.argmax(dt), dt.shape)
            out.append(dict(num=num, x=float(ix), y=float(iy), radius=depth))
            remain &= ((xx-ix)**2 + (yy-iy)**2) > (depth*SPREAD)**2
            if not remain.any(): break
        img.paste(0, (0,0), Image.fromarray(mask)); arr = np.array(img)
    return out

# -------------------------------------------------------------------- drawing
DEFAULT_COLORS = {1:(0.85,0.35,0.28), 2:(0.28,0.55,0.82), 3:(0.97,0.78,0.22),
                  4:(0.20,0.18,0.17), 5:(0.45,0.72,0.45), 6:(0.72,0.50,0.82),
                  7:(0.98,0.92,0.80), 8:(0.55,0.36,0.22)}

def _path(cr, pts, closed):
    cr.move_to(*pts[0])
    for p in pts[1:]: cr.line_to(*p)
    if closed: cr.close_path()

def draw_art(cr, page, x0, y0, size, filled=False, numbers=True, labels=None):
    k = size/1000.0
    cols = dict(DEFAULT_COLORS); cols.update(page.get('colors', {}))
    cr.save(); cr.translate(x0, y0); cr.scale(k, k)
    cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    if filled:
        for pts, num in page['shapes']:
            cr.set_source_rgb(*cols[num]); _path(cr, pts, True); cr.fill()
    cr.set_source_rgb(0,0,0)
    cr.set_line_width(2.4)
    for pts in page.get('thin', []):
        _path(cr, pts, False); cr.stroke()
    cr.set_line_width(7.0)
    for pts, num in page['shapes']:
        _path(cr, pts, True); cr.stroke()
    if numbers and labels:
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        for z in labels:
            cr.set_font_size(max(21.0, min(z['radius']*1.5, 42.0)))
            s = str(z['num']); xb, yb, w, h, _, _ = cr.text_extents(s)
            cr.set_source_rgb(0,0,0)
            cr.move_to(z['x'] - w/2 - xb, z['y'] - h/2 - yb); cr.show_text(s)
    cr.restore()

def preview(page, path, px=760):
    """Side-by-side PNG: line art with numbers | the coloured reveal."""
    labels = label_page(page)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, px*2 + 30, px + 20)
    c = cairo.Context(s); c.set_source_rgb(1,1,1); c.paint()
    draw_art(c, page, 10, 10, px, filled=False, numbers=True, labels=labels)
    draw_art(c, page, px+20, 10, px, filled=True,  numbers=False)
    s.write_to_png(path)
    from collections import Counter
    return dict(labels=len(labels), per_colour=dict(Counter(z['num'] for z in labels)))
