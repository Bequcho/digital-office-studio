from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]

CFG = {
    'en': {
        'path': ROOT/'en/lawyers/index.html',
        'url': 'https://beqson.com/en/lawyers/',
        'title': 'Law Firm Website Design & SEO for Lawyers | BEQSON',
        'desc': 'Website design for lawyers and law firms: multilingual sites, practice-area pages, local SEO, lead capture and CRM-ready enquiry flows by BEQSON.',
        'og_locale': 'en_US',
        'og_image': 'https://beqson.com/assets/concepts/en/lawyers-og.jpg',
        'alt': 'Law firm website design by BEQSON',
        'h1_old': 'A website that supports<br>your reputation.',
        'h1_new': 'Law firm website design<br>that builds trust and enquiries.',
        'lead_old': 'A refined presence for an independent lawyer or legal practice. Help visitors understand your expertise and take the first step towards a consultation.',
        'lead_new': 'Websites for lawyers, attorneys and law firms with clear practice areas, multilingual structure, local SEO foundations and a simple path from Google search to enquiry.',
        'breadcrumb_home': 'Home', 'breadcrumb_industry': 'Lawyers',
        'service_name': 'Law firm website design and SEO for lawyers',
        'service_type': 'Law firm website design, development and SEO',
        'faq': [
            ('What should a good law firm website include?', 'Clear practice areas, lawyer profiles, real credentials, contact options, working languages, location information and focused pages for the services people actually search for.'),
            ('Can BEQSON build a multilingual law firm website?', 'Yes. We can structure the website in multiple languages and connect localized pages with proper language signals so visitors and search engines reach the right version.'),
            ('Do you also help with SEO for lawyers?', 'Yes. We build search-ready page structure, metadata, internal links, local-search foundations and dedicated practice-area pages. Rankings are never guaranteed.'),
            ('How much does a lawyer website cost?', 'Our international launch pricing starts from $149 for a focused starter website. The final price depends on page count, languages, SEO scope, CRM and other features.')
        ],
        'section': '''<!-- LAWYERS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">LAW FIRM WEBSITE DESIGN</p><h2>Built for how legal clients<br>actually choose a lawyer.</h2></div><p>A legal website has to do more than look premium. It should explain what you handle, establish credibility quickly and make the next step obvious on desktop and mobile.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Practice-area SEO pages</h3><p>Separate pages for civil, criminal, administrative, family, immigration or other services help people and search engines understand your expertise.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Trust-first presentation</h3><p>Real experience, education, languages, office details and authentic photography presented clearly without exaggerated promises.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Multilingual structure</h3><p>English, Georgian, Russian or other language versions can be organized for both users and international search visibility.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Enquiries & CRM</h3><p>WhatsApp, Telegram, email, forms, analytics and CRM-ready lead capture can turn the website into a working client-acquisition system.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">REAL PROJECT</p><h2>Levani Law — a live multilingual legal website.</h2><p class="lead">We created a real website for lawyer Levani Khelkhelauri with Georgian, Russian and English versions, clear legal-service structure and local-search foundations.</p><a class="text-link" href="https://levanilaw.ge" target="_blank" rel="noopener">View live project <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>Three-language website architecture</p></li><li><span>02</span><p>Civil, administrative and criminal-law positioning</p></li><li><span>03</span><p>SEO, Google visibility and direct enquiry paths</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">LAUNCH PRICING</p><h2>Start small.<br>Grow when it works.</h2></div><p>International launch pricing starts from <strong>$149</strong>. Use our free tools before contacting us: audit an existing site or estimate a new project.</p></div><div class="features-grid"><article class="feature-card"><h3>Free SEO Audit</h3><p>Get an SEO Score, technical checks and a priority action plan.</p><a class="text-link" href="/en/audit/">Run audit →</a></article><article class="feature-card"><h3>Website Cost Calculator</h3><p>Answer five questions and get an estimated price range instantly.</p><a class="text-link" href="/en/calculator/">Calculate cost →</a></article><article class="feature-card"><h3>Start from $149</h3><p>Focused starter websites for early clients during our launch period.</p><a class="text-link" href="#contact">Discuss project →</a></article><article class="feature-card"><h3>Multilingual & scalable</h3><p>Add SEO pages, CRM, analytics and extra languages as the project grows.</p><a class="text-link" href="/en/tools/">Explore free tools →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Law firm website<br>questions.</h2></div><p>Practical answers before you start a legal website project.</p></div><div class="features-grid"><article class="feature-card"><h3>What should a good law firm website include?</h3><p>Clear practice areas, lawyer profiles, real credentials, contact options, working languages, location information and focused service pages.</p></article><article class="feature-card"><h3>Can you build a multilingual law firm website?</h3><p>Yes. We can structure localized versions and connect them correctly for visitors and search engines.</p></article><article class="feature-card"><h3>Do you also help with SEO for lawyers?</h3><p>Yes — technical foundations, metadata, internal links, local search and practice-area pages. We never promise specific rankings.</p></article><article class="feature-card"><h3>How much does it cost?</h3><p>International launch pricing starts from $149. Scope, languages, SEO, CRM and page count determine the final price.</p></article></div></div></section>
<!-- /LAWYERS_SEO_V1 -->'''
    },
    'ru': {
        'path': ROOT/'ru/lawyers/index.html',
        'url': 'https://beqson.com/ru/lawyers/',
        'title': 'Создание сайтов для адвокатов и юристов — BEQSON',
        'desc': 'Создание сайтов для адвокатов и юридических фирм: услуги, мультиязычность, локальное SEO, формы заявок и CRM. Стартовые цены BEQSON от 9 900 ₽.',
        'og_locale': 'ru_RU',
        'og_image': 'https://beqson.com/assets/concepts/ru/lawyers-og.jpg',
        'alt': 'Создание сайтов для адвокатов и юристов — BEQSON',
        'h1_old': 'Сайт, который говорит<br>в пользу вашей репутации.',
        'h1_new': 'Создание сайтов<br>для адвокатов и юристов.',
        'lead_old': 'Сдержанная премиальная подача для адвоката или юридической практики. Помогаем посетителю понять вашу специализацию и сделать первый шаг к консультации.',
        'lead_new': 'Сайты для адвокатов и юридических фирм: направления практики, мультиязычность, локальное SEO и понятный путь от поиска в Google до обращения за консультацией.',
        'breadcrumb_home': 'Главная', 'breadcrumb_industry': 'Адвокаты',
        'service_name': 'Создание сайтов и SEO для адвокатов и юристов',
        'service_type': 'Создание, разработка и SEO сайтов для адвокатов',
        'faq': [
            ('Что должно быть на хорошем сайте адвоката?', 'Направления практики, профиль адвоката, реальные сведения об опыте, рабочие языки, контакты, адрес и отдельные страницы под юридические услуги, которые ищут клиенты.'),
            ('Можно ли сделать сайт юридической фирмы на нескольких языках?', 'Да. Мы можем организовать русскую, грузинскую, английскую и другие языковые версии и корректно связать их для пользователей и поисковых систем.'),
            ('Вы занимаетесь SEO для адвокатов?', 'Да. Настраиваем техническую основу, метаданные, внутренние ссылки, локальный поиск и страницы по направлениям практики. Конкретные позиции в поиске не гарантируем.'),
            ('Сколько стоит сайт для адвоката?', 'На старте BEQSON стоимость простого сайта начинается от 9 900 ₽. Итоговая цена зависит от числа страниц, языков, SEO, CRM и дополнительных функций.')
        ],
        'section': '''<!-- LAWYERS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">САЙТ ДЛЯ АДВОКАТА</p><h2>Сделан под то,<br>как клиент выбирает юриста.</h2></div><p>Юридическому сайту недостаточно выглядеть дорого. Он должен быстро объяснить специализацию, вызвать доверие и привести человека к понятному следующему шагу.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>SEO-страницы услуг</h3><p>Отдельные страницы под гражданские, уголовные, административные, семейные и другие направления помогают и клиентам, и поисковикам понять специализацию.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Доверие без громких обещаний</h3><p>Опыт, образование, языки, офис и настоящие фотографии — аккуратно и без обещаний результата дела.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Несколько языков</h3><p>Русская, грузинская, английская и другие версии можно правильно организовать для пользователей и международного поиска.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Заявки и CRM</h3><p>WhatsApp, Telegram, email, формы, аналитика и CRM превращают сайт в рабочую систему привлечения клиентов.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">РЕАЛЬНЫЙ ПРОЕКТ</p><h2>Levani Law — действующий сайт адвоката.</h2><p class="lead">Мы создали сайт адвоката Levani Khelkhelauri на грузинском, русском и английском языках, структурировали юридические услуги и подготовили основу для локального поиска.</p><a class="text-link" href="https://levanilaw.ge" target="_blank" rel="noopener">Открыть сайт <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>Три языковые версии сайта</p></li><li><span>02</span><p>Гражданское, административное и уголовное право</p></li><li><span>03</span><p>SEO, Google и удобные точки обращения</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">СТАРТОВЫЕ ЦЕНЫ</p><h2>Начните недорого.<br>Расширяйте по мере роста.</h2></div><p>На старте сайт для адвоката можно запустить <strong>от 9 900 ₽</strong>. До обращения к нам можно бесплатно проверить текущий сайт или рассчитать новый проект.</p></div><div class="features-grid"><article class="feature-card"><h3>Бесплатный SEO-аудит</h3><p>SEO Score, технические проверки и приоритетный план действий.</p><a class="text-link" href="/ru/audit/">Проверить сайт →</a></article><article class="feature-card"><h3>Калькулятор стоимости</h3><p>Ответьте на пять вопросов и сразу получите ориентировочный диапазон цены.</p><a class="text-link" href="/ru/calculator/">Рассчитать стоимость →</a></article><article class="feature-card"><h3>От 9 900 ₽</h3><p>Стартовая цена на компактный сайт в период запуска BEQSON.</p><a class="text-link" href="#contact">Обсудить проект →</a></article><article class="feature-card"><h3>Можно расширять</h3><p>Добавим SEO-страницы, CRM, аналитику и дополнительные языки по мере роста.</p><a class="text-link" href="/ru/tools/">Все бесплатные инструменты →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Вопросы о сайте<br>для адвоката.</h2></div><p>Коротко о том, что обычно важно перед запуском юридического сайта.</p></div><div class="features-grid"><article class="feature-card"><h3>Что должно быть на хорошем сайте адвоката?</h3><p>Направления практики, профиль адвоката, реальные сведения об опыте, языки, контакты, адрес и отдельные страницы услуг.</p></article><article class="feature-card"><h3>Можно сделать сайт на нескольких языках?</h3><p>Да. Организуем локализованные версии и правильно свяжем их для посетителей и поисковиков.</p></article><article class="feature-card"><h3>Вы занимаетесь SEO для адвокатов?</h3><p>Да — техническая база, метаданные, локальный поиск, внутренние ссылки и страницы услуг. Без обещаний конкретных позиций.</p></article><article class="feature-card"><h3>Сколько стоит сайт?</h3><p>Стартовая цена — от 9 900 ₽. Итог зависит от количества страниц, языков, SEO, CRM и функций.</p></article></div></div></section>
<!-- /LAWYERS_SEO_V1 -->'''
    },
    'ka': {
        'path': ROOT/'ka/lawyers/index.html',
        'url': 'https://beqson.com/ka/lawyers/',
        'title': 'ვებსაიტების შექმნა ადვოკატებისთვის — BEQSON',
        'desc': 'ვებსაიტების შექმნა ადვოკატებისა და იურიდიული კომპანიებისთვის: მრავალენოვანი საიტი, ლოკალური SEO, სერვისების გვერდები, ლიდები და CRM. ფასი 299 ₾-დან.',
        'og_locale': 'ka_GE',
        'og_image': 'https://beqson.com/assets/concepts/ka/lawyers-og.jpg',
        'alt': 'ვებსაიტების შექმნა ადვოკატებისთვის — BEQSON',
        'h1_old': 'საიტი, რომელიც<br>თქვენს რეპუტაციას აძლიერებს.',
        'h1_new': 'ვებსაიტების შექმნა<br>ადვოკატებისთვის.',
        'lead_old': 'დახვეწილი პრეზენტაცია ადვოკატის ან იურიდიული პრაქტიკისთვის. დამთვალიერებელს ვეხმარებით გაიგოს თქვენი სპეციალიზაცია და მარტივად დაგიკავშირდეთ.',
        'lead_new': 'ვებსაიტები ადვოკატებისა და იურიდიული კომპანიებისთვის — პრაქტიკის მიმართულებებით, მრავალენოვანი სტრუქტურით, ლოკალური SEO-თი და მარტივი გზით Google-იდან მომართვამდე.',
        'breadcrumb_home': 'მთავარი', 'breadcrumb_industry': 'ადვოკატები',
        'service_name': 'ვებსაიტების შექმნა და SEO ადვოკატებისთვის',
        'service_type': 'ადვოკატებისთვის ვებსაიტის შექმნა, განვითარება და SEO',
        'faq': [
            ('რა უნდა ჰქონდეს კარგ ადვოკატის ვებსაიტს?', 'პრაქტიკის მიმართულებები, ადვოკატის პროფილი, რეალური გამოცდილება, სამუშაო ენები, საკონტაქტო ინფორმაცია, მისამართი და ცალკე გვერდები იმ იურიდიული სერვისებისთვის, რომლებსაც კლიენტები ეძებენ.'),
            ('შესაძლებელია მრავალენოვანი იურიდიული საიტის შექმნა?', 'დიახ. შეგვიძლია ქართული, რუსული, ინგლისური და სხვა ვერსიების სწორად ორგანიზება და ერთმანეთთან დაკავშირება მომხმარებლებისა და საძიებო სისტემებისთვის.'),
            ('აკეთებთ SEO-ს ადვოკატებისთვის?', 'დიახ. ვამზადებთ ტექნიკურ საფუძველს, მეტამონაცემებს, შიდა ბმულებს, ლოკალურ ძიებას და პრაქტიკის მიმართულებების გვერდებს. კონკრეტულ პოზიციებს Google-ში არ ვპირდებით.'),
            ('რა ღირს ადვოკატის ვებსაიტი?', 'BEQSON-ის საწყისი ფასი კომპაქტური საიტისთვის 299 ₾-დან იწყება. საბოლოო ღირებულება დამოკიდებულია გვერდების რაოდენობაზე, ენებზე, SEO-ზე, CRM-სა და დამატებით ფუნქციებზე.')
        ],
        'section': '''<!-- LAWYERS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">ადვოკატის ვებსაიტი</p><h2>შექმნილი იმისთვის,<br>როგორ არჩევს კლიენტი იურისტს.</h2></div><p>იურიდიული საიტი მხოლოდ ლამაზი არ უნდა იყოს. მან სწრაფად უნდა აჩვენოს სპეციალიზაცია, შექმნას ნდობა და მომხმარებელს მარტივი შემდეგი ნაბიჯი შესთავაზოს.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>SEO გვერდები სერვისებისთვის</h3><p>ცალკე გვერდები სამოქალაქო, სისხლის, ადმინისტრაციული, საოჯახო და სხვა მიმართულებებისთვის ეხმარება როგორც კლიენტს, ისე საძიებო სისტემას.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>ნდობა ზედმეტი დაპირებების გარეშე</h3><p>გამოცდილება, განათლება, სამუშაო ენები, ოფისი და რეალური ფოტოები — მკაფიოდ და საქმის შედეგის დაპირების გარეშე.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>მრავალენოვანი სტრუქტურა</h3><p>ქართული, რუსული, ინგლისური და სხვა ვერსიები შეიძლება სწორად მოეწყოს ადგილობრივი და საერთაშორისო ძიებისთვის.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>მომართვები და CRM</h3><p>WhatsApp, Telegram, email, ფორმები, ანალიტიკა და CRM ვებსაიტს კლიენტების მოზიდვის სამუშაო სისტემად აქცევს.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">რეალური პროექტი</p><h2>Levani Law — მოქმედი მრავალენოვანი იურიდიული საიტი.</h2><p class="lead">ადვოკატ Levani Khelkhelauri-სთვის შევქმენით ქართული, რუსული და ინგლისური ვერსიები, იურიდიული სერვისების მკაფიო სტრუქტურა და ლოკალური ძიების საფუძველი.</p><a class="text-link" href="https://levanilaw.ge" target="_blank" rel="noopener">საიტის ნახვა <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>სამენოვანი ვებსაიტის არქიტექტურა</p></li><li><span>02</span><p>სამოქალაქო, ადმინისტრაციული და სისხლის სამართლის მიმართულებები</p></li><li><span>03</span><p>SEO, Google და პირდაპირი საკონტაქტო გზები</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">საწყისი ფასები</p><h2>დაიწყეთ ხელმისაწვდომად.<br>გაზარდეთ ეტაპობრივად.</h2></div><p>BEQSON-ის გაშვების პერიოდში ადვოკატის საიტის ფასი იწყება <strong>299 ₾-დან</strong>. მანამდე შეგიძლიათ უფასოდ შეამოწმოთ არსებული საიტი ან გამოთვალოთ ახალი პროექტის ფასი.</p></div><div class="features-grid"><article class="feature-card"><h3>უფასო SEO აუდიტი</h3><p>SEO Score, ტექნიკური შემოწმება და პრიორიტეტული სამოქმედო გეგმა.</p><a class="text-link" href="/ka/audit/">საიტის შემოწმება →</a></article><article class="feature-card"><h3>ღირებულების კალკულატორი</h3><p>უპასუხეთ ხუთ კითხვას და მიიღეთ სავარაუდო ფასის დიაპაზონი.</p><a class="text-link" href="/ka/calculator/">ფასის გამოთვლა →</a></article><article class="feature-card"><h3>299 ₾-დან</h3><p>საწყისი ფასი კომპაქტური საიტისთვის BEQSON-ის გაშვების პერიოდში.</p><a class="text-link" href="#contact">პროექტის განხილვა →</a></article><article class="feature-card"><h3>მარტივად გასაფართოებელი</h3><p>შემდგომში დავამატებთ SEO გვერდებს, CRM-ს, ანალიტიკას და დამატებით ენებს.</p><a class="text-link" href="/ka/tools/">უფასო ინსტრუმენტები →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>კითხვები ადვოკატის<br>ვებსაიტზე.</h2></div><p>მოკლე პასუხები მთავარ საკითხებზე იურიდიული საიტის დაწყებამდე.</p></div><div class="features-grid"><article class="feature-card"><h3>რა უნდა ჰქონდეს კარგ ადვოკატის ვებსაიტს?</h3><p>პრაქტიკის მიმართულებები, ადვოკატის პროფილი, რეალური გამოცდილება, ენები, კონტაქტები, მისამართი და სერვისების ცალკე გვერდები.</p></article><article class="feature-card"><h3>შესაძლებელია მრავალენოვანი საიტი?</h3><p>დიახ. ლოკალიზებულ ვერსიებს სწორად დავაკავშირებთ მომხმარებლებისა და საძიებო სისტემებისთვის.</p></article><article class="feature-card"><h3>აკეთებთ SEO-ს ადვოკატებისთვის?</h3><p>დიახ — ტექნიკური საფუძველი, მეტამონაცემები, ლოკალური ძიება, შიდა ბმულები და სერვისების გვერდები. კონკრეტულ პოზიციებს არ ვპირდებით.</p></article><article class="feature-card"><h3>რა ღირს ვებსაიტი?</h3><p>საწყისი ფასი 299 ₾-დან. საბოლოო ღირებულება დამოკიდებულია გვერდებზე, ენებზე, SEO-ზე, CRM-სა და ფუნქციებზე.</p></article></div></div></section>
<!-- /LAWYERS_SEO_V1 -->'''
    }
}

