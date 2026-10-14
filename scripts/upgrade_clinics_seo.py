from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]

CFG = {
    'en': {
        'path': ROOT/'en/clinics/index.html',
        'url': 'https://beqson.com/en/clinics/',
        'title': 'Medical Website Design for Doctors & Clinics | BEQSON',
        'desc': 'Medical website design for doctors and private clinics: specialist profiles, service pages, local SEO, booking paths, multilingual structure and lead capture.',
        'og_locale': 'en_US',
        'og_image': 'https://beqson.com/assets/concepts/en/clinics-og.jpg',
        'alt': 'Medical website design for doctors and clinics by BEQSON',
        'h1_old': 'Care that starts<br>before the first visit.',
        'h1_new': 'Medical website design<br>for doctors and private clinics.',
        'lead_old': 'A professional website for a private doctor or clinic. Clear specialist and service navigation, reassuring presentation and accessible contact details.',
        'lead_new': 'Websites for doctors and private clinics with specialist profiles, focused service pages, local SEO foundations, multilingual structure and a clear path from search to appointment enquiry.',
        'home': 'Home', 'industry': 'Doctors / clinics',
        'service_name': 'Medical website design and SEO for doctors and private clinics',
        'service_type': 'Medical website design, development and local SEO',
        'faq': [
            ('What should a private clinic website include?', 'A strong clinic website should clearly present doctors, specialties, services, locations, opening information, contact methods and an easy path to request or book an appointment.'),
            ('Can you create separate pages for doctors and medical services?', 'Yes. We can organize individual doctor profiles and dedicated pages for specialties and services so visitors can find the right information quickly and search engines can understand the structure.'),
            ('Can you help a clinic appear in local search?', 'Yes. We can build local-search foundations with location information, structured pages, metadata, internal links and Google Business Profile support. Specific rankings are never guaranteed.'),
            ('How much does a medical website cost?', 'BEQSON international launch pricing starts from $149 for a focused starter website. Final scope depends on page count, doctors, services, languages, booking integrations, SEO and CRM needs.')
        ],
        'section': '''<!-- CLINICS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">MEDICAL WEBSITE DESIGN</p><h2>Built around the way patients<br>look for a doctor.</h2></div><p>A clinic website should make complex information easy to navigate. We structure doctors, specialties, services and contact points so a visitor can understand where to go next without friction.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Doctor & specialist profiles</h3><p>Individual pages can present qualifications, specialties, working languages, clinic locations and factual professional information.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Service & specialty pages</h3><p>Dedicated pages for consultations, diagnostics, procedures and specialties create a clearer experience and stronger search structure.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Appointment path</h3><p>Phone, WhatsApp, forms or supported booking systems can be placed where patients naturally need the next step.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Local & multilingual SEO</h3><p>Location pages and properly connected language versions help clinics serve local residents, expats and international patients.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">SEARCH → TRUST → APPOINTMENT</p><h2>A clearer patient journey.</h2><p class="lead">We design the site around real questions: which specialist do I need, what does the clinic offer, where is it located and how can I make contact?</p><a class="text-link" href="/en/audit/">Audit an existing clinic website <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>Search-ready pages for specialties, services and locations</p></li><li><span>02</span><p>Doctor profiles and factual trust signals</p></li><li><span>03</span><p>Appointment enquiries, analytics and CRM-ready lead capture</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">LAUNCH PRICING</p><h2>Start focused.<br>Add more when needed.</h2></div><p>International launch pricing starts from <strong>$149</strong>. A private doctor can begin with a compact website, while a clinic can expand into doctor, specialty, location and booking pages.</p></div><div class="features-grid"><article class="feature-card"><h3>Free SEO Audit</h3><p>Check technical basics, metadata, indexability and priority issues on an existing website.</p><a class="text-link" href="/en/audit/">Run audit →</a></article><article class="feature-card"><h3>Website Cost Calculator</h3><p>Estimate the cost of a new doctor or clinic website in a few minutes.</p><a class="text-link" href="/en/calculator/">Calculate cost →</a></article><article class="feature-card"><h3>From $149</h3><p>Launch pricing for focused starter websites during BEQSON's early-client period.</p><a class="text-link" href="#contact">Discuss project →</a></article><article class="feature-card"><h3>Responsible content</h3><p>Medical claims, credentials and service information should be factual and approved by the clinic or doctor. We do not invent outcomes or guarantees.</p><a class="text-link" href="/en/tools/">Explore free tools →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Medical website<br>questions.</h2></div><p>Practical answers before launching a website for a doctor or private clinic.</p></div><div class="features-grid"><article class="feature-card"><h3>What should a clinic website include?</h3><p>Doctors, specialties, services, locations, working information, contact methods and a simple appointment path.</p></article><article class="feature-card"><h3>Can every doctor have a profile?</h3><p>Yes. Doctor pages can include specialty, qualifications, languages, locations and other verified professional details.</p></article><article class="feature-card"><h3>Do you help with local SEO?</h3><p>Yes — location structure, metadata, internal links and local-search foundations. We never promise a specific Google position.</p></article><article class="feature-card"><h3>How much does it cost?</h3><p>International launch pricing starts from $149. The final price depends on doctors, services, languages, SEO, booking integrations and CRM scope.</p></article></div></div></section>
<!-- /CLINICS_SEO_V1 -->'''
    },
    'ru': {
        'path': ROOT/'ru/clinics/index.html',
        'url': 'https://beqson.com/ru/clinics/',
        'title': 'Создание сайтов для врачей и клиник — BEQSON',
        'desc': 'Создание сайтов для частных врачей и клиник: специалисты, услуги, локальное SEO, запись, мультиязычность, заявки и CRM. Старт от 9 900 ₽.',
        'og_locale': 'ru_RU',
        'og_image': 'https://beqson.com/assets/concepts/ru/clinics-og.jpg',
        'alt': 'Создание сайтов для врачей и частных клиник — BEQSON',
        'h1_old': 'Забота чувствуется<br>ещё до первого приёма.',
        'h1_new': 'Создание сайтов<br>для врачей и частных клиник.',
        'lead_old': 'Профессиональный сайт для частного врача или клиники. Удобная навигация по специалистам и услугам, спокойная подача и доступные контакты.',
        'lead_new': 'Сайты для частных врачей и клиник: профили специалистов, отдельные страницы услуг, локальное SEO, мультиязычность и понятный путь от поиска до заявки на приём.',
        'home': 'Главная', 'industry': 'Частные врачи / клиники',
        'service_name': 'Создание сайтов и SEO для врачей и частных клиник',
        'service_type': 'Создание, разработка и локальное SEO медицинских сайтов',
        'faq': [
            ('Что должно быть на сайте частной клиники?', 'На сайте важно понятно показать врачей, специализации, услуги, адреса, режим работы, способы связи и простой путь к записи или заявке на приём.'),
            ('Можно ли сделать отдельные страницы врачей и услуг?', 'Да. Мы можем создать профили специалистов и отдельные страницы направлений и услуг, чтобы посетителям было проще ориентироваться, а поисковым системам — понимать структуру сайта.'),
            ('Вы помогаете с локальным SEO клиники?', 'Да. Настраиваем структуру по локациям, метаданные, внутренние ссылки и основу для Google Business Profile и локального поиска. Конкретные позиции не гарантируем.'),
            ('Сколько стоит сайт для врача или клиники?', 'Стартовая цена BEQSON для компактного сайта — от 9 900 ₽. Итог зависит от числа врачей, услуг, языков, интеграции записи, SEO и CRM.')
        ],
        'section': '''<!-- CLINICS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">САЙТ ДЛЯ ВРАЧА И КЛИНИКИ</p><h2>Структура под то,<br>как пациент ищет специалиста.</h2></div><p>Медицинский сайт должен упрощать сложную информацию. Мы выстраиваем врачей, специализации, услуги и контакты так, чтобы человеку было понятно, куда двигаться дальше.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Профили врачей</h3><p>Отдельные страницы с реальными данными об образовании, специализации, языках, месте приёма и профессиональном опыте.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Страницы услуг и направлений</h3><p>Консультации, диагностика, процедуры и специализации получают собственную понятную структуру для пользователей и поиска.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Путь к записи</h3><p>Телефон, WhatsApp, формы или поддерживаемая система онлайн-записи размещаются там, где человеку логично сделать следующий шаг.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Локальное и мультиязычное SEO</h3><p>Страницы по локациям и правильно связанные языковые версии помогают работать с местной и международной аудиторией.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ПОИСК → ДОВЕРИЕ → ЗАПИСЬ</p><h2>Понятный путь пациента.</h2><p class="lead">Строим сайт вокруг реальных вопросов: какой специалист нужен, какие услуги есть, где находится клиника и как записаться на приём.</p><a class="text-link" href="/ru/audit/">Проверить текущий сайт клиники <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>Поисковые страницы по специализациям, услугам и локациям</p></li><li><span>02</span><p>Профили врачей и проверяемые факты для доверия</p></li><li><span>03</span><p>Заявки на приём, аналитика и CRM</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">СТАРТОВЫЕ ЦЕНЫ</p><h2>Начните с главного.<br>Расширяйте по мере необходимости.</h2></div><p>Стартовая цена — <strong>от 9 900 ₽</strong>. Частный врач может начать с компактного сайта, а клиника постепенно добавить страницы врачей, услуг, филиалов и интеграцию записи.</p></div><div class="features-grid"><article class="feature-card"><h3>Бесплатный SEO-аудит</h3><p>Проверим техническую основу, метаданные, индексируемость и приоритетные проблемы текущего сайта.</p><a class="text-link" href="/ru/audit/">Проверить сайт →</a></article><article class="feature-card"><h3>Калькулятор стоимости</h3><p>Рассчитайте ориентировочную стоимость нового сайта врача или клиники за несколько минут.</p><a class="text-link" href="/ru/calculator/">Рассчитать стоимость →</a></article><article class="feature-card"><h3>От 9 900 ₽</h3><p>Стартовая цена на компактные проекты для первых клиентов BEQSON.</p><a class="text-link" href="#contact">Обсудить проект →</a></article><article class="feature-card"><h3>Только реальные медицинские факты</h3><p>Сведения об услугах, квалификации и медицинские утверждения должны быть подтверждены врачом или клиникой. Мы не придумываем результаты лечения и гарантии.</p><a class="text-link" href="/ru/tools/">Бесплатные инструменты →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Вопросы о сайте<br>врача или клиники.</h2></div><p>Что обычно важно решить до запуска медицинского сайта.</p></div><div class="features-grid"><article class="feature-card"><h3>Что должно быть на сайте клиники?</h3><p>Врачи, специализации, услуги, адреса, режим работы, контакты и простой путь к записи или заявке.</p></article><article class="feature-card"><h3>Можно сделать страницу каждого врача?</h3><p>Да. В профиле можно показать специализацию, образование, языки, место приёма и другие подтверждённые профессиональные сведения.</p></article><article class="feature-card"><h3>Поможете с локальным SEO?</h3><p>Да — структура по локациям, метаданные, внутренние ссылки и локальный поиск. Конкретные позиции в Google не обещаем.</p></article><article class="feature-card"><h3>Сколько стоит сайт?</h3><p>Стартовая цена — от 9 900 ₽. Итог зависит от врачей, услуг, языков, SEO, записи и CRM.</p></article></div></div></section>
<!-- /CLINICS_SEO_V1 -->'''
    },
    'ka': {
        'path': ROOT/'ka/clinics/index.html',
        'url': 'https://beqson.com/ka/clinics/',
        'title': 'საიტების შექმნა ექიმებისა და კლინიკებისთვის — BEQSON',
        'desc': 'ვებსაიტების შექმნა კერძო ექიმებისა და კლინიკებისთვის: ექიმების პროფილები, სერვისები, ლოკალური SEO, ჩაწერა, მრავალენოვნება და CRM. ფასი 299 ₾-დან.',
        'og_locale': 'ka_GE',
        'og_image': 'https://beqson.com/assets/concepts/ka/clinics-og.jpg',
        'alt': 'ვებსაიტების შექმნა ექიმებისა და კერძო კლინიკებისთვის — BEQSON',
        'h1_old': 'ზრუნვა იგრძნობა<br>პირველ ვიზიტამდეც.',
        'h1_new': 'ვებსაიტების შექმნა<br>ექიმებისა და კერძო კლინიკებისთვის.',
        'lead_old': 'პროფესიონალური საიტი კერძო ექიმის ან კლინიკისთვის. სპეციალისტებისა და სერვისების მარტივი ძიება, მშვიდი პრეზენტაცია და ხელმისაწვდომი კონტაქტები.',
        'lead_new': 'საიტები კერძო ექიმებისა და კლინიკებისთვის: ექიმების პროფილები, სერვისების ცალკე გვერდები, ლოკალური SEO, მრავალენოვანი სტრუქტურა და მარტივი გზა ძიებიდან ჩაწერის მოთხოვნამდე.',
        'home': 'მთავარი', 'industry': 'ექიმები / კლინიკები',
        'service_name': 'ვებსაიტების შექმნა და SEO ექიმებისა და კერძო კლინიკებისთვის',
        'service_type': 'სამედიცინო ვებსაიტების შექმნა, განვითარება და ლოკალური SEO',
        'faq': [
            ('რა უნდა იყოს კერძო კლინიკის ვებსაიტზე?', 'საიტმა მკაფიოდ უნდა აჩვენოს ექიმები, სპეციალიზაციები, სერვისები, მისამართები, სამუშაო ინფორმაცია, საკონტაქტო არხები და ჩაწერის მარტივი გზა.'),
            ('შეიძლება თითოეული ექიმისა და სერვისისთვის ცალკე გვერდი?', 'დიახ. შეგვიძლია შევქმნათ ექიმების პროფილები და სპეციალიზაციებისა თუ სერვისების ცალკე გვერდები, რათა ინფორმაცია ადვილად მოიძებნოს როგორც მომხმარებლისთვის, ისე საძიებო სისტემისთვის.'),
            ('ეხმარებით კლინიკებს ლოკალურ SEO-ში?', 'დიახ. ვაწყობთ ლოკაციებზე დაფუძნებულ სტრუქტურას, მეტამონაცემებს, შიდა ბმულებს და Google Business Profile-ისა და ლოკალური ძიების საფუძველს. კონკრეტულ პოზიციებს არ ვპირდებით.'),
            ('რა ღირს ექიმის ან კლინიკის საიტი?', 'BEQSON-ის საწყისი ფასი კომპაქტური საიტისთვის 299 ₾-დან იწყება. საბოლოო ღირებულება დამოკიდებულია ექიმების, სერვისების, ენების, ჩაწერის ინტეგრაციის, SEO-სა და CRM-ის მოცულობაზე.')
        ],
        'section': '''<!-- CLINICS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">საიტი ექიმისა და კლინიკისთვის</p><h2>სტრუქტურა იმის მიხედვით,<br>როგორ ეძებს პაციენტი ექიმს.</h2></div><p>სამედიცინო საიტმა რთული ინფორმაცია მარტივად უნდა წარმოაჩინოს. ექიმებს, სპეციალიზაციებს, სერვისებსა და კონტაქტებს ისე ვაწყობთ, რომ შემდეგი ნაბიჯი მომხმარებლისთვის გასაგები იყოს.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>ექიმების პროფილები</h3><p>ცალკე გვერდები რეალური ინფორმაციით განათლებაზე, სპეციალიზაციაზე, სამუშაო ენებზე, მიღების ადგილსა და პროფესიულ გამოცდილებაზე.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>სერვისებისა და სპეციალიზაციების გვერდები</h3><p>კონსულტაციებს, დიაგნოსტიკას, პროცედურებსა და მიმართულებებს ცალკე, გასაგები სტრუქტურა ექნება მომხმარებლისა და ძიებისთვის.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>ჩაწერის მარტივი გზა</h3><p>ტელეფონი, WhatsApp, ფორმა ან მხარდაჭერილი ონლაინ-ჩაწერის სისტემა განთავსდება იქ, სადაც მომხმარებელს შემდეგი ნაბიჯის გადადგმა სჭირდება.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>ლოკალური და მრავალენოვანი SEO</h3><p>ლოკაციის გვერდები და სწორად დაკავშირებული ენების ვერსიები ეხმარება კლინიკას იმუშაოს ადგილობრივ და საერთაშორისო აუდიტორიასთან.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ძიება → ნდობა → ჩაწერა</p><h2>პაციენტის გასაგები გზა.</h2><p class="lead">საიტს რეალური კითხვების გარშემო ვაწყობთ: რომელი სპეციალისტი მჭირდება, რა სერვისებია, სად მდებარეობს კლინიკა და როგორ დავუკავშირდე.</p><a class="text-link" href="/ka/audit/">შეამოწმეთ არსებული საიტი <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>საძიებო გვერდები სპეციალიზაციების, სერვისებისა და ლოკაციების მიხედვით</p></li><li><span>02</span><p>ექიმების პროფილები და გადამოწმებადი ფაქტები ნდობისთვის</p></li><li><span>03</span><p>ჩაწერის მოთხოვნები, ანალიტიკა და CRM</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">საწყისი ფასები</p><h2>დაიწყეთ ძირითადით.<br>შემდეგ გააფართოვეთ.</h2></div><p>საწყისი ფასი — <strong>299 ₾-დან</strong>. კერძო ექიმს შეუძლია დაიწყოს კომპაქტური საიტით, ხოლო კლინიკამ შემდეგ დაამატოს ექიმების, სერვისების, ფილიალებისა და ჩაწერის გვერდები.</p></div><div class="features-grid"><article class="feature-card"><h3>უფასო SEO აუდიტი</h3><p>შეამოწმეთ ტექნიკური საფუძველი, მეტამონაცემები, ინდექსაცია და არსებული საიტის პრიორიტეტული პრობლემები.</p><a class="text-link" href="/ka/audit/">საიტის შემოწმება →</a></article><article class="feature-card"><h3>ღირებულების კალკულატორი</h3><p>რამდენიმე წუთში მიიღეთ ექიმის ან კლინიკის ახალი საიტის სავარაუდო ღირებულება.</p><a class="text-link" href="/ka/calculator/">ღირებულების გამოთვლა →</a></article><article class="feature-card"><h3>299 ₾-დან</h3><p>BEQSON-ის პირველი კლიენტებისთვის მოქმედი საწყისი ფასი კომპაქტურ პროექტებზე.</p><a class="text-link" href="#contact">პროექტის განხილვა →</a></article><article class="feature-card"><h3>მხოლოდ რეალური სამედიცინო ფაქტები</h3><p>სერვისები, კვალიფიკაცია და სამედიცინო ინფორმაცია უნდა იყოს ექიმის ან კლინიკის მიერ დადასტურებული. ჩვენ არ ვიგონებთ შედეგებსა და გარანტიებს.</p><a class="text-link" href="/ka/tools/">უფასო ინსტრუმენტები →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>კითხვები ექიმისა და<br>კლინიკის ვებსაიტზე.</h2></div><p>რა არის მნიშვნელოვანი სამედიცინო საიტის გაშვებამდე.</p></div><div class="features-grid"><article class="feature-card"><h3>რა უნდა იყოს კლინიკის საიტზე?</h3><p>ექიმები, სპეციალიზაციები, სერვისები, მისამართები, სამუშაო ინფორმაცია, კონტაქტები და ჩაწერის მარტივი გზა.</p></article><article class="feature-card"><h3>შეიძლება თითოეულ ექიმს ჰქონდეს გვერდი?</h3><p>დიახ. პროფილში შეიძლება იყოს სპეციალიზაცია, განათლება, ენები, მიღების ადგილი და სხვა დადასტურებული პროფესიული ინფორმაცია.</p></article><article class="feature-card"><h3>ლოკალურ SEO-შიც გვეხმარებით?</h3><p>დიახ — ლოკაციის სტრუქტურა, მეტამონაცემები, შიდა ბმულები და ლოკალური ძიების საფუძველი. Google-ში კონკრეტულ პოზიციას არ ვპირდებით.</p></article><article class="feature-card"><h3>რა ღირს საიტი?</h3><p>საწყისი ფასი 299 ₾-დან იწყება. საბოლოო ღირებულება დამოკიდებულია ექიმებზე, სერვისებზე, ენებზე, SEO-ზე, ჩაწერის ინტეგრაციასა და CRM-ზე.</p></article></div></div></section>
<!-- /CLINICS_SEO_V1 -->'''
    }
}

