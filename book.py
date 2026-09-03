import sys, math, cairo, importlib
sys.path.insert(0,'pages')
import engine

MODS = ['p1_owl','p2_jellyfish','p3_butterfly','p4_fish','p6_elephant','p7_city']
PAGES = [importlib.import_module(m).PAGE for m in MODS]
PT=72.0; PW,PH = 8.5*PT, 11*PT

def face(cr,b=False):
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_BOLD if b else cairo.FONT_WEIGHT_NORMAL)
def text(cr,s,x,y,size,b=False,al='c'):
    face(cr,b); cr.set_font_size(size); cr.set_source_rgb(0,0,0)
    xb,yb,w,h,xa,ya = cr.text_extents(s)
    if al=='c': x-=w/2+xb
    elif al=='r': x-=w+xb
    else: x-=xb
    cr.move_to(x,y); cr.show_text(s)

def cover(cr):
    text(cr,"OUTSIDE",PW/2,225,62,True); text(cr,"THE LINES",PW/2,291,62,True)
    text(cr,"a colouring book where nothing is what it looks like",PW/2,336,13)
    cr.set_line_width(3); cr.rectangle(PW/2-90,405,180,180); cr.stroke()
    cr.set_line_width(9); cr.set_source_rgb(0.87,0.29,0.26)
    cr.move_to(PW/2-70,455)
    for i in range(1,40):
        t=i/39.0; cr.line_to(PW/2-70+t*260, 455+95*math.sin(t*9)+t*70)
    cr.stroke()
    text(cr,"6 pictures that are secretly other pictures",PW/2,680,12)
    text(cr,"colours: your call",PW/2,700,12)

def howto(cr):
    text(cr,"HOW THIS WORKS",PW/2,120,26,True)
    L=[("For the grown-up",True),
       ("Every page looks like one thing - a house, an umbrella, a flower,",0),
       ("a tree. It is secretly a picture of something else.",0),
       ("The numbers know the secret. Colour by the numbers and the",0),
       ("hidden picture appears.",0),("",0),
       ("There is no correct palette: any colour works for any number,",0),
       ("as long as different numbers get different colours.",0),("",0),
       ("For the kid",True),
       ("1.  Pick a colour for each number and fill in the boxes below the picture.",0),
       ("2.  Find every 1 and colour it. Then every 2. Keep going.",0),
       ("3.  THICK lines are where a colour stops.",0),
       ("4.  THIN lines are decoration - colour straight over them",0),
       ("     like they are not even there. That is the whole trick.",0),
       ("5.  When you are done, look again. What is it now?",0)]
    y=190
    for s,b in L:
        if s: text(cr,s,90,y,16 if b else 12.5,bool(b),'l')
        y+= 26 if b else 21
    text(cr,"The lines are not the boss of you.",PW/2,706,15,True)

def swatches(cr,n,cy):
    size=34; gap=70; x=PW/2-((n-1)*gap+size)/2
    for i in range(1,n+1):
        text(cr,str(i),x+size/2,cy-size-8,13,True)
        cr.set_line_width(1.4); cr.set_source_rgb(0,0,0)
        cr.rectangle(x,cy-size,size,size); cr.stroke(); x+=gap

def colpage(cr,i,p,lb):
    text(cr,"%d.  %s"%(i,p['title']),PW/2,80,25,True)
    text(cr,p['prompt']+"  Or is it?",PW/2,103,12)
    engine.draw_art(cr,p,PW/2-268,118,536,filled=False,numbers=True,labels=lb)
    text(cr,"pick a colour for each number",PW/2,696,11,True)
    swatches(cr,p['ncolors'],752)
    text(cr,"thick line: stop.   thin line: keep going, straight over it.",PW/2,775,10)

def answers(cr, chunk, first_idx, last=False):
    text(cr,"WHAT WAS HIDING",PW/2,88,26,True)
    text(cr,"(your colours will be different - that is allowed)",PW/2,110,11)
    pos=[(PW/2-250,130),(PW/2+14,130),(PW/2-250,430),(PW/2+14,430)]
    for i,(p,(x,y)) in enumerate(zip(chunk,pos),first_idx):
        engine.draw_art(cr,p,x,y,236,filled=True,numbers=False)
        text(cr,"%d. %s -> %s"%(i,p['title'].title(),p['answer']),x+118,y+262,11.5,True)
    if last:
        text(cr,"The lines are not the boss of you.",PW/2,745,14,True)

def build(out):
    labs=[engine.label_page(p) for p in PAGES]
    surf=cairo.PDFSurface(out,PW,PH); cr=cairo.Context(surf)
    def page(fn,*a):
        cr.set_source_rgb(1,1,1); cr.rectangle(0,0,PW,PH); cr.fill()
        fn(cr,*a); cr.show_page()
    page(cover); page(howto)
    for i,(p,lb) in enumerate(zip(PAGES,labs),1): page(colpage,i,p,lb)
    page(answers, PAGES[:4], 1)
    page(answers, PAGES[4:], 5, True)
    surf.finish()

if __name__=='__main__':
    build('/sessions/modest-charming-curie/mnt/outputs/outside-the-lines.pdf')
    print('pdf built')
