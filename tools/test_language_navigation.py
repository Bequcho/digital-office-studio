#!/usr/bin/env python3
"""Same-page language links: offline Edge/Playwright, no production requests.

BEQSON_LANGUAGE_OUTPUT optionally stores screenshots and the completed matrix.
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from html.parser import HTMLParser

import test_lead_modal as fixture
from site_contract import ROUTES
from test_build import IGNORE, Page, changed, snapshot

ROOT = Path(__file__).resolve().parents[1]
LANGS = ('ru', 'ka', 'en')
SLUGS = ('audit', 'forme-home')
WIDTHS = (320, 375, 390, 430, 768, 1024, 1440)
SELECTOR = 'header .page-languages'


class Navigation(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.navs = []
        self.current = None
        self.link = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'nav' and 'page-languages' in attrs.get('class', '').split():
            self.current = {'attrs': attrs, 'links': []}
            self.navs.append(self.current)
        if tag == 'a' and self.current is not None:
            self.link = {**attrs, 'text': ''}
            self.current['links'].append(self.link)

    def handle_data(self, data):
        if self.link is not None:
            self.link['text'] += data

    def handle_endtag(self, tag):
        if tag == 'a':
            self.link = None
        if tag == 'nav':
            self.current = None


def validate(source, lang, slug, *, alias=False):
    """Require real, reciprocal same-family URLs, not just three labels."""
    navs = Navigation(source).navs
    assert len(navs) == 1, 'Exactly one language navigation required'
    nav = navs[0]
    assert nav['attrs'].get('aria-label', '').strip(), 'Navigation needs an accessible name'
    links = nav['links']
    assert [a['text'].strip() for a in links] == ['RU', 'KA', 'EN'], 'Visible language labels'
    assert len(links) == len(LANGS), 'One link per language'
    page = Page(source)
    canonical = f'https://beqson.com/{lang}/{slug}/'
    assert page.select('link', rel='canonical') == [{'rel': 'canonical', 'href': canonical}], 'Canonical'
    assert page.select('html', lang=lang), 'Document language'
    if alias:
        # /audit/ is a canonicalized Russian alias, not a fourth language URL.
        assert (lang, slug) == ('ru', 'audit'), 'Only the declared legacy audit alias'
        assert not page.select('link', rel='alternate'), 'Hreflang belongs to canonical pages'
        page = Page((ROOT / 'ru/audit/index.html').read_text(encoding='utf-8'))
    for target, a in zip(LANGS, links):
        route = f'{target}/{slug}/'
        assert route in ROUTES and (ROOT / route / 'index.html').is_file(), 'Real public equivalent'
        assert a.get('href') == '/' + route, 'Equivalent route, never the homepage'
        assert a.get('lang') == target and a.get('hreflang') == target, 'Link language'
        assert a.get('aria-label', '').strip(), 'Link accessible name'
        assert a.get('aria-current') == ('page' if target == lang else None), 'Current language'
        assert 'tabindex' not in a and 'target' not in a, 'Native keyboard navigation in same tab'
        assert page.select('link', rel='alternate', hreflang=target,
                           href='https://beqson.com/' + route), 'Head hreflang agrees with visible link'
    assert page.select('link', rel='alternate', hreflang='x-default',
                       href=f'https://beqson.com/en/{slug}/'), 'English x-default'


class LanguageNavigationSourceTests(unittest.TestCase):
    def test_real_routes_and_reciprocal_metadata(self):
        for slug in SLUGS:
            for lang in LANGS:
                with self.subTest(lang=lang, slug=slug):
                    validate((ROOT / lang / slug / 'index.html').read_text(encoding='utf-8'), lang, slug)
        validate((ROOT / 'audit/index.html').read_text(encoding='utf-8'), 'ru', 'audit', alias=True)

    def test_negative_controls(self):
        source = (ROOT / 'ru/audit/index.html').read_text(encoding='utf-8')
        validate(source, 'ru', 'audit')
        mutations = {
            'missing navigation': re.sub(r'<nav class="page-languages".*?</nav>', '', source),
            'homepage instead of equivalent': source.replace('href="/ka/audit/"', 'href="/ka/"'),
            'wrong family': source.replace('href="/ka/audit/"', 'href="/ka/forme-home/"'),
            'missing current language': source.replace(' aria-current="page"', ''),
            'two current languages': source.replace('hreflang="ka" lang="ka"', 'hreflang="ka" lang="ka" aria-current="page"'),
            'wrong hreflang': source.replace('hreflang="ka" href="https://beqson.com/ka/audit/"', 'hreflang="ka" href="https://beqson.com/ka/"'),
        }
        for name, bad in mutations.items():
            with self.subTest(defect=name):
                self.assertNotEqual(bad, source)
                with self.assertRaises(AssertionError):
                    validate(bad, 'ru', 'audit')

    def test_audit_pipeline_recreates_and_repeats_exactly(self):
        with TemporaryDirectory(prefix='beqson-language-build-') as temp:
            root = Path(temp) / 'site'
            shutil.copytree(ROOT, root, ignore=IGNORE)
            expected = snapshot(root)
            for lang in LANGS:
                (root / lang / 'audit/index.html').unlink()
            for iteration in range(2):
                for script in ('localize_audit.py', 'fix_audit_i18n.py', 'install_audit_pdf_v3.py'):
                    result = subprocess.run([sys.executable, 'scripts/' + script], cwd=root,
                        capture_output=True, text=True, timeout=60,
                        env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUTF8': '1'})
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(changed(expected, snapshot(root)), [], f'audit pipeline pass {iteration + 1}')


class LanguageNavigationBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.LeadModalTests.setUpClass()

    @classmethod
    def tearDownClass(cls):
        fixture.LeadModalTests.tearDownClass()

    def check_page(self, p, lang, slug, width):
        self.assertEqual(p.url, fixture.BASE + f'/{lang}/{slug}/')
        nav = p.locator(SELECTOR)
        self.assertEqual(nav.count(), 1)
        self.assertTrue(nav.is_visible())
        self.assertTrue(nav.get_attribute('aria-label'))
        self.assertEqual(nav.locator('[aria-current="page"]').count(), 1)
        self.assertEqual(nav.locator('[aria-current="page"]').inner_text(), lang.upper())
        self.assertEqual(nav.locator('a').all_text_contents(), ['RU', 'KA', 'EN'])
        self.assertEqual(p.locator('html').get_attribute('lang'), lang)
        self.assertEqual(p.locator('link[rel="canonical"]').get_attribute('href'),
                         f'https://beqson.com/{lang}/{slug}/')
        self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'), width + 1)
        for a in nav.locator('a').all():
            self.assertTrue(a.evaluate("""e=>{const r=e.getBoundingClientRect(),range=document.createRange();
                range.selectNodeContents(e);const t=range.getBoundingClientRect();
                return r.width>=40&&r.height>=40&&r.x>=0&&r.right<=innerWidth&&r.y>=0&&r.bottom<=innerHeight&&
                  t.left>=r.left&&t.right<=r.right&&t.top>=r.top&&t.bottom<=r.bottom&&
                  e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));}"""))
        active = nav.locator('[aria-current="page"]')
        other = nav.locator('a:not([aria-current])').first
        style = '(e)=>[getComputedStyle(e).backgroundColor,getComputedStyle(e).color,getComputedStyle(e).fontWeight]'
        self.assertNotEqual(active.evaluate(style), other.evaluate(style))

    def test_mouse_keyboard_touch_matrix(self):
        helper = fixture.LeadModalTests()
        rows = []
        output = Path(os.environ['BEQSON_LANGUAGE_OUTPUT']) if os.environ.get('BEQSON_LANGUAGE_OUTPUT') else None
        if output:
            output.mkdir(parents=True, exist_ok=True)
        # Eulerian walk covers all nine ordered language pairs (including the
        # active link) without redundant fixture/page reloads between actions.
        walk = ('ru', 'ru', 'ka', 'ka', 'en', 'en', 'ru', 'en', 'ka', 'ru')
        for slug in SLUGS:
            context, p = helper.open_page('ru', 320, touch=True)
            try:
                for width in WIDTHS:
                    with self.subTest(slug=slug, width=width):
                        p.set_viewport_size({'width': width, 'height': 900})
                        for mode in ('mouse', 'keyboard', 'touch'):
                            response = p.goto(fixture.BASE + f'/ru/{slug}/', wait_until='load')
                            self.assertEqual(response.status, 200)
                            for lang, target in zip(walk, walk[1:]):
                                with self.subTest(source=lang, target=target, input=mode):
                                    self.check_page(p, lang, slug, width)
                                    if output and mode == 'mouse' and lang == target and width in (320, 390, 768, 1440):
                                        p.screenshot(path=str(output / f'{slug}-{lang}-{width}.png'))
                                    link = p.locator(SELECTOR + f' a[hreflang="{target}"]')
                                    if mode == 'keyboard':
                                        # Reach every link through native Tab/Shift+Tab, not programmatic focus.
                                        p.keyboard.press('Tab')
                                        for _ in range(15):
                                            if link.evaluate('e=>e===document.activeElement'):
                                                break
                                            p.keyboard.press('Tab')
                                        self.assertTrue(link.evaluate('e=>e===document.activeElement'))
                                        self.assertTrue(link.evaluate("e=>e.matches(':focus-visible')&&getComputedStyle(e).outlineStyle!=='none'"))
                                        p.keyboard.press('Tab'); p.keyboard.press('Shift+Tab')
                                        self.assertTrue(link.evaluate('e=>e===document.activeElement'))
                                    # Even a tap on the active language reloads the
                                    # document. URL equality alone can observe the
                                    # previous document before that reload commits.
                                    with p.expect_navigation(wait_until='load'):
                                        if mode == 'mouse':
                                            link.click()
                                        elif mode == 'touch':
                                            link.tap()
                                        else:
                                            p.keyboard.press('Enter')
                                    p.wait_for_url(fixture.BASE + f'/{target}/{slug}/')
                                    p.wait_for_load_state('load')
                                    self.check_page(p, target, slug, width)
                                    rows.append({'slug': slug, 'from': lang, 'to': target, 'width': width, 'input': mode})
                        self.assertEqual(helper.errors, [])
                        self.assertEqual(helper.calls, [])
                        if output:
                            (output / 'language-results.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
                        print(f'{slug}/{width}: all nine pairs x mouse/keyboard/touch completed', flush=True)
            finally:
                context.close()
            print(f'{slug}: RU/KA/EN x seven widths x mouse/keyboard/touch completed', flush=True)
        expected = {(slug, lang, target, width, mode) for slug in SLUGS for lang in LANGS
                    for target in LANGS for width in WIDTHS for mode in ('mouse', 'keyboard', 'touch')}
        self.assertEqual({(r['slug'], r['from'], r['to'], r['width'], r['input']) for r in rows}, expected)
        self.assertEqual(len(rows), len(expected))
        if output:
            (output / 'language-results.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')

    def test_browser_negative_controls(self):
        helper = fixture.LeadModalTests()
        context, p = helper.open_page('ru', 320, touch=True)
        self.addCleanup(context.close)
        url = fixture.BASE + '/ru/audit/'
        for defect in ('hidden', 'covered', 'clipped', 'active'):
            with self.subTest(defect=defect):
                p.goto(url, wait_until='load')
                self.check_page(p, 'ru', 'audit', 320)
                if defect == 'hidden':
                    p.locator(SELECTOR).evaluate("e=>e.style.display='none'")
                elif defect == 'covered':
                    p.evaluate("let cover=document.createElement('div');cover.style='position:fixed;inset:0;z-index:99999';document.body.append(cover)")
                elif defect == 'clipped':
                    p.locator(SELECTOR + ' a').first.evaluate("e=>{e.style.width='10px';e.style.minWidth='10px';e.style.padding='0';e.style.overflow='hidden'}")
                else:
                    p.locator(SELECTOR + ' [aria-current]').evaluate("e=>e.removeAttribute('aria-current')")
                with self.assertRaises(AssertionError):
                    self.check_page(p, 'ru', 'audit', 320)


if __name__ == '__main__':
    unittest.main(verbosity=2)
