"""Offline signature motion regression; optional real-time WebM capture."""
import json
import hashlib
from PIL import Image, ImageFilter
from prepare_brand_reference import transparent_wordmark
import mimetypes
import os
from pathlib import Path
import unittest
from urllib.parse import urlsplit, unquote
import test_lead_modal as fixture

ROOT = Path(__file__).resolve().parents[1]
BASE = fixture.BASE
WIDTHS = (320, 375, 390, 430, 768, 1024, 1280, 1440, 1920)


class SignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.LeadModalTests.setUpClass()
        cls.browser = fixture.LeadModalTests.browser

    @classmethod
    def tearDownClass(cls):
        fixture.LeadModalTests.tearDownClass()

    def page(self, width, *, reduced=False, js=True, video=False, state=None):
        options = dict(viewport={'width': width, 'height': 900},
                       reduced_motion='reduce' if reduced else 'no-preference', java_script_enabled=js)
        if state:options['storage_state']=state
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
        brand=p.locator('.bq-brand')
        self.assertEqual(brand.get_attribute('aria-label'),'BEQSON Digital Studio')
        for selector in ('.bq-mark','.bq-wordmark'):
            image=brand.locator(selector)
            self.assertTrue(image.is_visible())
            self.assertTrue(image.evaluate('e=>e.complete&&e.naturalWidth>0'))
            self.assertEqual(image.evaluate('e=>getComputedStyle(e).opacity'),'1')
            self.assertEqual(image.evaluate('e=>getComputedStyle(e).transform'),'none')
            self.assertEqual(image.evaluate('e=>e.getAnimations().length'),0)
        self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),width+1)
        self.assertTrue(brand.evaluate('e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight}'))
        self.assertEqual(self.errors,[])

    def test_matrix_and_static_wordmark(self):
        for lang in ('ru','ka','en'):
            for width in WIDTHS:
                with self.subTest(lang=lang,width=width):
                    c,p=self.page(width)
                    # Establish the fully painted static baseline before starting
                    # the light, rather than comparing an initial image raster
                    # while fonts/styles and compositor layers are still settling.
                    held=[]
                    c.route('**/beqson-contours.json*',lambda route:held.append(route))
                    p.goto(BASE+f'/{lang}/',wait_until='load')
                    p.evaluate('document.fonts.ready')
                    p.locator('.bq-wordmark').evaluate('e=>e.decode()')
                    p.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
                    self.check(p,width)
                    brand=p.locator('.bq-brand');bounds=brand.bounding_box()
                    word=p.locator('.bq-wordmark');pixels=word.screenshot()
                    self.assertEqual(len(held),1)
                    held[0].fulfill(body=(ROOT/'assets/brand/beqson-contours.json').read_bytes(),content_type='application/json')
                    p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='running'")
                    for _ in range(4):
                        p.wait_for_timeout(750)
                        self.assertEqual(word.screenshot(),pixels,'Wordmark pixels changed during animation')
                        self.assertEqual(p.locator('.bq-mark').evaluate('e=>getComputedStyle(e).transform'),'none')
                        self.assertEqual(brand.bounding_box(),bounds)
                    p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='static'",timeout=7000)
                    self.assertEqual(brand.locator('[data-light][d]').count(),0)
                    self.assertEqual(word.screenshot(),pixels)
                    p.goto(BASE+'/en/' if lang!='en' else BASE+'/ru/')
                    self.assertNotEqual(brand.get_attribute('data-motion'),'running')
                    self.assertEqual(brand.locator('[data-light][d]').count(),0)
                    self.check(p,width)
                    state=c.storage_state();c.close()
                    # A separate browser context represents a later visit with saved storage.
                    c2,p2=self.page(width,state=state)
                    p2.goto(BASE+f'/{lang}/');self.check(p2,width)
                    self.assertNotEqual(p2.locator('.bq-brand').get_attribute('data-motion'),'running')
                    self.assertEqual(p2.locator('[data-light][d]').count(),0);c2.close()
            print('Contour/static-wordmark matrix:',lang,flush=True)

    def test_static_modes(self):
        for lang in ('ru','ka','en'):
            for width in (320,390,768,1440):
                for mode in ('reduced','no-js','no-storage','failed-light-data'):
                    with self.subTest(lang=lang,width=width,mode=mode):
                        c,p=self.page(width,reduced=mode=='reduced',js=mode!='no-js')
                        if mode=='no-storage':c.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw Error('Storage unavailable')}})")
                        if mode=='failed-light-data':c.route('**/beqson-contours.json*',lambda r:r.fulfill(status=503,body='unavailable'))
                        p.goto(BASE+f'/{lang}/');self.check(p,width)
                        self.assertEqual(p.locator('[data-light][d]').count(),0)
                        c.close()

    def test_reference_assets(self):
        pixels=Image.open(ROOT/'assets/brand/beqson-wordmark.webp').convert('RGBA')
        self.assertEqual(pixels.size,(849,205))
        self.assertEqual(pixels.getchannel('A').getextrema(),(0,255))
        self.assertTrue(all(pixels.getpixel((x,y))[3]==0 for x,y in [(0,0),(848,0),(0,204),(848,204)]))
        self.assertEqual(hashlib.sha256(pixels.tobytes()).hexdigest(),'5e80900c8530fdddf1f50d544a65393cc362c40f26835270f8c20e5e9367633a')
        self.assertEqual(hashlib.sha256((ROOT/'assets/beqson-mark-v3.png').read_bytes()).hexdigest(),
                         '1c86a0c18c4daf70b96ba972c51b2e5d1ef5e4dfb639f73cb1fd1c47e724c1e5')
        self.assertEqual(hashlib.sha256((ROOT/'assets/brand/beqson-contours.json').read_bytes()).hexdigest(),
                         '55149dcaaff532e1153cbe27827c4349730a8aea3a755cf1936f8073d261a423')
        data=json.loads((ROOT/'assets/brand/beqson-contours.json').read_text())
        self.assertEqual((data['fps'],len(data['frames'])),(30,146))
        self.assertAlmostEqual(data['duration'],4.8666666667)
        self.assertTrue(all(len(frame)==3 for frame in data['frames']))
        self.assertGreater(sum(bool(frame[1]) for frame in data['frames']),100)

    def test_transparent_matte_preserves_letter_cores(self):
        source=Image.open(ROOT/'tools/fixtures/brand-wordmark-source.webp').convert('RGBA')
        self.assertEqual(hashlib.sha256(source.tobytes()).hexdigest(),'fa9c570997f271952e634706c00e85ec157d56aaa9d2a1e330f8c86be1313746')
        actual=Image.open(ROOT/'assets/brand/beqson-wordmark.webp').convert('RGBA')
        self.assertEqual(transparent_wordmark(source).tobytes(),actual.tobytes())
        mask=Image.new('L',source.size)
        mask.putdata([255 if max(v[:3])>70 else 0 for v in source.getdata()])
        inner=mask.filter(ImageFilter.MinFilter(3))
        outer=mask.filter(ImageFilter.MaxFilter(5))
        for original,result,core,boundary in zip(source.getdata(),actual.getdata(),inner.getdata(),outer.getdata()):
            if core:self.assertEqual(result,original)
            if not boundary:self.assertEqual(result[3],0)

    def test_later_visit(self):
        c,p=self.page(390)
        c.add_init_script("localStorage.setItem('beqson-contour-seen-v1','1')")
        p.goto(BASE+'/ru/');self.check(p,390)
        self.assertEqual(p.locator('[data-light][d]').count(),0)
        self.assertNotEqual(p.locator('.bq-brand').get_attribute('data-motion'),'running');c.close()

    def test_video(self):
        output=os.environ.get('BEQSON_SIGNATURE_OUTPUT')
        if not output:return
        out=Path(output);out.mkdir(parents=True,exist_ok=True)
        for width in (390,1440):
            c,p=self.page(width,video=True)
            p.goto(BASE+'/ru/',wait_until='domcontentloaded')
            p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='running'")
            p.wait_for_timeout(1000);p.screenshot(path=str(out/f'contour-{width}-active.png'))
            p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='static'",timeout=7000)
            p.wait_for_timeout(800);self.check(p,width)
            p.screenshot(path=str(out/f'contour-{width}-final.png'))
            video=p.video;c.close();video.save_as(str(out/f'BEQSON-Contour-{width}.webm'))


if __name__=='__main__':unittest.main(verbosity=2)
