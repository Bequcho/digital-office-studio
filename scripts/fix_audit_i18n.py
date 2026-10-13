from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FIXES = {
    'en': {
        "btn.textContent='Анализируем…'": "btn.textContent='Analyzing…'",
        "+' мс'": "+' ms'",
        "(d.lang||'не задан').toUpperCase()": "(d.lang||'not set').toUpperCase()",
        "bad[0]?.label||(bad.length?'Найдены пункты для улучшения':'Базовые проверки пройдены')": "bad[0]?labelFor(bad[0]):(bad.length?'Issues found':'Core checks passed')",
        '<small>SEO-АУДИТ</small>': '<small>SEO AUDIT</small>',
        '<div class=\"pdfDate\">SEO-аудит сайта<br>': '<div class=\"pdfDate\">SEO website audit<br>',
        '<h1>SEO-аудит сайта</h1>': '<h1>SEO website audit</h1>',
        '<h2>Приоритетный план работ</h2>': '<h2>Priority action plan</h2>',
        '<h2>Результаты базовых проверок</h2>': '<h2>Core check results</h2>',
        'aria-label="Написать BEQSON в WhatsApp"': 'aria-label="Contact BEQSON on WhatsApp"',
        'aria-label="Написать BEQSON в Telegram"': 'aria-label="Contact BEQSON on Telegram"',
        'aria-label="Написать BEQSON по email"': 'aria-label="Email BEQSON"',
    },
    'ka': {
        "btn.textContent='Анализируем…'": "btn.textContent='ვამოწმებთ…'",
        "+' мс'": "+' ms'",
        "(d.lang||'не задан').toUpperCase()": "(d.lang||'არ არის მითითებული').toUpperCase()",
        "bad[0]?.label||(bad.length?'Найдены пункты для улучшения':'Базовые проверки пройдены')": "bad[0]?labelFor(bad[0]):(bad.length?'აღმოჩენილია გასაუმჯობესებელი პუნქტები':'ძირითადი შემოწმებები გავლილია')",
        '<small>SEO-АУДИТ</small>': '<small>SEO აუდიტი</small>',
        '<div class=\"pdfDate\">SEO-аудит сайта<br>': '<div class=\"pdfDate\">საიტის SEO აუდიტი<br>',
        '<h1>SEO-аудит сайта</h1>': '<h1>საიტის SEO აუდიტი</h1>',
        '<h2>Приоритетный план работ</h2>': '<h2>პრიორიტეტული სამოქმედო გეგმა</h2>',
        '<h2>Результаты базовых проверок</h2>': '<h2>ძირითადი შემოწმებების შედეგები</h2>',
        'aria-label="Написать BEQSON в WhatsApp"': 'aria-label="მიწერეთ BEQSON-ს WhatsApp-ში"',
        'aria-label="Написать BEQSON в Telegram"': 'aria-label="მიწერეთ BEQSON-ს Telegram-ში"',
        'aria-label="Написать BEQSON по email"': 'aria-label="მისწერეთ BEQSON-ს ელფოსტაზე"',
    },
}

for lang, fixes in FIXES.items():
    p = ROOT / f'{lang}/audit/index.html'
    s = p.read_text(encoding='utf-8')
    for old, new in fixes.items():
        s = s.replace(old, new)
    p.write_text(s, encoding='utf-8')

print('Audit translations polished.')
