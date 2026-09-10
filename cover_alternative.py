"""Paper-airplane cover, selected by the owner for the current book.

python cover_alternative.py --output book/cover-alternative.pdf
"""
import argparse
from pathlib import Path
from reportlab.pdfgen import canvas
from recreate import text, path

def cover(c):
    w,h=612,792
    c.setPageSize((w,h))
    c.setFillColorRGB(1,.982,.941)
    c.rect(0,0,w,h,stroke=0,fill=1)
    text(c,'OutOfLine',306,145,60,h,True,True)
    text(c,"The lines are not the boss of me!",306,187,16,h,centered=True)
    c.saveState()
    c.translate(0,h)
    c.scale(1,-1)
    c.setLineCap(1)
    c.setLineJoin(1)
    # A soft colour field creates a quiet stage for the large paper plane.
    c.setFillColorRGB(.98,.89,.78)
    c.circle(316,419,154,fill=1,stroke=0)
    # A loose drawing page with a folded corner, rather than a frame.
    paper=[(140,308),(323,324),(355,362),(336,572),(118,552)]
    c.setFillColorRGB(.89,.82,.72)
    c.drawPath(path(c,[(x+8,y+9) for x,y in paper],True),fill=1,stroke=0)
    c.setStrokeColorRGB(.13,.18,.21)
    c.setLineWidth(2)
    c.setFillColorRGB(1,1,.99)
    c.drawPath(path(c,paper,True),fill=1,stroke=1)
    c.setFillColorRGB(.9,.93,.9)
    c.drawPath(path(c,[(323,324),(320,359),(355,362)],True),fill=1,stroke=1)
    c.setStrokeColorRGB(.67,.72,.71)
    c.setLineWidth(1.2)
    for y in (357,383,409,435,461,487,513):
        c.line(152,y,315,y+14)
    # Colour leaves the page along a broad, buoyant flight path.
    p=c.beginPath()
    p.moveTo(141,506)
    p.curveTo(72,517,103,602,178,578)
    p.curveTo(261,551,184,462,259,448)
    p.curveTo(307,439,326,438,350,407)
    c.setStrokeColorRGB(.92,.32,.24)
    c.setLineWidth(24)
    c.drawPath(p)
    p=c.beginPath()
    p.moveTo(142,521)
    p.curveTo(91,538,134,590,183,563)
    p.curveTo(236,534,206,474,264,463)
    p.curveTo(317,453,331,443,358,418)
    c.setStrokeColorRGB(.99,.69,.13)
    c.setLineWidth(9)
    c.drawPath(p)
    # Folded paper airplane: one large readable motif, no puzzle spoilers.
    a,b,d,e,f=(188,403),(488,263),(381,492),(330,420),(269,455)
    c.setStrokeColorRGB(.13,.18,.21)
    c.setLineWidth(2.5)
    c.setFillColorRGB(1,.99,.91)
    c.drawPath(path(c,[a,b,e],True),fill=1,stroke=1)
    c.setFillColorRGB(.12,.58,.62)
    c.drawPath(path(c,[b,d,e],True),fill=1,stroke=1)
    c.setFillColorRGB(.61,.83,.80)
    c.drawPath(path(c,[b,f,e],True),fill=1,stroke=1)
    c.setFillColorRGB(.08,.31,.37)
    c.drawPath(path(c,[f,e,(304,449)],True),fill=1,stroke=1)
    # A few tiny marks suggest possibility, without a crowded scatter.
    c.setStrokeColorRGB(.13,.18,.21)
    c.setLineWidth(2)
    c.line(493,238,501,224)
    c.line(507,251,524,247)
    c.setFillColorRGB(.92,.32,.24)
    star=[(455,514),(460,528),(475,532),(460,537),(455,551),(450,537),(435,532),(450,528)]
    c.drawPath(path(c,star,True),fill=1,stroke=0)
    c.setFillColorRGB(.99,.69,.13)
    c.circle(134,271,12,fill=1,stroke=0)
    c.setStrokeColorRGB(.12,.58,.62)
    c.setLineWidth(3)
    c.circle(452,402,8,fill=0,stroke=1)
    c.restoreState()
    text(c,'Go on. Get carried away.',306,649,22,h,True,True)
    text(c,'A colouring book for curious minds',306,683,13,h,centered=True)
    text(c,'YOUR IMAGINATION STARTS HERE',306,745,9,h,True,True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'book/cover-alternative.pdf')
    args=ap.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(args.output),invariant=1)
    c.setTitle('OutOfLine - paper-airplane cover')
    cover(c)
    c.showPage()
    c.save()

if __name__=='__main__':
    main()
