from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CFG = {
    'en': {
        'path': ROOT / 'en/dentists/index.html',
        'url': 'https://beqson.com/en/dentists/',
        'title': 'Dental Website Design & SEO for Dentists | BEQSON',
        'desc': 'Dental website design for dentists and clinics: treatment pages, online booking, local SEO, multilingual structure, analytics and lead capture by BEQSON.',
        'locale': 'en_US',
        'image': 'https://beqson.com/assets/concepts/en/dentists-og.jpg',
        'alt': 'Dental website design for dentists and clinics — BEQSON',
        'h1_old': 'A confident smile<br>begins with trust.',
        'h1_new': 'Dental website design<br>that turns searches into bookings.',
        'lead_old': 'A light, reassuring website for a dental practice. Present the team, treatments and clinic so that a first appointment feels approachable.',
        'lead_new': 'Dental websites for clinics and independent dentists with treatment pages, doctor profiles, online booking, local SEO foundations and multilingual structure.',
        'home': 'Home', 'industry': 'Dentists',
        'service': 'Dental website design and SEO for dentists',
        'service_type': 'Dental clinic website design, development and SEO',
        'faq': [
            ('What should a dental clinic website include?', 'Clear treatment pages, dentist profiles, clinic information, location and hours, easy contact options, booking paths and trustworthy information about the practice.'),
            ('Can you add online booking to a dentist website?', 'Yes. We can connect booking forms, appointment requests, WhatsApp, phone and other contact paths depending on how the clinic works.'),
            ('Do you help with local SEO for dentists?', 'Yes. We build search-ready service pages, metadata, internal links and local-search foundations. Specific rankings are never guaranteed.'),
            ('How much does a dental website cost?', 'Our international launch pricing starts from $149 for a focused starter website. Final pricing depends on pages, languages, booking, SEO, CRM and other features.')
        ],
        'section': '''<!-- DENTISTS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">DENTAL WEBSITE DESIGN</p><h2>Built around the way patients<br>choose a dental clinic.</h2></div><p>A dental website should quickly answer three questions: what you treat, who the doctors are and how to book. We combine reassuring design with search-ready structure and clear conversion paths.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Treatment SEO pages</h3><p>Dedicated pages for implants, orthodontics, hygiene, cosmetic dentistry, emergency care and other services can match real patient searches.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Doctor profiles & trust</h3><p>Present dentists, qualifications, languages, clinic photos and practical information without exaggerated medical claims.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Booking-first UX</h3><p>Appointment forms, phone, WhatsApp and clear calls to action reduce friction between search and the first visit.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Local & multilingual SEO</h3><p>Location pages, map signals and multilingual versions help clinics serve local patients and international audiences.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">SEARCH · TRUST · BOOKING</p><h2>From Google search to appointment.</h2><p class="lead">We structure the site around the patient journey, then connect analytics so the clinic can see which pages and channels generate enquiries.</p><a class="text-link" href="/en/audit/">Audit an existing website <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>Search pages for treatments and location</p></li><li><span>02</span><p>Doctors, clinic, reviews and practical trust signals</p></li><li><span>03</span><p>Booking, enquiry tracking and CRM-ready lead capture</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">LAUNCH PRICING</p><h2>Start lean.<br>Add features as you grow.</h2></div><p>International launch pricing starts from <strong>$149</strong>. You can audit an existing clinic website or calculate a new project before contacting us.</p></div><div class="features-grid"><article class="feature-card"><h3>Free SEO Audit</h3><p>SEO Score, technical checks and a priority action plan.</p><a class="text-link" href="/en/audit/">Run audit →</a></article><article class="feature-card"><h3>Website Cost Calculator</h3><p>Answer five questions and get an instant estimated range.</p><a class="text-link" href="/en/calculator/">Calculate cost →</a></article><article class="feature-card"><h3>Start from $149</h3><p>Focused starter websites during the BEQSON launch period.</p><a class="text-link" href="#contact">Discuss project →</a></article><article class="feature-card"><h3>Built to expand</h3><p>Add treatment pages, languages, analytics, CRM and booking integrations later.</p><a class="text-link" href="/en/tools/">Explore free tools →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Dental website<br>questions.</h2></div><p>Practical answers before launching a dentist or dental clinic website.</p></div><div class="features-grid"><article class="feature-card"><h3>What should a dental clinic website include?</h3><p>Treatment pages, dentist profiles, clinic details, location, opening hours, contact options and a clear booking path.</p></article><article class="feature-card"><h3>Can you add online booking?</h3><p>Yes. We can connect appointment forms, booking requests, phone, WhatsApp and other contact methods.</p></article><article class="feature-card"><h3>Do you help with local SEO for dentists?</h3><p>Yes — service-page structure, metadata, internal links and local-search foundations. We do not promise specific rankings.</p></article><article class="feature-card"><h3>How much does it cost?</h3><p>International launch pricing starts from $149. Pages, languages, booking, SEO and CRM determine the final scope.</p></article></div></div></section>
<!-- /DENTISTS_SEO_V1 -->'''
    },
    'ru': {
        'path': ROOT / 'ru/dentists/index.html',
        'url': 'https://beqson.com/ru/dentists/',
        'title': 'Создание сайтов для стоматологий и стоматологов — BEQSON',
        'desc': 'Создание сайтов для стоматологий: услуги, врачи, онлайн-запись, локальное SEO, мультиязычность, аналитика и заявки. Стартовые цены от 9 900 ₽.',
        'locale': 'ru_RU',
        'image': 'https://beqson.com/assets/concepts/ru/dentists-og.jpg',
        'alt': 'Создание сайтов для стоматологий и стоматологов — BEQSON',
        'h1_old': 'Уверенная улыбка<br>начинается с доверия.',
        'h1_new': 'Создание сайтов<br>для стоматологий и стоматологов.',
        'lead_old': 'Светлый, спокойный сайт для стоматологии. Показываем врачей, услуги и атмосферу клиники, чтобы человеку было легче решиться на первый визит.',
        'lead_new': 'Сайты для стоматологий и частных стоматологов: услуги и врачи, онлайн-запись, локальное SEO, мультиязычность и понятный путь от поиска до визита.',
        'home': 'Главная', 'industry': 'Стоматологи',
        'service': 'Создание сайтов и SEO для стоматологий',
        'service_type': 'Создание, разработка и SEO сайтов для стоматологий',
        'faq': [
            ('Что должно быть на сайте стоматологии?', 'Страницы услуг, профили врачей, информация о клинике, адрес и часы работы, способы связи, запись на приём и понятные сведения о лечении.'),
            ('Можно ли подключить онлайн-запись?', 'Да. Можно подключить форму записи, заявку на приём, телефон, WhatsApp и другие способы связи в зависимости от процессов клиники.'),
            ('Вы занимаетесь локальным SEO для стоматологий?', 'Да. Готовим структуру услуг, метаданные, внутренние ссылки и основу локального поиска. Конкретные позиции в поиске не гарантируем.'),
            ('Сколько стоит сайт стоматологии?', 'На старте BEQSON компактный сайт начинается от 9 900 ₽. Итог зависит от количества страниц, языков, онлайн-записи, SEO, CRM и дополнительных функций.')
        ],
        'section': '''<!-- DENTISTS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">САЙТ ДЛЯ СТОМАТОЛОГИИ</p><h2>Построен вокруг того,<br>как пациент выбирает клинику.</h2></div><p>Сайт стоматологии должен быстро ответить на три вопроса: что вы лечите, кто принимает и как записаться. Мы соединяем спокойный дизайн, SEO-структуру и удобный путь до обращения.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>SEO-страницы услуг</h3><p>Отдельные страницы под имплантацию, ортодонтию, гигиену, эстетическую стоматологию, срочную помощь и другие направления.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Врачи и доверие</h3><p>Профили специалистов, образование, рабочие языки, фотографии клиники и практическая информация без медицинских обещаний.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Удобная запись</h3><p>Форма записи, телефон, WhatsApp и заметные кнопки сокращают путь от поиска до первого визита.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Локальное SEO и языки</h3><p>География, карты и несколько языковых версий помогают работать и с местными, и с иностранными пациентами.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ПОИСК · ДОВЕРИЕ · ЗАПИСЬ</p><h2>От запроса в Google — до приёма.</h2><p class="lead">Структурируем сайт по пути пациента и подключаем аналитику, чтобы клиника понимала, какие страницы и каналы приводят обращения.</p><a class="text-link" href="/ru/audit/">Проверить текущий сайт <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>Поисковые страницы по услугам и городу</p></li><li><span>02</span><p>Врачи, клиника и понятные факторы доверия</p></li><li><span>03</span><p>Запись, аналитика обращений и CRM</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">СТАРТОВЫЕ ЦЕНЫ</p><h2>Начните недорого.<br>Расширяйте сайт по мере роста.</h2></div><p>На старте сайт стоматологии можно запустить <strong>от 9 900 ₽</strong>. До обращения к нам можно бесплатно проверить текущий сайт или рассчитать новый проект.</p></div><div class="features-grid"><article class="feature-card"><h3>Бесплатный SEO-аудит</h3><p>SEO Score, технические проверки и приоритетный план действий.</p><a class="text-link" href="/ru/audit/">Проверить сайт →</a></article><article class="feature-card"><h3>Калькулятор стоимости</h3><p>Ответьте на пять вопросов и получите ориентировочный диапазон цены.</p><a class="text-link" href="/ru/calculator/">Рассчитать стоимость →</a></article><article class="feature-card"><h3>От 9 900 ₽</h3><p>Стартовая цена на компактный сайт в период запуска BEQSON.</p><a class="text-link" href="#contact">Обсудить проект →</a></article><article class="feature-card"><h3>Можно расширять</h3><p>Добавим услуги, языки, аналитику, CRM и интеграцию записи по мере роста.</p><a class="text-link" href="/ru/tools/">Все бесплатные инструменты →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Вопросы о сайте<br>стоматологии.</h2></div><p>Коротко о том, что важно перед запуском сайта стоматолога или клиники.</p></div><div class="features-grid"><article class="feature-card"><h3>Что должно быть на сайте стоматологии?</h3><p>Услуги, врачи, информация о клинике, адрес, часы работы, контакты и простой путь к записи.</p></article><article class="feature-card"><h3>Можно подключить онлайн-запись?</h3><p>Да. Подключим форму записи, заявку на приём, телефон, WhatsApp и другие каналы.</p></article><article class="feature-card"><h3>Вы делаете локальное SEO?</h3><p>Да — структура услуг, метаданные, внутренние ссылки и локальная поисковая база. Позиции не гарантируем.</p></article><article class="feature-card"><h3>Сколько стоит сайт?</h3><p>Стартовая цена — от 9 900 ₽. Итог зависит от страниц, языков, записи, SEO и CRM.</p></article></div></div></section>
<!-- /DENTISTS_SEO_V1 -->'''
    },
    'ka': {
        'path': ROOT / 'ka/dentists/index.html',
        'url': 'https://beqson.com/ka/dentists/',
        'title': 'საიტების შექმნა სტომატოლოგებისა და კლინიკებისთვის — BEQSON',
        'desc': 'სტომატოლოგიური კლინიკების ვებსაიტები: სერვისები, ექიმები, ონლაინ ჩაწერა, ლოკალური SEO, მრავალენოვანი გვერდები და ლიდების სისტემა. ფასი 299 ₾-დან.',
        'locale': 'ka_GE',
        'image': 'https://beqson.com/assets/concepts/ka/dentists-og.jpg',
        'alt': 'სტომატოლოგიური კლინიკის ვებსაიტის შექმნა — BEQSON',
        'h1_old': 'თავდაჯერებული ღიმილი<br>ნდობით იწყება.',
        'h1_new': 'ვებსაიტების შექმნა<br>სტომატოლოგებისა და კლინიკებისთვის.',
        'lead_old': 'ნათელი და მშვიდი საიტი სტომატოლოგიური კლინიკისთვის. წარმოვაჩენთ ექიმებს, სერვისებსა და გარემოს, რათა პირველი ვიზიტის დაგეგმვა გამარტივდეს.',
        'lead_new': 'ვებსაიტები სტომატოლოგიური კლინიკებისა და კერძო სტომატოლოგებისთვის: სერვისები, ექიმები, ონლაინ ჩაწერა, ლოკალური SEO და მრავალენოვანი სტრუქტურა.',
        'home': 'მთავარი', 'industry': 'სტომატოლოგები',
        'service': 'ვებსაიტების შექმნა და SEO სტომატოლოგიური კლინიკებისთვის',
        'service_type': 'სტომატოლოგიური ვებსაიტის დიზაინი, დეველოპმენტი და SEO',
        'faq': [
            ('რა უნდა ჰქონდეს სტომატოლოგიური კლინიკის ვებსაიტს?', 'სერვისების გვერდები, ექიმების პროფილები, კლინიკის ინფორმაცია, მისამართი და სამუშაო საათები, საკონტაქტო გზები და ჩაწერის მარტივი პროცესი.'),
            ('შესაძლებელია ონლაინ ჩაწერის დამატება?', 'დიახ. შესაძლებელია ჩაწერის ფორმის, ვიზიტის მოთხოვნის, ტელეფონის, WhatsApp-ის და სხვა საკონტაქტო არხების დაკავშირება.'),
            ('აკეთებთ ლოკალურ SEO-ს სტომატოლოგებისთვის?', 'დიახ. ვამზადებთ სერვისების სტრუქტურას, მეტამონაცემებს, შიდა ბმულებს და ლოკალური ძიების საფუძველს. კონკრეტულ პოზიციებს არ ვიძლევით გარანტიას.'),
            ('რა ღირს სტომატოლოგიური ვებსაიტი?', 'BEQSON-ის საწყისი შეთავაზება კომპაქტური საიტისთვის იწყება 299 ₾-დან. საბოლოო ფასი დამოკიდებულია გვერდებზე, ენებზე, ჩაწერაზე, SEO-ზე, CRM-ზე და დამატებით ფუნქციებზე.')
        ],
        'section': '''<!-- DENTISTS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">ვებსაიტი სტომატოლოგიისთვის</p><h2>აგებულია ისე,<br>როგორც პაციენტი ირჩევს კლინიკას.</h2></div><p>სტომატოლოგიის საიტმა სწრაფად უნდა უპასუხოს სამ კითხვას: რა სერვისები გაქვთ, ვინ არიან ექიმები და როგორ შეიძლება ჩაწერა. დიზაინს ვაერთიანებთ SEO სტრუქტურასთან და მარტივ საკონტაქტო გზებთან.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>SEO გვერდები სერვისებისთვის</h3><p>ცალკე გვერდები იმპლანტაციის, ორთოდონტიის, ჰიგიენის, ესთეტიკური სტომატოლოგიის და სხვა მიმართულებებისთვის.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>ექიმები და ნდობა</h3><p>ექიმების პროფილები, განათლება, სამუშაო ენები, კლინიკის ფოტოები და პრაქტიკული ინფორმაცია გადაჭარბებული სამედიცინო დაპირებების გარეშე.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>მარტივი ჩაწერა</h3><p>ჩაწერის ფორმა, ტელეფონი, WhatsApp და მკაფიო ღილაკები ამცირებს გზას ძიებიდან პირველ ვიზიტამდე.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>ლოკალური SEO და ენები</h3><p>ლოკაცია, რუკები და რამდენიმე ენობრივი ვერსია ეხმარება კლინიკას როგორც ადგილობრივ, ისე უცხოელ პაციენტებთან მუშაობაში.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ძიება · ნდობა · ჩაწერა</p><h2>Google-ის ძიებიდან — ვიზიტამდე.</h2><p class="lead">საიტს ვაწყობთ პაციენტის გზის მიხედვით და ვაერთებთ ანალიტიკას, რათა კლინიკამ დაინახოს რომელი გვერდები და არხები მოაქვს მომართვები.</p><a class="text-link" href="/ka/audit/">არსებული საიტის შემოწმება <svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></a></div><ol class="channel-list"><li><span>01</span><p>საძიებო გვერდები სერვისებისა და ქალაქის მიხედვით</p></li><li><span>02</span><p>ექიმები, კლინიკა და ნდობის ფაქტორები</p></li><li><span>03</span><p>ჩაწერა, მომართვების ანალიტიკა და CRM</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">საწყისი ფასები</p><h2>დაიწყეთ მარტივად.<br>გააფართოვეთ ზრდასთან ერთად.</h2></div><p>სტარტზე სტომატოლოგიური საიტის შექმნა შესაძლებელია <strong>299 ₾-დან</strong>. ჩვენთან დაკავშირებამდე შეგიძლიათ უფასოდ შეამოწმოთ არსებული საიტი ან გამოთვალოთ ახალი პროექტის ფასი.</p></div><div class="features-grid"><article class="feature-card"><h3>უფასო SEO აუდიტი</h3><p>SEO Score, ტექნიკური შემოწმებები და პრიორიტეტული სამოქმედო გეგმა.</p><a class="text-link" href="/ka/audit/">საიტის შემოწმება →</a></article><article class="feature-card"><h3>ღირებულების კალკულატორი</h3><p>უპასუხეთ ხუთ კითხვას და მიიღეთ სავარაუდო ფასის დიაპაზონი.</p><a class="text-link" href="/ka/calculator/">ღირებულების გამოთვლა →</a></article><article class="feature-card"><h3>299 ₾-დან</h3><p>საწყისი ფასი კომპაქტური საიტისთვის BEQSON-ის გაშვების პერიოდში.</p><a class="text-link" href="#contact">პროექტის განხილვა →</a></article><article class="feature-card"><h3>მარტივად ფართოვდება</h3><p>შემდგომ დავამატებთ სერვისებს, ენებს, ანალიტიკას, CRM-ს და ჩაწერის ინტეგრაციას.</p><a class="text-link" href="/ka/tools/">უფასო ინსტრუმენტები →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>კითხვები სტომატოლოგიურ<br>ვებსაიტზე.</h2></div><p>მოკლე პასუხები სტომატოლოგის ან კლინიკის საიტის დაწყებამდე.</p></div><div class="features-grid"><article class="feature-card"><h3>რა უნდა ჰქონდეს კლინიკის საიტს?</h3><p>სერვისები, ექიმები, კლინიკის ინფორმაცია, მისამართი, სამუშაო საათები, კონტაქტები და ჩაწერის მარტივი გზა.</p></article><article class="feature-card"><h3>შეიძლება ონლაინ ჩაწერა?</h3><p>დიახ. დავაკავშირებთ ჩაწერის ფორმას, ვიზიტის მოთხოვნას, ტელეფონს, WhatsApp-ს და სხვა არხებს.</p></article><article class="feature-card"><h3>აკეთებთ ლოკალურ SEO-ს?</h3><p>დიახ — სერვისების სტრუქტურა, მეტამონაცემები, შიდა ბმულები და ლოკალური ძიების საფუძველი. პოზიციებს არ ვიძლევით გარანტიას.</p></article><article class="feature-card"><h3>რა ღირს საიტი?</h3><p>საწყისი ფასი 299 ₾-დან იწყება. საბოლოო ღირებულება დამოკიდებულია გვერდებზე, ენებზე, ჩაწერაზე, SEO-სა და CRM-ზე.</p></article></div></div></section>
<!-- /DENTISTS_SEO_V1 -->'''
    }
}


