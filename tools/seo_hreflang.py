"""Shared hreflang rendering for equivalent BEQSON pages."""
import re


def hreflang_urls(slug=''):
    slug = slug or ''
    if slug and not re.fullmatch(r'[a-z0-9-]+', slug):
        raise ValueError(f'Invalid page slug: {slug}')
    suffix = slug + '/' if slug else ''
    urls = {lang: f'https://beqson.com/{lang}/{suffix}' for lang in ('ka', 'ru', 'en')}
    urls['x-default'] = urls['en']
    return urls


def render_hreflang(slug='', order=('ka', 'ru', 'en', 'x-default')):
    urls = hreflang_urls(slug)
    if len(order) != 4 or set(order) != set(urls):
        raise ValueError('Expected each hreflang exactly once')
    return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{urls[lang]}">'
                   for lang in order)
