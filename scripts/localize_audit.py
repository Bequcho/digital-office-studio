from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = (ROOT / 'audit/index.html').read_text(encoding='utf-8')

PAGES = {
    'ru': {
        'path': ROOT / 'ru/audit/index.html',
        'home': '/ru/',
        'canonical': 'https://beqson.com/ru/audit/',
        'html_lang': 'ru',
        'repl': {},
    },
    'en': {
        'path': ROOT / 'en/audit/index.html',
        'home': '/en/',
        'canonical': 'https://beqson.com/en/audit/',
        'html_lang': 'en',
        'repl': {
            'Бесплатный SEO-аудит сайта — BEQSON':'Free SEO website audit — BEQSON',
            'Бесплатная экспресс-проверка сайта: Title, Description, H1, Canonical, HTTPS, мобильная адаптация, Open Graph, structured data и индексируемость.':'Free express website check: Title, Description, H1, Canonical, HTTPS, mobile setup, Open Graph, structured data and indexability.',
            'Получите BEQSON Score, ключевые SEO-проблемы и план действий.':'Get a BEQSON Score, key SEO issues and an action plan.',
            '← На сайт':'← Back to website',
            'Бесплатный SEO-аудит сайта':'Free SEO website audit',
            'Введите адрес сайта. Мы проверим ключевые технические SEO-факторы и покажем BEQSON Score от 0 до 100 — без регистрации.':'Enter your website address. We’ll check the key technical SEO factors and show a BEQSON Score from 0 to 100 — no registration required.',
            'Проверить сайт →':'Run website audit →',
            'Экспресс-аудит проверяет текущую HTML-страницу и базовые SEO-настройки. Он не заменяет полный технический аудит.':'The express audit checks the current HTML page and core SEO settings. It does not replace a full technical audit.',
            'Оценка:':'Grade:',
            'Результат аудита':'Audit result',
            'Ответ сервера':'Server response',
            'Язык':'Language',
            'Ключевые результаты':'Key results',
            'Показываем до трёх наиболее важных пунктов экспресс-аудита.':'We show up to three of the most important findings from the express audit.',
            'Получить полный отчёт + план действий':'Get the full report + action plan',
            'Оставьте контакт — полный список проверок и приоритетный план исправлений откроются сразу. Запрос сохранится в BEQSON CRM.':'Leave your contact details — the full checklist and priority action plan will open immediately. Your request will be saved in BEQSON CRM.',
            'БЕСПЛАТНО':'FREE',
            'Ваше имя':'Your name',
            'Открыть полный отчёт →':'Open full report →',
            'Согласен(на), что BEQSON сохранит указанный контакт и свяжется со мной по результатам аудита.':'I agree that BEQSON may save my contact details and contact me about the audit results.',
            'Полный экспресс-отчёт':'Full express report',
            'Все базовые технические проверки, выполненные BEQSON Website Audit.':'All core technical checks performed by BEQSON Website Audit.',
            'Приоритетный план действий':'Priority action plan',
            'ГОТОВЫЙ ОТЧЁТ':'REPORT READY',
            'Скачать PDF-аудит BEQSON':'Download BEQSON PDF audit',
            'Сохраните аудит, отправьте партнёру или команде. В PDF: логотип BEQSON, адрес сайта, SEO Score, найденные проблемы, базовые проверки и приоритетный план работ.':'Save the audit and share it with a partner or your team. The PDF includes BEQSON branding, website address, SEO Score, detected issues, core checks and a priority action plan.',
            'Скачать PDF-аудит ↓':'Download PDF audit ↓',
            'Фирменный отчёт':'Branded report',
            'Удобно переслать':'Easy to share',
            'План исправлений':'Fix plan',
            'Ключевые проблемы':'Key issues',
            'Отчёт будет сформирован после аудита.':'The report will be generated after the audit.',
            'Хотите исправить найденное?':'Want us to fix the issues?',
            'BEQSON может взять техническое SEO, структуру сайта и систему привлечения клиентов под ключ.':'BEQSON can handle technical SEO, site structure and your client acquisition system end to end.',
            'Выберите удобный канал связи:':'Choose your preferred contact channel:',
            '© BEQSON Digital Studio · Экспресс-аудит носит диагностический характер':'© BEQSON Digital Studio · The express audit is diagnostic in nature',
            'Готовим отчёт…':'Preparing report…',
            'Формируем PDF…':'Generating PDF…',
        },
    },
    'ka': {
        'path': ROOT / 'ka/audit/index.html',
        'home': '/ka/',
        'canonical': 'https://beqson.com/ka/audit/',
        'html_lang': 'ka',
        'repl': {
            'Бесплатный SEO-аудит сайта — BEQSON':'საიტის უფასო SEO აუდიტი — BEQSON',
            'Бесплатная экспресс-проверка сайта: Title, Description, H1, Canonical, HTTPS, мобильная адаптация, Open Graph, structured data и индексируемость.':'საიტის უფასო სწრაფი შემოწმება: Title, Description, H1, Canonical, HTTPS, მობილური ადაპტაცია, Open Graph, სტრუქტურირებული მონაცემები და ინდექსაცია.',
            'Получите BEQSON Score, ключевые SEO-проблемы и план действий.':'მიიღეთ BEQSON Score, ძირითადი SEO პრობლემები და სამოქმედო გეგმა.',
            '← На сайт':'← საიტზე დაბრუნება',
            'Бесплатный SEO-аудит сайта':'საიტის უფასო SEO აუდიტი',
            'Введите адрес сайта. Мы проверим ключевые технические SEO-факторы и покажем BEQSON Score от 0 до 100 — без регистрации.':'შეიყვანეთ საიტის მისამართი. ჩვენ შევამოწმებთ ძირითად ტექნიკურ SEO ფაქტორებს და გაჩვენებთ BEQSON Score-ს 0-დან 100-მდე — რეგისტრაციის გარეშე.',
            'Проверить сайт →':'საიტის შემოწმება →',
            'Экспресс-аудит проверяет текущую HTML-страницу и базовые SEO-настройки. Он не заменяет полный технический аудит.':'სწრაფი აუდიტი ამოწმებს მიმდინარე HTML გვერდს და ძირითად SEO პარამეტრებს. ის არ ცვლის სრულ ტექნიკურ აუდიტს.',
            'Оценка:':'შეფასება:',
            'Результат аудита':'აუდიტის შედეგი',
            'Ответ сервера':'სერვერის პასუხი',
            'Язык':'ენა',
            'Ключевые результаты':'ძირითადი შედეგები',
            'Показываем до трёх наиболее важных пунктов экспресс-аудита.':'ვაჩვენებთ სწრაფი აუდიტის მაქსიმუმ სამ ყველაზე მნიშვნელოვან შედეგს.',
            'Получить полный отчёт + план действий':'სრული ანგარიში + სამოქმედო გეგმა',
            'Оставьте контакт — полный список проверок и приоритетный план исправлений откроются сразу. Запрос сохранится в BEQSON CRM.':'დატოვეთ საკონტაქტო ინფორმაცია — შემოწმებების სრული სია და პრიორიტეტული სამოქმედო გეგმა მაშინვე გაიხსნება. მოთხოვნა შეინახება BEQSON CRM-ში.',
            'БЕСПЛАТНО':'უფასოდ',
            'Ваше имя':'თქვენი სახელი',
            'Открыть полный отчёт →':'სრული ანგარიშის გახსნა →',
            'Согласен(на), что BEQSON сохранит указанный контакт и свяжется со мной по результатам аудита.':'ვეთანხმები, რომ BEQSON შეინახავს ჩემს საკონტაქტო ინფორმაციას და დამიკავშირდება აუდიტის შედეგებთან დაკავშირებით.',
            'Полный экспресс-отчёт':'სრული სწრაფი ანგარიში',
            'Все базовые технические проверки, выполненные BEQSON Website Audit.':'BEQSON Website Audit-ის მიერ შესრულებული ყველა ძირითადი ტექნიკური შემოწმება.',
            'Приоритетный план действий':'პრიორიტეტული სამოქმედო გეგმა',
            'ГОТОВЫЙ ОТЧЁТ':'ანგარიში მზადაა',
            'Скачать PDF-аудит BEQSON':'BEQSON PDF-აუდიტის ჩამოტვირთვა',
            'Сохраните аудит, отправьте партнёру или команде. В PDF: логотип BEQSON, адрес сайта, SEO Score, найденные проблемы, базовые проверки и приоритетный план работ.':'შეინახეთ აუდიტი და გაუზიარეთ პარტნიორს ან გუნდს. PDF-ში შედის BEQSON-ის ბრენდინგი, საიტის მისამართი, SEO Score, აღმოჩენილი პრობლემები, ძირითადი შემოწმებები და პრიორიტეტული სამოქმედო გეგმა.',
            'Скачать PDF-аудит ↓':'PDF-აუდიტის ჩამოტვირთვა ↓',
            'Фирменный отчёт':'ბრენდირებული ანგარიში',
            'Удобно переслать':'მარტივი გასაზიარებლად',
            'План исправлений':'გამოსწორების გეგმა',
            'Ключевые проблемы':'ძირითადი პრობლემები',
            'Отчёт будет сформирован после аудита.':'ანგარიში აუდიტის შემდეგ შეიქმნება.',
            'Хотите исправить найденное?':'გსურთ აღმოჩენილი პრობლემების გამოსწორება?',
            'BEQSON может взять техническое SEO, структуру сайта и систему привлечения клиентов под ключ.':'BEQSON-ს შეუძლია სრულად აიღოს ტექნიკური SEO, საიტის სტრუქტურა და კლიენტების მოზიდვის სისტემა.',
            'Выберите удобный канал связи:':'აირჩიეთ თქვენთვის მოსახერხებელი საკონტაქტო არხი:',
            '© BEQSON Digital Studio · Экспресс-аудит носит диагностический характер':'© BEQSON Digital Studio · სწრაფ აუდიტს დიაგნოსტიკური დანიშნულება აქვს',
            'Готовим отчёт…':'ვამზადებთ ანგარიშს…',
            'Формируем PDF…':'ვქმნით PDF-ს…',
        },
    },
}