def meta(name, value):
    return f'<meta name="{name}" content="{value}">' 


def prop(name, value):
    return f'<meta property="{name}" content="{value}">' 


def apply(lang, c):
    p = c['path']
    s = p.read_text(encoding='utf-8')

    s = re.sub(r'<title>.*?</title>', f"<title>{c['title']}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', meta('description', c['desc']), s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', '<link rel="alternate" hreflang="x-default" href="https://beqson.com/en/dentists/">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', prop('og:title', c['title']), s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', prop('og:description', c['desc']), s, count=1)
    s = re.sub(r'<meta property="og:image:alt" content="[^"]*">', prop('og:image:alt', c['alt']), s, count=1)
    s = re.sub(r'<meta name="twitter:image:alt" content="[^"]*">', meta('twitter:image:alt', c['alt']), s, count=1)

    if c['h1_old'] in s:
        s = s.replace(c['h1_old'], c['h1_new'], 1)
    else:
        s = re.sub(r'(<div class="industry-label">.*?</div>)<h1>.*?</h1>', r'\1<h1>' + c['h1_new'] + '</h1>', s, count=1, flags=re.S)
    if c['lead_old'] in s:
        s = s.replace(c['lead_old'], c['lead_new'], 1)

    graph = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'Organization', '@id': 'https://beqson.com/#organization', 'name': 'BEQSON Digital Studio', 'url': 'https://beqson.com/', 'logo': 'https://beqson.com/assets/beqson-mark-v3.png', 'email': 'digitalstudiobeqson@gmail.com', 'telephone': '+995551739333', 'sameAs': ['https://t.me/digital_studio_beqson']},
            {'@type': 'WebPage', '@id': c['url'] + '#webpage', 'url': c['url'], 'name': c['title'], 'description': c['desc'], 'inLanguage': lang, 'publisher': {'@id': 'https://beqson.com/#organization'}},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': c['home'], 'item': f'https://beqson.com/{lang}/'},
                {'@type': 'ListItem', 'position': 2, 'name': c['industry'], 'item': c['url']}
            ]},
            {'@type': 'Service', 'name': c['service'], 'description': c['desc'], 'provider': {'@id': 'https://beqson.com/#organization'}, 'url': c['url'], 'serviceType': c['service_type']},
            {'@type': 'FAQPage', 'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']
            ]}
        ]
    }
    js = '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False, separators=(',', ':')) + '</script>'
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', js, s, count=1, flags=re.S)

    s = re.sub(r'<!-- DENTISTS_SEO_V1 -->.*?<!-- /DENTISTS_SEO_V1 -->\s*', '', s, flags=re.S)
    marker = '<section class="contact-section section" id="contact">'
    if marker not in s:
        raise RuntimeError(f'contact marker missing: {p}')
    s = s.replace(marker, c['section'] + '\n' + marker, 1)

    p.write_text(s, encoding='utf-8')
    print('updated', p)


for lang, cfg in CFG.items():
    apply(lang, cfg)
