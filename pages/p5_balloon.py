"""THE TEACUP  ->  a hot air balloon."""
from engine import *

# ------------------------------------------------------------------ helpers
def smooth(p, n=10, closed=False):
    p = list(p)
    q = ([p[-1]] + p + [p[0], p[1]]) if closed else ([p[0]] + p + [p[-1]])
    out = []
    for i in range(len(q) - 3):
        p0, p1, p2, p3 = q[i], q[i+1], q[i+2], q[i+3]
        for j in range(n):
            t = j / float(n); t2 = t*t; t3 = t2*t
            out.append((
                0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2
                     + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3),
                0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2
                     + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)))
    if not closed: out.append(p[-1])
    return out

def flower(cx, cy, r):
    out = [circle(cx, cy, r*0.38)]
    for a in range(0, 360, 72):
        out.append(circle(cx + r*math.cos(math.radians(a)),
                          cy + r*math.sin(math.radians(a)), r*0.52))
    return out

CX, CY, R, RY = 500.0, 470.0, 250.0, 48.0    # cup rim
FOOT_Y, FOOT_K = 790.0, 0.36                 # cup foot
NG, NP = 7, 5                                # cup stripes / steam plumes
BUMP = [17, 11, 22, 12, 18]

def spread(n):
    return [CX - R + 2*R*(0.5*(i/float(n)) + 0.5*(0.5 - 0.5*math.cos(math.pi*i/n)))
            for i in range(n + 1)]

XS, PXS = spread(NG), spread(NP)

def up_arc(x):
    return CY - RY*math.sqrt(max(0.0, 1 - ((x - CX)/R)**2))

def rim_y(x):
    return CY + RY*math.sqrt(max(0.0, 1 - ((x - CX)/R)**2))

# steam: a domed mass of curling plumes  ->  the envelope ------------------
DOME = []
for j in range(541):
    a = math.radians(180 + 180.0*j/540)
    u = (math.cos(a) + 1)/2.0
    r = R + BUMP[min(NP - 1, int(u*NP))]*abs(math.sin(NP*math.pi*u))
    DOME.append((CX + r*math.cos(a), CY + r*math.sin(a)))

def dome_split(x):
    for k in range(1, len(DOME)):
        if DOME[k][0] >= x: return k
    return len(DOME) - 1

IDX = [0] + [dome_split(x) for x in PXS[1:-1]] + [len(DOME) - 1]

def plume(i, n=26):
    x0 = PXS[i]; y0 = up_arc(x0); ytop = DOME[IDX[i]][1]
    amp = 40*(x0 - CX)/R
    return [(x0 + amp*math.sin(math.pi*t) + 11*math.sin(3*math.pi*t),
             y0 + (ytop - y0)*t) for t in [j/float(n) for j in range(n + 1)]]

def arc_seg(f, a, b, n=22):
    return [(a + (b - a)*j/n, f(a + (b - a)*j/n)) for j in range(n + 1)]

# cup bowl ----------------------------------------------------------------
def side(x_top, n=24):
    y0 = rim_y(x_top)
    return [(CX + (x_top - CX)*(1 - (1 - FOOT_K)*t**1.3), y0 + (FOOT_Y - y0)*t)
            for t in [j/float(n) for j in range(n + 1)]]

PLUME_COL = [3, 2, 1, 2, 3]
GORE_COL  = [1, 3, 2, 1, 2, 3, 1]

SAUCER = [(CX + (366 + 15*abs(math.sin(9*math.radians(a))))*math.cos(math.radians(a)),
           906 + (62 + 10*abs(math.sin(9*math.radians(a))))*math.sin(math.radians(a)))
          for a in range(0, 360, 3)]

BASKET = smooth([(408,790),(592,790),(600,838),(594,890),(500,900),(406,890),(400,838)],
                6, closed=True)

HO = smooth([(748,478),(852,504),(908,566),(930,632),(896,704),(820,730),(662,712)], 8)
HM = smooth([(738,512),(824,538),(866,588),(880,630),(852,686),(792,702),(658,688)], 8)
HI = smooth([(726,548),(796,570),(826,604),(834,628),(812,666),(766,674),(652,664)], 8)

TAG = smooth([(150,538),(184,548),(202,572),(204,606),(196,646),(184,668),(150,674),
              (116,668),(104,646),(96,606),(98,572),(116,548)], 6, closed=True)

