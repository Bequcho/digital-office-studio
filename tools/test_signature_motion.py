"""Offline signature motion regression; optional real-time WebM capture."""
import json
import mimetypes
import os
from pathlib import Path
import unittest
from urllib.parse import urlsplit, unquote
import test_lead_modal as fixture

ROOT = Path(__file__).resolve().parents[1]
BASE = fixture.BASE
WIDTHS = (320, 375, 390, 430, 768, 1024, 1440)


class SignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.LeadModalTests.setUpClass()
        cls.browser = fixture.LeadModalTests.browser

    @classmethod
    def tearDownClass(cls):
        fixture.LeadModalTests.tearDownClass()

    def page(self, width, *, reduced=False, js=True, video=False):
        options = dict(viewport={'width': width, 'height': 900},
                       reduced_motion='reduce' if reduced else 'no-preference', java_script_enabled=js)
        if video:
            options.update(record_video_dir=os.environ['BEQSON_SIGNATURE_OUTPUT'],
                           record_video_size={'width': width, 'height':900})
        context = self.browser.new_context(**options)
        self.addCleanup(context.close)
        def route(r):
            if r.request.url.startswith(BASE+'/'):
                name = unquote(urlsplit(r.request.url).path.lstrip('/'))
                if name.endswith('/'): name += 'index.html'
                path = (ROOT/name).resolve()
                if path.is_relative_to(ROOT) and path.is_file():
                    r.fulfill(body=path.read_bytes(), content_type=mimetypes.guess_type(str(path))[0] or 'application/octet-stream')
                else: r.fulfill(status=404, body='Missing local file')
            else: r.abort()
        context.route('**/*', route)
        p = context.new_page(); p.set_default_timeout(5000)
        self.errors = []
        p.on('pageerror', lambda e:self.errors.append(str(e)))
        return context, p

    def check(self, p, width):
        brand = p.locator('.site-header .brand')
        self.assertEqual(brand.locator('b').inner_text(), 'BEQSON')
        self.assertTrue(brand.locator('b').is_visible())
        self.assertEqual(brand.locator('img').get_attribute('src'), '../assets/beqson-mark-v3.png')
        self.assertTrue(brand.locator('img').evaluate('e=>e.complete&&e.naturalWidth===128'))
        self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'), width+1)
        self.assertTrue(brand.evaluate('e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight}'))
        self.assertEqual(self.errors, [])

    def test_matrix_and_session(self):
        for lang in ('ru','ka','en'):
            for width in WIDTHS:
                with self.subTest(lang=lang,width=width):
                    c,p = self.page(width)
                    p.goto(BASE+f'/{lang}/', wait_until='domcontentloaded')
                    p.wait_for_function("document.querySelector('.brand').classList.contains('bq-signature')")
                    brand=p.locator('.site-header .brand'); before=brand.bounding_box()
                    if width>=359:
                        self.assertTrue(brand.evaluate("e=>e.getAnimations({subtree:true}).some(a=>a.animationName==='bq-signature-finish'&&a.effect.getTiming().duration===2600&&a.effect.getTiming().iterations===1)"))
                    else:
                        self.assertFalse(brand.locator('img').is_visible())
                        self.assertTrue(brand.locator('b').evaluate("e=>e.getAnimations().some(a=>a.animationName==='bq-signature-word')"))
                    brand.click(trial=True)
                    p.wait_for_function("!document.querySelector('.brand').classList.contains('bq-signature')")
                    self.assertEqual(brand.bounding_box(),before)
                    self.assertEqual(brand.evaluate('e=>e.getAnimations({subtree:true}).length'),0)
                    self.assertEqual(brand.locator('img').evaluate('e=>getComputedStyle(e).opacity'),'1')
                    self.assertEqual(brand.locator('b').evaluate('e=>getComputedStyle(e).clipPath'),'none')
                    self.check(p,width)
                    p.goto(BASE+'/en/' if lang!='en' else BASE+'/ru/')
                    self.assertFalse(brand.evaluate("e=>e.classList.contains('bq-signature')"))
                    self.assertEqual(brand.evaluate('e=>e.getAnimations({subtree:true}).length'),0)
                    c.close()
            print('Signature matrix:',lang,flush=True)

    def test_static_modes(self):
        for lang in ('ru','ka','en'):
            for width in WIDTHS:
                for mode in ('reduced','no-js','no-storage'):
                    with self.subTest(lang=lang,width=width,mode=mode):
                        c,p=self.page(width,reduced=mode=='reduced',js=mode!='no-js')
                        if mode=='no-storage':
                            c.add_init_script("Object.defineProperty(window,'sessionStorage',{get(){throw new Error('Storage unavailable')}})")
                        p.goto(BASE+f'/{lang}/');p.evaluate('document.fonts.ready')
                        self.check(p,width)
                        self.assertEqual(p.locator('.brand').evaluate('e=>e.getAnimations({subtree:true}).length'),0)
                        self.assertEqual(p.locator('.brand b').evaluate('e=>getComputedStyle(e).opacity'),'1')
                        c.close()

    def test_slow_fonts_fall_back_to_visible_logo(self):
        c,p=self.page(390)
        c.add_init_script("Object.defineProperty(document.fonts,'ready',{get:()=>new Promise(()=>{})})")
        p.goto(BASE+'/ru/')
        p.wait_for_function("!document.querySelector('.brand').classList.contains('bq-signature-pending')")
        self.assertEqual(p.locator('.brand').evaluate('e=>e.getAnimations({subtree:true}).length'),0)
        self.assertEqual(p.locator('.brand b').evaluate('e=>getComputedStyle(e).opacity'),'1')
        self.check(p,390)
        c.close()

    def test_video_and_frames(self):
        output=os.environ.get('BEQSON_SIGNATURE_OUTPUT')
        if not output: return
        out=Path(output);out.mkdir(parents=True,exist_ok=True)
        for width in (390,1440):
            c,p=self.page(width,video=True)
            p.goto(BASE+'/ru/',wait_until='domcontentloaded')
            p.wait_for_function("document.querySelector('.brand').classList.contains('bq-signature')")
            p.wait_for_timeout(3100)
            self.check(p,width)
            video=p.video;c.close();video.save_as(str(out/f'BEQSON-Signature-{width}.webm'))
            # Deterministic frames of the same CSS timelines, separate from real-time video.
            c,p=self.page(width);p.goto(BASE+'/ru/')
            p.wait_for_function("!document.querySelector('.brand').classList.contains('bq-signature')")
            p.wait_for_timeout(300)
            p.locator('.brand').evaluate("e=>{e.classList.remove('bq-signature');void e.offsetWidth;e.classList.add('bq-signature');e.getAnimations({subtree:true}).forEach(a=>a.pause())}")
            for t in (0,450,900,1400,1800,2150,2600):
                p.locator('.brand').evaluate('(e,t)=>e.getAnimations({subtree:true}).forEach(a=>a.currentTime=t)',t)
                p.screenshot(path=str(out/f'frame-{width}-{t}.png'))
            c.close()


if __name__=='__main__': unittest.main(verbosity=2)
