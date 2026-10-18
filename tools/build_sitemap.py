#!/usr/bin/env python3
"""Discover self-canonical, indexable public HTML and synchronize sitemap only.

Retain existing XML entries (including established hreflang annotations) verbatim;
new URLs receive only loc. Never invent lastmod, priority or changefreq.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, quote
import argparse
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://beqson.com/'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.canonicals = []; self.robots = []; self.refresh = False
        self.html = 0; self.language = ''; self.script = False; self.scripts = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.html += 1; self.language = attrs.get('lang', '')
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'meta':
            if attrs.get('name', '').lower() in ('robots', 'googlebot', 'bingbot'):
                self.robots.extend(re.split(r'[\s,]+', attrs.get('content', '').lower()))
            if attrs.get('http-equiv', '').lower() == 'refresh': self.refresh = True
        if tag == 'script': self.script = True; self.scripts.append('')

    def handle_endtag(self, tag):
        if tag == 'script': self.script = False

    def handle_data(self, data):
        if self.script: self.scripts[-1] += data


def blocked_by_robots(path, source):
    # Site uses the wildcard group. Longest matching path wins; Allow wins ties.
    wildcard = False; rules = []
    for line in source.splitlines():
        line = line.split('#', 1)[0].strip()
        if ':' not in line: continue
        key, value = (part.strip() for part in line.split(':', 1))
        if key.lower() == 'user-agent': wildcard = value == '*'
        elif wildcard and key.lower() in ('allow', 'disallow') and value:
            pattern = '^' + re.escape(value).replace(r'\*', '.*').replace(r'\$', '$')
            if re.search(pattern, path): rules.append((len(value.rstrip('$')), key.lower() == 'allow'))
    return bool(rules) and not max(rules)[1]


def discover(root=ROOT):
    included = {}; excluded = {}
    robots = (root / 'robots.txt').read_text() if (root / 'robots.txt').exists() else ''
    for file in sorted(root.rglob('*.html')):
        relative = file.relative_to(root); parts = relative.parts
        if any(part.startswith('.') or part in ('node_modules', '__pycache__', 'templates') for part in parts): continue
        if parts[0] in ('scripts', 'tests', 'test', 'backend'): continue
        if parts[0] == 'crm':
            excluded[str(relative)] = 'private CRM'; continue
        doc = Document(file.read_text())
        if doc.html != 1:
            excluded[str(relative)] = 'not a complete public HTML document'; continue
        route = '/' + relative.as_posix()
        if route.endswith('/index.html'): route = route[:-len('index.html')]
        actual = BASE.rstrip('/') + quote(route)
        reason = None
        if 'noindex' in doc.robots or 'none' in doc.robots: reason = 'noindex'
        elif doc.refresh or any(re.search(r'(?:window\.)?location\s*(?:\.\s*(?:replace|assign)\s*\(|(?:\.\s*href)?\s*=)', js) for js in doc.scripts): reason = 'redirect'
        elif blocked_by_robots(route, robots): reason = 'blocked by robots.txt'
        elif len(doc.canonicals) != 1: reason = 'missing or duplicate canonical'
        elif doc.canonicals[0] != actual: reason = 'canonical points elsewhere'
        else:
            url = urlsplit(doc.canonicals[0])
            if url.scheme != 'https' or url.netloc != 'beqson.com' or url.query or url.fragment:
                reason = 'noncanonical URL format'
        if reason: excluded[str(relative)] = reason
        else: included[actual] = file
    return included, excluded


def render(root=ROOT):
    urls, _ = discover(root)
    path = root / 'sitemap.xml'
    if not path.exists():
        source = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="'+NS+'">\n</urlset>\n'
    else: source = path.read_text()
    tree = ET.fromstring(source)
    if tree.tag != '{'+NS+'}urlset': raise ValueError('Expected sitemap urlset')
    seen = set()
    def retain(match):
        entry = ET.fromstring('<urlset xmlns="'+NS+'" xmlns:xhtml="http://www.w3.org/1999/xhtml">'+match[0]+'</urlset>')[0]
        locs = entry.findall('{'+NS+'}loc')
        if len(locs) != 1: raise ValueError('Every sitemap entry must have one loc')
        url = locs[0].text
        if url not in urls or url in seen: return ''
        seen.add(url)
        return match[0]
    output = re.sub(r'<url\b[^>]*>.*?</url>', retain, source, flags=re.S)
    additions = ''.join('  <url><loc>'+url+'</loc></url>\n' for url in sorted(set(urls)-seen))
    if additions: output = output.replace('</urlset>', additions+'</urlset>', 1)
    # Removing an entry must not leave indentation-only lines in XML.
    return re.sub(r'(?m)^[ \t]+$', '', output)


def build_sitemap(root=ROOT, check=False):
    result = render(root)
    path = root / 'sitemap.xml'
    if check:
        if not path.exists() or path.read_text() != result: raise SystemExit('Sitemap is out of date')
    elif not path.exists() or path.read_text() != result:
        path.write_text(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    build_sitemap(check=args.check)
    included, excluded = discover()
    print(f'Sitemap: {len(included)} indexable URLs')
    for path, reason in excluded.items(): print(f'Excluded: {path}: {reason}')


if __name__ == '__main__': main()
