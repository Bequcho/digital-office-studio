#!/usr/bin/env python3
"""Static regression checks: python3 tools/test_site.py (standard library only)."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import json
import subprocess
import sys
import os
from site_contract import public_files, expected_files, ROUTES, URLS, TECHNICAL
from test_seo_metadata import check
from test_seo_schema import validate as validate_schema
from test_sitemap import main as validate_sitemap
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://beqson.com/'
LANGS = ('ru', 'ka', 'en')
SLUGS = tuple(n['slug'] for n in json.loads((ROOT/'tools/industries.json').read_text()))


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path=path; self.doctypes=[]; self.elements=[]; self.ids=[]; self.scripts=[]; self.current_script=None
        self.feed(path.read_text())
    def handle_decl(self, decl):
        self.doctypes.append(decl.lower())
    def handle_starttag(self, tag, attributes):
        attrs=dict(attributes); self.elements.append((tag,attrs))
        if attrs.get('id'): self.ids.append(attrs['id'])
        if tag=='script' and attrs.get('type')=='application/ld+json':self.current_script=''
    def handle_data(self, data):
        if self.current_script is not None:self.current_script+=data
    def handle_endtag(self, tag):
        if tag=='script' and self.current_script is not None:
            self.scripts.append(self.current_script);self.current_script=None
    def select(self, tag, **attributes):
        return [a for t,a in self.elements if t==tag and all(a.get(k)==v for k,v in attributes.items())]


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages={route:Page(p) for route,p in public_files(ROOT).items()}
    def test_routes_and_language(self):
        expected=expected_files()
        self.assertEqual(set(self.pages),expected)
        for route,page in self.pages.items():
            with self.subTest(route=route):
                if route.split('/')[0] in LANGS:
                    self.assertEqual(page.select('html')[0]['lang'],route.split('/')[0])
                elif route!='projects/index.html':
                    self.assertIn(page.select('html')[0]['lang'], LANGS)
                redirects={'calculator/index.html','projects/index.html','tools/index.html','tools/search-preview/index.html','tools/utm-builder/index.html'}
                if route in redirects:
                    from build_sitemap import Document
                    doc=Document(page.path.read_text())
                    self.assertTrue(doc.refresh or any('location.replace' in js for js in doc.scripts),route)
                else:
                    self.assertEqual(len(page.select('h1')),2 if route=='crm/index.html' else 1)
                    self.assertEqual(len(page.select('main')),1)
                self.assertEqual(len(page.ids),len(set(page.ids)))
                self.assertEqual(page.doctypes,['doctype html'])
                self.assertEqual(len(page.select('html')),1)
                self.assertEqual(len(page.select('head')),1)
    def test_local_references_and_anchors(self):
        count=0
        for route,page in self.pages.items():
            for tag,attrs in page.elements:
                refs=[attrs[k] for k in ('href','src') if attrs.get(k)]
                refs+=[item.strip().split()[0] for item in attrs.get('srcset','').split(',') if item.strip()]
                for ref in refs:
                    dest=urlsplit(urljoin(BASE+route,ref))
                    if not (dest.netloc=='beqson.com' and dest.path.startswith('/')):continue
                    rel=unquote(dest.path.removeprefix('/'))
                    if not rel or rel.endswith('/'):rel+='index.html'
                    target=ROOT/rel
                    with self.subTest(route=route,reference=ref):
                        self.assertTrue(target.is_file(),str(target))
                        if dest.fragment and rel in self.pages:self.assertIn(unquote(dest.fragment),self.pages[rel].ids)
                    count+=1
        self.assertGreater(count,1500)
        print(f'Checked {count} local references and anchors.')
    def test_localized_images(self):
        for lang in LANGS:
            for slug in SLUGS:
                route=f'{lang}/{slug}/index.html';page=self.pages[route]
                pictures=[a for a in page.select('img') if '/concepts/' in a.get('src','')]
                self.assertGreaterEqual(len(pictures),2)
                for image in pictures:
                    self.assertIn(f'/concepts/{lang}/',image['src'])
                    self.assertTrue(image['alt']);self.assertEqual(image['width'],'1536');self.assertEqual(image['height'],'1024')
                for suffix in ['', '-320', '-480', '-768']:
                    for ext in ['webp','avif']:
                        self.assertTrue((ROOT/f'assets/concepts/{lang}/{slug}{suffix}.{ext}').is_file())
                self.assertTrue((ROOT/f'assets/concepts/{lang}/{slug}-og.jpg').is_file())
        manifest=json.loads((ROOT/'tools/mockups-manifest.json').read_text())
        self.assertEqual(len(manifest),24)
        for slug in SLUGS:self.assertEqual(len({manifest[f'{l}/{slug}']['title'] for l in LANGS}),3)
    def test_canonical_alternates_and_social_images(self):
        for route in ROUTES:
            source=(ROOT/route/'index.html').read_text()
            check(source, canonical=BASE+route, hreflang=True)
        for route in TECHNICAL:
            page=self.pages[route]
            targets={'404.html':'404.html', 'index.html':'ka/',
                     'audit/index.html':'ru/audit/', 'calculator/index.html':'en/calculator/'}
            self.assertEqual([a['href'] for a in page.select('link',rel='canonical')],
                             [BASE+targets[route]] if route in targets else [])
            if route.startswith('crm/'):
                self.assertTrue(any('noindex' in a.get('content','') for a in page.select('meta',name='robots')))
            elif route=='index.html':
                self.assertEqual(page.select('link',rel='canonical')[0]['href'],BASE+'ka/')
            elif route=='audit/index.html':
                self.assertEqual(page.select('link',rel='canonical')[0]['href'],BASE+'ru/audit/')
            else:
                self.assertTrue(any('noindex' in a.get('content','') for a in page.select('meta',name='robots')),route)
    def test_json_ld_and_sitemap(self):
        for route in ROUTES:
            validate_schema((ROOT/route/'index.html').read_text(), route)
        validate_sitemap()
        json.loads((ROOT/'site.webmanifest').read_text())
    def test_legacy_image_links_remain_available(self):
        for slug in SLUGS:
            for suffix in ['', '-small']:self.assertTrue((ROOT/f'assets/concepts/{slug}{suffix}.webp').is_file())
    def test_external_link_security(self):
        for route,page in self.pages.items():
            for link in page.select('a',target='_blank'):
                self.assertIn('noopener',link.get('rel',''))
    def test_icon_sprite_references(self):
        self.assertGreater(len(list(ET.parse(ROOT/'assets/icons.svg').getroot())),20)
        for route,page in self.pages.items():
            for use in page.select('use'):
                ref=use.get('href',use.get('xlink:href',''))
                dest=urlsplit(urljoin(BASE+route,ref))
                if not dest.netloc or dest.netloc=='beqson.com':
                    path=ROOT/unquote(dest.path.lstrip('/'))
                    if path.suffix=='.svg':
                        ids={e.get('id') for e in ET.parse(path).iter()}
                    else:
                        target=self.pages[unquote(dest.path.lstrip('/'))]
                        ids=set(target.ids)
                    self.assertTrue(dest.fragment and dest.fragment in ids,(route,ref))
    def test_no_early_lightbox_image_download(self):
        for route,page in self.pages.items():
            if route in {f'{l}/{slug}/index.html' for l in LANGS for slug in SLUGS}:
                image=next(a for t,a in page.elements if t=='img' and not a.get('src'))
                self.assertTrue(image['alt'])
    def test_generated_pages_are_current(self):
        with tempfile.TemporaryDirectory(prefix='beqson-build-test-') as tmp:
            output=Path(tmp)
            shutil.copytree(ROOT,output/'site',ignore=shutil.ignore_patterns('.git','__pycache__','.agents','.codex'))
            output=output/'site'
            from test_build import snapshot
            before=snapshot(output)
            result=subprocess.run([sys.executable,'tools/build.py'],cwd=output,
                env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertEqual(before,snapshot(output))


if __name__=='__main__':unittest.main(verbosity=2)