LABELS = {
    'en': {'https':'HTTPS','status':'HTTP status','title':'Title','description':'Meta description','h1':'H1','viewport':'Mobile viewport','canonical':'Canonical URL','lang':'Page language','og':'Open Graph','schema':'Structured data','indexable':'Indexing'},
    'ka': {'https':'HTTPS','status':'HTTP სტატუსი','title':'Title','description':'Meta description','h1':'H1','viewport':'მობილური viewport','canonical':'Canonical URL','lang':'გვერდის ენა','og':'Open Graph','schema':'სტრუქტურირებული მონაცემები','indexable':'ინდექსაცია'},
}

ACTIONS = {
    'en': {
        'https':'Enable HTTPS and configure one secure canonical website address.',
        'status':'Check page availability, redirects and the server HTTP response.',
        'title':'Improve the Title around the target search intent and a sensible length.',
        'description':'Rewrite the meta description with a clear offer, key message and suitable length.',
        'h1':'Check the main H1: one clear heading that matches the page topic.',
        'viewport':'Add a correct mobile viewport and verify the page on smartphones.',
        'canonical':'Set the canonical URL and eliminate competing duplicate pages.',
        'lang':'Set the correct lang attribute for the page language.',
        'og':'Add Open Graph so shared links look professional in social networks and messengers.',
        'schema':'Add relevant Schema.org JSON-LD structured data.',
        'indexable':'Remove accidental noindex rules and verify indexing settings.',
    },
    'ka': {
        'https':'ჩართეთ HTTPS და დააყენეთ საიტის ერთი უსაფრთხო ძირითადი მისამართი.',
        'status':'შეამოწმეთ გვერდის ხელმისაწვდომობა, გადამისამართებები და სერვერის HTTP პასუხი.',
        'title':'გააუმჯობესეთ Title სამიზნე საძიებო მოთხოვნისა და ოპტიმალური სიგრძის მიხედვით.',
        'description':'გადააკეთეთ meta description: მკაფიო შეთავაზება, მთავარი აზრი და შესაბამისი სიგრძე.',
        'h1':'შეამოწმეთ მთავარი H1: ერთი მკაფიო სათაური, რომელიც შეესაბამება გვერდის თემას.',
        'viewport':'დაამატეთ სწორი mobile viewport და შეამოწმეთ გვერდი სმარტფონებზე.',
        'canonical':'მიუთითეთ canonical URL და გამორიცხეთ კონკურენტი დუბლირებული გვერდები.',
        'lang':'მიუთითეთ გვერდის ენის შესაბამისი lang ატრიბუტი.',
        'og':'დაამატეთ Open Graph, რათა გაზიარებული ბმულები პროფესიონალურად გამოჩნდეს სოციალურ ქსელებსა და მესენჯერებში.',
        'schema':'დაამატეთ შესაბამისი Schema.org JSON-LD სტრუქტურირებული მონაცემები.',
        'indexable':'წაშალეთ შემთხვევითი noindex და გადაამოწმეთ ინდექსაციის წესები.',
    },
}

