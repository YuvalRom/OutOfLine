"""THE HOUSE  ->  an owl."""
from engine import *

WL, WR, WT, WB = 120, 880, 400, 900
APEX, EL, ER = (500, 72), (55, 400), (945, 400)
QIN, QOUT = 296, 224

def roof_span(y):
    k = (500-55)/(400-72.0); d = (400-y)*k
    return (55+d, 945-d)

def wing_band(y0, y1, right=False):
    e = quoin_edge(QIN, QOUT, y0, y1, 2)
    if right: e = mirror(e)
    return ([(WR, y0)] + e + [(WR, y1)]) if right else ([(WL, y0)] + e + [(WL, y1)])

B = [WT, WT+167, WT+333, WB]

shapes = [
    ([EL, APEX, ER], 1),                       # roof            -> head
    (rect(206,160,282,300), 1),                # chimney         -> ear tuft
    (mirror(rect(206,160,282,300)), 1),
    (circle(500,272,44), 1),                   # gable vent      -> (vanishes)
    ([(99,368),(901,368),(945,400),(55,400)], 7),   # eave board  -> brow
    (rect(WL,WT,WR,WB), 2),                    # wall            -> facial disc
    ([(WL,742)] + scallop_row(WL,WR,742,8) + [(WR,WB),(WL,WB)], 6),   # apron -> chest
]
for i, col in enumerate((1, 7, 1)):            # siding panels   -> wing feathers
    shapes.append((wing_band(B[i], B[i+1]), col))
    shapes.append((wing_band(B[i], B[i+1], right=True), col))
shapes += [
    (rect(306,398,490,428), 7),                # window header   -> brow
    (mirror(rect(306,398,490,428)), 7),
    (circle(398,512,76), 3),                   # window pane     -> eye
    (mirror(circle(398,512,76)), 3),
    (circle(398,512,30), 4),                   # pane centre     -> pupil
    (mirror(circle(398,512,30)), 4),
    ([(500,566),(548,626),(500,692),(452,626)], 4),   # gable vent -> beak
    (arch(414,776,586,898), 5),                # front door      -> tail
    (rect(428,898,468,948), 4),                # stoop posts     -> toes
    (rect(480,898,520,948), 4),
    (rect(532,898,572,948), 4),
    (rect(368,948,632,980), 4),                # step            -> foot
]

thin = []
for y in (168, 250, 332):                      # shingle courses
    a, b = roof_span(y); thin.append([(a,y),(b,y)])
for y in (452, 500, 548):                      # fish-scale siding -> feathers
    thin += [scallop_row(WL, QIN, y, 3), scallop_row(2*500-QIN, WR, y, 3)]
for y in (620, 668, 716):
    thin += [scallop_row(WL, QIN, y, 3), scallop_row(2*500-QIN, WR, y, 3)]
for y in (790, 845):
    thin += [scallop_row(WL, QIN, y, 3), scallop_row(2*500-QIN, WR, y, 3)]
thin += [rect(312,422,484,598) + [(312,422)],  # window frame
         mirror(rect(312,422,484,598) + [(312,422)]),
         [(398,422),(398,598)], [(312,510),(484,510)],       # muntins
         [(602,422),(602,598)], [(516,510),(688,510)]]
for x in (450, 500, 550):                      # door planks     -> tail quills
    thin.append([(x, 800), (x, 896)])
thin += [scallop_row(330, 670, 800, 5), scallop_row(330, 670, 856, 5)]  # chest feathers
thin.append([(40, 980), (960, 980)])           # ground

PAGE = dict(
    key="owl", title="THE HOUSE", answer="an owl",
    prompt="This looks like a house.",
    ncolors=7, shapes=shapes, thin=thin,
    colors={1:(0.62,0.42,0.25), 2:(0.97,0.91,0.79), 3:(0.98,0.74,0.12),
            4:(0.15,0.13,0.12), 5:(0.76,0.47,0.26), 6:(0.90,0.80,0.62),
            7:(0.38,0.24,0.15)},
)
