"""A mountain landscape becomes a sleeping cat; deterministic shared geometry.

The line drawing and reveal share every contour. Seven flat palette regions,
without the gradients or unmatched markings in the exploratory raster concept.
"""
from engine import rect


def curve(start, *segments):
    pts=[start]
    for a,b,end in segments:
        x,y=pts[-1]
        for j in range(1,41):
            t=j/40;u=1-t
            pts.append((u**3*x+3*u*u*t*a[0]+3*u*t*t*b[0]+t**3*end[0],
                        u**3*y+3*u*u*t*a[1]+3*u*t*t*b[1]+t**3*end[1]))
    return pts

shapes=[];details={}
def add(pts,col,lines=()):
    i=len(shapes);shapes.append((pts,col));details[i]=list(lines);return i

# Sky and the broad rounded hill/back.
add(rect(40,65,960,945),1)
back=curve((330,330),((475,300),(548,155),(687,155)),
           ((812,155),(901,222),(960,286)))+[(960,688),(330,688)]
add(back,2)
# Wide ridges become tabby markings, all present in the uncoloured version.
add(curve((562,192),((585,238),(605,305),(631,316)),
          ((663,326),(638,215),(629,164)))+[(598,173)],3)
add(curve((737,160),((725,225),(751,310),(778,325)),
          ((812,340),(817,232),(816,188))),3)
add(curve((892,225),((859,282),(869,350),(895,371)),
          ((921,389),(951,314),(960,286))),3)
# Two angular peaks read as mountains; a low ridge beneath is the head.
head=[(40,340),(125,295),(196,177),(253,261),(324,196),(381,291)]
head+=curve((381,291),((431,311),(468,333),(505,375)),
            ((432,390),(369,460),(293,481)),
            ((172,512),(80,465),(40,434)))
add(head,2,[[(196,177),(220,265),(253,261)],[(324,196),(298,278)]])
# A pale foothill/muzzle and one ridge that doubles as a closed eye.
add(curve((40,393),((76,360),(104,388),(142,409)),
          ((196,433),(245,440),(293,481)),
          ((172,512),(80,465),(40,434))),4)
# Low hill in front of the body / a folded foreleg.
add(curve((293,481),((350,390),(448,344),(521,369)),
          ((589,391),(658,404),(701,468)),
          ((618,529),(403,541),(293,481))),5)
# Meadow beyond the winding path; no unrelated texture.
add(curve((40,522),((200,501),(268,504),(365,526)),
          ((595,420),(819,425),(960,482)))+[(960,945),(40,945)],6)
# Stream around the hills.
add(curve((40,536),((205,527),(285,521),(365,526)),
          ((295,568),(359,585),(492,599)),
          ((365,659),(171,670),(40,706))),1)
# One continuous curling path/tail attached to the right flank.
tail=curve((960,440),((786,341),(654,386),(532,472)),
           ((459,520),(407,541),(368,548)),
           ((431,580),(715,563),(786,620)),
           ((871,688),(736,790),(599,786)),
           ((471,782),(479,689),(561,684)),
           ((619,680),(637,731),(683,697)),
           ((751,645),(545,626),(434,655)),
           ((295,691),(256,789),(409,844)),
           ((586,904),(881,829),(960,736)))
add(tail,2)
# A rock at the hill foot is the cat's small nose.
add(curve((98,455),((110,425),(145,430),(156,458)),
          ((143,488),(108,480),(98,455))),7)
# A second rock repeats that colour without introducing another face feature.
add(curve((143,799),((163,758),(197,757),(219,801)),
          ((196,811),(158,811),(143,799))),7)
# Sparse landscape ridges, including the sleeping eye. Present in both versions.
foreground=[curve((167,400),((193,366),(243,394),(278,356))),
            curve((95,337),((127,320),(150,329),(166,310))),
            curve((350,305),((366,329),(385,340),(402,346)))]
PAGE=dict(key='cat',title='THE MOUNTAINS',answer='a sleeping cat',
          prompt='This looks like a mountain landscape.',ncolors=7,
          shapes=shapes,colors={1:(.70,.87,.96),2:(.98,.65,.24),
          3:(.74,.33,.13),4:(1.,.94,.77),5:(1.,.79,.36),
          6:(.57,.72,.37),7:(.30,.32,.31)},thin=[],details=details,
          occlude_outlines=True,background=[],foreground=foreground)
