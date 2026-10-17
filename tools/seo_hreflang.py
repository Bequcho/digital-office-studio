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


def render_hreflang(slug=''):
    return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{url}">'
                   for lang, url in hreflang_urls(slug).items())
