"""THE TREE  ->  an elephant."""
from engine import *
import math
import numpy as np

TAU = 2*math.pi

# ------------------------------------------------------------ local helpers
def eshape(cx, cy, rx, ry, wob=0.05, seed=0, lobes=9):
    """Angle->point sampler for a wobbly ellipse (leaf mass)."""
    rng = np.random.RandomState(seed)
    ph = rng.uniform(0, TAU, 3)
    def rr(a):
        return 1 + wob*(0.6*math.sin(lobes*a+ph[0]) + 0.3*math.sin(2*a+ph[1])
                        + 0.12*math.sin(3*lobes*a+ph[2]))
    def pts(a0=0.0, a1=TAU, m=96):
        out = []
        for i in range(m+1):
            a = a0 + (a1-a0)*i/m
            k = rr(a)
            out.append((cx + rx*k*math.cos(a), cy + ry*k*math.sin(a)))
        return out
    return pts

def closed(sampler, m=96):
    return sampler(0.0, TAU, m)[:-1]

def wavy(x, y0, y1, amp, per, ph, n=22):
    return [(x + amp*math.sin(ph + TAU*(y-y0)/per), y)
            for y in (y0 + (y1-y0)*i/n for i in range(n+1))]

def resample(pts, step=9.0):
    out=[pts[0]]
    for a,b in zip(pts,pts[1:]):
        L=math.hypot(b[0]-a[0],b[1]-a[1])
        n=max(1,int(L/step))
        for i in range(1,n+1):
            out.append((a[0]+(b[0]-a[0])*i/n, a[1]+(b[1]-a[1])*i/n))
    return out

def lumpy(pts, amp=10.0, per=86.0, step=9.0, ph=0.0):
    q=resample(pts, step); out=[]; s=0.0
    for i,(x,y) in enumerate(q):
        a=q[max(0,i-1)]; b=q[min(len(q)-1,i+1)]
        dx,dy=b[0]-a[0], b[1]-a[1]; L=math.hypot(dx,dy) or 1.0
        if i: s+=math.hypot(x-q[i-1][0], y-q[i-1][1])
        k=amp*math.sin(ph+TAU*s/per)
        out.append((x+dy/L*k, y-dx/L*k))
    return out

# --------------------------------------------------------------- geometry
# ONE round leaf mass.  Everything face-like lives INSIDE it as leaf clusters.
CAN  = eshape(500, 340, 360, 300, 0.030, seed=3,  lobes=13)   # canopy -> head+ears
EARL = eshape(274, 378,  92, 156, 0.050, seed=7,  lobes=8)    # left cluster  -> ear
EARR = eshape(726, 378,  92, 156, 0.050, seed=9,  lobes=8)    # right cluster -> ear
HEAD = eshape(500, 372, 122, 182, 0.045, seed=5,  lobes=9)    # middle cluster -> face
FORE = eshape(500, 268,  76,  40, 0.050, seed=6,  lobes=7)    # top cluster -> forehead

# main tree trunk (straight, ordinary) -> near front leg
LTOP = CAN(1.585, 2.03, 24)
leg1 = LTOP + [(346, 700), (350, 800), (334, 902), (486, 902), (476, 800), (480, 700)]
# second smaller trunk -> far front leg
RTOP = CAN(0.88, 1.26, 20)
leg2 = RTOP[::-1] + [(720, 700), (726, 800), (740, 902), (576, 902), (598, 790), (602, 700)]
# root flares at the base -> feet / toenail bands
foot1 = [(304, 854), (496, 854), (508, 902), (294, 902)]
foot2 = [(564, 854), (750, 854), (760, 902), (554, 902)]
# ONE drooping branch, slightly kinked -> the elephant's trunk
branch = CAN(1.28, 1.545, 10) + [(500, 690), (488, 750), (496, 800),
                                (502, 824), (520, 844), (546, 846), (562, 826),
                                (556, 802), (548, 756), (560, 700)]

