#!/usr/bin/env python3
"""Keep redundant CTA arrows out of every public route; retain navigation icons."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
import unittest

from site_contract import ROUTES

ROOT = Path(__file__).resolve().parents[1]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Controls(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.stack = []
        self.controls = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('a', 'button', 'summary', 'select'):
            self.controls.append({'tag': tag, 'attrs': attrs, 'text': '', 'arrow': False})
        current = self.controls[-1] if tag in ('a', 'button', 'summary', 'select') else (
            self.stack[-1][1] if self.stack else None)
        if current:
            classes = attrs.get('class', '').split()
            current['arrow'] |= bool(set(classes) & {'card-arrow', 'project-action-arrow', 'clutch-arrow'})
            if tag == 'use':
                current['arrow'] |= bool(re.search(r'#arrow(?:-up)?$', attrs.get('href', attrs.get('xlink:href', ''))))
        if tag not in VOID:
            self.stack.append((tag, current))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, text):
        if self.stack and self.stack[-1][1]:
            self.stack[-1][1]['text'] += text


def violations(source):
    result = []
    for c in Controls(source).controls:
        # Icon-only controls convey an action (top/fullscreen/previous/next).
        # Summary/select and explicitly identified carousel/dropdown controls
        # retain their functional direction indicators even with visible text.
        attrs, text = c['attrs'], c['text']
        identity = ' '.join(attrs.get(k, '') for k in ('class', 'id', 'data-action', 'aria-label'))
        functional = re.search(r'carousel|slider|swiper|(?:^|[-_ ])(?:prev(?:ious)?|next)(?:$|[-_ ])|dropdown|toggle|fullscreen', identity, re.I)
        if c['tag'] in ('summary', 'select') or functional or not any(x.isalnum() for x in text):
            continue
        if c['arrow'] or any('ARROW' in unicodedata.name(x, '') for x in text):
            result.append((attrs.get('href', attrs.get('class', 'button')), text.strip()[:80]))
    return result


class DecorativeLinkTests(unittest.TestCase):
    def test_all_public_routes(self):
        for route in sorted(ROUTES):
            with self.subTest(route=route):
                self.assertEqual(violations((ROOT / route / 'index.html').read_text(encoding='utf-8')), [])

    def test_detects_reintroduced_decoration(self):
        for decoration in (' →', '<span aria-hidden="true">↗</span>',
                           '<svg><use href="/assets/icons.svg#arrow-up"/></svg>',
                           '<span class="project-action-arrow"></span>'):
            with self.subTest(decoration=decoration):
                self.assertTrue(violations('<a href="/en/projects/">Projects' + decoration + '</a>'))

    def test_retains_functional_navigation(self):
        self.assertEqual(violations('<a href="#top" aria-label="Back to top">↑</a>'
                                    '<button class="carousel-next">Next →</button>'
                                    '<summary>Details ↓</summary>'
                                    '<a href="/en/">English</a>'), [])


if __name__ == '__main__':
    unittest.main()