shapes = [(SAUCER, 4),                                   # fluted saucer -> cloud bank
          (ellipse(500, 898, 236, 38), 6)]               # saucer well   -> sky gap
for i in range(NP):                                      # steam plumes  -> upper gores
    shapes.append((plume(i) + DOME[IDX[i]:IDX[i+1]+1] + plume(i+1)[::-1]
                   + arc_seg(up_arc, PXS[i+1], PXS[i]), PLUME_COL[i]))
shapes.append((ellipse(CX, CY, R, RY), 1))               # the tea       -> solid red band
for i in range(NG):                                      # cup stripes   -> lower gores
    shapes.append((arc_seg(rim_y, XS[i], XS[i+1]) + side(XS[i+1])
                   + side(XS[i])[::-1], GORE_COL[i]))
shapes += [(ellipse(CX, 288, 68, 26), 4),                # steam swirl   -> crown vent
           (BASKET, 5),                                  # cup foot      -> basket
           (rect(404, 790, 596, 838), 7),                # foot collar   -> basket rim
           (HO + HM[::-1], 4),                           # handle        -> cloud
           (HM + HI[::-1], 6),                           # handle inner  -> cloud shade
           (TAG, 1),                                     # teabag tag    -> far balloon
           (circle(500, 616, 40), 1),                    # china medallion -> (vanishes)
           (rect(276, 878, 332, 922), 6),                # sugar cube    -> (vanishes)
           (rect(342, 886, 398, 928), 6)]                # sugar cube    -> (vanishes)

# ---------------------------------------------------------------------- thin
thin = []
for t in (0.20, 0.40, 0.60, 0.80):                       # china bands -> fabric seams
    thin.append([side(XS[0] + (XS[-1] - XS[0])*j/40.0)[int(t*24)] for j in range(41)])
for t in (0.30, 0.70):
    p0, p1 = side(XS[0])[int(t*24)], side(XS[-1])[int(t*24)]
    thin.append(scallop_row(p0[0], p1[0], p0[1], 9))
for i in range(NG + 1):                                  # cup flutes -> rigging
    thin.append(side(XS[i])[9:])
for x, y in ((338,600),(662,600),(416,706),(584,706)):
    thin += flower(x, y, 19)                             # china flowers
thin += [circle(500, 616, 22), circle(500, 616, 9)]
for i in range(1, NP):                                   # steam curls
    p = plume(i)
    thin.append([(x + 22*math.sin(2.4*math.pi*j/26.0), y)
                 for j, (x, y) in enumerate(p)])
thin += [smooth([(300,250),(336,196),(392,178),(430,196)], 8),
         smooth([(700,244),(668,190),(608,172),(570,192)], 8)]     # escaping wisps
thin += [ellipse(CX, CY, R - 24, RY - 10), ellipse(CX, 288, 42, 15)]
for x in range(418, 592, 22):                            # wicker
    thin.append([(x, 792), (x + 12, 898)])
thin += [[(404, 858), (596, 858)], [(408, 878), (592, 878)]]
thin += [ellipse(500, 898, 302, 50), ellipse(500, 902, 168, 25)]   # saucer rings
for a in range(0, 360, 12):                              # saucer flutes
    thin.append([(500 + 310*math.cos(math.radians(a)), 906 + 52*math.sin(math.radians(a))),
                 (500 + 368*math.cos(math.radians(a)), 906 + 64*math.sin(math.radians(a)))])
thin += [smooth([(150,532),(196,472),(268,444),(330,458),(362,488)], 8)]   # teabag string
thin += [ellipse(150, 604, 58, 62), [(126,626),(174,626)]]
thin += [smooth([(770,520),(858,548),(896,606),(902,668)], 8),
         smooth([(752,700),(830,690),(872,652)], 8)]     # handle gilt lines
thin += [scallop_row(280, 720, 966, 6), [(56, 942), (214, 934)], [(792, 936), (952, 944)]]

PAGE = dict(
    key="balloon", title="THE TEACUP", answer="a hot air balloon",
    prompt="This looks like a teacup.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1:(0.87,0.29,0.26), 2:(0.98,0.78,0.20), 3:(0.18,0.52,0.72),
            4:(0.99,0.98,0.94), 5:(0.52,0.33,0.19), 6:(0.72,0.82,0.90),
            7:(0.26,0.28,0.33)},
)
