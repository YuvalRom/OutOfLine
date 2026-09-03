"""THE TREE -> an elephant.  Reconstruction of the first-run 40-region page."""
import math
from engine import *

_C = blob(500, 310, 296, 0.055, seed=11, n=88, lobes=9)
CANOPY = [(500 + (x-500)*1.38, y) for x, y in _C]

def leg(x0, x1):
    return [(x0,540),(x0-14,700),(x0-20,850),(x1+20,850),(x1+14,700),(x1,540)]

TRUNK = [(455,540),(442,640),(448,730),(470,800),(506,846),(560,864),(600,842),
         (560,812),(532,764),(516,700),(512,620),(545,540)]
TUSK_L = [(430,560),(348,630),(302,712),(282,760),(316,770),(360,700),(416,630),(452,586)]
TUSK_R = mirror(TUSK_L)

shapes = [
    (CANOPY, 1),                                    # leaf mass      -> head + ears rim
    (ellipse(238,392,138,206,rot=-0.10), 7),        # leaf cluster   -> left inner ear
    (ellipse(762,392,138,206,rot= 0.10), 7),        # leaf cluster   -> right inner ear
    (arch(378,180,622,545), 2),                     # central cluster-> face
    (arch(408,206,592,352), 3),                     # sunlit cluster -> forehead dome
    (leg(190,368), 1),                              # tree trunk     -> front leg
    (leg(632,810), 1),                              # tree trunk     -> front leg
    (rect(158,796,398,862), 3),                     # root flare     -> foot pad
    (rect(602,796,842,862), 3),                     # root flare     -> foot pad
    (circle(438,436,32), 4),                        # bark knot      -> eye
    (circle(562,436,32), 4),                        # bark knot      -> eye
    (TUSK_L, 5),                                    # bare branch    -> tusk
    (TUSK_R, 5),                                    # bare branch    -> tusk
    (TRUNK, 3),                                     # drooping bough -> the trunk
    ([(60,876)] + scallop_row(60,940,876,10,down=False) + [(940,876),(940,946),(60,946)], 6),  # ground -> grass
]

thin = []
for y in (120, 175, 230, 285, 340, 395, 450, 505):        # leaf courses -> hide
    k = int(2 + 8*math.sin(math.pi*min(1,(y-60)/460.0)))
    r = 296*math.sin(math.acos(min(0.999,abs(y-310)/296.0)))
    thin.append(scallop_row(500-r*1.30, 500+r*1.30, y, max(k,3)))
for cx, sgn in ((238,-1),(762,1)):                        # leaf veins -> ear webbing
    for a in (-55,-20,15,50):
        thin.append([(cx,392),(cx+sgn*130*math.cos(math.radians(a))*1.0,
                      392+200*math.sin(math.radians(a)))])
    thin.append(ellipse(cx,392,96,150,rot=-0.10*sgn))
for i,y in enumerate((250,300,350,400,450,500)):          # cluster ribs -> face wrinkles
    thin.append(scallop_row(408 if y<352 else 386, 592 if y<352 else 614, y, 3))
thin += [circle(438,436,46)+[circle(438,436,46)[0]],      # knot rings -> eye rings
         circle(562,436,46)+[circle(562,436,46)[0]],
         arc(438,424,60,200,340), arc(562,424,60,200,340)]  # brow arcs
for t in range(1,7):                                      # bough rungs -> trunk wrinkles
    a = t/7.0
    x0 = 452 + (482-452)*a - 10; y0 = 540 + (780-540)*a
    thin.append([(x0,y0),(x0+86,y0-14)])
for lx in (238,300,700,762):                              # bark grain on the legs
    thin.append([(lx,552),(lx-8,650),(lx+6,760),(lx-4,840)])
for x in (200,340,660,800):                               # toe arcs on the pads
    thin.append(arc(x,862,26,180,360))
thin += [circle(320,640,14)+[circle(320,640,14)[0]],      # decoy bark knots
         circle(690,690,12)+[circle(690,690,12)[0]],
         circle(600,240,12)+[circle(600,240,12)[0]]]
for gx in (140,320,520,700,880):                          # grass tufts
    thin.append([(gx,905),(gx+10,884),(gx+20,905)])

PAGE = dict(
    key="elephant", title="THE TREE", answer="an elephant",
    prompt="This looks like a tree.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1:(0.52,0.53,0.57), 2:(0.68,0.69,0.73), 3:(0.84,0.85,0.88),
            4:(0.19,0.18,0.20), 5:(0.95,0.92,0.80), 6:(0.44,0.66,0.38),
            7:(0.84,0.62,0.62)},
)
