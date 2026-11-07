"""Offline signature motion regression; optional real-time WebM capture."""
import json
import hashlib
import io
import math
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

# Deterministic browser clock for the isolated, unmodified logo IIFE. It lets
# lifecycle tests inspect pending work without waiting minutes or exporting hooks
# from production. The full-page matrix below still uses real browser time.
CLOCK = r'''() => {
  let now=0, id=0, hidden=window.__hidden, fetches=0, calls=0, deliver;
  const jobs=new Map(), nativeRAF=requestAnimationFrame.bind(window);
  Object.defineProperty(performance,'now',{value:()=>now});
  Object.defineProperty(document,'hidden',{get:()=>hidden});
  window.requestAnimationFrame=cb=>{jobs.set(++id,{at:now+1000/60,cb,raf:true});return id};
  window.setTimeout=(cb,ms)=>{jobs.set(++id,{at:now+ms,cb,raf:false});return id};
  window.cancelAnimationFrame=window.clearTimeout=key=>jobs.delete(key);
  window.fetch=()=>{fetches++;const reply={ok:true,json:async()=>window.__light};
    return window.__defer?new Promise(r=>deliver=()=>r(reply)):Promise.resolve(reply)};
  const state=()=>({now,fetches,calls,motion:document.querySelector('.bq-brand').dataset.motion,
    underline:{opacity:document.querySelector('.bq-underline')?.style.opacity,x:document.querySelector('.bq-underline')?.style.getPropertyValue('--bq-streak-x')},
    paths:[...document.querySelectorAll('[data-light]')].map(p=>p.getAttribute('d')),
    opacity:document.querySelector('.bq-contour').style.opacity,
    raf:[...jobs.values()].filter(j=>j.raf).length,
    timers:[...jobs.values()].filter(j=>!j.raf).length,
    next:jobs.size?Math.min(...[...jobs.values()].map(j=>j.at))-now:null});
  window.__clock={state,deliver:()=>deliver(),
    hidden:value=>{hidden=value;document.dispatchEvent(new Event('visibilitychange'))},
    flush:()=>new Promise(r=>nativeRAF(()=>nativeRAF(r))),
    advance:ms=>{const end=now+ms;let steps=0;for(;;){
      const next=[...jobs].sort((a,b)=>a[1].at-b[1].at)[0];if(!next||next[1].at>end)break;
      if(++steps>10000)throw Error('Unbounded scheduler');
      const [key,job]=next;jobs.delete(key);now=job.at;calls++;job.cb(now);
    }now=end;return state()}};
}'''


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

    def painted_wordmark(self,p):
        # Require a stable pre-animation raster, not just decoded source bytes.
        word=p.locator('.bq-wordmark');previous=word.screenshot()
        for _ in range(5):
            p.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
            current=word.screenshot()
            if current==previous:
                self.wordmark_bounds=word.bounding_box();return current
            previous=current
        self.fail('Wordmark raster did not settle before releasing light data')

    def assert_wordmark_pixels(self,p,expected,label):
        actual=p.locator('.bq-wordmark').screenshot()
        same=actual==expected
        if not same:
            before=Image.open(io.BytesIO(expected)).convert('RGB');after=Image.open(io.BytesIO(actual)).convert('RGB')
            self.assertEqual(after.size,before.size)
            # Only the original transparent interline gap may change. Both text
            # lines and every surrounding pixel remain exact, without tolerance.
            top=math.floor(124*before.height/205);bottom=math.ceil(165*before.height/205)
            same=all(before.crop(box).tobytes()==after.crop(box).tobytes() for box in
                     [(0,0,before.width,top),(0,bottom,before.width,before.height)])
        output=os.environ.get('BEQSON_SIGNATURE_DIAGNOSTICS')
        if not same and output:
            out=Path(output);out.mkdir(parents=True,exist_ok=True)
            (out/(label+'-expected.png')).write_bytes(expected)
            (out/(label+'-actual.png')).write_bytes(actual)
            (out/(label+'-bounds.json')).write_text(json.dumps(p.locator('.bq-wordmark').bounding_box()))
        self.assertTrue(same,'Wordmark text pixels changed during animation')
        self.assertEqual(p.locator('.bq-wordmark').bounding_box(),self.wordmark_bounds)
        self.assertEqual(p.locator('.bq-wordmark').evaluate("e=>[getComputedStyle(e).opacity,getComputedStyle(e).transform,getComputedStyle(e).filter,e.getAnimations().length]"),['1','none','none',0])

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
                    word=p.locator('.bq-wordmark');pixels=self.painted_wordmark(p)
                    self.assertEqual(len(held),1)
                    held[0].fulfill(body=(ROOT/'assets/brand/beqson-contours.json').read_bytes(),content_type='application/json')
                    p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='running'")
                    for sample in range(4):
                        p.wait_for_timeout(750)
                        self.assert_wordmark_pixels(p,pixels,f'{lang}-{width}-{sample}')
                        self.assertEqual(p.locator('.bq-mark').evaluate('e=>getComputedStyle(e).transform'),'none')
                        self.assertEqual(brand.bounding_box(),bounds)
                    p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='static'",timeout=7000)
                    self.assertEqual(brand.locator('[data-light][d]').count(),0)
                    self.assert_wordmark_pixels(p,pixels,f'{lang}-{width}-end')
                    c.unroute('**/beqson-contours.json*')
                    p.goto(BASE+'/en/' if lang!='en' else BASE+'/ru/')
                    p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='running'")
                    p.wait_for_function("document.querySelector('[data-light][d]')!==null")
                    self.check(p,width)
                    state=c.storage_state();c.close()
                    # A separate browser context represents a later visit with saved storage.
                    c2,p2=self.page(width,state=state)
                    p2.goto(BASE+f'/{lang}/');self.check(p2,width)
                    p2.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='running'")
                    p2.wait_for_function("document.querySelector('[data-light][d]')!==null");c2.close()
            print('Contour/static-wordmark matrix:',lang,flush=True)

    def test_motion_preferences_and_fallbacks(self):
        for lang in ('ru','ka','en'):
            for width in (320,390,768,1440):
                for mode in ('reduced','no-js','no-storage','failed-light-data'):
                    with self.subTest(lang=lang,width=width,mode=mode):
                        c,p=self.page(width,reduced=mode=='reduced',js=mode!='no-js')
                        if mode=='no-storage':c.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw Error('Storage unavailable')}})")
                        if mode=='failed-light-data':c.route('**/beqson-contours.json*',lambda r:r.fulfill(status=503,body='unavailable'))
                        p.goto(BASE+f'/{lang}/');self.check(p,width)
                        if mode=='no-storage':
                            p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='running'")
                            p.wait_for_function("document.querySelector('[data-light][d]')!==null")
                        else:self.assertEqual(p.locator('[data-light][d]').count(),0)
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
        p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='running'")
        p.wait_for_function("document.querySelector('[data-light][d]')!==null");c.close()

    def test_wordmark_pixel_negative_control(self):
        c,p=self.page(1920,reduced=True);p.goto(BASE+'/en/');p.evaluate('document.fonts.ready');p.locator('.bq-wordmark').evaluate('e=>e.decode()')
        pixels=self.painted_wordmark(p)
        p.locator('.bq-wordmark').evaluate("e=>e.style.opacity='0.9'")
        with self.assertRaises(AssertionError):self.assert_wordmark_pixels(p,pixels,'negative-opacity')
        c.close()

    def clock_page(self, engine=None, *, hidden=False, defer=False):
        c,p=self.page(390)
        p.set_content('<a class="bq-brand"><svg class="bq-contour">'+
                      ''.join(f'<path data-light="{i}"></path>' for i in range(3))+'</svg><span class="bq-underline"></span></a>')
        p.evaluate('(v)=>Object.assign(window,v)',{'__light':json.loads((ROOT/'assets/brand/beqson-contours.json').read_text()),'__hidden':hidden,'__defer':defer})
        p.evaluate(CLOCK)
        if engine is None:engine=(ROOT/'assets/home-motion.js').read_text().split('/* BEQSON Homepage Motion')[0]
        p.evaluate(engine);p.evaluate('async()=>{await Promise.resolve();await Promise.resolve()}')
        return c,p

    def assert_loop_schedule(self,p):
        first=p.evaluate('__clock.advance(20)')
        self.assertEqual((first['motion'],first['raf'],first['timers'],first['fetches']),('running',1,0,1))
        self.assertTrue(first['underline']['x']);self.assertGreater(float(first['underline']['opacity']),0)
        self.assertAlmostEqual(float(first['underline']['x'].rstrip('%')),-100+350*(1000/60)/4866.6666667,delta=.001)
        self.assertEqual(first['paths'],json.loads((ROOT/'assets/brand/beqson-contours.json').read_text())['frames'][0])
        fade=p.evaluate('__clock.advance(4780)');self.assertGreater(float(fade['opacity']),0);self.assertLess(float(fade['opacity']),1)
        idle=p.evaluate('__clock.advance(100)')
        self.assertEqual((idle['motion'],idle['raf'],idle['timers'],idle['paths']),('static',0,1,[None]*3))
        self.assertEqual(idle['underline'],{'opacity':'0','x':''})
        self.assertAlmostEqual(idle['now']+idle['next'],4866.6666667+3000,delta=20)
        still=p.evaluate('__clock.advance(__clock.state().next-1)')
        self.assertEqual((still['motion'],still['calls']),('static',idle['calls']))
        p.evaluate('__clock.advance(1)');again=p.evaluate('__clock.advance(20)')
        self.assertEqual((again['motion'],again['paths'],again['raf'],again['fetches']),('running',first['paths'],1,1))
        self.assertAlmostEqual(float(again['underline']['x'].rstrip('%')),float(first['underline']['x'].rstrip('%')),delta=.001)
        p.evaluate('__clock.advance(1000)');p.evaluate('__clock.hidden(true)')
        paused=p.evaluate('__clock.state()');self.assertEqual((paused['raf'],paused['timers']),(0,0))
        frozen=p.evaluate('__clock.advance(60000)')
        self.assertEqual((frozen['paths'],frozen['opacity'],frozen['calls']),(paused['paths'],paused['opacity'],paused['calls']))
        self.assertEqual(frozen['underline'],paused['underline'])
        p.evaluate('__clock.hidden(false)');resumed=p.evaluate('__clock.advance(1)')
        self.assertEqual((resumed['motion'],resumed['paths'],resumed['raf']),('running',paused['paths'],1))
        p.evaluate('__clock.advance(5000)');p.evaluate('__clock.hidden(true)')
        wait=p.evaluate('__clock.state()');self.assertEqual((wait['raf'],wait['timers']),(0,0))
        p.evaluate('__clock.advance(60000)');p.evaluate('__clock.hidden(false)')
        wait=p.evaluate('__clock.state()');self.assertEqual((wait['motion'],wait['raf'],wait['timers']),('static',0,1))
        self.assertGreater(wait['next'],1000);self.assertLess(wait['next'],3000)
        p.evaluate('__clock.advance(__clock.state().next-1)');self.assertEqual(p.evaluate('__clock.state().motion'),'static')
        p.evaluate('__clock.advance(2)');self.assertEqual(p.evaluate('__clock.state().motion'),'running')
        p.evaluate('__clock.advance(50000)');self.assertEqual(p.evaluate('__clock.state().fetches'),1)
        self.assertEqual(self.errors,[])

    def test_loop_timing_and_suspension(self):
        c,p=self.clock_page();self.assert_loop_schedule(p)
        p.emulate_media(reduced_motion='reduce');p.evaluate('__clock.flush()')
        s=p.evaluate('__clock.advance(60000)');self.assertEqual((s['motion'],s['raf'],s['timers'],s['paths']),('static',0,0,[None]*3))
        self.assertEqual(s['underline'],{'opacity':'0','x':''})
        p.emulate_media(reduced_motion='no-preference');p.evaluate('__clock.flush()')
        self.assertEqual(p.evaluate('__clock.advance(20).motion'),'running')
        p.evaluate("dispatchEvent(new Event('pagehide'))")
        self.assertEqual(p.evaluate('[__clock.state().raf,__clock.state().timers]'),[0,0])
        p.evaluate("dispatchEvent(new Event('pageshow'));dispatchEvent(new Event('pageshow'))")
        self.assertEqual(p.evaluate('[__clock.state().raf,__clock.state().timers,__clock.state().fetches]'),[1,0,1]);c.close()

    def test_hidden_and_loading_lifecycle(self):
        c,p=self.clock_page(hidden=True)
        self.assertEqual(p.evaluate('[__clock.state().fetches,__clock.state().raf,__clock.state().timers]'),[0,0,0])
        p.evaluate('__clock.hidden(false)');p.evaluate('async()=>{await Promise.resolve();await Promise.resolve()}')
        self.assertEqual(p.evaluate('__clock.advance(20).motion'),'running');c.close()
        for event in ('hidden','pagehide'):
            with self.subTest(event=event):
                c,p=self.clock_page(defer=True)
                p.evaluate("__clock.hidden(true)" if event=='hidden' else "dispatchEvent(new Event('pagehide'))")
                p.evaluate('__clock.deliver()');p.evaluate('async()=>{await Promise.resolve();await Promise.resolve()}')
                self.assertEqual(p.evaluate('[__clock.state().raf,__clock.state().timers]'),[0,0])
                p.evaluate('__clock.hidden(false)' if event=='hidden' else "dispatchEvent(new Event('pageshow'))")
                self.assertEqual(p.evaluate('[__clock.advance(20).motion,__clock.state().fetches]'),['running',1]);c.close()

    def test_loop_negative_controls(self):
        engine=(ROOT/'assets/home-motion.js').read_text().split('/* BEQSON Homepage Motion')[0]
        for old,new in [('timer = setTimeout(beginPass, pause)','timer = 0'),
                        ('cancelAnimationFrame(frame); clearTimeout(timer);','clearTimeout(timer);'),
                        ('clearTimeout(timer); frame = timer = 0;','frame = timer = 0;'),
                        ("underline.style.setProperty('--bq-streak-x', `${-100 + 350 * time / duration}%`);",'')]:
            with self.subTest(mutation=old):
                self.assertIn(old,engine);c,p=self.clock_page(engine.replace(old,new))
                with self.assertRaises(AssertionError):self.assert_loop_schedule(p)
                c.close()

    def test_underline_layout_and_text(self):
        alpha=Image.open(ROOT/'assets/brand/beqson-wordmark.webp').getchannel('A')
        self.assertEqual(alpha.crop((0,128,849,160)).getextrema(),(0,0))
        for lang in ('en','ru','ka'):
            for width in (1440,390,320):
                with self.subTest(lang=lang,width=width):
                    c,p=self.page(width);held=[]
                    c.route('**/beqson-contours.json*',lambda r:held.append(r))
                    p.goto(BASE+f'/{lang}/',wait_until='load');p.evaluate('document.fonts.ready');p.locator('.bq-wordmark').evaluate('e=>e.decode()')
                    pixels=self.painted_wordmark(p);self.check(p,width)
                    word=p.locator('.bq-wordmark').bounding_box();wrap=p.locator('.bq-wordmark-wrap').bounding_box();line=p.locator('.bq-underline');box=line.bounding_box()
                    self.assertEqual(wrap,word)
                    self.assertAlmostEqual((box['y']-word['y'])/word['height']*205,128,delta=.3)
                    self.assertAlmostEqual((box['y']+box['height']-word['y'])/word['height']*205,160,delta=.3)
                    self.assertEqual((box['x'],box['width']),(word['x'],word['width']))
                    self.assertEqual(line.get_attribute('aria-hidden'),'true')
                    self.assertEqual(line.evaluate("e=>[getComputedStyle(e).overflow,getComputedStyle(e).pointerEvents,getComputedStyle(e).opacity]"),['hidden','none','0'])
                    self.assertEqual(p.locator('.site-header').bounding_box()['height'],72 if width==1440 else 64)
                    self.assertEqual(word['width'],132 if width==1440 else 108 if width==390 else 94)
                    self.assertEqual(len(held),1);held[0].fulfill(body=(ROOT/'assets/brand/beqson-contours.json').read_bytes(),content_type='application/json')
                    p.wait_for_function("document.querySelector('.bq-brand').dataset.motion==='running'");last=-100
                    for sample in range(2):
                        p.wait_for_timeout(400);self.assert_wordmark_pixels(p,pixels,f'underline-{lang}-{width}-{sample}')
                        x=line.evaluate("e=>parseFloat(e.style.getPropertyValue('--bq-streak-x'))")
                        self.assertGreater(x,last);last=x;self.assertGreater(float(line.evaluate('e=>e.style.opacity')),0)
                    self.check(p,width);c.close()

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
