#!/usr/bin/env python3
"""Browser regression audit; requires Playwright and Chromium, optional axe-core.

python3 tools/audit_browser.py --output /tmp/beqson-audit --axe /path/to/axe.min.js
Start `python3 -m http.server 8000 --directory /workspace/digital-office-studio` before running.
"""
from pathlib import Path
import argparse
import json
import os
import shutil
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
LANGS=('ru','ka','en')
SLUGS=[n['slug'] for n in json.loads((ROOT/'tools/industries.json').read_text())]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',default='http://127.0.0.1:8000/')
    parser.add_argument('--output',type=Path,default=Path('/tmp/beqson-audit'))
    parser.add_argument('--axe',type=Path)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    routes=['', '404.html']+[l+'/' for l in LANGS]+[f'{l}/{s}/' for l in LANGS for s in SLUGS]
    widths=[320,390,768,1001,1181,1440]
    results={'geometry':[],'accessibility':[],'interactions':[],'errors':[]}
    def check(value,label):
        if not value:results['errors'].append(label)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page()
        page.on('pageerror',lambda e:results['errors'].append(str(e)))
        page.on('response',lambda r:results['errors'].append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
        for route in routes:
            for width in widths:
                page.set_viewport_size({'width':width,'height':900})
                response=page.goto(args.base+route)
                check(response.status==200,f'{route}: HTTP failed')
                page.evaluate('document.fonts.ready')
                page.evaluate('''async () => { await Promise.all([...document.images].filter(i => i.hasAttribute('src') && i.getBoundingClientRect().top < innerHeight && i.getBoundingClientRect().bottom > 0).map(i => i.decode().catch(() => null))); }''')
                geometry=page.evaluate('''() => {
                    const header=document.querySelector('.header-inner');
                    const pieces=[...header.children].filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.height&&getComputedStyle(e).position!=='absolute'});
                    const overlap=pieces.some((a,i)=>pieces.slice(i+1).some(b=>{const r=a.getBoundingClientRect(),s=b.getBoundingClientRect();return r.left<s.right-1&&r.right>s.left+1&&r.top<s.bottom-1&&r.bottom>s.top+1}));
                    const pricingOverlap=[...document.querySelectorAll('.plan-top')].some(e=>{const r=e.querySelector('.plan-tag').getBoundingClientRect(),s=e.querySelector('.icon-tile').getBoundingClientRect();return r.left<s.right&&r.right>s.left&&r.top<s.bottom&&r.bottom>s.top});
                    return {overflow:document.documentElement.scrollWidth>innerWidth+1,headerOverlap:overlap,pricingOverlap,missingImages:[...document.images].filter(i=>i.getBoundingClientRect().top<innerHeight&&i.getBoundingClientRect().bottom>0&&getComputedStyle(i).display!=='none'&&i.hasAttribute('src')&&i.complete&&!i.naturalWidth).map(i=>i.src)};
                }''')
                check(not geometry['overflow'],f'{route} {width}: horizontal overflow')
                check(not geometry['headerOverlap'],f'{route} {width}: header overlap')
                check(not geometry['pricingOverlap'],f'{route} {width}: pricing badge overlaps icon')
                check(not geometry['missingImages'],f'{route} {width}: missing visible image')
                results['geometry'].append({'route':route or '/', 'width':width,**geometry})
                if args.axe and width in [390,1440]:
                    page.add_script_tag(path=str(args.axe))
                    violations=page.evaluate("""async () => (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','best-practice']}})).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))""")
                    results['accessibility'].append({'route':route or '/', 'width':width,'violations':violations})
                    check(not violations,f'{route} {width}: axe violations {[(v["id"],len(v["nodes"])) for v in violations]}')
            print(f'Checked {route or "/"}',flush=True)
        for lang in LANGS:
            page.set_viewport_size({'width':390,'height':844});page.goto(args.base+lang+'/')
            button=page.locator('.menu-toggle')
            button.focus();page.keyboard.press('Enter');check(button.get_attribute('aria-expanded')=='true',f'{lang}: menu open')
            check(page.locator('#main-nav > a').first.evaluate('(e)=>e===document.activeElement'),f'{lang}: keyboard enters disclosure links')
            page.keyboard.press('Escape');check(button.get_attribute('aria-expanded')=='false',f'{lang}: menu escape')
            check(button.evaluate('(e)=>e===document.activeElement'),f'{lang}: escape returns focus')
            button.click();page.locator('#main-nav > a').first.click()
            check(button.get_attribute('aria-expanded')=='false',f'{lang}: menu closes on section')
            summary=page.locator('.faq-list summary').first;summary.click()
            check(summary.evaluate('(e)=>e.parentElement.open'),f'{lang}: FAQ')
            page.set_viewport_size({'width':1440,'height':900})
            page.locator('#main-nav > a').first.focus()
            page.set_viewport_size({'width':390,'height':844})
            check(button.evaluate('(e)=>e===document.activeElement'),f'{lang}: resize preserves visible focus')
            page.set_viewport_size({'width':1440,'height':900})
            check(page.locator('#main-nav > a').first.evaluate('(e)=>e===document.activeElement'),f'{lang}: desktop resize preserves visible focus')
            page.set_viewport_size({'width':390,'height':844})
            page.screenshot(path=str(args.output/f'{lang}-mobile.png'),full_page=True)
            results['interactions'].append(f'{lang}: menu, Escape, anchor, FAQ, resize focus')
            for slug in SLUGS:
                page.goto(args.base+f'{lang}/{slug}/')
                link=page.locator('.concept-toolbar [data-lightbox]');link.click()
                check(page.locator('.lightbox').evaluate('(e)=>e.open'),f'{lang}/{slug}: lightbox open')
                page.wait_for_function("document.querySelector('.lightbox img').naturalWidth===1536")
                page.keyboard.press('Escape')
                check(not page.locator('.lightbox').evaluate('(e)=>e.open'),f'{lang}/{slug}: lightbox closes')
                check(link.evaluate('(e)=>e===document.activeElement'),f'{lang}/{slug}: lightbox restores focus')
                destination=LANGS[(LANGS.index(lang)+1)%3]
                page.locator(f'.flag-link[hreflang="{destination}"]').click()
                check(page.url.endswith(f'/{destination}/{slug}/'),f'{lang}/{slug}: language preserves profession')
                results['interactions'].append(f'{lang}/{slug}: lightbox, Escape, focus, language route')
        # Fallback links remain usable without JS; no external contact is invoked.
        context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        fallback=context.new_page()
        for lang in LANGS:
            fallback.goto(args.base+lang+'/lawyers/')
            check(fallback.locator('#main-nav > a').first.is_visible(),f'{lang}: no-JS navigation')
            href=fallback.locator('.full-concept').get_attribute('href')
            check(href.endswith(f'concepts/{lang}/lawyers.webp'),f'{lang}: no-JS full image link')
            results['interactions'].append(f'{lang}: no-JS navigation and image fallback')
        context.close();browser.close()
    (args.output/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(f'Geometry: {len(results["geometry"])}; axe: {len(results["accessibility"])}; interactions: {len(results["interactions"])}; errors: {len(results["errors"])}')
    if results['errors']:raise SystemExit('\n'.join(results['errors']))


if __name__=='__main__':main()
