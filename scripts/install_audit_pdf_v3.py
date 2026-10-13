from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TAG = '<script src="/assets/audit-pdf-v3.js?v=4"></script>'
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

    # Remove every previously injected audit PDF module tag. An earlier
    # installer could place it inside the print fallback template string,
    # where a literal </script> prematurely terminated the page script.
    s = re.sub(
        r'\s*<script src="/assets/audit-pdf-v3\.js\?v=\d+"></script>',
        '',
        s,
    )

    # Insert only before the final, real closing body tag. Audit pages also
    # contain </body> inside a JavaScript template string used for printing.
    pos = s.rfind('</body>')
    if pos == -1:
        raise RuntimeError(f'final </body> not found in {path}')

    s = s[:pos] + TAG + '\n' + s[pos:]
    path.write_text(s, encoding='utf-8')
    print('patched', path.relative_to(ROOT))
