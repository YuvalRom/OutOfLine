"""Steam becomes the balloon envelope; a conventional cup becomes its basket.

The cup stays short and wide with a distinct rim, handle and saucer. Its steam
forms one continuous coloured envelope, separated from the cup/basket by two
wisps that also read as suspension ropes. No unrelated ornaments are added.
"""
import math
from engine import ellipse, rect
from p5_balloon import smooth


def redesign(p):
    cx=470.
    ys=[140+i*(638-140)/180 for i in range(181)]
    def width(y):
        if y<=345:
            return 268*math.sqrt(max(0,1-((y-345)/205)**2))
        t=(y-345)/(638-345)
        return 66+202*math.cos(math.pi*t/2)
    def seam(f):
        # Small offsets suggest rising steam without rippling the silhouette.
        return [(cx+f*width(y)+(0 if abs(f)==1 else 10*math.sin((y-140)/95)*(1-abs(f))),y)
                for y in ys]
    saucer=smooth([(210,866),(265,845),(363,834),(470,831),(578,834),
                   (679,847),(730,866),(680,884),(578,899),(470,903),
                   (363,899),(263,884)],closed=True)
    shapes=[(rect(55,70,945,963),6),(saucer,4)]
    fractions=[-1.,-.63,-.24,.24,.63,1.]
    for a,b,col in zip(fractions,fractions[1:],[3,2,1,2,3]):
        shapes.append((seam(a)+seam(b)[::-1],col))
    cup=smooth([(295,705),(314,769),(369,823),(470,845),
                 (571,823),(626,769),(645,705)],closed=True)
    shapes += [(cup,5),(ellipse(470,704,175,28),7)]
    p.update(shapes=shapes,thin=[],occlude_outlines=True,
             details={},detail_widths={},background=[],foreground=[])
    # Steam boundaries are lighter than the cup silhouette, but remain
    # stronger than the 2.4-unit interior decoration.
    p['outline_widths']={i:4.2 for i in range(2,7)}
    p['colors']={1:(.96,.30,.28),2:(1.,.78,.19),3:(.08,.64,.69),
                 4:(1.,.99,.95),5:(.70,.43,.23),6:(.77,.91,.97),
                 7:(.35,.23,.16)}
    handle=smooth([(626,713),(715,714),(757,746),(754,787),(712,817),(625,816)])
    inside=smooth([(637,744),(701,742),(724,759),(719,782),(693,793),(638,789)])
    p['details'][0]=[handle,inside]
    p['detail_widths'][0]=3.4
    # Two rising wisps also suspend the basket below the coloured envelope.
    p['foreground']=[smooth([(413,634),(420,659),(392,688)]),
                       smooth([(527,634),(520,659),(548,688)])]
    p['details'][8]=[ellipse(470,701,150,17)]
    # Restrained geometric china decoration doubles as a wicker pattern.
    p['details'][7]=[[(x,716),(x+14,846)] for x in (329,378,427,476,525,574,623)]
    p['details'][7]+=[[(298,y),(642,y)] for y in (761,799,829)]
    p['details'][1]=[ellipse(470,867,204,20)]
