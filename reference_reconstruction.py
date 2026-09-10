"""Editable approximations of details missing from the saved Git history.

The two supplied contact sheets are visual references, not executable input.
Original page modules are retained unchanged. These overrides are explicit.
"""
from copy import deepcopy
from engine import *
from p5_balloon import smooth

def rebuild(pages):
    pages = deepcopy(pages)
    for p in pages:
        key = p['key']
        if key == 'balloon':
            from teacup_balloon import redesign
            redesign(p)
        elif key == 'city':
            city(p)
        elif key == 'butterfly':
            butterfly(p)
        elif key == 'fish':
            fish(p)
        elif key == 'elephant':
            elephant(p)
    from cleanup import clean
    for p in pages:
        clean(p)
    return pages

def city(p):
    import p7_city as old
    books = deepcopy(old.BOOKS)
    books[5][2].append((780, old.BASE, 5))
    p['shapes'] = [(rect(44,44,964,974),1), (rect(44,866,964,974),6),
        ([(378,866),(462,866),(502,940),(342,940)],7),
        (circle(146,196,86),5)]
    for at, col, bands in books:
        p['shapes'].append((old.body(at),col))
        for y0,y1,bc in bands:
            p['shapes'].append((old.band(at,y0,y1),bc))
    p['shapes'] += [(rect(612,56,684,108),4), (rect(262,544,360,600),4),
        (blob(886,728,78,.13,seed=4),2),
        ([(848,802),(932,802),(920,866),(860,866)],6)]
    thin = [[(44,62),(964,62)]]
    for at, col, bands in books:
        thin += old.band_grid(at, at.top, old.BASE)
    for x0,x1,y,a in ((60,566,80,6),(690,938,66,5),(60,352,212,7),
                     (700,940,258,6),(474,588,306,4),(60,148,404,5)):
        thin.append(old.wave(x0,x1,y,a))
    for i in range(12):
        a=math.radians(i*30)
        thin.append([(146+68*math.cos(a),196+68*math.sin(a)),
                     (146+80*math.cos(a),196+80*math.sin(a))])
    thin += [circle(146,196,26), [(44,902),(964,902)], old.wave(56,944,946,4,260)]
    for x in range(80,930,96):
        thin.append([(x,928),(x+52,928)])
    for a in range(0,360,40):
        a=math.radians(a)
        thin.append([(886,728),(886+64*math.cos(a),728+64*math.sin(a))])
    p['thin']=thin
    p['colors']={1:(.73,.89,.98),2:(.36,.76,.59),3:(.98,.48,.39),
                 4:(.66,.57,.86),5:(1.,.83,.31),6:(.88,.72,.54),
                 7:(1.,.97,.88)}
    p['answer']='a city in daylight'

def butterfly(p):
    import p3_butterfly as b
    # Reuse the original parametric petals with the reference's wider wings.
    b.CX,b.CY = 500.,415.
    fw=b.ray(306,430,132)
    hw=b.ray(20,390,136)
    tw=b.t_at_disc(fw,110)
    right=[(b.petal(fw,tw,disc=True),1),
           (b.petal(fw,tw,.47,bow1=.02,disc=True),2),
           (b.petal(fw,.73,1,bow0=.02),3),
           (b.spot(fw,.57,-.18,40),6),
           (b.spot(fw,.84,-.42,27),4),
           (b.spot(fw,.88,.48,23),4),
           (b.petal(hw,tw,disc=True),7),
           (b.petal(hw,.78,1,bow0=.02),3),
           (b.spot(hw,.57,.12,40),6),
           (b.spot(hw,.69,-.52,28),7),
           (b.spot(hw,.83,.42,26),4)]
    shapes=right+[(mirror(pts),num) for pts,num in right]
    shapes += [(smooth([(460,506),(463,594),(477,700),(523,700),(537,594),(540,506)],closed=True),3),
               ([(468,700),(532,700),(544,952),(456,952)],5)]
    leaves=[(468.,790.,250.,872.,66.,-44.,.34,.72),
            (532.,850.,742.,912.,60.,34.,.34,.72)]
    shapes += [(b.petal(leaf),5) for leaf in leaves]
    shapes += [(ellipse(500,415,106,126),3),(circle(500,361,49),3),
               (circle(500,460,42),7), (circle(420,107,26),3),(circle(580,107,26),3)]
    thin=[]
    for wing in (fw,hw):
        a,l,r=b._axis(*wing)
        grid=[]
        for u in (.14,.30,.46,.62,.78,.91):
            grid.append([b.mix(l[i],r[i],u) for i in range(int(tw*b.N),b.N)])
        for t in (.28,.40,.52,.64,.76,.88,.96):
            j=int(t*b.N)
            grid.append(b.qb(l[j],a[min(b.N,j+2)],r[j]))
        thin += grid+[mirror(pts) for pts in grid]
    thin += [ellipse(500,415,92,114),[(420,128),(480,295)],[(580,128),(520,295)],
             [(487,704),(480,949)],[(513,704),(522,949)]]
    for y in (556,594,630,668):
        thin.append(scallop_row(473,527,y,1))
    for leaf in leaves:
        a,l,r=b._axis(*leaf,n=40)
        thin.append(a)
        for j in (10,18,26,34):
            thin += [b.qb(a[max(0,j-8)],a[max(0,j-3)],l[j]),
                     b.qb(a[max(0,j-8)],a[max(0,j-3)],r[j])]
    for x,y in ((108,166),(62,266),(936,266),(893,165),(66,726),(934,726),
                (168,936),(860,806),(352,946),(912,946),(500,60)):
        thin.append(ellipse(x,y,13,10))
    p.update(shapes=shapes,thin=thin)
    p['colors'].update({1:(1.,.55,.05),2:(1.,.85,.25),7:(.88,.23,.17)})