def schema(c, lang):
    graph = [
        {"@type":"Organization","@id":"https://beqson.com/#organization","name":"BEQSON Digital Studio","url":"https://beqson.com/","logo":"https://beqson.com/assets/beqson-mark-v3.png","email":"digitalstudiobeqson@gmail.com","telephone":"+995551739333","sameAs":["https://t.me/digital_studio_beqson"]},
        {"@type":"WebPage","@id":c['url']+'#webpage',"url":c['url'],"name":c['title'],"description":c['desc'],"inLanguage":lang,"publisher":{"@id":"https://beqson.com/#organization"}},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":c['home'],"item":f"https://beqson.com/{lang}/"},{"@type":"ListItem","position":2,"name":c['industry'],"item":c['url']}]},
        {"@type":"Service","name":c['service_name'],"description":c['desc'],"provider":{"@id":"https://beqson.com/#organization"},"url":c['url'],"serviceType":c['service_type']},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c['faq']]}
    ]
    return json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, separators=(',',':'))

def set_meta(html, c, lang):
    html = re.sub(r'<title>.*?</title>', f'<title>{c["title"]}</title>', html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{c["desc"]}">', html, count=1)
    html = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', '<link rel="alternate" hreflang="x-default" href="https://beqson.com/en/clinics/">', html, count=1)
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
    html = re.sub(r'<!-- CLINICS_SEO_V1 -->.*?<!-- /CLINICS_SEO_V1 -->\s*', '', html, flags=re.S)
    marker = '<section class="contact-section section" id="contact">'
    if marker not in html:
        raise RuntimeError(f'contact marker not found: {p}')
    html = html.replace(marker, c['section']+'\n'+marker, 1)
    p.write_text(html, encoding='utf-8')
    print('updated', p.relative_to(ROOT))

for lang, c in CFG.items():
    patch(lang, c)
