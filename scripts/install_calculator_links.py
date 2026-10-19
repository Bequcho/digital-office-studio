from pathlib import Path
import re

cards = {
    'ru': '''<section class="audit-home-strip calculator-home-strip"><div class="shell"><div class="audit-home-card"><div><span class="audit-home-kicker">BEQSON WEBSITE COST CALCULATOR</span><h2>Рассчитайте стоимость сайта</h2><p>Ответьте на 5 быстрых вопросов — сразу получите ориентировочный бюджет проекта и подходящий пакет BEQSON.</p></div><a class="audit-home-btn" href="/ru/calculator/">Рассчитать стоимость →</a></div></div></section>''',
    'en': '''<section class="audit-home-strip calculator-home-strip"><div class="shell"><div class="audit-home-card"><div><span class="audit-home-kicker">BEQSON WEBSITE COST CALCULATOR</span><h2>Estimate your website cost</h2><p>Answer 5 quick questions and get an instant project range plus the recommended BEQSON package.</p></div><a class="audit-home-btn" href="/en/calculator/">Calculate website cost →</a></div></div></section>''',
    'ka': '''<section class="audit-home-strip calculator-home-strip"><div class="shell"><div class="audit-home-card"><div><span class="audit-home-kicker">BEQSON WEBSITE COST CALCULATOR</span><h2>გაიგეთ ვებსაიტის სავარაუდო ღირებულება</h2><p>უპასუხეთ 5 მოკლე კითხვას და მყისიერად მიიღეთ პროექტის სავარაუდო ბიუჯეტი და შესაბამისი BEQSON პაკეტი.</p></div><a class="audit-home-btn" href="/ka/calculator/">ღირებულების გამოთვლა →</a></div></div></section>'''
}

for lang, card in cards.items():
    p = Path(lang) / 'index.html'
    s = p.read_text(encoding='utf-8')
    # Detect the entry point structurally; its translated wording can evolve.
    if 'calculator-home-strip' not in s:
        m = re.search(r'(<section class="audit-home-strip">.*?</section>)', s, flags=re.S)
        if not m:
            raise SystemExit(f'audit block not found in {p}')
        s = s[:m.end()] + card + s[m.end():]
        p.write_text(s, encoding='utf-8')

sitemap = Path('sitemap.xml')
s = sitemap.read_text(encoding='utf-8')
if 'https://beqson.com/ru/calculator/' not in s:
    block = '''  <url><loc>https://beqson.com/ru/calculator/</loc><xhtml:link rel="alternate" hreflang="ru" href="https://beqson.com/ru/calculator/" /><xhtml:link rel="alternate" hreflang="ka" href="https://beqson.com/ka/calculator/" /><xhtml:link rel="alternate" hreflang="en" href="https://beqson.com/en/calculator/" /><xhtml:link rel="alternate" hreflang="x-default" href="https://beqson.com/en/calculator/" /></url>\n  <url><loc>https://beqson.com/ka/calculator/</loc><xhtml:link rel="alternate" hreflang="ru" href="https://beqson.com/ru/calculator/" /><xhtml:link rel="alternate" hreflang="ka" href="https://beqson.com/ka/calculator/" /><xhtml:link rel="alternate" hreflang="en" href="https://beqson.com/en/calculator/" /><xhtml:link rel="alternate" hreflang="x-default" href="https://beqson.com/en/calculator/" /></url>\n  <url><loc>https://beqson.com/en/calculator/</loc><xhtml:link rel="alternate" hreflang="ru" href="https://beqson.com/ru/calculator/" /><xhtml:link rel="alternate" hreflang="ka" href="https://beqson.com/ka/calculator/" /><xhtml:link rel="alternate" hreflang="en" href="https://beqson.com/en/calculator/" /><xhtml:link rel="alternate" hreflang="x-default" href="https://beqson.com/en/calculator/" /></url>\n'''
    s = s.replace('</urlset>', block + '</urlset>')
    sitemap.write_text(s, encoding='utf-8')
