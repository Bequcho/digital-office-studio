from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TAG = '<script src="/assets/audit-pdf-v3.js?v=3"></script>'
FILES = [
    ROOT / 'audit/index.html',
    ROOT / 'ru/audit/index.html',
    ROOT / 'en/audit/index.html',
    ROOT / 'ka/audit/index.html',
]

for path in FILES:
    if not path.exists():
        continue
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'\s*<script src="/assets/audit-pdf-v3\.js\?v=\d+"></script>', '', s)
    if '</body>' not in s:
        raise RuntimeError(f'</body> not found in {path}')
    s = s.replace('</body>', TAG + '\n</body>', 1)
    path.write_text(s, encoding='utf-8')
    print('patched', path.relative_to(ROOT))