def fish(p):
    # The screenshot's curved sail edges, oval hull and rounded fins.
    top=(698,128)
    hull=smooth([(47,598),(148,512),(366,464),(602,458),(822,504),
                 (888,580),(858,690),(704,784),(490,835),(278,812),(130,730)],closed=True)
    outer=smooth([top,(755,164),(774,201),(815,229),(836,273),(875,310),
                  (889,354),(925,398),(944,452),(984,562)],n=8)+[(684,477),top]
    inner=smooth([top,(698,210),(741,263),(759,310),(787,365),(800,417),
                  (839,475),(902,537)],n=8)+[(693,483),top]
    jib=smooth([top,(588,207),(442,278),(254,389),(47,598)],n=8)+[(528,496),top]
    gold=smooth([top,(658,224),(622,294),(582,350),(543,404),(461,474)],n=8)+[(341,493),
          (438,423),(500,352),(552,303),(563,253),(606,237),top]
    belly=smooth([(77,688),(271,713),(504,724),(738,713),(880,659),
                   (811,742),(682,796),(490,835),(278,812),(130,730)],closed=True)
    deck=smooth([(47,598),(148,512),(366,464),(602,458),(822,504),(888,580),
                  (804,546),(710,547),(621,526),(527,544),(437,520),(339,535),
                  (222,544),(135,564)],closed=True)
    gill=smooth([(325,471),(304,575),(314,716),(368,824),(286,819),
                 (261,723),(275,616),(294,513)],closed=True)
    fin=smooth([(376,730),(492,705),(605,745),(685,826),(749,911),
                (631,916),(476,882),(394,820)],closed=True)
    tail=smooth([(866,640),(935,698),(986,773),(957,838),(910,815),(862,736)],closed=True)
    p['shapes']=[(tail,4),(jib,4),(gold,5),(outer,5),(inner,4),
        ([(692,130),(705,137),(697,482),(680,477)],5),
        (hull,2),(belly,3),(deck,1),(gill,5),(fin,4),
        (circle(202,620,76),5),(circle(202,620,52),7),(circle(194,625,17),6),
        (ellipse(101,659,54,31,.52),6),(circle(556,638,48),2),
        (circle(728,630,43),2),(circle(610,789,36),4)]
    thin=[]
    for y in (545,595,650,710,757):
        thin.append(scallop_row(287,840,y,6))
    for shift in (0,26,52):
        thin.append(smooth([(438,728+shift),(500,762+shift),(586,780+shift),(672,795+shift)]))
    for y in (850,905):
        thin.append([(395,y),(672,y+14)])
    for t in (.28,.47,.66,.83):
        thin.append([(698,128+400*t),(698+285*t,128+432*t)])
        thin.append([(698-650*t,128+470*t),(698-174*t,128+350*t)])
    thin += [[(697,150),(592,407),(386,481)],[(710,220),(900,550)],
             [(701,295),(748,511)],[(42,804),(960,966)]]
    for i in range(8):
        a=math.pi*i/4
        thin.append(circle(202+64*math.cos(a),620+64*math.sin(a),7))
    for y in (875,930):
        thin += [scallop_row(50,320,y,3),scallop_row(780,970,y+12,2)]
    thin += [[(230,960),(700,944)],[(847,690),(912,805)]]
    p['thin']=thin
    p['colors'].update({1:(.03,.35,.43),2:(.98,.53,.12),4:(.88,.26,.21)})

