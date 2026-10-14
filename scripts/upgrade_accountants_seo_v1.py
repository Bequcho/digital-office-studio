from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]

CFG = {
    'en': {
        'path': ROOT/'en/accountants/index.html',
        'url': 'https://beqson.com/en/accountants/',
        'title': 'Accountant Website Design & SEO for Tax Advisers | BEQSON',
        'desc': 'Website design for accountants, bookkeeping firms and tax advisers: service pages, local SEO, B2B enquiries, multilingual content, analytics and CRM-ready lead capture.',
        'og_locale': 'en_US',
        'og_image': 'https://beqson.com/assets/concepts/en/accountants-og.jpg',
        'alt': 'Accountant and tax adviser website design by BEQSON',
        'h1': 'Accountant website design<br>built to win business trust.',
        'lead': 'Websites for accountants, bookkeeping firms and tax advisers with clear service pages, local SEO, B2B enquiry paths, multilingual content and CRM-ready lead capture.',
        'breadcrumb_home': 'Home', 'breadcrumb_industry': 'Accountants / tax advisers',
        'service_name': 'Accountant and tax adviser website design and SEO',
        'service_type': 'Accountant website design, development and SEO',
        'faq': [
            ('What should an accountant website include?', 'Clear service pages, industries or client types served, professional credentials where relevant, contact options, useful answers to common questions and a simple consultation request path.'),
            ('Can you create separate pages for bookkeeping and tax services?', 'Yes. Services such as bookkeeping, payroll, tax consulting, company setup support or reporting can each have focused pages for clearer search intent and stronger conversion.'),
            ('Do you provide SEO for accountants and tax advisers?', 'Yes. We can structure service and location pages, improve metadata and internal linking, and prepare the website for local and organic search. Specific rankings are never guaranteed.'),
            ('How much does an accountant website cost?', 'Our international launch pricing starts from $149 for a focused starter website. More services, languages, CRM, forms and advanced SEO increase the final scope.')
        ],
        'section': '''<!-- ACCOUNTANTS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">ACCOUNTANT WEBSITE DESIGN</p><h2>Make expertise easy to understand<br>before the first call.</h2></div><p>Accounting buyers look for clarity, trust and relevance. We structure your services so a business owner can quickly see what you handle, who you work with and how to start a conversation.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Service pages with search intent</h3><p>Bookkeeping, payroll, tax consulting, reporting and other services can each have focused pages instead of being buried in one generic list.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Trust for B2B buyers</h3><p>Explain your process, client types, experience and verified credentials in a calm professional structure built for business decision-makers.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Local & niche SEO</h3><p>Pages can target relevant services, locations and business audiences so search visitors land on a page that matches what they actually need.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Consultations, analytics & CRM</h3><p>Forms, WhatsApp, email, source tracking and CRM-ready enquiries make it easier to qualify and follow up with potential clients.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">SEARCH → SERVICE → CONSULTATION</p><h2>A clearer route from a business question<br>to a qualified enquiry.</h2><p class="lead">Build pages around the accounting and tax questions clients search for, then connect each service to one simple consultation action.</p></div><ol class="channel-list"><li><span>01</span><p>Focused pages for individual accounting and tax services</p></li><li><span>02</span><p>Local and industry-specific search entry points</p></li><li><span>03</span><p>Lead forms, source tracking and CRM-ready follow-up</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">LAUNCH PRICING</p><h2>Start with your core services.<br>Expand as the practice grows.</h2></div><p>International launch pricing starts from <strong>$149</strong>. Before contacting us, you can audit an existing website or estimate a new project for free.</p></div><div class="features-grid"><article class="feature-card"><h3>Free SEO Audit</h3><p>Check technical SEO, metadata and priority issues on an existing accounting website.</p><a class="text-link" href="/en/audit/">Run audit →</a></article><article class="feature-card"><h3>Website Cost Calculator</h3><p>Estimate pages, languages, SEO, CRM and lead-generation features.</p><a class="text-link" href="/en/calculator/">Calculate cost →</a></article><article class="feature-card"><h3>Start from $149</h3><p>Launch with the essential service pages and expand content or automation later.</p><a class="text-link" href="#contact">Discuss project →</a></article><article class="feature-card"><h3>Built for B2B</h3><p>Structure the site around business questions, trust and qualified consultation enquiries.</p><a class="text-link" href="/en/tools/">Explore free tools →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Accountant website<br>questions.</h2></div><p>Practical answers for accountants, bookkeeping firms and tax advisers planning a stronger online presence.</p></div><div class="features-grid"><article class="feature-card"><h3>What should an accountant website include?</h3><p>Clear services, client types, trust signals, useful answers, mobile-friendly navigation and a simple consultation request.</p></article><article class="feature-card"><h3>Can every service have its own page?</h3><p>Yes. Focused pages for bookkeeping, payroll, tax and reporting can improve clarity for both visitors and search engines.</p></article><article class="feature-card"><h3>Can the site target local searches?</h3><p>Yes. We can structure relevant location and service pages as part of the SEO plan without promising specific rankings.</p></article><article class="feature-card"><h3>How much does it cost?</h3><p>International launch pricing starts from $149. Languages, service count, CRM and SEO scope determine the final price.</p></article></div></div></section>
<!-- /ACCOUNTANTS_SEO_V1 -->'''
    },
    'ru': {
        'path': ROOT/'ru/accountants/index.html',
        'url': 'https://beqson.com/ru/accountants/',
        'title': 'Создание сайтов для бухгалтеров и налоговых консультантов — BEQSON',
        'desc': 'Создание сайтов для бухгалтеров, аутсорсинга и налоговых консультантов: страницы услуг, локальное SEO, B2B-заявки, несколько языков, аналитика и CRM. От 9 900 ₽.',
        'og_locale': 'ru_RU',
        'og_image': 'https://beqson.com/assets/concepts/ru/accountants-og.jpg',
        'alt': 'Создание сайтов для бухгалтеров и налоговых консультантов — BEQSON',
        'h1': 'Создание сайтов<br>для бухгалтеров и налоговых консультантов.',
        'lead': 'Сайты для бухгалтеров, аутсорсинговых компаний и налоговых консультантов: понятные страницы услуг, локальное SEO, B2B-заявки, несколько языков и интеграция обращений с CRM.',
        'breadcrumb_home': 'Главная', 'breadcrumb_industry': 'Бухгалтеры / налоговые консультанты',
        'service_name': 'Создание сайтов и SEO для бухгалтеров и налоговых консультантов',
        'service_type': 'Создание, разработка и SEO сайтов для бухгалтерских услуг',
        'faq': [
            ('Что должно быть на сайте бухгалтера?', 'Понятные страницы услуг, типы клиентов и бизнеса, подтверждённая информация об опыте и квалификации, ответы на частые вопросы и простой путь к консультации.'),
            ('Можно ли сделать отдельные страницы под бухгалтерию и налоги?', 'Да. Бухгалтерское сопровождение, зарплата, отчётность, налоговые консультации и другие направления можно вынести на отдельные страницы под конкретный поисковый запрос.'),
            ('Вы делаете SEO для бухгалтеров?', 'Да. Можно создавать страницы под услуги, города и типы клиентов, улучшать метаданные и внутреннюю перелинковку. Конкретные позиции в поиске не гарантируются.'),
            ('Сколько стоит сайт для бухгалтера?', 'Стартовая цена BEQSON начинается от 9 900 ₽ за компактный сайт. Количество услуг, языки, CRM, формы и расширенное SEO увеличивают объём проекта.')
        ],
        'section': '''<!-- ACCOUNTANTS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">САЙТ ДЛЯ БУХГАЛТЕРА</p><h2>Покажите экспертизу понятно<br>ещё до первого звонка.</h2></div><p>Клиенту бухгалтерской компании нужны ясность, доверие и понимание, подходит ли ему ваш формат работы. Мы превращаем перечень услуг в понятную B2B-структуру.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Отдельные страницы услуг</h3><p>Бухгалтерское сопровождение, зарплата, отчётность, налоги и другие направления получают собственные страницы вместо общего списка.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Доверие для бизнеса</h3><p>Показываем процесс работы, типы клиентов, опыт и только подтверждённые квалификации в спокойной профессиональной подаче.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Локальное и нишевое SEO</h3><p>Страницы под услуги, города и типы бизнеса помогают приводить посетителя сразу на релевантное решение его задачи.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Консультации, аналитика и CRM</h3><p>Формы, WhatsApp, email, отслеживание источников и CRM помогают быстрее обрабатывать и квалифицировать обращения.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ПОИСК → УСЛУГА → КОНСУЛЬТАЦИЯ</p><h2>Понятный путь от вопроса бизнеса<br>до целевой заявки.</h2><p class="lead">Создаём страницы вокруг реальных бухгалтерских и налоговых задач, а каждое направление связываем с простым действием — запросить консультацию.</p></div><ol class="channel-list"><li><span>01</span><p>SEO-страницы отдельных бухгалтерских и налоговых услуг</p></li><li><span>02</span><p>Локальные и отраслевые точки входа из поиска</p></li><li><span>03</span><p>Формы, аналитика источников и передача заявок в CRM</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">СТАРТОВЫЕ ЦЕНЫ</p><h2>Начните с основных услуг.<br>Расширяйте сайт постепенно.</h2></div><p>Стартовая цена сайта для бухгалтера — <strong>от 9 900 ₽</strong>. Перед заказом можно бесплатно проверить текущий сайт или рассчитать новый проект.</p></div><div class="features-grid"><article class="feature-card"><h3>Бесплатный SEO-аудит</h3><p>Проверим техническое SEO, метаданные и основные проблемы существующего сайта.</p><a class="text-link" href="/ru/audit/">Проверить сайт →</a></article><article class="feature-card"><h3>Калькулятор стоимости</h3><p>Оцените проект с учётом услуг, языков, SEO, CRM и форм заявок.</p><a class="text-link" href="/ru/calculator/">Рассчитать стоимость →</a></article><article class="feature-card"><h3>От 9 900 ₽</h3><p>Можно начать с ключевых направлений и позже добавлять новые услуги, статьи и автоматизацию.</p><a class="text-link" href="#contact">Обсудить проект →</a></article><article class="feature-card"><h3>Под B2B-клиентов</h3><p>Структура сайта строится вокруг бизнес-задач, доверия и целевых консультаций.</p><a class="text-link" href="/ru/tools/">Бесплатные инструменты →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Вопросы о сайте<br>для бухгалтера.</h2></div><p>Что стоит продумать бухгалтеру или налоговому консультанту перед запуском сайта.</p></div><div class="features-grid"><article class="feature-card"><h3>Что должно быть на сайте бухгалтера?</h3><p>Услуги, типы клиентов, подтверждённая экспертиза, ответы на частые вопросы и удобная заявка на консультацию.</p></article><article class="feature-card"><h3>Можно сделать отдельные страницы услуг?</h3><p>Да. Бухгалтерия, налоги, зарплата и отчётность могут иметь собственные SEO-страницы.</p></article><article class="feature-card"><h3>Можно продвигаться по локальным запросам?</h3><p>Да. Можно создавать релевантные страницы под услуги и локации, не обещая конкретных позиций в поиске.</p></article><article class="feature-card"><h3>Сколько стоит сайт?</h3><p>Стартовая цена — от 9 900 ₽. Итог зависит от числа услуг, языков, CRM и объёма SEO.</p></article></div></div></section>
<!-- /ACCOUNTANTS_SEO_V1 -->'''
    },
    'ka': {
        'path': ROOT/'ka/accountants/index.html',
        'url': 'https://beqson.com/ka/accountants/',
        'title': 'ვებსაიტის შექმნა ბუღალტრებისა და საგადასახადო კონსულტანტებისთვის — BEQSON',
        'desc': 'ვებსაიტის შექმნა ბუღალტრებისთვის, საბუღალტრო კომპანიებისა და საგადასახადო კონსულტანტებისთვის: სერვისების გვერდები, ლოკალური SEO, B2B მოთხოვნები, რამდენიმე ენა, ანალიტიკა და CRM. 299 ₾-დან.',
        'og_locale': 'ka_GE',
        'og_image': 'https://beqson.com/assets/concepts/ka/accountants-og.jpg',
        'alt': 'ვებსაიტის შექმნა ბუღალტრებისა და საგადასახადო კონსულტანტებისთვის — BEQSON',
        'h1': 'ვებსაიტების შექმნა<br>ბუღალტრებისა და საგადასახადო კონსულტანტებისთვის.',
        'lead': 'საიტები ბუღალტრებისთვის, აუთსორსინგული საბუღალტრო კომპანიებისა და საგადასახადო კონსულტანტებისთვის: მკაფიო სერვისების გვერდები, ლოკალური SEO, B2B მოთხოვნები, რამდენიმე ენა და CRM-თან დაკავშირებული განაცხადები.',
        'breadcrumb_home': 'მთავარი', 'breadcrumb_industry': 'ბუღალტრები / საგადასახადო კონსულტანტები',
        'service_name': 'ვებსაიტების შექმნა და SEO ბუღალტრებისა და საგადასახადო კონსულტანტებისთვის',
        'service_type': 'საბუღალტრო ვებსაიტის შექმნა, განვითარება და SEO',
        'faq': [
            ('რა უნდა იყოს ბუღალტრის ვებსაიტზე?', 'მკაფიო სერვისების გვერდები, კლიენტებისა და ბიზნესების ტიპები, დადასტურებული გამოცდილება და კვალიფიკაცია, ხშირ კითხვებზე პასუხები და კონსულტაციის მოთხოვნის მარტივი გზა.'),
            ('შეიძლება ცალკე გვერდები ბუღალტერიისა და საგადასახადო სერვისებისთვის?', 'დიახ. ბუღალტრული აღრიცხვა, ხელფასები, ანგარიშგება, საგადასახადო კონსულტაცია და სხვა მიმართულებები შეიძლება განთავსდეს ცალკე გვერდებზე კონკრეტული საძიებო მოთხოვნებისთვის.'),
            ('აკეთებთ SEO-ს ბუღალტრებისთვის?', 'დიახ. შესაძლებელია სერვისების, ქალაქებისა და კლიენტების ტიპების მიხედვით გვერდების შექმნა, მეტამონაცემებისა და შიდა ბმულების გაუმჯობესება. კონკრეტული პოზიციები ძიებაში გარანტირებული არ არის.'),
            ('რა ღირს ბუღალტრის ვებსაიტი?', 'BEQSON-ის საწყისი ფასი იწყება 299 ₾-დან კომპაქტური საიტისთვის. სერვისების რაოდენობა, ენები, CRM, ფორმები და გაფართოებული SEO ზრდის პროექტის მოცულობას.')
        ],
        'section': '''<!-- ACCOUNTANTS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">ვებსაიტი ბუღალტრისთვის</p><h2>აჩვენეთ პროფესიონალიზმი გასაგებად<br>პირველ ზარამდეც კი.</h2></div><p>ბუღალტრული მომსახურების კლიენტს სჭირდება სიცხადე, ნდობა და სწრაფი პასუხი კითხვაზე — შეესაბამება თუ არა თქვენი მომსახურება მის ბიზნესს. ჩვენ სერვისების ჩამონათვალს მკაფიო B2B სტრუქტურად ვაქცევთ.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>ცალკე სერვისების გვერდები</h3><p>ბუღალტრული მომსახურება, ხელფასები, ანგარიშგება, გადასახადები და სხვა მიმართულებები იღებს საკუთარ გვერდებს საერთო ჩამონათვალის ნაცვლად.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>ნდობა ბიზნეს კლიენტებისთვის</h3><p>ვაჩვენებთ მუშაობის პროცესს, კლიენტების ტიპებს, გამოცდილებას და მხოლოდ დადასტურებულ კვალიფიკაციას მშვიდ და პროფესიონალურ სტრუქტურაში.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>ლოკალური და ნიშური SEO</h3><p>სერვისების, ქალაქებისა და ბიზნესის ტიპების მიხედვით გვერდები მომხმარებელს ძიებიდან პირდაპირ მისთვის შესაბამის შეთავაზებაზე გადაიყვანს.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>კონსულტაციები, ანალიტიკა და CRM</h3><p>ფორმები, WhatsApp, email, წყაროს მონიტორინგი და CRM ხელს უწყობს მოთხოვნების სწრაფად დამუშავებას და კვალიფიცირებას.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ძიება → სერვისი → კონსულტაცია</p><h2>გასაგები გზა ბიზნესის კითხვიდან<br>მიზნობრივ მოთხოვნამდე.</h2><p class="lead">ვქმნით გვერდებს რეალური საბუღალტრო და საგადასახადო ამოცანების გარშემო და თითოეულ სერვისს ვუკავშირებთ მარტივ მოქმედებას — კონსულტაციის მოთხოვნას.</p></div><ol class="channel-list"><li><span>01</span><p>ცალკეული საბუღალტრო და საგადასახადო სერვისების SEO-გვერდები</p></li><li><span>02</span><p>ლოკალური და დარგობრივი საძიებო შესასვლელები</p></li><li><span>03</span><p>ფორმები, წყაროს ანალიტიკა და მოთხოვნების CRM-ში გადაცემა</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">საწყისი ფასები</p><h2>დაიწყეთ ძირითადი სერვისებით.<br>საიტი ეტაპობრივად გააფართოვეთ.</h2></div><p>ბუღალტრის ვებსაიტის საწყისი ფასი არის <strong>299 ₾-დან</strong>. შეკვეთამდე შეგიძლიათ უფასოდ შეამოწმოთ არსებული საიტი ან გამოთვალოთ ახალი პროექტის ფასი.</p></div><div class="features-grid"><article class="feature-card"><h3>უფასო SEO აუდიტი</h3><p>შევამოწმებთ ტექნიკურ SEO-ს, მეტამონაცემებსა და არსებული საიტის ძირითად პრობლემებს.</p><a class="text-link" href="/ka/audit/">საიტის შემოწმება →</a></article><article class="feature-card"><h3>ღირებულების კალკულატორი</h3><p>შეაფასეთ პროექტი სერვისების, ენების, SEO-ს, CRM-ისა და განაცხადების ფორმების მიხედვით.</p><a class="text-link" href="/ka/calculator/">ღირებულების გამოთვლა →</a></article><article class="feature-card"><h3>299 ₾-დან</h3><p>შეგიძლიათ დაიწყოთ ძირითადი მიმართულებებით და მოგვიანებით დაამატოთ ახალი სერვისები, სტატიები და ავტომატიზაცია.</p><a class="text-link" href="#contact">პროექტის განხილვა →</a></article><article class="feature-card"><h3>B2B კლიენტებისთვის</h3><p>საიტის სტრუქტურა ეწყობა ბიზნესის ამოცანებს, ნდობასა და მიზნობრივ კონსულტაციებს.</p><a class="text-link" href="/ka/tools/">უფასო ინსტრუმენტები →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>კითხვები ბუღალტრის<br>ვებსაიტზე.</h2></div><p>რა უნდა გაითვალისწინოს ბუღალტერმა ან საგადასახადო კონსულტანტმა ახალი საიტის გაშვებამდე.</p></div><div class="features-grid"><article class="feature-card"><h3>რა უნდა იყოს ბუღალტრის ვებსაიტზე?</h3><p>სერვისები, კლიენტების ტიპები, დადასტურებული პროფესიონალიზმი, ხშირ კითხვებზე პასუხები და კონსულტაციის მოთხოვნის მარტივი გზა.</p></article><article class="feature-card"><h3>შეიძლება სერვისებისთვის ცალკე გვერდების შექმნა?</h3><p>დიახ. ბუღალტერია, გადასახადები, ხელფასები და ანგარიშგება შეიძლება ცალკე SEO-გვერდებზე განთავსდეს.</p></article><article class="feature-card"><h3>შეიძლება ლოკალურ ძიებაზე მუშაობა?</h3><p>დიახ. შესაძლებელია სერვისებისა და ლოკაციების მიხედვით შესაბამისი გვერდების შექმნა კონკრეტული პოზიციების გარანტიის გარეშე.</p></article><article class="feature-card"><h3>რა ღირს საიტი?</h3><p>საწყისი ფასი 299 ₾-დან იწყება. საბოლოო ფასი დამოკიდებულია სერვისების რაოდენობაზე, ენებზე, CRM-სა და SEO-ს მოცულობაზე.</p></article></div></div></section>
<!-- /ACCOUNTANTS_SEO_V1 -->'''
    }
}

