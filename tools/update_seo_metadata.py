#!/usr/bin/env python3
"""Apply only title and meta description from the shared SEO config.

Run this scoped update instead of rebuilding unrelated page content.
Use --check to verify the checked-in HTML without writing files.
"""
from pathlib import Path
import argparse
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
METADATA = json.loads((ROOT / 'tools/seo_metadata.json').read_text())


def update(source, metadata):
    head = re.search(r'<head\b[^>]*>(.*?)</head>', source, re.S)
    if not head:
        raise ValueError('Missing head')
    content = head[1]
    replacements = [
        (r'<title\b[^>]*>.*?</title>', '<title>' + html.escape(metadata['title']) + '</title>'),
        (r'<meta\b(?=[^>]*\bname=[\"\']description[\"\'])[^>]*>',
         '<meta name="description" content="' + html.escape(metadata['description'], quote=True) + '">'),
    ]
    for pattern, replacement in replacements:
        content, count = re.subn(pattern, lambda _: replacement, content, flags=re.S | re.I)
        if count != 1:
            raise ValueError(f'Expected exactly one metadata element, found {count}: {pattern}')
    return source[:head.start(1)] + content + source[head.end(1):]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    pages = {route + 'index.html': value for route, value in METADATA.items()}
    pages['index.html'] = METADATA['ka/']  # Existing redirect fallback only.
    for filename, metadata in pages.items():
        path = ROOT / filename
        source = path.read_text()
        result = update(source, metadata)
        if args.check:
            if source != result:
                raise SystemExit(f'Metadata differs: {filename}')
        elif source != result:
            path.write_text(result)
    print(f'{len(pages)} HTML documents: metadata {"verified" if args.check else "updated"}')


if __name__ == '__main__':
    main()
