#!/usr/bin/env python3
"""Offline browser geometry/interaction regressions: 72 routes x seven widths.

Uses the shared Playwright fixture; all APIs mocked and external traffic blocked.
BEQSON_RESPONSIVE_OUTPUT optionally stores JSON and screenshots outside the repo.
"""
import json
import os
from pathlib import Path
import unittest
import test_lead_modal as fixture
from site_contract import LANGS, ROUTES

WIDTHS=(320,375,390,430,768,1024,1440)

CONTROL_SELECTOR='button,a.btn,a.button,a.audit-home-btn,a.classic-btn'

GEOMETRY = r"""() => {
 const width=document.documentElement.clientWidth;
 const visible=e=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e);
   return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'&&
     !e.closest('[hidden],[aria-hidden="true"]')&&r.right>0;};
 const textRects=e=>{let walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT),rects=[],n;
   while(n=walker.nextNode()){if(!n.textContent.trim()||!visible(n.parentElement))continue;
     let range=document.createRange();range.selectNodeContents(n);rects.push(...range.getClientRects());}
   return rects;};
 const textOverflow=[...document.querySelectorAll('h1,h2')].filter(visible)
   .filter(e=>textRects(e).some(r=>r.left< -1||r.right>width+1))
   .map(e=>({tag:e.tagName,text:e.textContent.slice(0,100)}));
 const scrollContainer=e=>{for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){
   if(['auto','scroll'].includes(getComputedStyle(a).overflowX)&&a.scrollWidth>a.clientWidth+1)return a;}return null;};
 const controlElements=[...document.querySelectorAll('button,a.btn,a.button,a.audit-home-btn,a.classic-btn')];
 const overflowControls=controlElements.filter(visible).filter(e=>{let r=e.getBoundingClientRect();
   return r.left< -1||r.right>width+1||e.scrollWidth>e.clientWidth+2;});
 const scrollableControls=overflowControls.filter(e=>scrollContainer(e)).map(e=>controlElements.indexOf(e));
 const controls=overflowControls.filter(e=>!scrollContainer(e)).map(e=>({text:e.textContent.slice(0,80),class:e.className}));
 const headings=[...document.querySelectorAll('h1,h2')].filter(visible);
 const clipped=headings.filter(e=>{let rects=textRects(e);for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){
   if(['hidden','clip'].includes(getComputedStyle(a).overflowX)){let r=a.getBoundingClientRect();
     if(rects.some(t=>t.left<r.left-1||t.right>r.right+1))return true;}}return false;})
   .map(e=>e.textContent.slice(0,100));
 return {width,scrollWidth:document.documentElement.scrollWidth,textOverflow,controls,clipped,scrollableControls,
   runningAnimations:document.getAnimations().filter(a=>a.playState==='running').length,
   missingImages:[...document.images].filter(i=>i.currentSrc.startsWith(location.origin)&&i.hasAttribute('src')&&i.complete&&!i.naturalWidth).map(i=>i.currentSrc)};
}"""

class ResponsiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):fixture.LeadModalTests.setUpClass()
    @classmethod
    def tearDownClass(cls):fixture.LeadModalTests.tearDownClass()

    def test_all_public_routes_at_all_widths(self):
        helper=fixture.LeadModalTests();rows=[]
        output=Path(os.environ['BEQSON_RESPONSIVE_OUTPUT']) if os.environ.get('BEQSON_RESPONSIVE_OUTPUT') else None
        if output:output.mkdir(parents=True,exist_ok=True)
        for lang in LANGS:
            context,p=helper.open_page(lang,320)
            try:
                for route in sorted(r for r in ROUTES if r.startswith(lang+'/')):
                    for width in WIDTHS:
                        with self.subTest(route=route,width=width):
                            p.set_viewport_size({'width':width,'height':900})
                            response=p.goto(fixture.BASE+'/'+route,wait_until='load')
                            p.evaluate('document.fonts.ready')
                            p.evaluate("async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].filter(i=>i.hasAttribute('src')).map(i=>i.decode().catch(()=>{})))}")
                            p.evaluate('scrollTo(0,0)')
                            data=p.evaluate(GEOMETRY);rows.append({'route':route,'width':width,**data})
                            if output:
                                (output/'responsive-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
                                if data['scrollWidth']>width+1 or data['textOverflow'] or data['clipped'] or data['controls']:
                                    p.screenshot(path=str(output/(route.replace('/','_')+str(width)+'.png')))
                            self.assertEqual(response.status,200)
                            self.assertEqual(data['width'],width)
                            self.assertLessEqual(data['scrollWidth'],width+1)
                            self.assertEqual(data['textOverflow'],[])
                            self.assertEqual(data['clipped'],[])
                            self.assertEqual(data['controls'],[])
                            # Intentional horizontal carousels must expose every
                            # offscreen control through ordinary scrolling.
                            for index in data['scrollableControls']:
                                control=p.locator(CONTROL_SELECTOR).nth(index)
                                control.evaluate("e=>e.scrollIntoView({block:'center',inline:'nearest',behavior:'instant'})")
                                r=control.bounding_box()
                                self.assertGreaterEqual(r['x'],-1)
                                self.assertLessEqual(r['x']+r['width'],width+1)
                                control.click(trial=True)
                                self.assertTrue(control.evaluate("e=>{let r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}"))
                            self.assertEqual(p.evaluate('scrollX'),0)
                            self.assertEqual(data['missingImages'],[])
                            self.assertEqual(data['runningAnimations'],0)
                            self.assertEqual(helper.errors,[])
                            self.assertEqual(helper.calls,[])
                print('Responsive matrix complete:',lang,flush=True)
            finally:context.close()
        self.assertEqual({(r['route'],r['width']) for r in rows},{(r,w) for r in ROUTES for w in WIDTHS})

    def test_negative_controls(self):
        helper=fixture.LeadModalTests()
        context,p=helper.open_page('ka',320)
        try:
            p.add_style_tag(content='.audit-home-card{grid-template-columns:1fr}.audit-home-btn{white-space:nowrap;min-width:auto}')
            self.assertGreater(p.evaluate(GEOMETRY)['scrollWidth'],320)
            p.goto(fixture.BASE+'/ka/ai-consultant/');p.evaluate('document.fonts.ready')
            p.add_style_tag(content='.hero-grid>div{min-width:auto}:lang(ka) .hero h1{font-size:42px;overflow-wrap:normal}')
            data=p.evaluate(GEOMETRY)
            self.assertTrue(data['clipped'])
            self.assertTrue(data['textOverflow'])
            p.goto(fixture.BASE+'/en/projects/');p.evaluate('document.fonts.ready')
            data=p.evaluate(GEOMETRY)
            self.assertTrue(data['scrollableControls'])
            p.add_style_tag(content='.project-filters{overflow-x:hidden!important}')
            self.assertTrue(p.evaluate(GEOMETRY)['controls'])
        finally:context.close()

    def test_home_menu_ai_panel_and_motion(self):
        helper=fixture.LeadModalTests()
        for lang in LANGS:
            for width in WIDTHS:
                with self.subTest(lang=lang,width=width):
                    context,p=helper.open_page(lang,width,touch=True)
                    try:
                        menu=p.locator('.menu-toggle')
                        if menu.is_visible():
                            menu.tap();self.assertEqual(menu.get_attribute('aria-expanded'),'true')
                            p.keyboard.press('Escape');self.assertEqual(menu.get_attribute('aria-expanded'),'false')
                        p.locator('#beqson-ai-assistant-link').tap()
                        panel=p.locator('#beqson-ai-panel');self.assertTrue(panel.is_visible())
                        r=panel.bounding_box();self.assertGreaterEqual(r['x'],-1);self.assertLessEqual(r['x']+r['width'],width+1)
                        panel.locator('button').tap();panel.wait_for(state='hidden')
                        p.emulate_media(reduced_motion='no-preference')
                        p.reload();p.evaluate('document.fonts.ready');p.wait_for_timeout(150)
                        self.assertTrue(p.locator('.brand').first.is_visible())
                        self.assertIn('BEQSON',p.locator('.brand').first.inner_text())
                        self.assertTrue(p.locator('.bq-hero-art').is_visible())
                        self.assertGreater(p.evaluate("document.getAnimations().filter(a=>a.playState==='running').length"),0)
                        p.emulate_media(reduced_motion='reduce')
                        self.assertEqual(p.evaluate("document.getAnimations().filter(a=>a.playState==='running').length"),0)
                        self.assertEqual(helper.errors,[])
                    finally:context.close()

if __name__=='__main__':unittest.main(verbosity=2)
