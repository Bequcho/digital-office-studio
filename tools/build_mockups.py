#!/usr/bin/env python3
"""Render exact GE/RU/EN typography over original generated artwork.

Development only: pip install pillow playwright fonttools brotli
Requires a local Chromium executable (CHROMIUM_PATH may override discovery).
Does not contact external services or change existing legacy concept images.
"""
from pathlib import Path
import argparse
import html
import json
import os
import shutil
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent.parent
LANGS = ('ka', 'ru', 'en')


def prepare_fonts():
    from fontTools.ttLib import TTFont
    for source in (ROOT / 'assets/fonts').glob('*.woff'):
        target = source.with_suffix('.woff2')
        if not target.exists():
            font = TTFont(source)
            font.flavor = 'woff2'
            font.save(target)


def document(slug, lang, data, brand, base_url):
    esc = html.escape
    arrow = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 18 18 6M6 6h12v12"/></svg>'
    nav = {
        'ru': ('Услуги', 'О нас', 'Контакты'),
        'ka': ('სერვისები', 'ჩვენ შესახებ', 'კონტაქტი'),
        'en': ('Services', 'About', 'Contact'),
    }[lang]
    css = (ROOT / 'tools/mockups.css').read_text()
    css = css.replace("url('../assets/", f"url('{base_url}/assets/")
    photo = f'{base_url}/assets/concepts/art/{slug}.webp'
    services = ''.join(
        f'<div class="service"><span class="number">0{i+1}</span>'
        f'<span>{esc(label)}</span><span class="arrow">{arrow}</span></div>'
        for i, label in enumerate(data['services'])
    )
    return f'''<!doctype html><html lang="{lang}"><meta charset="utf-8">
<style>{css}</style><body class="{slug}" style="--photo:url('{photo}')">
<header class="top"><div class="logo">{brand}</div><div class="nav">{''.join('<span>'+esc(x)+'</span>' for x in nav)}</div><div class="top-cta">{esc(data['cta'])}</div></header>
<main><section class="hero"><div class="copy"><p class="eyebrow">{esc(data['eyebrow'])}</p><h1>{esc(data['title']).replace(chr(10), '<br>')}</h1><p class="intro">{esc(data['text'])}</p><div class="cta">{esc(data['cta'])}<span>{arrow}</span></div></div><div class="photo"></div></section><section class="services"><p class="section-label">{esc(data['section'])}</p><div class="service-grid">{services}</div></section></main></body></html>'''


def main():
    from PIL import Image
    from playwright.sync_api import sync_playwright
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--slug', choices=list(json.loads((ROOT/'tools/mockups.json').read_text())))
    args = parser.parse_args()
    prepare_fonts()
    data = json.loads((ROOT/'tools/mockups.json').read_text())
    brands = {n['slug']: n['brand'] for n in json.loads((ROOT/'tools/industries.json').read_text())}
    executable = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
    if not executable:
        raise SystemExit('Chromium is required; set CHROMIUM_PATH to its executable.')
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base_url = f'http://127.0.0.1:{server.server_port}'
    with tempfile.TemporaryDirectory(prefix='beqson-mockups-') as tmp, sync_playwright() as p:
        browser = p.chromium.launch(executable_path=executable, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width':1536, 'height':1024}, device_scale_factor=1)
        manifest = {}
        for slug, languages in data.items():
            if args.slug and slug != args.slug:
                continue
            if not (ROOT/f'assets/concepts/art/{slug}.webp').exists():
                raise SystemExit(f'Missing original artwork for {slug}')
            for lang, content in languages.items():
                page.goto(base_url+'/tools/mockups.json')
                page.set_content(document(slug,lang,content,brands[slug],base_url), wait_until='networkidle')
                page.evaluate("""async () => { await Promise.all([document.fonts.load('600 20px Georgian', 'ქართული'), document.fonts.load('400 20px Manrope', 'Адвокаты')]); }""")
                page.evaluate('document.fonts.ready')
                page.wait_for_function('''() => [...document.fonts].every(f => f.status !== 'loading')''')
                assert page.evaluate('''() => document.fonts.check('600 20px Georgian') && document.fonts.check('400 20px Manrope')'''), 'Fonts missing'
                # Detect clipped copy or service text before exporting.
                assert page.evaluate('''() => [...document.querySelectorAll('.copy,.service,.top')].every(e => e.scrollWidth <= e.clientWidth + 1 && e.scrollHeight <= e.clientHeight + 1)'''), f'Overflow in {slug}/{lang}'
                screenshot=Path(tmp)/f'{slug}-{lang}.png'
                page.screenshot(path=str(screenshot))
                out=ROOT/f'assets/concepts/{lang}';out.mkdir(parents=True,exist_ok=True)
                with Image.open(screenshot) as original:
                    for width,suffix in [(320,'-320'),(480,'-480'),(768,'-768'),(1536,'')]:
                        image=original.resize((width,width*2//3),Image.Resampling.LANCZOS)
                        # Preserve the crisp typography; photograph compression is optional AVIF.
                        image.save(out/f'{slug}{suffix}.webp','WEBP',quality=88,method=6)
                        image.save(out/f'{slug}{suffix}.avif','AVIF',quality=68,speed=6)
                    original.resize((1200,800),Image.Resampling.LANCZOS).convert('RGB').save(out/f'{slug}-og.jpg','JPEG',quality=88,optimize=True,progressive=True)
                manifest[f'{lang}/{slug}']={'title':content['title'],'size':[1536,1024], 'formats':['avif','webp'], 'widths':[320,480,768,1536]}
                print(f'Rendered {lang}/{slug}',flush=True)
        browser.close()
    server.shutdown()
    if not args.slug:
        (ROOT/'tools/mockups-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')


if __name__ == '__main__':
    main()
