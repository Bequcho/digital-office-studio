#!/usr/bin/env python3
"""Rebuild from sources in isolation; approved checked-in output is the baseline.

Run: python tools/test_build.py
No application file is written in the working checkout. No network is used.
"""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import re
import shutil
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
LANGS = ('ru', 'ka', 'en')
SLUGS = tuple(row['slug'] for row in json.loads((ROOT / 'tools/industries.json').read_text()))
GENERATED = ['index.html', '404.html', 'assets/icons.svg', 'site.webmanifest'] + [
    f'{lang}/{slug + "/" if slug else ""}index.html' for lang in LANGS for slug in ('', *SLUGS)]
IGNORE = shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache', '.agents', '.codex')


def snapshot(root):
    """Include sources, all public files and CRM, not just generated pages."""
    return {p.relative_to(root).as_posix(): sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()
            and not any(part in {'.git', '__pycache__', '.pytest_cache', '.agents', '.codex'}
                        for part in p.relative_to(root).parts)}


def changed(before, after):
    return sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def select(self, tag, **attrs):
        return [a for t, a in self.elements if t == tag and all(a.get(k) == v for k, v in attrs.items())]


class BuildRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix='beqson-build-regression-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name) / 'site'
        shutil.copytree(ROOT, cls.root, ignore=IGNORE)
        cls.before = snapshot(cls.root)
        # A no-op/preserve-existing implementation must fail: recreate all owned
        # outputs from the generator, components and configs, with no HTML to copy.
        for name in GENERATED:
            (cls.root / name).unlink()
        cls.run_build()
        cls.first = snapshot(cls.root)
        cls.run_build()
        cls.second = snapshot(cls.root)

    @classmethod
    def run_build(cls):
        result = subprocess.run([sys.executable, 'tools/build.py'], cwd=cls.root,
                                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                                text=True, capture_output=True, timeout=60)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    def source(self, route):
        return (self.root / route / 'index.html').read_text(encoding='utf-8')

    def test_all_outputs_recreated_without_changes(self):
        # Byte equality includes visible content, all attributes, H1, head/SEO,
        # forms, script/style/image references, root redirect and file endings.
        self.assertEqual(changed(self.before, self.first), [])

    def test_second_build_is_idempotent(self):
        self.assertEqual(changed(self.first, self.second), [])

    def test_prices_and_currencies(self):
        expected = {'ru': ('₽', ['9 900', '19 900', '34 900']),
                    'ka': ('₾', ['299', '599', '999']),
                    'en': ('$', ['149', '299', '499'])}
        for lang, (currency, prices) in expected.items():
            with self.subTest(lang=lang):
                actual = re.findall(r'<p class="price-amount"><span>(.*?)</span>(.*?)<small>', self.source(lang))
                self.assertEqual(actual, [(currency, price) for price in prices])
        self.assertIn('от 2 900 ₽ / месяц', self.source('ru'))

    def test_home_tools_portfolio_and_navigation(self):
        for lang in LANGS:
            page = Page(self.source(lang))
            with self.subTest(lang=lang):
                for cls in ('audit-home-strip', 'audit-home-strip calculator-home-strip',
                            'home-projects-strip', 'clutch-trust-strip'):
                    self.assertEqual(len(page.select('section', **{'class': cls})), 1, cls)
                for slug in ('audit', 'calculator', 'projects', 'tools'):
                    self.assertTrue(page.select('a', href=f'/{lang}/{slug}/'), slug)
                self.assertEqual(len(page.select('a', **{'class': 'legacy-niche'})), 8)
                self.assertEqual(len(page.select('a', **{'class': 'home-project-card'})), 6)

    def test_lead_system_and_section_inventory(self):
        for lang in LANGS:
            for slug in ('', *SLUGS):
                route = f'{lang}/{slug}'.rstrip('/')
                with self.subTest(route=route):
                    actual = Page(self.source(route))
                    baseline = Page((ROOT / route / 'index.html').read_text())
                    self.assertEqual(len(actual.select('script', src='/assets/lead-system.js?v=2')), 1)
                    self.assertEqual(len(actual.select('link', href='/assets/lead-system.css?v=1')), 1)
                    self.assertEqual(actual.select('section'), baseline.select('section'))
                    self.assertEqual(actual.select('script'), baseline.select('script'))
                    self.assertEqual(actual.select('form'), baseline.select('form'))

    def test_lawyers_additional_sections(self):
        for lang in LANGS:
            source = self.source(f'{lang}/lawyers')
            with self.subTest(lang=lang):
                details = re.search(r'<!-- LAWYERS_SEO_V1 -->(.*?)<!-- /LAWYERS_SEO_V1 -->', source, re.S)
                self.assertIsNotNone(details)
                page = Page(details[1])
                self.assertEqual(len(page.select('section')), 4)
                self.assertEqual(len(page.select('h2')), 4)
                self.assertTrue(page.select('a', href='https://levanilaw.ge'))
                for target in ('audit', 'calculator', 'tools'):
                    self.assertTrue(page.select('a', href=f'/{lang}/{target}/'))

    def test_seo_steps_one_to_eight(self):
        for test in ('test_seo_metadata.py', 'test_seo_schema.py', 'test_sitemap.py', 'test_seo_social.py'):
            with self.subTest(test=test):
                result = subprocess.run([sys.executable, 'tools/' + test], cwd=self.root,
                                        env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                                        capture_output=True, text=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                print(result.stdout.strip())

    def test_sitemap_robots_crm_and_assets_preserved(self):
        protected = [name for name in self.before
                     if name.startswith(('crm/', 'assets/')) or name in ('robots.txt', 'sitemap.xml')]
        self.assertTrue(any(name.startswith('crm/') for name in protected))
        for name in protected:
            self.assertEqual(self.first.get(name), self.before[name], name)
        self.assertIn('Disallow: /crm/', (self.root / 'robots.txt').read_text())

    def test_root_redirect_and_fallback(self):
        source = self.source('')
        self.assertIn('location.replace("/ka/" + location.search + location.hash)', source)
        self.assertIn('<html lang="ka">', source)
        self.assertNotIn('type="application/ld+json"', source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
