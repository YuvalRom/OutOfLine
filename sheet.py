import sys, importlib, cairo
sys.path.insert(0,'pages')
import engine
MODS = ['p1_owl','p2_jellyfish','p3_butterfly','p4_fish','p5_balloon','p6_elephant','p7_city']
def load():
    out=[]
    for m in MODS:
        out.append(importlib.import_module(m).PAGE)
    return out
if __name__=='__main__':
    which = sys.argv[1:] or MODS
    pages=[importlib.import_module(m).PAGE for m in which]
    px=430; n=len(pages)
    s=cairo.ImageSurface(cairo.FORMAT_RGB24, px*2+30, (px+34)*n+10)
    c=cairo.Context(s); c.set_source_rgb(1,1,1); c.paint()
    c.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    for i,p in enumerate(pages):
        y=10+(px+34)*i
        lb=engine.label_page(p)
        c.set_source_rgb(0,0,0); c.set_font_size(19)
        c.move_to(12,y+20); c.show_text("%s  ->  %s   (%d numbers, %d colours)"%(p['title'],p['answer'],len(lb),p['ncolors']))
        engine.draw_art(c,p,10,y+26,px,filled=False,numbers=True,labels=lb)
        engine.draw_art(c,p,px+20,y+26,px,filled=True,numbers=False)
    s.write_to_png('/sessions/modest-charming-curie/mnt/outputs/_sheet.png')
    print('ok', n)
