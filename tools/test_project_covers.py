#!/usr/bin/env python3
"""Validate portfolio illustrations and their multilingual card references."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
COVERS = {'beqson': 'beqson', 'gsc': 'seo', 'geo': 'geo', 'booth': 'booth',
          'brandkit': 'brandkit', 'report': 'report', 'aivisual': 'ai-visual',
          'packaging': 'hair-wellness'}

class Cards(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.cards = {}
        self.current = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article' and 'project-card' in attrs.get('class', '').split():
            self.current = attrs['id']
            self.cards[self.current] = []
        if tag == 'img' and self.current:
            self.cards[self.current].append(attrs)

    def handle_endtag(self, tag):
        if tag == 'article':
            self.current = None

class CoverTests(unittest.TestCase):
    def test_self_contained_vector_artwork(self):
        for name in COVERS.values():
            with self.subTest(cover=name):
                path = ROOT / 'assets/project-covers' / (name + '.svg')
                svg = ET.parse(path).getroot()
                self.assertEqual(svg.get('viewBox'), '0 0 1600 1000')
                self.assertLess(path.stat().st_size, 40000)
                self.assertTrue(svg.find('{http://www.w3.org/2000/svg}title').text)
                ids = [e.get('id') for e in svg.iter() if e.get('id')]
                self.assertEqual(len(ids), len(set(ids)))
                for element in svg.iter():
                    self.assertNotIn(element.tag.split('}')[-1], ('image', 'script', 'foreignObject'))
                    for key, value in element.attrib.items():
                        if key.endswith('href'):
                            self.assertTrue(value.startswith('#'))
                        self.assertNotIn('data:', value)

    def test_three_languages_keep_eleven_cards(self):
        for lang in ('en', 'ru', 'ka'):
            with self.subTest(lang=lang):
                cards = Cards((ROOT / lang / 'projects/index.html').read_text()).cards
                self.assertEqual(len(cards), 11)
                for project, name in COVERS.items():
                    self.assertEqual(len(cards[project]), 1)
                    image = cards[project][0]
                    self.assertEqual(image['src'], f'/assets/project-covers/{name}.svg')
                    self.assertTrue(image['alt'])
                    self.assertEqual(image['decoding'], 'async')
                    self.assertEqual(image['width'], '1600')
                    self.assertEqual(image['height'], '1000')
                    self.assertTrue((ROOT / image['src'].lstrip('/')).is_file())
                for project in ('levani', 'redesign', 'industry'):
                    for image in cards[project]:
                        self.assertIn(f'/assets/concepts/{lang}/', image['src'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
