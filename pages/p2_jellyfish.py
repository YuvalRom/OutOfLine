"""THE UMBRELLA  ->  a jellyfish."""
from engine import *

CX, RIM = 500.0, 546.0          # canopy centre-x, rim height
RX, RY  = 400.0, 344.0          # canopy half-width, height
NP      = 6                     # canopy panels
SAGD    = 46.0                  # how far the fabric sags between ribs
BW      = 78.0                  # rim border band width

HALF = [(CX + RX*math.cos(math.radians(270 - 90.0*i/40)),
         RIM + RY*math.sin(math.radians(270 - 90.0*i/40))) for i in range(41)]

def seam(f):                    # apex -> rim, squashed copy of the dome edge
    return [(CX + (x-CX)*f, y) for x, y in HALF]

F     = [1 - 2.0*i/NP for i in range(NP+1)]
CUSPS = [CX - RX*f for f in F]

def dome_x(y):
    t = (RIM-y)/RY
    return RX*math.sqrt(max(0.0, 1 - t*t))

def sag(x0, x1, y, d, n=16):
    cx = (x0+x1)/2.0; r = (x1-x0)/2.0
    return [(cx - r*math.cos(math.pi*i/n), y + d*math.sin(math.pi*i/n)) for i in range(n+1)]

def sag_chain(xs, y, d):
    out = []
    for i in range(len(xs)-1):
        out += sag(xs[i], xs[i+1], y, d)[(1 if i else 0):]
    return out

def cbot(x):                    # y of the scalloped canopy edge at x
    x = min(max(x, CUSPS[0]), CUSPS[-1])
    for i in range(NP):
        if x <= CUSPS[i+1] + 1e-9:
            t = (x - CUSPS[i])/(CUSPS[i+1]-CUSPS[i])
            return RIM + SAGD*math.sin(math.pi*t)
    return RIM

def hang(xc, w0, w1, ylen, amp, freq, phase, n=24):
    """Tassel strand off the fringed edge -> tentacle."""
    y0 = cbot(xc); L = []; R = []
    for i in range(n+1):
        t = i/float(n)
        y = y0 + ylen*t
        dx = amp*math.sin(freq*math.pi*t + phase)*(t**1.3)
        w  = w0 + (w1-w0)*(t**0.8)
        L.append((xc + dx - w/2, y)); R.append((xc + dx + w/2, y))
    top = [(x, cbot(x)) for x in
           (xc + w0/2, xc + w0/4, xc, xc - w0/4, xc - w0/2)]
    return L + R[::-1] + top

# ------------------------------------------------------------------- shapes
shapes = []

# --- hanging tassels first, so the canopy edge paints over their tops
TENT = [(CUSPS[1],  86, 58, 302, -86, 0.85, 0.15, 5),
        (CUSPS[2], 112, 66, 232,  50, 1.45, 0.85, 6),
        (CUSPS[4], 112, 66, 232, -50, 1.45, 0.85, 6),
        (CUSPS[5],  86, 58, 302,  86, 0.85, 0.15, 5)]
for xc, w0, w1, L, a, fq, ph, col in TENT:
    shapes.append((hang(xc, w0, w1, L, a, fq, ph), col))

# --- handle: shaft + crook -> the long central oral arm
HX0, HX1, HY = 478.0, 542.0, 856.0
HC, RO, RI = 446.0, 96.0, 32.0
oarc = [(HC + RO*math.cos(math.radians(a)), HY + RO*math.sin(math.radians(a)))
        for a in [182*i/34 for i in range(35)]]
MR, CR = (RO+RI)/2.0, (RO-RI)/2.0
ccx = HC + MR*math.cos(math.radians(182)); ccy = HY + MR*math.sin(math.radians(182))
tipcap = [(ccx + CR*math.cos(math.radians(182 + 180.0*i/16)),
           ccy + CR*math.sin(math.radians(182 + 180.0*i/16))) for i in range(17)]
iarc = [(HC + RI*math.cos(math.radians(a)), HY + RI*math.sin(math.radians(a)))
        for a in [182 - 182*i/34 for i in range(35)]]
handle = ([(x, cbot(x)) for x in (HX0, 494, 510, 526, HX1)] +
          [(HX1, HY)] + oarc + tipcap + iarc + [(HX0, HY)])
shapes.append((handle, 5))

# --- the canopy panels -> radial bands of the bell
PCOL = [1, 2, 4, 4, 2, 1]
for i in range(NP):
    shapes.append((seam(F[i]) + sag(CUSPS[i], CUSPS[i+1], RIM, SAGD)
                   + seam(F[i+1])[::-1], PCOL[i]))

# --- border band round the hem -> translucent bell margin
top_xs = [CX - dome_x(RIM-BW)] + CUSPS[1:-1] + [CX + dome_x(RIM-BW)]
shapes.append((sag_chain(top_xs, RIM-BW, SAGD*0.72)
               + sag_chain(CUSPS, RIM, SAGD)[::-1], 3))

