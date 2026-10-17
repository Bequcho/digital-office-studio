#!/usr/bin/env python3
"""Check source HTML metadata, uniqueness and the shared page generator."""
from html.parser import HTMLParser
from pathlib import Path
import importlib.util
import json
import re

ROOT = Path(__file__).resolve().parents[1]
METADATA = json.loads((ROOT / 'tools/seo_metadata.json').read_text())


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_title = False
        self.titles = []
        self.descriptions = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'head':
            self.in_head = True
        if tag == 'title':
            assert self.in_head, 'Title outside head'
            self.in_title = True
            self.titles.append('')
        if tag == 'meta' and attrs.get('name', '').lower() == 'description':
            assert self.in_head, 'Description outside head'
            self.descriptions.append(attrs.get('content', ''))

    def handle_endtag(self, tag):
        if tag == 'head':
            self.in_head = False
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.titles[-1] += data


def check(source, expected=None):
    parser = MetadataParser()
    parser.feed(source)
    assert len(parser.titles) == len(parser.descriptions) == 1
    assert parser.titles[0].strip() and parser.descriptions[0].strip()
    if expected:
        assert parser.titles == [expected['title']]
        assert parser.descriptions == [expected['description']]


def main():
    for field in ['title', 'description']:
        assert len({value[field] for value in METADATA.values()}) == 30, field
    for route, expected in METADATA.items():
        check((ROOT / route / 'index.html').read_text(), expected)
    check((ROOT / 'index.html').read_text(), METADATA['ka/'])
    count = 0
    for path in ROOT.rglob('*.html'):
        parts = path.relative_to(ROOT).parts
        if parts[0] == 'tools' or any(part in {'.git', 'node_modules'} for part in parts):
            continue
        source = path.read_text()
        if re.search(r'noindex|http-equiv=[\"\']refresh', source, re.I):
            continue
        check(source)
        count += 1
    spec = importlib.util.spec_from_file_location('site_build', ROOT / 'tools/build.py')
    build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build)
    for route, expected in METADATA.items():
        parts = route.strip('/').split('/')
        if parts[-1] == 'projects':
            continue  # The dedicated portfolio workflow has its own generator.
        lang = parts[0]
        slug = parts[1] if len(parts) == 2 else None
        check(build.head(lang, '../', 'Existing social title', 'Existing schema description', slug), expected)
    print(f'PASS: 30 target pages, root fallback, {count} indexable documents, unique values and build output')


if __name__ == '__main__':
    main()
