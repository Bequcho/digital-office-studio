"""English root routing: offline Chromium, no external requests or submissions."""
import json
import mimetypes
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit
import test_lead_modal as fixture
from test_build import Page
from test_seo_metadata import check, METADATA

ROOT = Path(__file__).resolve().parents[1]
BASE = fixture.BASE


class DefaultLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.LeadModalTests.setUpClass()
        cls.browser = fixture.LeadModalTests.browser

    @classmethod
    def tearDownClass(cls):
        fixture.LeadModalTests.tearDownClass()

    def context(self, locale='en-US', width=390, js=True, stored='ka'):
        geo = {'ru-RU': (55.75, 37.62), 'ka-GE': (41.72, 44.79), 'en-US': (40.71, -74.01)}[locale]
        c = self.browser.new_context(locale=locale, viewport={'width':width,'height':900},
            java_script_enabled=js, geolocation={'latitude':geo[0], 'longitude':geo[1]},
            permissions=['geolocation'])
        self.addCleanup(c.close)
        c.add_cookies([{'name':key,'value':stored,'url':BASE} for key in ('lang','language','locale')])
        c.add_init_script("try{for(const key of ['lang','language','locale','preferredLanguage','beqson-language','beqson_lang']){localStorage.setItem(key,"+json.dumps(stored)+");sessionStorage.setItem(key,"+json.dumps(stored)+");}}catch(_){}")
        def serve(route):
            if not route.request.url.startswith(BASE+'/'):
                route.abort();return
            name=unquote(urlsplit(route.request.url).path.lstrip('/'))
            if not name or name.endswith('/'):name+='index.html'
            path=(ROOT/name).resolve()
            if path.is_relative_to(ROOT) and path.is_file():
                route.fulfill(body=path.read_bytes(),content_type=mimetypes.guess_type(str(path))[0] or 'application/octet-stream')
            else:route.fulfill(status=404,body='Not found')
        c.route('**/*',serve)
        p=c.new_page();p.set_default_timeout(5000)
        return c,p

    def test_root_ignores_preferences_and_manual_languages_stay(self):
        for locale,stored in [('ru-RU','ka'),('ka-GE','ru'),('en-US','ru')]:
            for width in (390,1440):
                with self.subTest(locale=locale,stored=stored,width=width):
                    c,p=self.context(locale,width,stored=stored);documents=[]
                    p.on('request',lambda r:documents.append(urlsplit(r.url).path) if r.resource_type=='document' else None)
                    p.goto(BASE+'/?utm_source=qa&lang=ka#contact',wait_until='domcontentloaded')
                    p.wait_for_url(re.compile(BASE+r'/(en|ru|ka)/.*'),wait_until='domcontentloaded')
                    self.assertEqual(p.url,BASE+'/en/?utm_source=qa&lang=ka#contact')
                    # Observe the first cycle before waiting for all page assets.
                    p.wait_for_function("()=>{const brand=document.querySelector('.bq-brand');return brand&&brand.dataset.motion==='running'}")
                    p.wait_for_load_state('load')
                    self.assertEqual(documents,['/','/en/'])
                    self.assertEqual(p.locator('html').get_attribute('lang'),'en')
                    for lang in ('ru','ka','en'):
                        with p.expect_navigation(wait_until='load'):
                            p.locator(f'header .languages a[lang="{lang}"]').click()
                        p.wait_for_timeout(100)
                        self.assertEqual(p.url,BASE+f'/{lang}/')
                        self.assertEqual(p.locator('html').get_attribute('lang'),lang)
                        self.assertEqual(p.locator('header .languages [aria-current="page"]').get_attribute('lang'),lang)
                        p.reload(wait_until='load')
                        self.assertEqual(p.url,BASE+f'/{lang}/')
                    c.close()

    def test_no_javascript_meta_refresh(self):
        for locale in ('ru-RU','ka-GE','en-US'):
            with self.subTest(locale=locale):
                c,p=self.context(locale,js=False)
                p.goto(BASE+'/',wait_until='domcontentloaded')
                p.wait_for_url(BASE+'/en/')
                self.assertEqual(p.locator('html').get_attribute('lang'),'en')
                self.assertTrue(p.locator('.bq-wordmark').is_visible())
                c.close()

    def test_unavailable_storage(self):
        c,p=self.context('ru-RU')
        c.add_init_script("for(const name of ['localStorage','sessionStorage'])Object.defineProperty(window,name,{get(){throw Error('Unavailable')}})")
        p.goto(BASE+'/',wait_until='domcontentloaded');p.wait_for_url(BASE+'/en/')
        with p.expect_navigation(wait_until='load'):
            p.locator('header .languages a[lang="ru"]').click()
        self.assertEqual(p.url,BASE+'/ru/');c.close()

    def test_root_seo_and_manifest_contract(self):
        source=(ROOT/'index.html').read_text(encoding='utf-8')
        check(source,METADATA['en/'],'https://beqson.com/en/',hreflang=True)
        page=Page(source)
        self.assertEqual(page.select('meta',**{'http-equiv':'refresh'}),[{'http-equiv':'refresh','content':'0;url=/en/'}])
        self.assertEqual(len(page.select('script')),1)
        self.assertIn('location.replace("/en/" + location.search + location.hash)',source)
        self.assertTrue(page.select('a',href='/en/'))
        self.assertNotIn('type="application/ld+json"',source)
        manifest=json.loads((ROOT/'site.webmanifest').read_text())
        self.assertEqual(manifest['lang'],'en')
        self.assertEqual(manifest['start_url'],'./')


if __name__=='__main__':unittest.main(verbosity=2)
