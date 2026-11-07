"""Independent route inventory and validation shared by offline tests.

Families are explicit so a missing page cannot disappear from expectations merely
because discovery/sitemap stopped seeing it. Templates are composition inputs.
"""
from pathlib import Path
BASE = 'https://beqson.com/'
LANGS = ('ru', 'ka', 'en')
FAMILIES = ('', 'accountants', 'ai-consultant', 'audit', 'autoservices',
 'calculator', 'clinics', 'construction', 'dentists', 'forme-home', 'geo',
 'hotels', 'kakheti-wine-house', 'lawyers', 'meta-static-ads', 'motion-lab',
 'projects', 'realtors', 'shopify', 'tools', 'tools/google-business-description',
 'tools/meta-checker', 'tools/search-preview', 'tools/utm-builder')
ROUTES = {lang + '/' + (slug + '/' if slug else '') for lang in LANGS for slug in FAMILIES}
URLS = {BASE + route for route in ROUTES}
TECHNICAL = {'index.html', '404.html', 'audit/index.html', 'calculator/index.html',
 'projects/index.html', 'tools/index.html', 'tools/search-preview/index.html',
 'tools/utm-builder/index.html', 'crm/index.html', 'crm/proposals/index.html',
 'demo/aristocrat/index.html', 'demo/aristocrat/rooms/index.html',
 'demo/aristocrat/contact/index.html'}
# Dedicated pages retain their own valid schema and social representations.
DEDICATED = {'ai-consultant', 'forme-home', 'geo', 'kakheti-wine-house',
 'meta-static-ads', 'shopify'}
def public_files(root):
    return {p.relative_to(root).as_posix(): p for p in root.rglob('*.html')
            if not any(x.startswith('.') or x in ('templates','node_modules','__pycache__')
                       for x in p.relative_to(root).parts)}
def expected_files():
    return {route + 'index.html' for route in ROUTES} | TECHNICAL
def family(route):
    return route.strip('/').split('/', 1)[1] if '/' in route.strip('/') else ''
def xdefault(route):
    return 'en'
