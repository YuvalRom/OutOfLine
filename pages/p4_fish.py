"""THE SAILBOAT  ->  a fish leaping from the splash."""
from engine import *

# ---------------------------------------------------------------- key lines
DECK   = 650.0            # hull sheer line (straight, horizontal)
KEELY  = 800.0            # hull bottom
FOOT   = 595.0            # foot of both sails / top of boom
MASTL, MASTR = 477.0, 523.0
MASTT  = 118.0            # masthead

# hull: simple trapezoid sitting on the waterline ---------------------------
HULL = [(200, DECK), (800, DECK), (725, KEELY), (275, KEELY)]

def hull_x(y, left=True):
    t = (y - DECK) / (KEELY - DECK)
    return (200 + 75*t) if left else (800 - 75*t)

# mainsail: straight luff on the mast, gently bellied leech -----------------
def leech_x(t):
    return MASTR + 312*math.sin(0.5*math.pi*t)**1.15

def mainsail(n=40):
    pts = [(leech_x(i/float(n)), 205 + (FOOT-205)*(i/float(n))) for i in range(n+1)]
    return pts + [(MASTR, FOOT)]

# jib: forestay hypotenuse from up near the masthead down to the bow --------
JIB = [(MASTL, 220), (MASTL, FOOT), (235, FOOT)]

def jib_x(y):                       # forestay x at height y
    return MASTL - (y - 220)*(MASTL - 235)/(FOOT - 220)

# water: horizontal waterline with round wave crests ------------------------
WAVE = scallop_row(0, 1000, 828, 12, down=False) + [(1000, 1000), (0, 1000)]

# ------------------------------------------------------------------- shapes
shapes = [
    (circle(880, 130, 70), 6),                       # sun          -> sun
    (blob(150, 165, 62, 0.22, seed=5), 5),           # cloud        -> spray puff
    (WAVE, 2),                                       # sea          -> splash
    ([(655,795),(722,798),(738,872),(668,864)], 1),  # rudder       -> tail tip
    (HULL, 1),                                       # hull         -> fish body
    (circle(315, 722, 42), 4),                       # porthole     -> eye
    (circle(580, 722, 44), 1),                       # life ring    -> (vanishes)
    (rect(MASTL, MASTT, MASTR, DECK), 5),            # mast         -> jet of spray
    ([(MASTR,120),(662,158),(MASTR,196)], 5),        # pennant      -> spray curl
    (mainsail(), 7),                                 # mainsail     -> the wave, curling over
    (rect(MASTR, FOOT, 840, DECK), 1),               # boom         -> tail base
    (JIB, 7),                                        # jib          -> front of the wave
    (circle(140, 610, 27), 5),                       # spray        -> flying droplet
    (circle(868, 598, 25), 5),
    (circle(205, 528, 22), 5),
]

# --------------------------------------------------------------------- thin
thin = []
for a in range(0, 360, 45):                          # sun rays
    thin.append([(880 + 82*math.cos(math.radians(a)), 130 + 82*math.sin(math.radians(a))),
                 (880 + 108*math.cos(math.radians(a)), 130 + 108*math.sin(math.radians(a)))])
thin += [arc(330, 108, 20, 195, 330), arc(366, 108, 20, 210, 345)]   # gulls
thin += [arc(690, 300, 20, 195, 330), arc(726, 300, 20, 210, 345)]
for y in (290, 400, 505):                            # sail seams   -> tail-fin rays
    t = (y - 205)/(FOOT - 205)
    thin.append([(MASTR + 5, y), (leech_x(t) - 10, y)])
for y in (390, 480, 555):                            # jib seams    -> dorsal-fin rays
    thin.append([(jib_x(y) + 10, y), (MASTL - 5, y)])
thin += [[(235, FOOT), (200, DECK)],                 # forestay run to the bow
         [(MASTL, 222), (495, 128)],                 # forestay top
         [(510, 130), (510, 640)]]                   # halyard on the mast
for y in (700, 750):                                 # hull planks  -> body contours
    thin.append([(hull_x(y, True) + 6, y), (hull_x(y, False) - 6, y)])
thin += [circle(315, 722, 54),                       # porthole rim -> eye ring
         circle(580, 722, 26)]                       # life-ring hole
for a in (45, 135, 225, 315):                        # life-ring spokes
    thin.append([(580 + 26*math.cos(math.radians(a)), 722 + 26*math.sin(math.radians(a))),
                 (580 + 44*math.cos(math.radians(a)), 722 + 44*math.sin(math.radians(a)))])
thin += [scallop_row(80, 920, 905, 7),               # wavelets     -> splash swirls
         scallop_row(150, 850, 958, 6),
         arc(150, 660, 32, 200, 335)]                # spray curl near the bow

PAGE = dict(
    key="fish", title="THE SAILBOAT", answer="a fish under a big wave",
    prompt="This looks like a sailboat.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1:(0.92,0.44,0.18), 2:(0.16,0.42,0.70), 3:(0.98,0.70,0.16),
            4:(0.16,0.14,0.13), 5:(0.93,0.96,0.99), 6:(0.99,0.83,0.12),
            7:(0.52,0.74,0.92)},
)
