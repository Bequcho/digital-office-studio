#!/usr/bin/env python3
"""Render static social metadata; update sitemap-selected public pages only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, quote
import argparse
import html
import json
import re
import xml.etree.ElementTree as ET
try:
    from .seo_schema import PageMetadata, ROOT, BASE, METADATA, SERVICE_NAMES
    from .build_sitemap import discover
except ImportError:
    from seo_schema import PageMetadata, ROOT, BASE, METADATA, SERVICE_NAMES
    from build_sitemap import discover

LOCALES = {'ka':'ka_GE', 'ru':'ru_RU', 'en':'en_US'}
HERO_IMAGES = {
    'ka': ('assets/неоновый_crm_дашборд_будущего.png', 1774, 887),
    'ru': ('assets/hero-bg-ru.png', 1672, 941),
    'en': ('assets/неоновый_crm_дашборд_в_синем_свете.png', 1672, 941),
}
META_RE = re.compile(r'<meta\b[^>]*>', re.I)


class MetaTag(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.attrs = {}; self.feed(text)
    def handle_starttag(self, tag, attrs):
        if tag == 'meta': self.attrs = dict(attrs)


def is_social(tag):
    attrs = MetaTag(tag).attrs
    return any(attrs.get(key, '').lower().startswith(('og:', 'twitter:')) for key in ('property', 'name'))


def image_info(language, slug, title):
    if slug == 'motion-lab':
        path = 'assets/project-covers/beqson-motion-lab-og.jpg'; width, height = 1600, 1000
        alt = {
            'ka': 'BEQSON Motion Lab — ინტერაქტიული ვებდიზაინისა და AI ინტერფეისის კონცეფცია',
            'ru': 'BEQSON Motion Lab — интерактивный концепт веб-дизайна и AI-интерфейса',
            'en': 'BEQSON Motion Lab — interactive web design and AI interface concept',
        }[language]
        mime = 'image/jpeg'
    elif slug in SERVICE_NAMES:
        path = f'assets/concepts/{language}/{slug}-og.jpg'; width, height = 1200, 800
        label = {'ka':'BEQSON-ის ვებსაიტის კონცეფცია', 'ru':'Концепция сайта BEQSON', 'en':'BEQSON website concept'}[language]
        alt = label + ' — ' + SERVICE_NAMES[slug][('ka','ru','en').index(language)]
        mime = 'image/jpeg'
    else:
        path, width, height = HERO_IMAGES[language]; mime = 'image/png'
        alt = {
            'ka':'BEQSON — ვებსაიტის, CRM-ისა და ანალიტიკის ინტერფეისები ლეპტოპსა და ტელეფონზე',
            'ru':'BEQSON — интерфейсы сайта, CRM и аналитики на ноутбуке и телефоне',
            'en':'BEQSON — website, CRM and analytics interfaces on a laptop and phone',
        }[language]
    if not (ROOT/path).is_file(): raise ValueError(f'Missing social image: {path}')
    return BASE + quote(path), width, height, mime, alt


def render_social(language, canonical, title, description):
    if language not in LOCALES: raise ValueError('Unsupported social locale')
    url = urlsplit(canonical)
    if url.scheme != 'https' or url.netloc != 'beqson.com' or url.query or url.fragment:
        raise ValueError('Social URL must use the canonical domain')
    route = url.path.lstrip('/')
    if route in METADATA:
        title, description = METADATA[route]['title'], METADATA[route]['description']
    slug = route[len(language)+1:].strip('/') if route.startswith(language+'/') else ''
    image, width, height, mime, alt = image_info(language, slug, title)
    og = {'og:type':'website', 'og:site_name':'BEQSON', 'og:title':title,
          'og:description':description, 'og:url':canonical, 'og:locale':LOCALES[language],
          'og:image':image, 'og:image:type':mime, 'og:image:width':str(width),
          'og:image:height':str(height), 'og:image:alt':alt}
    twitter = {'twitter:card':'summary_large_image', 'twitter:title':title,
               'twitter:description':description, 'twitter:image':image, 'twitter:image:alt':alt}
    return ''.join(f'<meta {attribute}="{key}" content="{html.escape(value, quote=True)}">'
                   for attribute, values in [('property', og), ('name', twitter)] for key, value in values.items())


def update_social(source):
    meta = PageMetadata(source)
    tags = render_social(meta.language, meta.canonical, meta.title, meta.description)
    start = source.index('<head'); end = source.index('</head>', start)
    prefix, head, suffix = source[:start], source[start:end], source[end:]
    inserted = False
    def replace(match):
        nonlocal inserted
        if not is_social(match[0]): return match[0]
        if inserted: return ''
        inserted = True
        return tags
    head = META_RE.sub(replace, head)
    if not inserted: head += tags
    head = re.sub(r'(?m)^[ \t]+$', '', head)
    return prefix + head + suffix


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(); pages, _ = discover()
    sitemap = ET.parse(ROOT/'sitemap.xml')
    assert set(pages) == {node.text for node in sitemap.findall('{*}url/{*}loc')}
    for url, path in pages.items():
        source = path.read_text(); result = update_social(source)
        if args.check:
            if source != result: raise SystemExit(f'Stale social metadata: {url}')
        elif source != result: path.write_text(result)
    print(f'Social metadata {"verified" if args.check else "updated"}: {len(pages)} pages')


if __name__ == '__main__': main()
