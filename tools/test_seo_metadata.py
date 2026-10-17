#!/usr/bin/env python3
"""Check source HTML metadata, uniqueness and the shared page generator."""
from html.parser import HTMLParser
from pathlib import Path
import importlib.util
import json
import re
import ast
import textwrap
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
METADATA = json.loads((ROOT / 'tools/seo_metadata.json').read_text())


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_title = False
        self.titles = []
        self.descriptions = []
        self.canonicals = []
        self.alternates = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'head':
            self.in_head = True
        if tag == 'link' and 'alternate' in attrs.get('rel', '').lower().split() and 'hreflang' in attrs:
            assert self.in_head, 'Hreflang outside head'
            self.alternates.append((attrs['hreflang'], attrs.get('href', '')))
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            assert self.in_head, 'Canonical outside head'
            self.canonicals.append(attrs.get('href', ''))
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


def check(source, expected=None, canonical=None, hreflang=False):
    parser = MetadataParser()
    parser.feed(source)
    assert len(parser.titles) == len(parser.descriptions) == 1
    assert parser.titles[0].strip() and parser.descriptions[0].strip()
    if canonical is not None:
        assert parser.canonicals == [canonical], (parser.canonicals, canonical)
        url = urlsplit(parser.canonicals[0])
        assert url.scheme == 'https' and url.netloc == 'beqson.com'
        assert url.path.endswith('/') and not url.query and not url.fragment
    if hreflang:
        assert canonical is not None
        suffix = urlsplit(canonical).path.split('/', 2)[2]
        expected_links = {lang: f'https://beqson.com/{lang}/{suffix}' for lang in ('ka', 'ru', 'en')}
        expected_links['x-default'] = expected_links['en']
        assert len(parser.alternates) == 4, parser.alternates
        assert dict(parser.alternates) == expected_links, parser.alternates
        for _, href in parser.alternates:
            url = urlsplit(href)
            assert url.scheme == 'https' and url.netloc == 'beqson.com'
            assert url.path.endswith('/') and not url.query and not url.fragment
    if expected:
        assert parser.titles == [expected['title']]
        assert parser.descriptions == [expected['description']]
    return parser


def main():
    for field in ['title', 'description']:
        assert len({value[field] for value in METADATA.values()}) == 30, field
    for route, expected in METADATA.items():
        check((ROOT / route / 'index.html').read_text(), expected, 'https://beqson.com/' + route, hreflang=True)
    check((ROOT / 'index.html').read_text(), METADATA['ka/'], 'https://beqson.com/ka/', hreflang=True)
    # Verify actual reciprocal links, self-reference and target files in every group.
    for route in METADATA:
        source = check((ROOT / route / 'index.html').read_text())
        language = route.split('/')[0]
        for target_language, href in source.alternates:
            if target_language == 'x-default':
                continue
            target_route = urlsplit(href).path.lstrip('/')
            assert target_route in METADATA
            target = check((ROOT / target_route / 'index.html').read_text())
            assert dict(target.alternates)[language] == 'https://beqson.com/' + route
    count = 0
    for path in ROOT.rglob('*.html'):
        parts = path.relative_to(ROOT).parts
        if parts[0] == 'tools' or any(part in {'.git', 'node_modules'} for part in parts):
            continue
        source = path.read_text()
        if re.search(r'noindex|http-equiv=[\"\']refresh', source, re.I):
            continue
        route = path.parent.relative_to(ROOT).as_posix() + '/'
        check(source, canonical='https://beqson.com/' + route)
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
        check(build.head(lang, '../', 'Existing social title', 'Existing schema description', slug), expected, 'https://beqson.com/' + route, hreflang=True)
    # Evaluate only declarations from the portfolio generator, never its write loop.
    workflow = (ROOT / '.github/workflows/build-projects-portfolio.yml').read_text()
    code = textwrap.dedent(workflow.split("python - <<'PY'\n", 1)[1].split('\n          PY', 1)[0])
    tree = ast.parse(code)
    tree.body = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef))]
    namespace = {}
    import os
    previous = Path.cwd()
    try:
        os.chdir(ROOT)
        import sys
        sys.path.insert(0, str(ROOT))
        exec(compile(tree, 'portfolio-generator', 'exec'), namespace)
        for lang in ('ka', 'ru', 'en'):
            route = lang + '/projects/'
            check(namespace['page'](lang), METADATA[route], 'https://beqson.com/' + route, hreflang=True)
    finally:
        sys.path.pop(0)
        os.chdir(previous)
    print(f'PASS: 30 target pages, root fallback, {count} indexable documents, unique values, self-canonicals, reciprocal hreflang and both generators')


if __name__ == '__main__':
    main()
