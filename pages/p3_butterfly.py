"""THE FLOWER  ->  a butterfly.

Line art: a child's fat five-petal pansy on a stem with two leaves.
Colour reveal: four petals become wings, the bottom petal the abdomen,
the flower disc the thorax + head, the curling stamens the antennae,
and the stem + leaves the twig it rests on.
"""
from engine import *

CX, CY = 500.0, 415.0            # flower disc centre  ->  thorax
DR     = 120.0                   # disc radius
PP, QQ = 0.72, 0.55              # fat, round-tipped petal width profile
N = 60

# --------------------------------------------------------------- petal maths
def _axis(x0, y0, x1, y1, wmax, curve, p, q, n=N):
    dx, dy = x1-x0, y1-y0
    L2 = math.hypot(dx, dy); ux, uy = dx/L2, dy/L2; px, py = -uy, ux
    pk = p/(p+q); norm = (pk**p)*((1-pk)**q)
    A = []; LL = []; RR = []
    for i in range(n+1):
        t = i/float(n)
        w = wmax*(t**p)*((1-t)**q)/norm
        c = curve*math.sin(math.pi*t)
        ax, ay = x0 + dx*t + px*c, y0 + dy*t + py*c
        A.append((ax, ay)); LL.append((ax+px*w, ay+py*w)); RR.append((ax-px*w, ay-py*w))
    return A, LL, RR

def qb(p0, p1, p2, n=12):
    return [((1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0],
             (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1])
            for t in [i/float(n) for i in range(n+1)]]

def mix(a, b, u):
    return (a[0] + (b[0]-a[0])*u, a[1] + (b[1]-a[1])*u)

def petal(W, t0=0.0, t1=1.0, bow0=0.05, bow1=0.06, disc=False):
    """Petal outline; disc=True closes the base with an arc that hides
    under the flower-disc outline instead of a visible chord."""
    A, L, R = _axis(*W)
    i0, i1 = int(round(t0*N)), int(round(t1*N))
    out = list(L[i0:i1+1])
    if i1 < N:
        out += qb(L[i1], A[max(0, min(N, int(round((t1+bow1)*N))))], R[i1])[1:-1]
    out += list(reversed(R[i0:i1+1]))
    if i0 > 0:
        if disc:
            x0, y0 = R[i0]; x1, y1 = L[i0]
            r0 = math.hypot(x0-CX, y0-CY); r1 = math.hypot(x1-CX, y1-CY)
            a0 = math.atan2(y0-CY, x0-CX); a1 = math.atan2(y1-CY, x1-CX)
            da = (a1 - a0 + math.pi) % (2*math.pi) - math.pi
            out += [(CX + (r0+(r1-r0)*u)*math.cos(a0+da*u),
                     CY + (r0+(r1-r0)*u)*math.sin(a0+da*u))
                    for u in [j/14.0 for j in range(1, 14)]]
        else:
            out += qb(R[i0], A[max(0, min(N, int(round((t0+bow0)*N))))], L[i0])[1:-1]
    return out

def spot(W, t, s, r):
    A, L, R = _axis(*W)
    i = int(round(t*N)); a = A[i]; e = L[i] if s > 0 else R[i]
    return circle(a[0] + (e[0]-a[0])*abs(s), a[1] + (e[1]-a[1])*abs(s), r)

def ray(deg, reach, wmax, curve=0.0, p=PP, q=QQ):
    a = math.radians(deg)
    return (CX, CY, CX + reach*math.cos(a), CY + reach*math.sin(a), wmax, curve, p, q)

def t_at_disc(W, rr=115.0):
    """First t where the petal edge clears the disc - base clip point."""
    A, L, R = _axis(*W)
    for i in range(N+1):
        if math.hypot(L[i][0]-CX, L[i][1]-CY) >= rr: return i/float(N)
    return 0.3

# --- five round petals radiating from the disc ------------------------------
FW = ray(306, 345.0, 104.0)                  # upper-right petal -> forewing
HW = ray(18,  345.0, 104.0)                  # lower-right petal -> hindwing
AB = ray(90, 310.0, 80.0, 0.0, 0.60, 0.75)   # bottom petal -> abdomen
TW, TA = t_at_disc(FW), t_at_disc(AB)

# ------------------------------------------------------------------- shapes
right = []                                            # right half, mirrored later