def schema(c, lang):
    graph = [
        {'@type':'Organization','@id':'https://beqson.com/#organization','name':'BEQSON Digital Studio','url':'https://beqson.com/','logo':'https://beqson.com/assets/beqson-mark-v3.png','email':'digitalstudiobeqson@gmail.com','telephone':'+995551739333','sameAs':['https://t.me/digital_studio_beqson']},
        {'@type':'WebPage','@id':c['url']+'#webpage','url':c['url'],'name':c['title'],'description':c['desc'],'inLanguage':lang,'publisher':{'@id':'https://beqson.com/#organization'}},
        {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':c['breadcrumb_home'],'item':f'https://beqson.com/{lang}/'},{'@type':'ListItem','position':2,'name':c['breadcrumb_industry'],'item':c['url']}]},
        {'@type':'Service','name':c['service_name'],'description':c['desc'],'provider':{'@id':'https://beqson.com/#organization'},'url':c['url'],'serviceType':c['service_type'],'areaServed':'Worldwide'},
        {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in c['faq']]}
    ]
    return json.dumps({'@context':'https://schema.org','@graph':graph}, ensure_ascii=False, separators=(',',':'))

def set_meta(html, c, lang):
    html = re.sub(r'<title>.*?</title>', f'<title>{c["title"]}</title>', html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{c["desc"]}">', html, count=1)
    html = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', '<link rel="alternate" hreflang="x-default" href="https://beqson.com/en/lawyers/">', html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{c["title"]}">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{c["desc"]}">', html, count=1)
    html = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{c["alt"]}">', html, count=1)
    html = re.sub(r'<meta name="twitter:image:alt" content="[^"]*">', f'<meta name="twitter:image:alt" content="{c["alt"]}">', html, count=1)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">'+schema(c,lang)+'</script>', html, count=1, flags=re.S)
    return html

def patch(lang, c):
    p = c['path']
    html = p.read_text(encoding='utf-8')
    html = set_meta(html, c, lang)
    html = html.replace(c['h1_old'], c['h1_new'])
    html = html.replace(c['lead_old'], c['lead_new'])
    # Replace prior injected version if rerun; otherwise add after hero, before concept.
    html = re.sub(r'<!-- LAWYERS_SEO_V1 -->.*?<!-- /LAWYERS_SEO_V1 -->', c['section'], html, flags=re.S)
    if '<!-- LAWYERS_SEO_V1 -->' not in html:
        marker = '<section class="section concept-section" id="concept">'
        html = html.replace(marker, c['section']+'\n'+marker, 1)
    p.write_text(html, encoding='utf-8')
    print('updated', p.relative_to(ROOT))

for lang,c in CFG.items():
    patch(lang,c)
