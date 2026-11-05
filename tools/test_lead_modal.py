#!/usr/bin/env python3
"""Offline Playwright regression matrix for the shared RU/KA/EN lead dialog.

Run with the existing Playwright Python environment. CHROMIUM_PATH may select
an installed browser. All local files are served via route.fulfill; every other
request is mocked or aborted. No server, CRM, email or external network is used.
"""
import json
import mimetypes
import os
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://beqson.test'
LANGS = ('ru', 'ka', 'en')
WIDTHS = (320, 375, 390, 430, 768, 1024, 1440)
MESSAGES = {'ru':'Заполните это поле.', 'ka':'გთხოვთ, შეავსოთ ეს ველი.', 'en':'Please fill out this field.'}

class LeadModalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        edge = Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
        executable = os.environ.get('CHROMIUM_PATH') or (str(edge) if edge.exists() else None)
        cls.browser = cls.pw.chromium.launch(executable_path=executable, headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def open_page(self, lang, width, touch=False):
        self.calls = []
        self.errors = []
        self.crm_ok = True
        context = self.browser.new_context(viewport={'width':width,'height':900},
            reduced_motion='reduce', is_mobile=touch, has_touch=touch)
        self.addCleanup(context.close)
        context.add_init_script("window.BEQSON_CRM_ENDPOINT='https://crm.example.test/create-lead';window.BEQSON_EMAIL_ENDPOINT='https://email.example.test/send';")
        def intercept(route):
            request=route.request; parts=urlsplit(request.url)
            if request.url.startswith(BASE+'/'):
                name=unquote(parts.path.lstrip('/'))
                if not name or name.endswith('/'): name+='index.html'
                file=(ROOT/name).resolve()
                if not file.is_relative_to(ROOT) or not file.is_file():
                    route.fulfill(status=404,body='Not found'); return
                mime=mimetypes.guess_type(str(file))[0] or 'application/octet-stream'
                route.fulfill(status=200,body=file.read_bytes(),content_type=mime)
            elif parts.hostname in ('crm.example.test','email.example.test'):
                self.assertEqual(request.method,'POST')
                self.calls.append((parts.hostname, request.post_data_json))
                ok=self.crm_ok or parts.hostname=='email.example.test'
                route.fulfill(status=200 if ok else 503,content_type='application/json',
                    body=json.dumps({'ok':ok,'success':ok}))
            else: route.abort()
        context.route('**/*',intercept)
        page=context.new_page();page.set_default_timeout(5000)
        page.on('pageerror',lambda e:self.errors.append(str(e)))
        page.goto(BASE+'/'+lang+'/',wait_until='load')
        page.evaluate('document.fonts.ready')
        return context,page

    def show(self,p):
        p.locator('.bls-launcher').click()
        p.wait_for_function("document.querySelector('.bls-modal').contains(document.activeElement)")
        self.assertEqual(p.locator('.bls-modal').get_attribute('aria-modal'),'true')
        self.assertEqual(p.locator('.bls-launcher').get_attribute('aria-expanded'),'true')

    def closed(self,p):
        p.locator('.bls-modal').wait_for(state='hidden')
        self.assertEqual(p.locator('.bls-launcher').get_attribute('aria-expanded'),'false')
        self.assertTrue(p.locator('.bls-launcher').evaluate('(e)=>e===document.activeElement'))
        self.assertFalse(p.locator('html').evaluate("e=>e.classList.contains('bls-lock')"))

    def test_mouse_hit_testing_escape_and_backdrop(self):
        for lang in LANGS:
            for width in WIDTHS:
                with self.subTest(lang=lang,width=width):
                    context,p=self.open_page(lang,width)
                    self.show(p)
                    self.assertTrue(p.locator('.bls-close').evaluate("e=>{const r=e.getBoundingClientRect();return [0.25,0.5,0.75].every(k=>e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height*k)))}"))
                    p.locator('.bls-close').click();self.closed(p)
                    self.show(p);p.keyboard.press('Escape');self.closed(p)
                    self.show(p);p.locator('.bls-backdrop').click(position={'x':3,'y':3});self.closed(p)
                    self.assertEqual(self.calls,[]);self.assertEqual(self.errors,[])
                    context.close()

    def test_touch_close(self):
        for lang in LANGS:
            for width in WIDTHS:
                with self.subTest(lang=lang,width=width):
                    context,p=self.open_page(lang,width,touch=True)
                    # Exercise touch close independently of the keyboard opener;
                    # the complete touch-open path is tested separately below.
                    p.locator('.bls-launcher').focus()
                    p.keyboard.press('Enter')
                    p.wait_for_function("document.querySelector('.bls-modal').contains(document.activeElement)")
                    p.locator('.bls-close').tap();self.closed(p)
                    self.assertEqual(self.errors,[]);self.assertEqual(self.calls,[])
                    context.close()

    def test_touch_launcher_homepage(self):
        # Keep the full touch integration gate, including the formerly failing
        # KA/320 case. Do not force clicks or bypass pointer hit testing.
        for lang in LANGS:
            for width in WIDTHS:
                with self.subTest(lang=lang,width=width):
                    context,p=self.open_page(lang,width,touch=True)
                    p.locator('.bls-launcher').tap()
                    p.wait_for_function("document.querySelector('.bls-modal').contains(document.activeElement)")
                    p.locator('.bls-close').tap();self.closed(p)
                    self.assertEqual(self.errors,[])
                    context.close()

    def test_keyboard_focus_and_background(self):
        for lang in LANGS:
            for width in WIDTHS:
                with self.subTest(lang=lang,width=width):
                    context,p=self.open_page(lang,width)
                    p.evaluate("let e=document.createElement('aside');e.id='already-inert';e.inert=true;document.body.append(e)")
                    self.show(p)
                    self.assertTrue(p.locator('main').evaluate('e=>e.inert'))
                    close=p.locator('.bls-close');close.focus()
                    p.keyboard.press('Shift+Tab')
                    self.assertTrue(p.locator('.bls-direct a').last.evaluate('e=>e===document.activeElement'))
                    p.keyboard.press('Tab');self.assertTrue(close.evaluate('e=>e===document.activeElement'))
                    for key in ('Tab','Shift+Tab'):
                        for _ in range(14):
                            p.keyboard.press(key)
                            self.assertTrue(p.locator('.bls-modal').evaluate('e=>e.contains(document.activeElement)'))
                    p.locator('.brand').first.evaluate('e=>e.focus()')
                    self.assertTrue(p.locator('.bls-modal').evaluate('e=>e.contains(document.activeElement)'))
                    p.keyboard.press('Escape');self.closed(p)
                    self.assertFalse(p.locator('main').evaluate('e=>e.inert'))
                    self.assertTrue(p.locator('#already-inert').evaluate('e=>e.inert'))
                    # A nonmodal AI panel is not subject to the dialog's focus trap.
                    p.locator('#beqson-ai-assistant-link').click()
                    p.locator('.brand').first.focus()
                    self.assertTrue(p.locator('.brand').first.evaluate('e=>e===document.activeElement'))
                    self.assertEqual(self.errors,[])
                    context.close()

    def test_whitespace_normalization_mock_error_and_retry(self):
        for lang in LANGS:
            for width in WIDTHS:
                with self.subTest(lang=lang,width=width):
                    context,p=self.open_page(lang,width);self.show(p)
                    p.locator('[name=industry]').select_option(index=1)
                    fields={name:p.locator(f'.bls-form [name={name}]') for name in ('name','contact','message')}
                    values={'name':'QA  Example','contact':'qa@example.test','message':'First  line\nSecond line'}
                    for contact in ('qa@example.test','+995 000 00 00 00','@qa_example'):
                        values['contact']=contact
                        for name,field in fields.items(): field.fill('  '+values[name]+'  ')
                        if contact=='qa@example.test':
                            for name,field in fields.items():
                                field.fill(' \t\u00a0\u2003 ')
                                p.locator('.bls-submit').click()
                                self.assertEqual(self.calls,[])
                                self.assertEqual(field.evaluate('e=>e.validationMessage'),MESSAGES[lang])
                                self.assertEqual(field.get_attribute('aria-invalid'),'true')
                                field.fill('  '+values[name]+'  ')
                            p.locator('[name=website]').fill('invalid-url')
                            p.locator('.bls-submit').click();self.assertEqual(self.calls,[])
                            p.locator('[name=website]').fill('  https://example.test/  ')
                            self.crm_ok=False
                            p.locator('.bls-submit').click()
                            p.locator('.bls-status.is-error').wait_for()
                            self.assertEqual(fields['contact'].input_value(),contact)
                            self.assertTrue(p.locator('.bls-submit').is_enabled())
                            self.crm_ok=True
                        else:
                            p.locator('[name=industry]').select_option(index=1)
                        p.locator('.bls-submit').click()
                        p.locator('.bls-status.is-success').wait_for()
                        crm=[body for host,body in self.calls if host=='crm.example.test'][-1]
                        for name in values:self.assertEqual(crm[name],values[name])
                        self.assertEqual(crm['language'],lang)
                        self.assertTrue(crm['consent'])
                        self.assertEqual(set(crm),{'name','contact','niche','website','message','budget','language','source','page_url','referrer','utm_source','utm_medium','utm_campaign','consent'})
                        email=[body for host,body in self.calls if host=='email.example.test'][-1]
                        for name in values:self.assertEqual(email[name],values[name])
                        self.assertEqual(fields['name'].input_value(),'')
                    self.assertEqual(self.errors,[])
                    context.close()

    def test_reopen_race_and_removed_trigger(self):
        for lang in LANGS:
            with self.subTest(lang=lang):
                context,p=self.open_page(lang,390);self.show(p)
                p.keyboard.press('Escape')
                p.locator('.bls-launcher').evaluate('e=>e.click()')
                p.wait_for_timeout(250)
                self.assertTrue(p.locator('.bls-modal').is_visible())
                self.assertTrue(p.locator('.bls-modal').evaluate('e=>e.contains(document.activeElement)'))
                p.locator('.bls-launcher').evaluate('e=>e.remove()')
                p.keyboard.press('Escape');p.locator('.bls-modal').wait_for(state='hidden')
                self.assertFalse(p.locator('main').evaluate('e=>e.inert'))
                self.assertEqual(self.errors,[])
                context.close()

if __name__=='__main__':unittest.main(verbosity=2)