ERRORS = {
    'en': {
        'url_required':'Enter a website address.','unsupported_protocol':'Only HTTP/HTTPS are supported.','credentials_not_allowed':'URLs with usernames or passwords are not supported.','unsafe_host':'This address cannot be audited.','invalid_host':'Check the website address.','unsafe_redirect':'The site redirected to an unavailable address.','page_too_large':'The page is too large for the express audit.','not_html':'No HTML page was found at this address.','fallback':'We could not audit the website. Try again or check the address.'
    },
    'ka': {
        'url_required':'შეიყვანეთ საიტის მისამართი.','unsupported_protocol':'მხარდაჭერილია მხოლოდ HTTP/HTTPS.','credentials_not_allowed':'ლოგინით ან პაროლით URL არ არის მხარდაჭერილი.','unsafe_host':'ამ მისამართის შემოწმება შეუძლებელია.','invalid_host':'გადაამოწმეთ საიტის მისამართი.','unsafe_redirect':'საიტმა გადამისამართება მიუწვდომელ მისამართზე გააკეთა.','page_too_large':'გვერდი ზედმეტად დიდია სწრაფი აუდიტისთვის.','not_html':'ამ მისამართზე HTML გვერდი ვერ მოიძებნა.','fallback':'საიტის შემოწმება ვერ მოხერხდა. სცადეთ ხელახლა ან გადაამოწმეთ მისამართი.'
    },
}

