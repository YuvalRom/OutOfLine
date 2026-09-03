"""THE SAILBOAT -> a fat orange fish.  Reconstruction of the first-run page."""
import math
from engine import *

def earc(cx, cy, rx, ry, rot, a0, a1, n=48):
    c, s = math.cos(rot), math.sin(rot); out = []
    for i in range(n+1):
        a = math.radians(a0 + (a1-a0)*i/n)
        x, y = rx*math.cos(a), ry*math.sin(a)
        out.append((cx + x*c - y*s, cy + x*s + y*c))
    return out

CX, CY, RX, RY, ROT = 435, 665, 385, 192, -0.10
HULL  = earc(CX, CY, RX, RY, ROT, 0, 360, 96)
BELLY = earc(CX, CY, RX, RY, ROT, 16, 164)                      # bottom arc + chord
DECK  = earc(CX, CY, RX, RY, ROT, 188, 350) \
      + earc(CX, CY+8, RX-36, RY-98, ROT, 346, 192)[::1]        # curved teal band

MHX, MHY = 640, 66                                              # masthead

shapes = [
    ([(700,716),(796,692),(836,852),(716,876)], 4),             # rudder  -> rear fin
    ([(448,776),(566,782),(548,946),(460,940)], 4),             # keel    -> pelvic fin
    ([(MHX+6,MHY+10),(924,414),(846,486),(600,560)], 5),        # mainsail-> tail fin
    ([(MHX+6,MHY+10),(834,398),(730,448),(624,520),(600,560)], 4),  # inner field
    ([(MHX-16,MHY+18),(186,470),(430,540),(560,560)], 5),       # jib     -> dorsal fin
    ([(MHX-16,MHY+18),(280,452),(420,500),(560,560)], 4),       # jib inner field
    ([(556,560),(582,552),(MHX+13,MHY),(MHX-13,MHY)], 5),       # mast    -> fin spine
    ([(MHX-13,MHY+4),(MHX-13,MHY+46),(538,84)], 4),             # pennant -> tail tip
    (HULL, 2),                                                  # hull    -> body
    (ellipse(292,650,44,124,rot=-0.08), 5),                     # bulkhead-> gill plate
    (BELLY, 3),                                                 # boot top-> belly
    (DECK, 1),                                                  # sheer   -> dark back
    (ellipse(402,712,58,90,rot=0.35), 4),                       # leeboard-> pectoral fin
    (circle(168,630,58), 5),                                    # port ring -> eye ring
    (circle(168,630,40), 7),                                    # glass   -> eye white
    (circle(168,630,17), 6),                                    # bolt    -> pupil
    ([(70,680),(150,670),(152,714),(88,728)], 6),               # hawse   -> mouth
    (circle(516,656,30), 2),                                    # porthole-> (vanishes)
    (circle(618,638,30), 2),                                    # porthole-> (vanishes)
]

thin = []
for dy in (-8, 44, 96):                                         # planking -> scale rows
    thin.append(earc(CX, CY+dy, RX-26, RY-30, ROT, 18, 162, 40))
thin += [scallop_row(150, 700, 706, 7), scallop_row(180, 660, 756, 6)]
for f in (0.34, 0.62):                                          # sail seams -> fin rays
    thin.append([(MHX+6+(924-MHX-6)*f, MHY+10+(414-MHY-10)*f),
                 (600+(846-600)*f*0.6, 560-(560-486)*f*0.4)])
    thin.append([(MHX-16+(186-MHX+16)*f, MHY+18+(470-MHY-18)*f),
                 (560-(560-430)*f, 560-(560-540)*f)])
thin += [[(MHX-4,MHY),(110,594)], [(MHX+4,MHY),(788,540)]]      # stays
for i in range(8):                                              # bolts on the port ring
    bx = 168 + 72*math.cos(math.pi*i/4); by = 630 + 72*math.sin(math.pi*i/4)
    thin.append(circle(bx, by, 6) + [circle(bx, by, 6)[0]])
for y in (908, 946, 980):                                       # wake
    thin.append(scallop_row(60, 940, y, 8))

PAGE = dict(
    key="fish", title="THE SAILBOAT", answer="a fish",
    prompt="This looks like a sailboat.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1:(0.13,0.36,0.44), 2:(0.94,0.55,0.18), 3:(0.98,0.92,0.77),
            4:(0.88,0.30,0.23), 5:(0.98,0.75,0.20), 6:(0.17,0.14,0.12),
            7:(0.99,0.99,0.96)},
)
