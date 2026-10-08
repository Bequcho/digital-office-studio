#!/usr/bin/env python3
"""Static regression checks: python3 tools/test_site.py (standard library only)."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import json
import runpy
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
        self.path=path; self.elements=[]; self.ids=[]; self.scripts=[]; self.current_script=None
        self.feed(path.read_text())
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
        cls.pages={p.relative_to(ROOT).as_posix():Page(p) for p in ROOT.rglob('*.html')}
    def test_routes_and_language(self):
        expected={'index.html','404.html'}|{f'{l}/index.html' for l in LANGS}|{f'{l}/{s}/index.html' for l in LANGS for s in SLUGS}
        self.assertEqual(set(self.pages),expected)
        for route,page in self.pages.items():
            with self.subTest(route=route):
                self.assertEqual(page.select('html')[0]['lang'],route.split('/')[0] if '/' in route else ('ka' if route=='index.html' else 'ru'))
                self.assertEqual(len(page.select('h1')),1)
                self.assertEqual(len(page.select('main')),1)
                self.assertEqual(len(page.ids),len(set(page.ids)))
                self.assertEqual(page.path.read_text().lower().count('<!doctype html>'),1)
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
        for route,page in self.pages.items():
            canonical=page.select('link',rel='canonical')
            self.assertEqual(len(canonical),1)
            expected=BASE+('ka/' if route=='index.html' else route.removesuffix('index.html'))
            self.assertEqual(canonical[0]['href'],expected)
            alternates=page.select('link',rel='alternate')
            self.assertEqual(len(alternates),0 if route=='404.html' else 4)
            if route!='404.html':self.assertEqual({a['hreflang'] for a in alternates},{*LANGS,'x-default'})
            if route!='404.html':
                suffix=route.split('/')[1]+'/' if route.count('/')==2 else ''
                self.assertEqual(next(a['href'] for a in alternates if a['hreflang']=='x-default'),BASE+'ka/'+suffix)
            self.assertEqual(len(page.select('meta',name='description')),1)
            self.assertEqual(len(page.select('title')),1)
            for attribute in ['og:image','og:image:width','og:image:height','og:image:alt']:
                self.assertEqual(len(page.select('meta',property=attribute)),1)
            if route=='404.html':self.assertEqual(page.select('meta',name='robots')[0]['content'],'noindex,follow')
    def test_json_ld_and_sitemap(self):
        for route,page in self.pages.items():
            for raw in page.scripts:
                graph=json.loads(raw)['@graph'];ids=[x['@id'] for x in graph if '@id' in x]
                self.assertEqual(len(ids),len(set(ids)))
                webpage=next(x for x in graph if x['@type']=='WebPage')
                self.assertEqual(webpage['url'],page.select('link',rel='canonical')[0]['href'])
        tree=ET.parse(ROOT/'sitemap.xml');urls=tree.findall('{*}url');self.assertEqual(len(urls),27)
        for entry in urls:
            self.assertEqual(len(entry.findall('{*}link')),4)
            self.assertNotIn('404',entry.find('{*}loc').text)
        json.loads((ROOT/'site.webmanifest').read_text())
    def test_legacy_image_links_remain_available(self):
        for slug in SLUGS:
            for suffix in ['', '-small']:self.assertTrue((ROOT/f'assets/concepts/{slug}{suffix}.webp').is_file())
    def test_external_link_security(self):
        for route,page in self.pages.items():
            for link in page.select('a',target='_blank'):
                self.assertIn('noopener',link.get('rel',''))
    def test_icon_sprite_references(self):
        tree=ET.parse(ROOT/'assets/icons.svg')
        ids={node.attrib['id'] for node in tree.getroot() if 'id' in node.attrib}
        self.assertGreater(len(ids),20)
        for page in self.pages.values():
            for use in page.select('use'):self.assertIn(urlsplit(use['href']).fragment,ids)
    def test_no_early_lightbox_image_download(self):
        for route,page in self.pages.items():
            if len(route.split('/'))==3:
                image=next(a for t,a in page.elements if t=='img' and not a.get('src'))
                self.assertTrue(image['alt'])
    def test_generated_pages_are_current(self):
        with tempfile.TemporaryDirectory(prefix='beqson-build-test-') as tmp:
            output=Path(tmp)
            shutil.copytree(ROOT/'tools',output/'tools',ignore=shutil.ignore_patterns('__pycache__'))
            runpy.run_path(str(output/'tools/build.py'),run_name='__main__')
            for generated in output.rglob('*'):
                relative=generated.relative_to(output)
                if not generated.is_file() or relative.parts[0]=='tools':continue
                self.assertEqual(generated.read_bytes(),(ROOT/relative).read_bytes(),str(relative))


if __name__=='__main__':unittest.main(verbosity=2)