DYN = {
    'en': {
        'preview_bad':'What should be improved','preview_bad_sub':'Items needing attention: {n}. We show the most important ones here — the full report is below.','gate_bad':'Leave your contact details — we’ll unlock the full checklist and priority fix plan. The request will be saved automatically in BEQSON CRM.','preview_ok':'Core checks passed','preview_ok_sub':'No critical issues were found in the express check. You can unlock the full report and next-level recommendations below.','gate_ok':'Leave your contact details — we’ll unlock the full report and a deeper SEO plan covering speed, semantics, content and local visibility.','first_audit':'Run a website audit first.','consent':'Please confirm that we may contact you about the audit results.','lead_error':'We could not open the full report. Check your details and try again.','success':'✓ Full report unlocked. Your request has been saved in BEQSON CRM.','package':'Recommended package','cw_title':'Core Web Vitals','cw_text':'Run a separate LCP, INP and CLS check on key pages.','sem_title':'Semantics and content','sem_text':'Review search queries, landing-page structure and search intent alignment.','local_title':'Local visibility','local_text':'Review Google/Yandex profiles, NAP data, reviews and local landing pages.','contact':'Hello! I ran a BEQSON SEO audit for {host} and would like to discuss the fixes.','email_subject':'BEQSON SEO audit — {host}','pdf_fix':'fix','pdf_good':'✓ No critical issues were found in the core technical checks. Below is the next-level SEO action plan.','status_ok':'HTTP response is healthy.','status_bad':'The HTTP response needs attention.','yes':'Configured correctly.','no':'Missing or needs attention.','length':'Length: {n} characters.'
    },
    'ka': {
        'preview_bad':'რისი გაუმჯობესებაა საჭირო','preview_bad_sub':'ყურადღებას საჭიროებს {n} პუნქტი. აქ ვაჩვენებთ ყველაზე მნიშვნელოვანს — სრული ანგარიში ქვემოთაა.','gate_bad':'დატოვეთ საკონტაქტო ინფორმაცია — გავხსნით შემოწმებების სრულ სიასა და პრიორიტეტულ გამოსწორების გეგმას. მოთხოვნა ავტომატურად შეინახება BEQSON CRM-ში.','preview_ok':'ძირითადი შემოწმებები გავლილია','preview_ok_sub':'სწრაფ შემოწმებაში კრიტიკული პრობლემები ვერ მოიძებნა. სრული ანგარიში და შემდეგი დონის რეკომენდაციები შეგიძლიათ ქვემოთ გახსნათ.','gate_ok':'დატოვეთ საკონტაქტო ინფორმაცია — გავხსნით სრულ ანგარიშსა და უფრო ღრმა SEO გეგმას: სიჩქარე, სემანტიკა, კონტენტი და ლოკალური ხილვადობა.','first_audit':'ჯერ გაუშვით საიტის აუდიტი.','consent':'დაადასტურეთ თანხმობა, რომ აუდიტის შედეგებთან დაკავშირებით დაგიკავშირდეთ.','lead_error':'სრული ანგარიშის გახსნა ვერ მოხერხდა. გადაამოწმეთ მონაცემები და სცადეთ ხელახლა.','success':'✓ სრული ანგარიში გახსნილია. მოთხოვნა შენახულია BEQSON CRM-ში.','package':'რეკომენდებული პაკეტი','cw_title':'Core Web Vitals','cw_text':'ძირითად გვერდებზე ცალკე გაზომეთ LCP, INP და CLS.','sem_title':'სემანტიკა და კონტენტი','sem_text':'შეამოწმეთ საძიებო მოთხოვნები, სადესანტო გვერდების სტრუქტურა და ძიების მიზანთან შესაბამისობა.','local_title':'ლოკალური ხილვადობა','local_text':'შეამოწმეთ Google/Yandex პროფილები, NAP მონაცემები, შეფასებები და ლოკალური სადესანტო გვერდები.','contact':'გამარჯობა! BEQSON-ზე ჩავატარე {host}-ის SEO აუდიტი და მსურს გამოსწორებების განხილვა.','email_subject':'BEQSON SEO აუდიტი — {host}','pdf_fix':'გამოსასწორებელია','pdf_good':'✓ ძირითადი ტექნიკური შემოწმებების მიხედვით კრიტიკული პრობლემები ვერ მოიძებნა. ქვემოთ მოცემულია შემდეგი დონის SEO სამოქმედო გეგმა.','status_ok':'HTTP პასუხი გამართულია.','status_bad':'HTTP პასუხი ყურადღებას საჭიროებს.','yes':'სწორად არის კონფიგურირებული.','no':'არ არის ან ყურადღებას საჭიროებს.','length':'სიგრძე: {n} სიმბოლო.'
    },
}