shapes = []
# grass first so trunks and feet stand on it
shapes.append((lumpy([(40, 898), (500, 892), (960, 898), (960, 962), (40, 962)], 6, 110), 6))
shapes.append((leg1, 2))
shapes.append((leg2, 2))
shapes.append((foot1, 5))
shapes.append((foot2, 5))
shapes.append((branch, 3))
# the one round canopy
shapes.append((closed(CAN, 128), 1))
# decoy clusters, same colour as the canopy -> vanish in the reveal
shapes.append((closed(eshape(352, 138, 70, 40, 0.08, seed=11, lobes=7)), 1))
shapes.append((closed(eshape(655, 148, 64, 40, 0.08, seed=12, lobes=7)), 1))
# leaf clusters inside the canopy -> ears and face
shapes.append((closed(EARL), 7))
shapes.append((closed(EARR), 7))
shapes.append((closed(HEAD), 2))
shapes.append((closed(FORE), 3))
# two bark knots -> eyes (offset heights + sizes, so the line art stays tree-ish)
shapes.append((ellipse(432, 322, 36, 26, -0.15), 4))
shapes.append((ellipse(564, 344, 38, 28, 0.20), 4))
# decoy bark knot on the far trunk, same colour as the trunk -> vanishes
shapes.append((ellipse(660, 748, 30, 22, 0.25), 2))

# ------------------------------------------------------------------- thin
thin = []
# leaf courses running straight across canopy, ears and face alike
for y in (130, 205, 280, 355, 430, 505, 578):
    dx = 360*math.sqrt(max(0.0, 1-((y-340)/300.0)**2)) - 26
    if dx > 60:
        k = max(3, int(2*dx/64))
        thin.append(scallop_row(500-dx, 500+dx, y, k))
# short twigs peeking between the trunks and the leaf mass
thin += [[(422, 634), (452, 584), (472, 552)], [(452, 584), (500, 566)],
         [(646, 620), (612, 578), (596, 548)]]
# leaf tufts hanging off the drooping branch
thin.append([(566, 694), (582, 700)])
thin.append(blob(594, 706, 22, 0.28, seed=8, lobes=6))
thin.append([(350, 736), (336, 732)])
thin.append(blob(324, 730, 20, 0.30, seed=10, lobes=6))
# knot rings: inside the eye knots AND the decoy trunk knot
thin.append(ellipse(432, 322, 17, 11, -0.15))
thin.append(ellipse(564, 344, 18, 12, 0.20))
thin.append(ellipse(660, 748, 14, 9, 0.25))
# extra decoy knots in thin line scattered around
for kx, ky, kr, rot in ((330, 214, 26, 0.3), (690, 468, 23, -0.2),
                        (556, 196, 20, 0.1), (398, 758, 15, 0.2)):
    thin.append(ellipse(kx, ky, kr, kr*0.68, rot))
    thin.append(ellipse(kx, ky, kr*0.5, kr*0.33, rot))
# bark grain down both trunks
for i, x in enumerate(range(368, 468, 28)):
    thin.append(wavy(x, 656, 846, 6, 190, i*0.9))
for i, x in enumerate(range(610, 722, 30)):
    thin.append(wavy(x, 648, 846, 6, 190, 1.3 + i*0.9))
# root ridges -> toes
thin.append(scallop_row(312, 488, 872, 4))
thin.append(scallop_row(572, 744, 872, 3))
# grass blades
for x in range(64, 946, 42):
    thin.append([(x, 956), (x+9, 922), (x+3, 906)])

PAGE = dict(
    key="elephant", title="THE TREE", answer="an elephant",
    prompt="This looks like a tree.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1: (0.45, 0.46, 0.50), 2: (0.66, 0.67, 0.70), 3: (0.83, 0.83, 0.85),
            4: (0.14, 0.13, 0.14), 5: (0.97, 0.94, 0.82), 6: (0.42, 0.66, 0.36),
            7: (0.76, 0.57, 0.57)},
)
