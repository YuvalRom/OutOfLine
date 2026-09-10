"""Portable, deterministic reconstruction. No native Cairo required.

python recreate.py --output-dir ./book/recreated
"""
from pathlib import Path
import argparse
import importlib
import json
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import engine

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'pages'))
MODS = ['p1_owl', 'p2_jellyfish', 'p3_butterfly', 'p4_fish',
        'p5_balloon', 'p6_elephant', 'p7_city']
FONT = 'Helvetica'
BOLD = 'Helvetica-Bold'
if (ROOT / 'fonts/DejaVuSans.ttf').exists():
    pdfmetrics.registerFont(TTFont('Book', str(ROOT / 'fonts/DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('BookBold', str(ROOT / 'fonts/DejaVuSans-Bold.ttf')))
    FONT, BOLD = 'Book', 'BookBold'

def labels(page):
    """Same taxicab erosion/spread rule as the recovered engine, accelerated.

    Cleaned pages mask hidden outlines in the same order as vector rendering.
    Untouched pages retain the recovered prototype's original outline rule.
    """
    size = engine.S
    lab = Image.new('L', (size, size), 0)
    d = ImageDraw.Draw(lab)
    ink = Image.new('L', (size, size), 0)
    di = ImageDraw.Draw(ink)
    for i, (pts, num) in enumerate(page['shapes']):
        d.polygon(pts, fill=num)
        if page.get('occlude_outlines'):
            di.polygon(pts, fill=0)
        di.line(pts + [pts[0]], fill=255,
                width=round(page.get('outline_widths', {}).get(i, engine.LINE_W)), joint='curve')
    arr = np.array(lab)
    arr[np.array(ink) > 0] = 0
    yy, xx = np.mgrid[:size, :size]
    result, missing = [], []
    for num in sorted(page['colors']):
        components, count = ndimage.label(arr == num)
        for component in range(1, count + 1):
            mask = components == component
            remain = mask.copy()
            placed = 0
            for _ in range(engine.MAXLBL):
                # Explicit padding agrees with erosion treating the edge as outside.
                dt = ndimage.distance_transform_cdt(np.pad(remain, 1), metric='taxicab')[1:-1, 1:-1]
                depth = int(dt.max())
                if depth < engine.MINR:
                    break
                iy, ix = np.unravel_index(np.argmax(dt), dt.shape)
                result.append(dict(num=int(num), x=int(ix), y=int(iy), radius=depth))
                placed += 1
                remain &= ((xx-ix)**2 + (yy-iy)**2) > (depth*engine.SPREAD)**2
            if not placed:
                missing.append(dict(num=int(num), area=int(mask.sum())))
    return result, missing

def path(c, pts, close=False):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for xy in pts[1:]:
        p.lineTo(*xy)
    if close:
        p.close()
    return p

def art(c, page, x, top, size, height, filled=False, numbered=None):
    c.saveState()
    c.translate(x, height-top)
    c.scale(size/1000, -size/1000)
    c.setLineJoin(1)
    c.setLineCap(1)
    if page.get('occlude_outlines'):
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(2.4)
        for pts in page.get('background', []):
            c.drawPath(path(c, pts))
        for i, (pts, num) in enumerate(page['shapes']):
            c.setFillColorRGB(*(page['colors'][num] if filled else (1,1,1)))
            c.drawPath(path(c, pts, True), fill=1, stroke=0)
            # Detail belongs to one shape and is clipped to that shape.
            # Later filled shapes also hide it, so scales cannot cover fins,
            # portholes, the deck band, or the space outside the hull.
            c.saveState()
            c.clipPath(path(c, pts, True), stroke=0, fill=0)
            c.setLineWidth(page.get('detail_widths', {}).get(i, 2.4))
            for line in page.get('details', {}).get(i, []):
                c.drawPath(path(c, line))
            c.restoreState()
            c.setLineWidth(page.get('outline_widths', {}).get(i, 7))
            c.drawPath(path(c, pts, True))
        c.setLineWidth(2.4)
        for pts in page.get('foreground', []):
            c.drawPath(path(c, pts))
    elif filled:
        for pts, num in page['shapes']:
            c.setFillColorRGB(*page['colors'][num])
            c.drawPath(path(c, pts, True), fill=1, stroke=0)
    if not page.get('occlude_outlines'):
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(2.4)
        for pts in page['thin']:
            c.drawPath(path(c, pts))
        c.setLineWidth(7)
        for pts, _ in page['shapes']:
            c.drawPath(path(c, pts, True))
    for z in numbered or []:
        c.saveState()
        c.translate(z['x'], z['y'])
        c.scale(1, -1)
        fs = max(21, min(z['radius']*1.5, 42))
        c.setFillColorRGB(0, 0, 0)
        c.setFont(BOLD, fs)
        if page.get('occlude_outlines'):
            # Keep retained thin details from running through a digit.
            c.setStrokeColorRGB(1, 1, 1)
            c.setLineWidth(5)
            halo = c.beginText()
            halo.setTextOrigin(-pdfmetrics.stringWidth(str(z['num']), BOLD, fs)/2, -fs*.36)
            halo.setFont(BOLD, fs)
            halo.setTextRenderMode(2)
            halo.textOut(str(z['num']))
            halo.setTextRenderMode(0)
            c.drawText(halo)
        c.drawCentredString(0, -fs*.36, str(z['num']))
        c.restoreState()
    c.restoreState()

def text(c, s, x, top, size, height, bold=False, centered=False):
    c.setFillColorRGB(0, 0, 0)
    c.setFont(BOLD if bold else FONT, size)
    (c.drawCentredString if centered else c.drawString)(x, height-top, s)

def contact(c, pages, all_labels):
    width, height = 890, 464*len(pages)+10
    c.setPageSize((width, height))
    for i, p in enumerate(pages):
        y = 10+464*i
        lb = all_labels[p['key']]
        caption = f"{p['title']}  ->  {p['answer']}   ({len(lb)} numbers, 7 colours)"
        text(c, caption, 12, y+20, 19, height, True)
        art(c, p, 10, y+26, 430, height, numbered=lb)
        art(c, p, 450, y+26, 430, height, filled=True)
    c.showPage()

def cover(c):
    """A crayon escaping a frame: no puzzle artwork or answers on the cover."""
    w, h = 612, 792
    text(c, 'OutOfLine', w/2, 165, 58, h, True, True)
    text(c, "What if the lines weren't the boss?", w/2, 207, 16, h, centered=True)
    c.saveState()
    c.translate(0, h)
    c.scale(1, -1)
    c.setLineCap(1)
    c.setLineJoin(1)
    # A slightly wonky box, with colour happily travelling beyond its edges.
    c.setStrokeColorRGB(.12,.13,.16)
    c.setLineWidth(3)
    c.drawPath(path(c, [(181,303),(400,288),(418,505),(199,520)], True))
    p=c.beginPath()
    p.moveTo(214,455)
    p.curveTo(250,473,265,348,302,358)
    p.curveTo(345,369,302,466,350,454)
    p.curveTo(397,442,397,350,454,324)
    c.setStrokeColorRGB(.08,.65,.69)
    c.setLineWidth(15)
    c.drawPath(p)
    p=c.beginPath()
    p.moveTo(145,405)
    p.curveTo(175,341,255,333,276,390)
    p.curveTo(300,452,199,482,205,420)
    p.curveTo(213,352,363,398,447,441)
    c.setStrokeColorRGB(.99,.68,.12)
    c.setLineWidth(12)
    c.drawPath(p)
    p=c.beginPath()
    p.moveTo(235,490)
    p.curveTo(191,540,313,570,337,514)
    p.curveTo(363,452,258,430,314,398)
    p.curveTo(350,377,403,386,444,372)
    c.setStrokeColorRGB(.55,.35,.75)
    c.setLineWidth(10)
    c.drawPath(p)
    # Crayon tip touches the purple trail outside the box.
    c.saveState()
    c.translate(444,372)
    c.rotate(-27)
    c.setStrokeColorRGB(.12,.13,.16)
    c.setLineWidth(2)
    c.setFillColorRGB(.78,.65,.89)
    c.drawPath(path(c, [(0,0),(27,-15),(107,-15),(114,-9),(114,9),(107,15),(27,15)],True),fill=1)
    c.setFillColorRGB(.55,.35,.75)
    c.drawPath(path(c, [(0,0),(27,-15),(27,15)],True),fill=1)
    c.setFillColorRGB(.91,.84,.96)
    c.rect(39,-15,57,30,fill=1,stroke=1)
    c.setLineWidth(3)
    c.line(47,-10,47,10)
    c.line(87,-10,87,10)
    c.restoreState()
    # Small, open-ended doodles invite the reader to add their own.
    for x,y,r in [(124,302,12),(472,506,15),(369,255,9)]:
        c.setStrokeColorRGB(.12,.13,.16)
        c.setLineWidth(2)
        c.drawPath(path(c,[(x,y-r),(x+3,y-3),(x+r,y),(x+3,y+3),
                           (x,y+r),(x-3,y+3),(x-r,y),(x-3,y-3)],True))
    for x,y,color in [(122,475,(.99,.68,.12)),(459,268,(.55,.35,.75)),
                      (421,562,(.08,.65,.69))]:
        c.setFillColorRGB(*color)
        c.circle(x,y,5,fill=1,stroke=0)
    c.restoreState()
    text(c, 'Go on. Get carried away.', w/2, 622, 21, h, True, True)
    text(c, 'A colouring book for curious minds', w/2, 657, 13, h, centered=True)
    text(c, 'YOUR IMAGINATION STARTS HERE', w/2, 732, 9, h, True, True)

def book(c, pages, all_labels):
    w, h = 612, 792
    c.setPageSize((w, h))
    from cover_alternative import cover as airplane_cover
    airplane_cover(c)
    c.showPage()
    text(c, 'Look. Colour. Look again.', 48, 88, 28, h, True)
    instructions = [
        'Start with what you see. A house? An umbrella? A flower?',
        'You can colour that picture any way you like.',
        '',
        'To try the hidden picture:',
        '1. Pick a different colour for each number.',
        '2. Fill the colour boxes at the bottom of the page.',
        '3. Use the same colour wherever you find that number.',
        '4. Colour across the thin decoration lines.',
        '5. Stop at the thick lines. Then look again.',
        '',
        'Or invent a third picture. Add something nobody else sees.',
        '',
        'For a grown-up',
        'This is a reconstruction to review together, not a finished edition.',
        'Some spaces are small; younger children may want a helper.',
        'The examples at the back show just one possible colour palette.',
    ]
    for i, line in enumerate(instructions):
        text(c, line, 48, 150+i*28, 12, h, i in (3, 12))
    text(c, 'The lines are not the boss of you.', w/2, 720, 16, h, True, True)
    c.showPage()
    for i, p in enumerate(pages, 1):
        text(c, f"{i:02d}  /  {p['title']}", 48, 66, 24, h, True)
        text(c, p['prompt']+'  What else could it be?', 48, 91, 12, h)
        art(c, p, 42, 112, 528, h, numbered=all_labels[p['key']])
        text(c, 'YOUR COLOURS', 48, 679, 10, h, True)
        for num in range(1, 8):
            x = 55+(num-1)*76
            text(c, str(num), x+18, 701, 12, h, True, True)
            c.setLineWidth(1)
            c.rect(x, h-744, 36, 34)
        text(c, 'Thick line: stop.    Thin line: colour across it.', w/2, 769, 10, h, centered=True)
        c.showPage()
    for start in range(0, len(pages), 4):
        text(c, 'A SECOND LOOK', 48, 70, 25, h, True)
        text(c, 'One possible palette. Your colours can be different.', 48, 95, 11, h)
        for j, p in enumerate(pages[start:start+4]):
            x = 42+(j%2)*270
            y = 125+(j//2)*300
            art(c, p, x, y, 240, h, filled=True)
            text(c, f"{start+j+1}. {p['answer']}", x+120, y+267, 12, h, True, True)
        c.showPage()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', type=Path, default=ROOT/'book/recreated')
    ap.add_argument('--saved-geometry', action='store_true', help='Render the unchanged Git geometry instead of reference reconstructions.')
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pages = [importlib.import_module(m).PAGE for m in MODS]
    if not args.saved_geometry:
        from reference_reconstruction import rebuild
        pages = rebuild(pages)
    all_labels, audit = {}, {}
    for p in pages:
        lb, missing = labels(p)
        all_labels[p['key']] = lb
        audit[p['key']] = dict(labels=len(lb), unlabelled_components=missing)
        print(p['key'], len(lb), 'labels;', len(missing), 'unlabelled small components', flush=True)
    c = canvas.Canvas(str(args.output_dir/'outofline-reconstruction-sheets.pdf'), invariant=1)
    c.setTitle('OutOfLine - reconstruction contact sheets')
    contact(c, pages[:4], all_labels)
    contact(c, pages[4:], all_labels)
    c.save()
    c = canvas.Canvas(str(args.output_dir/'outofline-reconstruction-book.pdf'), invariant=1)
    c.setTitle('OutOfLine - reconstruction proof')
    book(c, pages, all_labels)
    c.save()
    (args.output_dir/'region-audit.json').write_text(json.dumps(audit, indent=2)+'\n')

if __name__ == '__main__':
    main()
