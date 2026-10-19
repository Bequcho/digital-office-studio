#!/usr/bin/env python3
"""Calculator 3 browser regressions; no external network or real CRM leads.

Uses an existing Playwright/Chromium installation. Run: python tools/test_calculator.py
Optional CALCULATOR_SCREENSHOTS=/tmp/path writes desktop/mobile previews outside repo.
"""
import hashlib
import json
import os
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
# Generated from the approved Calculator 2.0 commit 6ad4da3, not the new code.
# Each hash covers all 8192 combinations of type, size, extras and timeline,
# including range, recommended package and CRM budget bracket.
PRICE_BASELINES = {
    'ru': 'bda9c2efe44de27055da9599a670ddfe03349c9527d02672588d6f32b9c82f2f',
    'ka': '9e3a692e7c59d97a86ccfe66fd01f75321301ff531b63abc70db643b697ed8d6',
    'en': '889df58d162d2d0c26de8f0c463400b01895d79b6d34d674018f5711ff173aaf',
}

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

class CalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'), args=['--no-sandbox'])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close(); cls.playwright.stop(); cls.server.shutdown(); cls.server.server_close()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width':1440,'height':1000}, reduced_motion='reduce')
        self.addCleanup(self.context.close)
        self.page = self.context.new_page(); self.errors=[]; self.missing=[]; self.payloads=[]; self.external=[]
        self.page.on('pageerror', lambda error:self.errors.append(str(error)))
        self.page.on('response', lambda response:self.missing.append(response.url) if response.url.startswith(self.base) and response.status>=400 else None)
        self.reply_ok = True
        self.context.route('**/*', self.intercept)

    def intercept(self, route):
        request=route.request
        if request.url.startswith(self.base):
            if '/assets/website-calculator.js' in request.url:
                code=(ROOT/'assets/website-calculator.js').read_text()
                # Test-only instrumentation in the served response; never in product files.
                code=code.replace('staticText();setupConfigurator();renderAll();', 'window.__calc={state,estimate,budgetBracket,briefText,renderAll};staticText();setupConfigurator();renderAll();')
                route.fulfill(status=200,content_type='application/javascript',body=code)
            else: route.continue_()
        elif request.url.endswith('/functions/v1/create-lead'):
            self.assertEqual(request.method,'POST')
            self.payloads.append(request.post_data_json)
            route.fulfill(status=200 if self.reply_ok else 503, content_type='application/json',body=json.dumps({'ok':self.reply_ok,'recommended_package':'Growth'}))
        else:
            self.external.append(request.url);route.abort()

    def open(self, lang='en'):
        self.page.goto(self.base+f'/{lang}/calculator/',wait_until='domcontentloaded')
        self.page.wait_for_function("document.querySelectorAll('#serviceCategories button').length === 5")
        self.assertEqual(self.page.locator('#serviceCategories button').count(),5)
        self.assertEqual(self.page.locator('main h1').count(),0)
        self.assertEqual(self.page.locator('h1').count(),1)

    def select_category(self, value):
        self.page.locator(f'[data-category="{value}"]').click()

    def select_type(self, value):
        self.page.locator(f'[data-group="type"][data-value="{value}"]').click()

    def tearDown(self):
        self.assertEqual(self.errors,[])
        self.assertEqual(self.missing,[])
        self.assertEqual(self.external,[],'Unexpected external request was blocked')

    def test_website_prices_match_all_v2_combinations(self):
        for lang, expected in PRICE_BASELINES.items():
            with self.subTest(lang=lang):
                self.open(lang)
                results=self.page.evaluate('''() => {
                  const {state,estimate,budgetBracket}=window.__calc, results=[];
                  const extras=['seo','local','crm','languages','copy','analytics','payments','booking'];
                  for(const type of ['landing','business','redesign','store'])for(const size of ['one','small','medium','large'])
                  for(let mask=0;mask<256;mask++)for(const timeline of ['standard','urgent']){
                    Object.assign(state,{type,size,timeline,extras:new Set(extras.filter((_,i)=>mask&(1<<i)))});
                    const e=estimate();results.push([e.low,e.high,e.pkg,budgetBracket((e.low+e.high)/2)]);
                  }
                  return JSON.stringify(results);
                }''')
                self.assertEqual(hashlib.sha256(results.encode()).hexdigest(),expected)

    def test_context_switching_and_saved_selections(self):
        self.open();self.select_type('store');self.page.select_option('#context-products','large')
        self.page.select_option('#context-platform','wordpress')
        self.page.fill('#projectRequirements','Worldwide shipping')
        self.page.locator('#extras input').first.check()
        self.select_category('automation');self.page.select_option('#context-channel','telegram')
        self.assertFalse(self.page.locator('#context-products').count())
        self.select_type('auto_crm')
        self.assertFalse(self.page.locator('#context-channel').count())
        self.assertNotIn('Telegram',self.page.locator('#summary').inner_text())
        self.select_category('website')
        self.assertEqual(self.page.input_value('#context-products'),'large')
        self.assertEqual(self.page.input_value('#projectRequirements'),'Worldwide shipping')
        self.assertTrue(self.page.locator('#extras input').first.is_checked())
        self.select_type('business')
        self.assertFalse(self.page.locator('#context-products').count())
        self.assertNotIn('500',self.page.locator('#summary').inner_text())
        self.select_type('store');self.assertEqual(self.page.input_value('#context-products'),'large')
        self.select_category('automation');self.select_type('auto_bot')
        self.assertEqual(self.page.input_value('#context-channel'),'telegram')

    def test_all_services_and_localized_controls(self):
        for lang in ('ru','ka','en'):
            self.open(lang)
            for category in ('website','seo','automation','design','care'):
                self.select_category(category)
                types=self.page.locator('#types button').evaluate_all('(els)=>els.map(e=>e.dataset.value)')
                for service in types:
                    self.select_type(service)
                    fields=self.page.locator('#contextFields select')
                    self.assertGreaterEqual(fields.count(),2)
                    for select in fields.all():
                        select.select_option(index=1)
                        self.assertTrue(self.page.locator(f'label[for="{select.get_attribute("id")}"]').inner_text().strip())
                    summary=self.page.locator('#summary').inner_text()
                    self.assertNotIn('undefined',summary);self.assertNotIn('NaN',summary)
                    if category!='website':
                        self.assertEqual(self.page.evaluate('window.__calc.estimate().low'),None)
                        self.assertNotIn('2–4',self.page.locator('#timelines').inner_text())
                        self.assertNotIn('7–14',self.page.locator('#timelines').inner_text())
                        self.assertTrue(self.page.locator('#price').get_attribute('class').endswith('isQuote'))
            self.assertEqual(self.page.locator('.calculatorLanguages [aria-current]').get_attribute('lang'),lang)

    def test_accessibility_focus_and_mobile_layout(self):
        shots=os.environ.get('CALCULATOR_SCREENSHOTS')
        for lang in ('ru','ka','en'):
            self.open(lang)
            for width in (320,390,768,1440):
                self.page.set_viewport_size({'width':width,'height':900})
                self.select_category('care');self.select_category('website')
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'))
                self.assertTrue(self.page.locator('[data-category="website"]').evaluate('(e)=>e===document.activeElement'))
                self.page.locator('[data-category="seo"]').focus();self.page.keyboard.press('Enter')
                self.assertEqual(self.page.locator('[data-category="seo"]').get_attribute('aria-pressed'),'true')
                self.assertTrue(self.page.locator('[data-category="seo"]').evaluate('(e)=>e===document.activeElement'))
                self.assertEqual(self.page.locator('select').evaluate_all('(els)=>els.every(e=>!!e.labels.length)'),True)
                if width<=768:
                    self.assertTrue(self.page.locator('.mobileEstimate').is_visible())
                    self.page.locator('.mobileEstimate a').click()
                if shots and width in (390,1440):
                    self.page.evaluate('scrollTo(0,0)');self.page.screenshot(path=str(Path(shots)/f'{lang}-{width}.png'))

    def test_brief_copy_print_privacy_and_injection(self):
        self.open();self.page.fill('#projectRequirements','<img src=x onerror=alert(1)>\nNeed a multilingual launch')
        self.page.locator('#exact').click()
        self.page.fill('#leadName','PRIVATE NAME');self.page.fill('#leadContact','private@example.test')
        self.page.fill('#leadWebsite','https://private.example.test')
        self.page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>{window.copied=text}},configurable:true})")
        self.page.locator('#copyBrief').click();text=self.page.evaluate('window.copied')
        self.assertIn('Need a multilingual launch',text)
        self.assertIn('<img',text);self.assertEqual(self.page.locator('#summary img').count(),0)
        for private in ('PRIVATE NAME','private@example.test','private.example.test'):
            self.assertNotIn(private,text);self.assertNotIn(private,self.page.url)
        self.page.evaluate('window.print=()=>{window.printCalled=true}')
        self.page.locator('#printBrief').click();self.assertTrue(self.page.evaluate('window.printCalled'))
        self.assertIn('Need a multilingual launch',self.page.locator('#printBriefText').text_content())
        self.assertNotIn('PRIVATE NAME',self.page.locator('#printBriefText').text_content())
        self.page.emulate_media(media='print')
        self.assertTrue(self.page.locator('#projectBrief').is_visible());self.assertFalse(self.page.locator('main').is_visible())
        self.page.emulate_media(media='screen')
        self.page.evaluate("() => {navigator.clipboard.writeText=async()=>{throw Error('denied')}}")
        self.page.locator('#copyBrief').click();self.assertTrue(self.page.locator('#briefFallback').is_visible())
        self.assertEqual(self.page.input_value('#briefFallback'),text)

    def test_form_validation_and_mocked_crm_payloads(self):
        for lang in ('ru','ka','en'):
            self.open(lang);self.page.locator('#exact').click()
            self.page.locator('#leadSubmit').click();self.assertEqual(self.payloads,[])
            self.page.fill('#leadName',' ');self.page.fill('#leadContact',' ');self.page.check('#consent')
            self.page.locator('#leadSubmit').click();self.assertEqual(self.payloads,[])
            self.page.fill('#leadName','Test');self.page.fill('#leadContact','test@example.test');self.page.uncheck('#consent')
            self.page.locator('#leadSubmit').click();self.assertEqual(self.payloads,[])
            for category in ('website','seo','automation','design','care'):
                self.select_category(category)
                self.page.select_option('#contextFields select >> nth=0',index=1)
                self.page.fill('#projectRequirements','QA requirements — do not send live')
                self.page.locator('#exact').click();self.page.fill('#leadName','Test');self.page.fill('#leadContact','test@example.test');self.page.check('#consent')
                expected=self.page.evaluate('window.__calc.briefText()')
                self.page.locator('#leadSubmit').click()
                self.page.wait_for_function("document.getElementById('leadSuccess').classList.contains('show')")
                payload=self.payloads.pop()
                self.assertEqual(payload['message'],expected);self.assertEqual(payload['language'],lang)
                self.assertTrue(payload['consent']);self.assertEqual(payload['_beqson_hp'],'')
                self.assertEqual(payload['source'],'website_calculator' if category=='website' else 'digital_services_calculator')
                if category=='website':self.assertIsNotNone(payload['budget'])
                else:self.assertIsNone(payload['budget'])
                self.assertFalse(self.page.is_checked('#consent'))

    def test_failed_submission_keeps_form_and_allows_retry(self):
        self.open();self.page.locator('#exact').click();self.page.fill('#leadName','Test');self.page.fill('#leadContact','test@example.test');self.page.check('#consent')
        self.reply_ok=False;self.page.locator('#leadSubmit').click()
        self.page.wait_for_function("document.getElementById('leadError').classList.contains('show')")
        self.assertEqual(self.page.input_value('#leadContact'),'test@example.test')
        self.assertTrue(self.page.locator('#leadSubmit').is_enabled())
        self.reply_ok=True;self.page.locator('#leadSubmit').click()
        self.page.wait_for_function("document.getElementById('leadSuccess').classList.contains('show')")
        self.assertEqual(len(self.payloads),2)

if __name__=='__main__':unittest.main(verbosity=2)