# --- printed motif at the canopy centre -> stomach + gonads
for k in range(4):
    a = math.radians(45 + 90*k)
    shapes.append((circle(CX + 78*math.cos(a), 388 + 78*math.sin(a), 46), 7))
shapes.append((circle(201, 398, 38), 1))         # decoy dots - vanish
shapes.append((circle(799, 398, 38), 1))

# --- ferrule spike + knob
shapes.append(([(CX-38, RIM-RY), (CX-26, 162), (CX+26, 162), (CX+38, RIM-RY)], 4))
shapes.append((circle(CX, 128, 36), 4))

# --------------------------------------------------------------------- thin
thin = []
for i in range(NP):                              # rib under each panel
    thin.append(seam((F[i]+F[i+1])/2.0))
for i in range(1, NP):                           # rib tips at the hem points
    thin.append(circle(CUSPS[i], RIM + 6, 22))
    thin.append([(CUSPS[i], RIM - 22), (CUSPS[i], RIM + 6)])
for y in (272, 340, 408, 476):                   # fabric contour stitching
    w = dome_x(y)
    thin.append(sag(CX-w+6, CX+w-6, y, 26))
thin.append(sag_chain([CX - dome_x(RIM-36)] + CUSPS[1:-1] + [CX + dome_x(RIM-36)],
                      RIM-36, SAGD*0.86))        # hem stitch line
for xc, w0, w1, L, a, fq, ph, col in TENT:       # beads knotted on the tassels
    for t in (0.22, 0.46, 0.70):
        y = cbot(xc) + L*t
        dx = a*math.sin(fq*math.pi*t + ph)*(t**1.3)
        w  = (w0 + (w1-w0)*(t**0.8))/2 + 4
        thin.append([(xc+dx-w, y-7), (xc+dx+w, y+7)])
        thin.append([(xc+dx-w, y+7), (xc+dx+w, y-7)])
for t in (0.15, 0.35, 0.55, 0.75):               # ruffled edging on the wide ties
    for xc, sgn in ((CUSPS[2], 1), (CUSPS[4], -1)):
        y = cbot(xc) + 232*t
        dx = 50*sgn*math.sin(1.45*math.pi*t + 0.85)*(t**1.3)
        w = (112 - 46*(t**0.8))/2
        thin.append(sag(xc+dx-w+4, xc+dx+w-4, y, 18))
thin += [[(496, 600), (496, 850)], [(524, 600), (524, 850)]]   # handle grain
thin.append([(HC + 64*math.cos(math.radians(a)), HY + 64*math.sin(math.radians(a)))
             for a in [182 - 182*i/24 for i in range(25)]])
def wisp(x, L, amp, fq, ph, n=22):                # fine fringe threads -> wisp tentacles
    return [(x + amp*math.sin(fq*math.pi*(i/float(n)) + ph)*((i/float(n))**1.3),
             cbot(x) + L*(i/float(n))) for i in range(n+1)]
for x, L, a, fq, ph in ((116, 300, -54, 1.0, 0.2), (142, 236, -40, 1.3, 0.5),
                        (167, 322, -30, 0.9, 0.1), (293, 268,  34, 1.5, 0.7),
                        (296, 190, -26, 1.2, 0.4), (441, 344,  30, 1.1, 0.3),
                        (559, 344, -30, 1.1, 0.3), (704, 190,  26, 1.2, 0.4),
                        (707, 268, -34, 1.5, 0.7), (833, 322,  30, 0.9, 0.1),
                        (858, 236,  40, 1.3, 0.5), (884, 300,  54, 1.0, 0.2)):
    thin.append(wisp(x, L, a, fq, ph))
thin.append(sag_chain([CX - dome_x(RIM-14)] + CUSPS[1:-1] + [CX + dome_x(RIM-14)],
                      RIM-14, SAGD*0.94))        # fringe braid
for cx, cy, r in ((86, 706, 20), (914, 668, 18), (128, 900, 16),
                  (876, 916, 18), (70, 486, 15), (932, 522, 16),
                  (268, 946, 15), (686, 950, 17)):
    thin.append(ellipse(cx, cy, r*0.78, r))      # raindrops -> plankton
for x, y in ((66, 300), (118, 196), (884, 214), (928, 320),
             (206, 128), (792, 116), (52, 604), (930, 616)):
    thin.append([(x, y), (x+22, y+52)])          # rain -> marine snow


PAGE = dict(
    key="jellyfish", title="THE UMBRELLA", answer="a jellyfish",
    prompt="This looks like an umbrella.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1: (0.45, 0.22, 0.60), 2: (0.78, 0.42, 0.78), 3: (0.99, 0.79, 0.88),
            4: (1.00, 0.95, 0.80), 5: (0.20, 0.70, 0.74), 6: (0.92, 0.36, 0.50),
            7: (0.20, 0.13, 0.38)},
)
