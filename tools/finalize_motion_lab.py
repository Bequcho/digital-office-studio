#!/usr/bin/env python3
"""Apply the site's existing JSON-LD and social-meta generators to Motion Lab only."""

from pathlib import Path
from seo_schema import update_schema
from seo_social import update_social


ROOT = Path(__file__).resolve().parents[1]


def main():
    for language in ('ru', 'en', 'ka'):
        page = ROOT / language / 'motion-lab' / 'index.html'
        source = page.read_text()
        result = update_social(update_schema(source, 'motion-lab'))
        if result != source:
            page.write_text(result)
        print(f'Finalized {language}/motion-lab/index.html')


if __name__ == '__main__':
    main()
