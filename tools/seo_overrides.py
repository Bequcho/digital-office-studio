"""Small shared SEO overrides for public tools and the legacy audit alias.

Only head metadata is changed. The alias continues to serve its working tool.
"""
from pathlib import Path
import json
import re
from html import escape
try:
    from .seo_schema import update_schema
    from .seo_social import update_social
except ImportError:
    from seo_schema import update_schema
    from seo_social import update_social

ROOT = Path(__file__).resolve().parents[1]
OVERRIDES = json.loads((ROOT / 'tools/seo_overrides.json').read_text())


def apply_overrides(root=ROOT):
    for route, values in OVERRIDES.items():
        path = root / route / 'index.html'
        source = path.read_text()
        head, body = source.split('</head>', 1)
        if 'title' in values:
            head, count = re.subn(r'<title>.*?</title>', lambda _: '<title>' + escape(values['title']) + '</title>', head, flags=re.S)
            if count != 1: raise ValueError(f'Expected one title: {route}')
        if 'canonical' in values:
            head, count = re.subn(r'<link rel="canonical" href="[^"]+">', lambda _: '<link rel="canonical" href="' + values['canonical'] + '">', head)
            if count != 1: raise ValueError(f'Expected one canonical: {route}')
        slug = 'audit' if route == 'audit/' else route.split('/', 1)[1].strip('/')
        result = update_social(update_schema(head + '</head>' + body, slug))
        if result != source: path.write_text(result)


if __name__ == '__main__':
    apply_overrides()
