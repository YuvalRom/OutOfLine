"""Run with: python -m unittest test_reconstruction.py"""
import unittest
import importlib
import numpy as np
from PIL import Image, ImageDraw
import recreate
from reference_reconstruction import rebuild
from copy import deepcopy
from pathlib import Path
import shutil
import subprocess
import tempfile
from scipy import ndimage
from reportlab.pdfgen import canvas

class ReconstructionTests(unittest.TestCase):
    def test_cat_replaces_city_only_in_current_book(self):
        current = [importlib.import_module(m).PAGE['key'] for m in recreate.MODS]
        saved = [importlib.import_module(m).PAGE['key'] for m in recreate.SAVED_MODS]
        self.assertEqual(current, saved[:-1] + ['cat'])
        self.assertEqual(saved[-1], 'city')
        self.assertEqual(len(current), 7)

    def test_palette_and_label_identity(self):
        pages = rebuild([importlib.import_module(m).PAGE for m in recreate.MODS])
        self.assertEqual(len(pages), 7)
        for page in pages:
            with self.subTest(page=page['key']):
                self.assertEqual(set(page['colors']), set(range(1,8)))
                raster = Image.new('L',(1000,1000))
                draw = ImageDraw.Draw(raster)
                for pts,num in page['shapes']:
                    self.assertTrue(np.isfinite(pts).all())
                    draw.polygon(pts, fill=num)
                labels,_ = recreate.labels(page)
                self.assertEqual({z['num'] for z in labels}, set(range(1,8)))
                for z in labels:
                    self.assertEqual(raster.getpixel((z['x'],z['y'])), z['num'])

    def test_original_owl_placement_preserved(self):
        page = importlib.import_module('p1_owl').PAGE
        original = recreate.engine.label_page(page)
        accelerated,_ = recreate.labels(page)
        def ordered(seq):
            return sorted((z['num'],z['x'],z['y'],z['radius']) for z in seq)
        self.assertEqual(ordered(original),ordered(accelerated))

    @unittest.skipUnless(shutil.which('pdftoppm'), 'Poppler required for vector clipping regression test')
    def test_fish_scales_stay_in_visible_body(self):
        pages=rebuild([importlib.import_module(m).PAGE for m in recreate.MODS])
        fish=next(p for p in pages if p['key']=='fish')
        fish['background']=[]
        fish['foreground']=[]
        fish['details']={6:fish['details'][6]}
        bare=deepcopy(fish)
        bare['details']={}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            pdf=root/'clipping.pdf'
            c=canvas.Canvas(str(pdf),pagesize=(1000,1000),invariant=1)
            for page in (bare,fish):
                recreate.art(c,page,0,0,1000,1000)
                c.showPage()
            c.save()
            subprocess.run(['pdftoppm','-r','72','-png',str(pdf),str(root/'page')],check=True,capture_output=True)
            base=np.array(Image.open(root/'page-1.png').convert('L')).astype(int)
            scales=np.array(Image.open(root/'page-2.png').convert('L')).astype(int)
            changed=base-scales>24
            owner=Image.new('L',(1000,1000))
            d=ImageDraw.Draw(owner)
            for i,(pts,_) in enumerate(fish['shapes']):
                d.polygon(pts,fill=255 if i==6 else 0)
            # Accommodate subpixel antialiasing along vector polygon edges.
            allowed=ndimage.binary_dilation(np.array(owner)>0,iterations=3)
            self.assertGreater(int(changed.sum()),500)
            self.assertEqual(int((changed & ~allowed).sum()),0)

if __name__ == '__main__':
    unittest.main()