def js_obj(mapping):
    parts = []
    for k, v in mapping.items():
        v = v.replace('\\', '\\\\').replace("'", "\\'")
        parts.append(f"'{k}':'{v}'")
    return '{' + ','.join(parts) + '}'


def add_hreflang(s, canonical):
    block = (
        f'<link rel="canonical" href="{canonical}">'
        '<link rel="alternate" hreflang="ru" href="https://beqson.com/ru/audit/">'
        '<link rel="alternate" hreflang="ka" href="https://beqson.com/ka/audit/">'
        '<link rel="alternate" hreflang="en" href="https://beqson.com/en/audit/">'
        '<link rel="alternate" hreflang="x-default" href="https://beqson.com/ka/audit/">'
    )
    return re.sub(r'<link rel="canonical" href="[^"]+">(?:<link rel="alternate" hreflang="(?:ru|ka|en|x-default)" href="[^"]+">)*', block, s, count=1)


def localize_js(s, lang):
    labels = js_obj(LABELS[lang])
    actions = js_obj(ACTIONS[lang])
    err_map = dict(ERRORS[lang]); fallback = err_map.pop('fallback')
    errors = js_obj(err_map)
    d = DYN[lang]

    error_fn = "function errorText(code){const map=" + errors + ";return map[code]||'" + fallback.replace("'", "\\'") + "'}"
    s = re.sub(r'function errorText\(code\)\{.*?\}\nfunction checkHtml', error_fn + '\nfunction checkHtml', s, count=1, flags=re.S)

    helper = (
        "const AUDIT_LABELS=" + labels + ";\n"
        "function labelFor(c){return AUDIT_LABELS[c.id]||c.label||c.id}\n"
        "function detailFor(c){const ok=Number(c.points)===Number(c.max);"
        + "if(c.id==='status')return ok?'" + d['status_ok'].replace("'", "\\'") + "':'" + d['status_bad'].replace("'", "\\'") + "';"
        + "if(c.id==='title'||c.id==='description'){const m=String(c.detail||'').match(/\\d+/);if(m)return '" + d['length'].replace("'", "\\'") + "'.replace('{n}',m[0])}"
        + "return ok?'" + d['yes'].replace("'", "\\'") + "':'" + d['no'].replace("'", "\\'") + "'}\n"
        + "function checkHtml(c){const cls=c.points===c.max?'ok':(c.points>0?'partial':'bad'),ico=cls==='ok'?'✓':(cls==='partial'?'!':'×');return '<div class=\"check '+cls+'\"><div class=\"ico\">'+ico+'</div><div><strong>'+esc(labelFor(c))+'</strong><div class=\"detail\">'+esc(detailFor(c))+'</div></div><div class=\"pts\">'+c.points+'/'+c.max+'</div></div>'}"
    )
    s = re.sub(r'function checkHtml\(c\)\{.*?\}\nfunction issues', helper + '\nfunction issues', s, count=1, flags=re.S)

    action_fn = "function actionFor(c){const actions=" + actions + ";return actions[c.id]||labelFor(c)}"
    s = re.sub(r'function actionFor\(c\)\{.*?\}\nfunction planItems', action_fn + '\nfunction planItems', s, count=1, flags=re.S)

    plan_fn = (
        "function planItems(d){const bad=issues(d);if(bad.length)return bad.map(c=>({title:labelFor(c),text:actionFor(c)}));return["
        + "{title:'" + d['cw_title'].replace("'", "\\'") + "',text:'" + d['cw_text'].replace("'", "\\'") + "'},"
        + "{title:'" + d['sem_title'].replace("'", "\\'") + "',text:'" + d['sem_text'].replace("'", "\\'") + "'},"
        + "{title:'" + d['local_title'].replace("'", "\\'") + "',text:'" + d['local_text'].replace("'", "\\'") + "'}]}"
    )
    s = re.sub(r'function planItems\(d\)\{.*?\}\nfunction updateContactLinks', plan_fn + '\nfunction updateContactLinks', s, count=1, flags=re.S)

    contact = d['contact'].replace("'", "\\'")
    subject = d['email_subject'].replace("'", "\\'")
    contact_fn = (
        "function updateContactLinks(d){const site=d?.final_url||d?.url||'',host=d?.host||site,msg='" + contact + "'.replace('{host}',host);"
        "$('ctaWhatsapp').href='https://wa.me/995551739333?text='+encodeURIComponent(msg);"
        "$('ctaTelegram').href='https://t.me/digital_studio_beqson';"
        "$('ctaEmail').href='mailto:digitalstudiobeqson@gmail.com?subject='+encodeURIComponent('" + subject + "'.replace('{host}',host))+'&body='+encodeURIComponent(msg+'\\n\\n'+site)}"
    )
    s = re.sub(r'function updateContactLinks\(d\)\{.*?\}\nform.addEventListener', contact_fn + '\nform.addEventListener', s, count=1, flags=re.S)

    replacements = {
        "$('previewTitle').textContent='Что стоит улучшить'": "$('previewTitle').textContent='" + d['preview_bad'].replace("'", "\\'") + "'",
        "$('previewSub').textContent=`Найдено пунктов для внимания: ${bad.length}. Показываем самые важные — полный отчёт ниже.`": "$('previewSub').textContent='" + d['preview_bad_sub'].replace("'", "\\'") + "'.replace('{n}',bad.length)",
        "$('gateText').textContent='Оставьте контакт — откроем полный список проверок и приоритетный план исправлений. Запрос автоматически сохранится в BEQSON CRM.'": "$('gateText').textContent='" + d['gate_bad'].replace("'", "\\'") + "'",
        "$('previewTitle').textContent='Базовые проверки пройдены'": "$('previewTitle').textContent='" + d['preview_ok'].replace("'", "\\'") + "'",
        "$('previewSub').textContent='Критичных проблем в экспресс-проверке не найдено. Полный отчёт и следующий уровень рекомендаций можно открыть ниже.'": "$('previewSub').textContent='" + d['preview_ok_sub'].replace("'", "\\'") + "'",
        "$('gateText').textContent='Оставьте контакт — откроем полный отчёт и план более глубокого SEO-разбора: скорость, семантика, контент и локальное продвижение.'": "$('gateText').textContent='" + d['gate_ok'].replace("'", "\\'") + "'",
        "ge.textContent='Сначала запустите аудит сайта.'": "ge.textContent='" + d['first_audit'].replace("'", "\\'") + "'",
        "ge.textContent='Нужно подтвердить согласие на связь по результатам аудита.'": "ge.textContent='" + d['consent'].replace("'", "\\'") + "'",
        "ge.textContent='Не удалось открыть полный отчёт. Проверьте данные и попробуйте ещё раз.'": "ge.textContent='" + d['lead_error'].replace("'", "\\'") + "'",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)

    s = re.sub(
        r"\$\('gateSuccess'\)\.innerHTML=`✓ Полный отчёт открыт\. Запрос сохранён в BEQSON CRM\.<br><span class=\"packagePill\">Рекомендованный пакет: \$\{esc\(pkg\)\}</span>`",
        "$('gateSuccess').innerHTML='" + d['success'].replace("'", "\\'") + "<br><span class=\"packagePill\">" + d['package'].replace("'", "\\'") + ": '+esc(pkg)+'</span>'",
        s,
        count=1,
    )

    # Localize dynamic labels/details used by the generated PDF.
    s = s.replace('${esc(c.label)}', '${esc(labelFor(c))}')
    s = s.replace('${esc(c.detail)}', '${esc(detailFor(c))}')
    s = s.replace('>исправить</div>', '>' + d['pdf_fix'] + '</div>')
    s = s.replace('✓ По базовым техническим проверкам критичных проблем не выявлено. Ниже — план следующего уровня SEO-работ.', d['pdf_good'])
    s = s.replace("new Date().toLocaleDateString('ru-RU'", "new Date().toLocaleDateString('en-GB'" if lang == 'en' else "new Date().toLocaleDateString('ka-GE'")
    return s


