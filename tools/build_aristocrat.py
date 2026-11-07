#!/usr/bin/env python3
"""Build the local-only Aristocrat demo; never touch BEQSON output."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / 'tools' / 'templates' / 'aristocrat'


def main():
    galleries = json.loads((ROOT / 'tools' / 'aristocrat_rooms.json').read_text(encoding='utf-8'))
    for template, route in (('homepage.html', ''), ('rooms.html', 'rooms/'), ('contact.html', 'contact/')):
        page = (TEMPLATES / template).read_text(encoding='utf-8')
        for component in ('header', 'footer'):
            markup = (TEMPLATES / f'{component}.html').read_text(encoding='utf-8').strip()
            if route and component == 'header':
                active = f'/demo/aristocrat/{route}'
                markup = markup.replace(f'<a href="{active}">',
                                        f'<a href="{active}" aria-current="page">')
            page = page.replace('{{' + component + '}}', markup)
        page = page.replace('{{room_galleries}}', json.dumps(galleries['galleries'], ensure_ascii=False).replace('<', '\\u003c'))
        if '{{' in page:
            raise ValueError(f'Unresolved template placeholder in {template}')
        output = ROOT / 'demo' / 'aristocrat' / route / 'index.html'
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(page, encoding='utf-8', newline='\n')
    print('Built Aristocrat homepage, rooms and contact pages (noindex, local demo only).')


if __name__ == '__main__':
    main()
