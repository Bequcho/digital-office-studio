from pathlib import Path

CSS_MARKER = '/* generated portfolio covers v2 */'
CSS_BLOCK = r'''

/* generated portfolio covers v2 */
.project-visual.cover-sprite{
  background-image:url('/assets/project-covers-sprite.webp?v=2');
  background-size:400% 200%;
  background-repeat:no-repeat;
  background-color:#091f3a;
}
.project-visual.cover-sprite:after{background:linear-gradient(180deg,transparent 72%,rgba(6,23,47,.48))}
.cover-beqson{background-position:0% 0%}
.cover-seo{background-position:33.333333% 0%}
.cover-geo{background-position:66.666667% 0%}
.cover-booth{background-position:100% 0%}
.cover-brandkit{background-position:0% 100%}
.cover-report{background-position:33.333333% 100%}
.cover-ai{background-position:66.666667% 100%}
.cover-hair{background-position:100% 100%}
'''

css_path = Path('assets/projects.css')
css = css_path.read_text(encoding='utf-8')
if CSS_MARKER not in css:
    css_path.write_text(css + CSS_BLOCK, encoding='utf-8')

replacements = {
    '<div class="project-visual synthetic"><div class="visual-ui a"></div><div class="visual-ui b"></div><div class="visual-ui c"></div><div class="visual-word">BEQSON<small>DIGITAL STUDIO</small></div></div>': '<div class="project-visual cover-sprite cover-beqson" role="img" aria-label="BEQSON multilingual business website portfolio cover"></div>',
    '<div class="project-visual synthetic"><div class="visual-ui a"></div><div class="visual-ui b"></div><div class="visual-ui c"></div><div class="visual-word">SEARCH<small>SEO / INDEXING</small></div></div>': '<div class="project-visual cover-sprite cover-seo" role="img" aria-label="SEO and search indexing project portfolio cover"></div>',
    '<div class="project-visual synthetic"><div class="visual-ui a"></div><div class="visual-ui b"></div><div class="visual-ui c"></div><div class="visual-word">AI × GEO<small>CHATGPT / GEMINI</small></div></div>': '<div class="project-visual cover-sprite cover-geo" role="img" aria-label="AI search visibility and GEO audit portfolio cover"></div>',
    '<div class="project-visual synthetic"><div class="visual-ui a"></div><div class="visual-ui b"></div><div class="visual-ui c"></div><div class="visual-word">SAAS<small>EVENT / PRINT</small></div></div>': '<div class="project-visual cover-sprite cover-booth" role="img" aria-label="SaaS event booth and print design portfolio cover"></div>',
    '<div class="project-visual synthetic"><div class="visual-ui a"></div><div class="visual-ui b"></div><div class="visual-ui c"></div><div class="visual-word">B2B<small>MARKETING KIT</small></div></div>': '<div class="project-visual cover-sprite cover-brandkit" role="img" aria-label="B2B SaaS marketing and brand asset kit portfolio cover"></div>',
    '<div class="project-visual synthetic"><div class="visual-ui a"></div><div class="visual-ui b"></div><div class="visual-ui c"></div><div class="visual-word">REPORT<small>CASE STUDY</small></div></div>': '<div class="project-visual cover-sprite cover-report" role="img" aria-label="B2B SaaS report and case study design portfolio cover"></div>',
    '<div class="project-visual synthetic"><div class="visual-ui a"></div><div class="visual-ui b"></div><div class="visual-ui c"></div><div class="visual-word">AI VISUAL<small>ART DIRECTION</small></div></div>': '<div class="project-visual cover-sprite cover-ai" role="img" aria-label="AI-assisted marketing visual exploration portfolio cover"></div>',
    '<div class="project-visual synthetic"><div class="visual-ui a"></div><div class="visual-ui b"></div><div class="visual-ui c"></div><div class="visual-word">HAIR<small>WELLNESS</small></div></div>': '<div class="project-visual cover-sprite cover-hair" role="img" aria-label="Hair wellness packaging design portfolio cover"></div>',
}

for lang in ('en', 'ru', 'ka'):
    path = Path(lang) / 'projects' / 'index.html'
    text = path.read_text(encoding='utf-8')
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace('/assets/projects.css?v=1', '/assets/projects.css?v=2-covers')
    path.write_text(text, encoding='utf-8')