for lang, cfg in PAGES.items():
    s = BASE
    s = re.sub(r'<html lang="[^"]+">', f'<html lang="{cfg["html_lang"]}">', s, count=1)
    s = add_hreflang(s, cfg['canonical'])
    s = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{cfg["canonical"]}">', s, count=1)
    s = s.replace('href="/ru/" class="brand"', f'href="{cfg["home"]}" class="brand"', 1)
    s = s.replace('class="back" href="/ru/"', f'class="back" href="{cfg["home"]}"', 1)
    for old, new in cfg['repl'].items():
        s = s.replace(old, new)
    if lang != 'ru':
        s = localize_js(s, lang)
    cfg['path'].parent.mkdir(parents=True, exist_ok=True)
    cfg['path'].write_text(s, encoding='utf-8')

# Homepage links should always keep the visitor in the same language.
for lang in ('ru', 'ka', 'en'):
    p = ROOT / f'{lang}/index.html'
    s = p.read_text(encoding='utf-8')
    s = s.replace('href="/audit/"', f'href="/{lang}/audit/"')
    p.write_text(s, encoding='utf-8')

# Add the three localized audit URLs to sitemap once.
sitemap = ROOT / 'sitemap.xml'
if sitemap.exists():
    s = sitemap.read_text(encoding='utf-8')
    urls = [f'https://beqson.com/{lang}/audit/' for lang in ('ru','ka','en')]
    missing = [u for u in urls if u not in s]
    if missing:
        block = ''.join(f'  <url><loc>{u}</loc></url>\n' for u in missing)
        s = s.replace('</urlset>', block + '</urlset>')
        sitemap.write_text(s, encoding='utf-8')

print('Localized audit pages built successfully.')