def make_schema(lang, c):
    graph = [
        {"@type":"Organization","@id":"https://beqson.com/#organization","name":"BEQSON Digital Studio","url":"https://beqson.com/","logo":"https://beqson.com/assets/beqson-mark-v3.png","email":"digitalstudiobeqson@gmail.com","telephone":"+995551739333","sameAs":["https://t.me/digital_studio_beqson"]},
        {"@type":"WebPage","@id":c['url']+'#webpage',"url":c['url'],"name":c['title'],"description":c['desc'],"inLanguage":lang,"publisher":{"@id":"https://beqson.com/#organization"}},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":c['breadcrumb_home'],"item":f"https://beqson.com/{lang}/"},{"@type":"ListItem","position":2,"name":c['breadcrumb_industry'],"item":c['url']}]},
        {"@type":"Service","name":c['service_name'],"description":c['desc'],"provider":{"@id":"https://beqson.com/#organization"},"url":c['url'],"serviceType":c['service_type']},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c['faq']]}
    ]
    return json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, separators=(',',':'))

def patch(lang, c):
    p = c['path']
    s = p.read_text(encoding='utf-8')
    if '<!-- ACCOUNTANTS_SEO_V1 -->' in s:
        print(f'{lang}: already upgraded')
        return

    s = re.sub(r'<title>.*?</title>', f"<title>{c['title']}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{c["desc"]}">', s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', '<link rel="alternate" hreflang="x-default" href="https://beqson.com/en/accountants/">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{c["title"]}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{c["desc"]}">', s, count=1)
    s = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{c["alt"]}">', s, count=1)
    s = re.sub(r'<meta name="twitter:image:alt" content="[^"]*">', f'<meta name="twitter:image:alt" content="{c["alt"]}">', s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">'+make_schema(lang,c)+'</script>', s, count=1, flags=re.S)
    s, n = re.subn(r'<h1>.*?</h1><p class="lead">.*?</p>', f'<h1>{c["h1"]}</h1><p class="lead">{c["lead"]}</p>', s, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f'Hero block not found in {p}')
    pattern = r'<section class="section industry-features">.*?<section class="contact-section section" id="contact">'
    s, n = re.subn(pattern, c['section']+'\n<section class="contact-section section" id="contact">', s, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f'Industry section block not found in {p}')
    p.write_text(s, encoding='utf-8')
    print(f'{lang}: upgraded')

for lang, c in CFG.items():
    patch(lang, c)