# forewing petal: orange, yellow base blush, dark tip blush, blotches
right.append((petal(FW, TW, disc=True), 1))
right.append((petal(FW, TW, 0.46, bow1=0.02, disc=True), 2))   # base blush -> wing flash
right.append((petal(FW, 0.78, 1.0, bow0=0.03), 3))             # tip blush -> margin
right.append((spot(FW, 0.62, -0.30, 40), 6))                   # blotch -> eyespot
right.append((spot(FW, 0.64,  0.60, 26), 4))                   # little companion fleck

# hindwing petal: red, orange base blush, dark tip blush, blotches
right.append((petal(HW, TW, disc=True), 7))
right.append((petal(HW, TW, 0.46, bow1=0.02, disc=True), 1))   # base blush -> wing flash
right.append((petal(HW, 0.78, 1.0, bow0=0.03), 3))             # tip blush -> margin
right.append((spot(HW, 0.62,  0.30, 40), 6))                   # blotch -> eyespot

shapes = list(right) + [(mirror(p), c) for p, c in right]

# stem + leaves -> the twig it rests on
shapes.append(([(468, 688), (532, 688), (538, 952), (462, 952)], 5))
LEAF = [(468.0, 790.0, 258.0, 884.0, 66.0, -44.0, 0.34, 0.72),
        (532.0, 848.0, 742.0, 916.0, 60.0,  34.0, 0.34, 0.72)]
shapes += [(petal(Lf, 0.0), 5) for Lf in LEAF]
LA, LL_, LR_ = _axis(*LEAF[0], n=40)
shapes.append((circle(LA[20][0], LA[20][1], 26), 5))           # dew drop decoy - vanishes

# bottom petal -> abdomen, flower disc -> thorax, inner boss -> head
shapes.append((petal(AB, TA, disc=True), 3))
shapes.append((circle(CX, CY, DR), 3))
shapes.append((circle(CX, CY - 44, 50), 3))

# --------------------------------------------------------------------- thin
thin = []
rthin = []
for W in (FW, HW):                                    # soft petal veins
    A, L, R = _axis(*W)
    i0, i9 = int(round(TW*N)) + 2, int(round(0.90*N))
    for u in (0.16, 0.33, 0.50, 0.67, 0.84):
        rthin.append([mix(L[i], R[i], u) for i in range(i0, i9)])
rthin.append(qb((CX+10, CY-118), (CX+4, CY-220), (CX+52, CY-290), 22))  # curling stamen -> antenna
rthin.append(arc(CX+66, CY-300, 17, 120, 430, 30))                      # tendril curl -> club
thin += rthin + [mirror(p) for p in rthin]

A, L, R = _axis(*AB)                                  # petal crinkles -> abdomen segments
for f in (0.46, 0.60, 0.74, 0.87):
    j = int(round(f*N))
    thin.append(qb(L[j], A[min(N, j+4)], R[j], 12))

thin.append(circle(CX, CY, 105, n=60))                 # disc ring
for k in range(14):                                   # stamen dots -> floret ring
    a = math.radians(k*360.0/14 + 13)
    thin.append(circle(CX + 84*math.cos(a), CY + 84*math.sin(a), 7.5, n=16))
thin.append(arc(CX, CY, 58, 25, 155, 24))             # floret smile lines
thin.append(arc(CX, CY, 40, 35, 145, 20))

thin += [[(486, 700), (484, 948)], [(514, 700), (516, 948)]]   # stem grain
for Lf in LEAF:                                       # leaf veins
    A, L, R = _axis(*Lf, n=40)
    thin.append([A[i] for i in range(1, 39)])
    for f in (0.26, 0.46, 0.66, 0.84):
        j = int(round(f*40))
        thin.append(qb(A[max(0, j-8)], A[max(0, j-3)], L[j], 8))
        thin.append(qb(A[max(0, j-8)], A[max(0, j-3)], R[j], 8))
for x, y, r in ((66, 726, 16), (934, 726, 16), (168, 936, 14), (860, 806, 14),
                (62, 296, 13), (938, 296, 13), (352, 946, 12), (912, 946, 12),
                (108, 166, 12), (892, 166, 12)):
    thin.append(ellipse(x, y, r, r*0.78))             # pollen motes

PAGE = dict(
    key="butterfly", title="THE FLOWER", answer="a butterfly",
    prompt="This looks like a flower.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1: (0.95, 0.55, 0.13), 2: (0.99, 0.83, 0.28), 3: (0.17, 0.12, 0.11),
            4: (1.00, 0.97, 0.88), 5: (0.42, 0.66, 0.32), 6: (0.15, 0.36, 0.56),
            7: (0.79, 0.25, 0.19)},
)
