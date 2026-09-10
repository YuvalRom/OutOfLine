"""Owner-requested line cleanup, limited to four illustrations.

Every retained detail has an explicit shape owner. The renderer clips it to
that shape and hides it beneath later shapes. The owl, teacup and bookshelf
are intentionally untouched in this pass.
"""
import math
from engine import scallop_row, ellipse
from p5_balloon import smooth

def clean(p):
    funcs = {'jellyfish': umbrella, 'butterfly': flower,
             'fish': sailboat, 'elephant': tree}
    if p['key'] not in funcs:
        return
    p['occlude_outlines'] = True
    p['thin'] = []
    p['details'] = {}
    p['background'] = []
    p['foreground'] = []
    funcs[p['key']](p)

def umbrella(p):
    import p2_jellyfish as u
    # One canopy contour supports the umbrella's domed volume. The bold
    # panel edges already serve as its ribs. No floating dots, stray
    # wisps, duplicate ribs, tassel crosshatching or stacked hem stitches.
    y=340
    span=u.dome_x(y)
    contour=u.sag(u.CX-span+6,u.CX+span-6,y,26)
    for i in range(5,11):
        p['details'][i]=[contour]
    # Restore the requested rain, keeping it separate from the canopy.
    p['background']=[[(x,y),(x+22,y+52)] for x,y in
                     ((66,300),(118,196),(884,214),(928,320),
                      (206,128),(792,116),(52,604),(930,616))]

def flower(p):
    import p3_butterfly as b
    fw=b.ray(306,430,132)
    hw=b.ray(20,390,136)
    tw=b.t_at_disc(fw,110)
    # Two flowing veins per petal, instead of the former grid.
    for wing,indices in [(fw,range(0,3)),(hw,range(6,8))]:
        a,l,r=b._axis(*wing)
        lines=[[b.mix(l[i],r[i],u) for i in range(int(tw*b.N),b.N)]
               for u in (.35,.65)]
        for idx in indices:
            p['details'][idx]=lines
            p['details'][idx+11]=[[(1000-x,y) for x,y in line] for line in lines]
    # A few abdominal segments and a single stem centreline.
    p['details'][22]=[scallop_row(463,537,y,1) for y in (582,625,667)]
    p['details'][23]=[[(500,706),(500,948)]]
    leaves=[(468.,790.,250.,872.,66.,-44.,.34,.72),
            (532.,850.,742.,912.,60.,34.,.34,.72)]
    for idx,leaf in zip((24,25),leaves):
        a,l,r=b._axis(*leaf,n=40)
        lines=[a]
        for j in (16,29):
            lines += [b.qb(a[j-8],a[j-3],l[j]), b.qb(a[j-8],a[j-3],r[j])]
        p['details'][idx]=lines
    # Short stamens double as antennae. No ring of dots or pollen clutter.
    p['foreground']=[[(420,128),(480,295)],[(580,128),(520,295)]]

def sailboat(p):
    # Scales belong only to the hull. Overlay shapes mask them, including
    # the belly, gill, fins and the two portholes of the starting image.
    p['details'][6]=[scallop_row(290,880,y,6) for y in (565,621,677)]
    left=[]
    right=[]
    for t in (.4,.7):
        left.append([(698-650*t,128+470*t),(698-174*t,128+350*t)])
        right.append([(698,128+400*t),(698+285*t,128+432*t)])
    for idx in (1,2):
        p['details'][idx]=left
    for idx in (3,4):
        p['details'][idx]=right
    # Minimal fin rays. These are clipped just like the scales.
    p['details'][10]=[smooth([(438,756),(506,801),(666,860)]),
                       smooth([(451,785),(516,836),(670,889)])]
    p['details'][0]=[[(872,672),(953,806)]]
    # Reinforce the slender mast with a black centre stroke. It remains
    # finer than the 7-unit structural outlines and inside the mast shape.
    p['details'][5]=[[(698,149),(689,473)]]
    p['detail_widths']={5:4.0}
    # A small amount of water establishes the boat; no diagonal guides.
    p['background']=[scallop_row(70,330,921,3),scallop_row(782,962,930,2)]

def tree(p):
    # Two bark knots keep the tree reading. Remove all canopy scales,
    # ear webs, proportion grids, extra eye rings and repeated grass marks.
    # Rounded foliage lobes strengthen the first reading as a tree.
    # The leaf mass keeps the same grey role in the elephant reveal.
    half=[(500,72),(443,78),(390,63),(345,100),(283,96),(249,148),
          (188,155),(160,216),(110,252),(119,312),(71,362),(85,424),
          (67,482),(106,531),(111,590),(163,615),(202,664),
          (268,657),(317,693),(381,664),(445,686),(500,668)]
    crown=smooth(half+[(1000-x,y) for x,y in half[-2:0:-1]],n=10,closed=True)
    p['shapes'][0]=(crown,p['shapes'][0][1])
    # Bring the legs together into a closed stance and a continuous tree
    # trunk. Both feet meet at the centre instead of leaving a white gap.
    leg=[(340,546),(500,552),(500,897),(294,897),(311,715)]
    foot=[(289,863),(500,863),(500,921),(290,921)]
    p['shapes'][5]=(leg,1)
    p['shapes'][6]=([(1000-x,y) for x,y in leg],1)
    p['shapes'][7]=(foot,2)
    p['shapes'][8]=([(1000-x,y) for x,y in foot],2)
    pts,col=p['shapes'][9]
    p['shapes'][9]=([(x,535+.68*(y-535)) for x,y in pts],col)
    # Shorter tusks retain their attachment points beneath the cheek leaves.
    for idx,anchor in ((10,420),(11,580)):
        pts,col=p['shapes'][idx]
        p['shapes'][idx]=([(anchor+.8*(x-anchor),552+.65*(y-552)) for x,y in pts],col)
    # Slightly irregular eyes read as knots in the uncoloured drawing.
    p['shapes'][14]=(ellipse(380,355,38,26,-.14),4)
    p['shapes'][15]=(ellipse(620,370,38,26,.16),4)
    p['details'][14]=[ellipse(380,355,17,10,-.14)]
    p['details'][15]=[ellipse(620,370,17,10,.16)]
    p['details'][0]=[ellipse(280,188,27,18),ellipse(280,188,12,8),
                      ellipse(746,170,27,18),ellipse(746,170,12,8)]
    for idx, xs in ((5,(344,407)),(6,(593,656))):
        p['details'][idx]=[smooth([(x,592),(x-10,716),(x+5,855)]) for x in xs]
    # Three short trunk wrinkles contribute to the elephant reading only;
    # they are contained inside the trunk instead of crossing the legs.
    p['details'][9]=[[(x,535+.68*(yy-535)) for x,yy in
                      smooth([(428,y),(480,y+17),(545,y+3)])] for y in (666,730,795)]
    # A few forked veins give the leaf clusters a botanical reading;
    # their curves also follow the folds of the coloured elephant's ears.
    left=[smooth([(204,579),(214,494),(224,421),(248,330)]),
          smooth([(217,472),(183,424),(159,395)]),
          smooth([(223,429),(259,403),(285,361)])]
    p['details'][1]=left
    p['details'][2]=[[(1000-x,y) for x,y in line] for line in left]
    sprig=[smooth([(300,549),(354,519),(417,483)]),
           [(341,527),(334,498)],[(370,510),(385,539)]]
    p['details'][12]=sprig
    p['details'][13]=[[(1000-x,y) for x,y in line] for line in sprig]