def elephant(p):
    canopy=[(500+(x-500)*1.46,370+(y-370)*1.08)
            for x,y in blob(500,370,304,.10,seed=9,n=160,lobes=13)]
    ear=smooth([(278,230),(211,246),(183,296),(128,330),(117,435),
                 (147,554),(207,614),(271,607),(298,556),(310,434),(300,325)],closed=True)
    head=smooth([(324,358),(344,233),(407,158),(500,136),(593,158),
                  (656,233),(676,358),(640,479),(560,531),(440,531),(360,479)],closed=True)
    forehead=smooth([(353,274),(406,186),(500,156),(594,186),(647,274),
                      (575,314),(425,314)],closed=True)
    leftleg=[(340,546),(457,552),(458,704),(475,897),(294,897),(311,715)]
    trunk=smooth([(455,535),(543,535),(522,645),(520,751),(562,854),
                  (543,909),(500,897),(449,815),(427,736),(441,630)],closed=True)
    tusk=smooth([(421,552),(386,638),(359,724),(338,817),(290,788),
                 (326,711),(352,634),(365,569)],closed=True)
    cheek=smooth([(397,449),(322,482),(280,533),(320,580),(399,566),(442,507)],closed=True)
    grass=smooth([(44,928),(140,939),(250,926),(390,938),(510,930),
                  (680,939),(820,930),(960,944)],n=6)
    grass+=smooth([(960,977),(820,968),(680,978),(510,966),(390,977),
                   (250,969),(140,978),(44,969)],n=6)
    p['shapes']=[(canopy,1),(ear,7),(mirror(ear),7),(head,2),(forehead,3),
         (leftleg,1),(mirror(leftleg),1),
         ([(289,863),(463,863),(478,921),(290,921)],2),
         (mirror([(289,863),(463,863),(478,921),(290,921)]),2),
         (trunk,3),(tusk,5),(mirror(tusk),5),
         (cheek,1),(mirror(cheek),1),(ellipse(380,362,39,29),4),
         (ellipse(620,362,39,29),4),(grass,6)]
    thin=[]
    for y in (177,229,281,333,385,437,489,541,593):
        dx=425*math.sqrt(max(0,1-((y-370)/330)**2))
        thin.append(scallop_row(500-dx,500+dx,y,max(3,int(dx/34))))
    for x in (220,780):
        for a in (-65,-35,0,35,65):
            thin.append([(x,289),(x+103*math.sin(math.radians(a)),480+80*math.cos(math.radians(a)))])
    for x in (380,620):
        thin += [arc(x,357,57,195,345),arc(x,350,76,195,345)]
    for y in (635,675,715,755,795,835):
        thin.append(smooth([(439,y),(480,y+20),(536,y+6)]))
    for x in (326,352,387,423,577,613,648,674):
        thin.append(smooth([(x,565),(x-17,688),(x+8,777),(x-4,880)]))
    for y in (598,641,687,732,779,831,882):
        thin += [[(295,y),(449,y+11)],[(551,y+11),(705,y)]]
    thin += [scallop_row(294,466,883,4),scallop_row(534,706,883,4)]
    for x,y,r in ((280,188,27),(746,170,27),(355,489,22),(637,493,22),
                  (502,470,35),(399,709,25),(626,697,25)):
        thin += [ellipse(x,y,r,r*.67),ellipse(x,y,r*.55,r*.38)]
    for x in range(66,949,47):
        thin.append([(x,973),(x+5,941),(x-7,923)])
    p['thin']=thin
    p['colors'].update({1:(.46,.46,.50),2:(.65,.65,.67),3:(.77,.77,.79),
                        4:(.14,.14,.15),7:(.73,.54,.55)})
