from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]

CFG = {
    'en': {
        'path': ROOT/'en/realtors/index.html',
        'url': 'https://beqson.com/en/realtors/',
        'title': 'Real Estate Website Design & SEO for Realtors | BEQSON',
        'desc': 'Website design for real estate agents and agencies: property listings, location SEO, multilingual pages, lead capture, WhatsApp and CRM-ready enquiry flows.',
        'og_locale': 'en_US',
        'og_image': 'https://beqson.com/assets/concepts/en/realtors-og.jpg',
        'alt': 'Real estate website design for agents and agencies by BEQSON',
        'h1_old': 'Properties worth<br>a closer look.',
        'h1_new': 'Real estate website design<br>built to generate enquiries.',
        'lead_old': 'A website for an agent or agency where photography, property details and professional expertise create a compelling presentation.',
        'lead_new': 'Websites for real estate agents and agencies with property pages, location-focused SEO, multilingual structure and clear enquiry paths from every listing.',
        'breadcrumb_home': 'Home', 'breadcrumb_industry': 'Real estate',
        'service_name': 'Real estate website design and SEO for agents and agencies',
        'service_type': 'Real estate website design, development and SEO',
        'faq': [
            ('What should a real estate website include?', 'Clear property pages, strong photography, price and location details, agent profiles, enquiry buttons, mobile usability and pages for the areas and property types you serve.'),
            ('Can you build property listings and enquiry forms?', 'Yes. We can structure property catalogues and create listing-specific enquiry paths through forms, WhatsApp, Telegram or email, with CRM-ready lead capture.'),
            ('Do you provide SEO for real estate businesses?', 'Yes. We can build location and property-type pages, improve metadata and internal linking, and prepare the site for local search. Specific rankings are never guaranteed.'),
            ('How much does a real estate website cost?', 'Our international launch pricing starts from $149 for a focused starter website. Larger catalogues, multilingual pages, CRM and advanced SEO increase the final scope.')
        ],
        'section': '''<!-- REALTORS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">REAL ESTATE WEBSITE DESIGN</p><h2>Turn property interest<br>into a real conversation.</h2></div><p>A real estate website should make every listing easy to explore and every next step easy to take. We connect presentation, local search and enquiry capture in one system.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Property pages that sell the details</h3><p>Photos, price, location, specifications, amenities and a clear viewing or enquiry action on every listing.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Location & neighbourhood SEO</h3><p>Dedicated pages for cities, districts, neighbourhoods and property types create more relevant entry points from search.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Multilingual buyer journeys</h3><p>English, Georgian, Russian and other versions can support international buyers, investors and owners.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Lead capture & CRM</h3><p>Listing-specific forms, WhatsApp, Telegram, analytics and CRM-ready enquiries help you see which property generated each lead.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">SEARCH → PROPERTY → ENQUIRY</p><h2>A clearer route from Google<br>to a viewing request.</h2><p class="lead">Build pages around the places and property types people search for, then connect every listing to a simple enquiry action.</p></div><ol class="channel-list"><li><span>01</span><p>Location and neighbourhood landing pages</p></li><li><span>02</span><p>Property pages with specific enquiry context</p></li><li><span>03</span><p>CRM, analytics and source tracking for incoming leads</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">LAUNCH PRICING</p><h2>Start lean.<br>Add the catalogue as you grow.</h2></div><p>International launch pricing starts from <strong>$149</strong>. You can also run a free SEO audit or estimate the project before contacting us.</p></div><div class="features-grid"><article class="feature-card"><h3>Free SEO Audit</h3><p>Check technical SEO, metadata and priority issues on an existing real estate website.</p><a class="text-link" href="/en/audit/">Run audit →</a></article><article class="feature-card"><h3>Website Cost Calculator</h3><p>Estimate a new website based on pages, SEO, CRM, languages and other features.</p><a class="text-link" href="/en/calculator/">Calculate cost →</a></article><article class="feature-card"><h3>Start from $149</h3><p>Launch with a focused agent or agency website, then expand the catalogue and SEO structure.</p><a class="text-link" href="#contact">Discuss project →</a></article><article class="feature-card"><h3>International-ready</h3><p>Add languages, location pages and lead tracking for buyers from different markets.</p><a class="text-link" href="/en/tools/">Explore free tools →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Real estate website<br>questions.</h2></div><p>Practical answers for agents and agencies planning a stronger online presence.</p></div><div class="features-grid"><article class="feature-card"><h3>What should a real estate website include?</h3><p>Property pages, strong photography, location details, agent information, clear enquiry actions and mobile-friendly navigation.</p></article><article class="feature-card"><h3>Can you build property listings?</h3><p>Yes. Listings can have their own galleries, details and enquiry paths through forms or messengers.</p></article><article class="feature-card"><h3>Can the site target locations in Google?</h3><p>Yes. We can create relevant pages for cities, districts, neighbourhoods and property types as part of the SEO structure.</p></article><article class="feature-card"><h3>How much does it cost?</h3><p>International launch pricing starts from $149. Catalogue size, languages, CRM and SEO scope determine the final price.</p></article></div></div></section>
<!-- /REALTORS_SEO_V1 -->'''
    },
    'ru': {
        'path': ROOT/'ru/realtors/index.html',
        'url': 'https://beqson.com/ru/realtors/',
        'title': 'Создание сайтов для риелторов и агентств недвижимости — BEQSON',
        'desc': 'Создание сайтов для риелторов и агентств недвижимости: каталог объектов, SEO по районам, заявки с объектов, мессенджеры и CRM. От 9 900 ₽.',
        'og_locale': 'ru_RU',
        'og_image': 'https://beqson.com/assets/concepts/ru/realtors-og.jpg',
        'alt': 'Создание сайтов для риелторов и агентств недвижимости — BEQSON',
        'h1_old': 'Недвижимость,<br>которую хочется увидеть.',
        'h1_new': 'Создание сайтов<br>для риелторов и агентств.',
        'lead_old': 'Сайт для риелтора или агентства, где фотографии, детали объектов и личная экспертиза складываются в убедительную презентацию.',
        'lead_new': 'Сайты для риелторов и агентств недвижимости: карточки объектов, SEO по районам и типам недвижимости, мультиязычность и понятные заявки с каждого объекта.',
        'breadcrumb_home': 'Главная', 'breadcrumb_industry': 'Риелторы',
        'service_name': 'Создание сайтов и SEO для риелторов и агентств недвижимости',
        'service_type': 'Создание, разработка и SEO сайтов для недвижимости',
        'faq': [
            ('Что должно быть на сайте риелтора?', 'Карточки объектов с фото, ценой и локацией, профиль специалиста, понятные контакты, мобильная версия и страницы районов или типов недвижимости.'),
            ('Можно ли сделать каталог объектов и заявки по каждому объекту?', 'Да. У каждого объекта может быть своя страница и отдельная заявка через форму, WhatsApp, Telegram или email с передачей контекста в CRM.'),
            ('Вы делаете SEO для недвижимости?', 'Да. Можно создавать страницы под города, районы, жилые комплексы и типы недвижимости, настраивать метаданные и внутреннюю перелинковку. Позиции в поиске не гарантируются.'),
            ('Сколько стоит сайт для риелтора?', 'Стартовая цена BEQSON начинается от 9 900 ₽ за компактный сайт. Каталог, несколько языков, CRM и расширенное SEO увеличивают объём проекта.')
        ],
        'section': '''<!-- REALTORS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">САЙТ ДЛЯ НЕДВИЖИМОСТИ</p><h2>От интереса к объекту<br>до реальной заявки.</h2></div><p>Сайт риелтора должен не только красиво показывать недвижимость, но и помогать находить объекты через поиск, быстро сравнивать детали и легко записываться на просмотр.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Карточки объектов</h3><p>Фото, цена, район, характеристики, преимущества и отдельная кнопка заявки или записи на просмотр.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>SEO по районам и типам</h3><p>Отдельные страницы под города, районы, жилые комплексы, квартиры, дома и коммерческую недвижимость.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Несколько языков</h3><p>Русская, грузинская, английская и другие версии помогают работать с местными и иностранными покупателями.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Заявки и CRM</h3><p>Формы, WhatsApp, Telegram, аналитика и CRM сохраняют, с какого объекта пришёл каждый потенциальный клиент.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ПОИСК → ОБЪЕКТ → ЗАЯВКА</p><h2>Понятный путь от Google<br>до записи на просмотр.</h2><p class="lead">Создаём страницы под реальные локации и запросы, а каждую карточку объекта связываем с удобным способом обращения.</p></div><ol class="channel-list"><li><span>01</span><p>SEO-страницы районов и направлений</p></li><li><span>02</span><p>Заявка с конкретного объекта, а не без контекста</p></li><li><span>03</span><p>CRM и аналитика источников обращений</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">СТАРТОВЫЕ ЦЕНЫ</p><h2>Начните компактно.<br>Расширяйте каталог постепенно.</h2></div><p>Стартовая цена сайта для риелтора — <strong>от 9 900 ₽</strong>. Перед заказом можно бесплатно проверить текущий сайт или рассчитать новый проект.</p></div><div class="features-grid"><article class="feature-card"><h3>Бесплатный SEO-аудит</h3><p>Проверим техническое SEO, метаданные и основные проблемы текущего сайта.</p><a class="text-link" href="/ru/audit/">Проверить сайт →</a></article><article class="feature-card"><h3>Калькулятор стоимости</h3><p>Оцените сайт с учётом страниц, SEO, CRM, языков и дополнительных функций.</p><a class="text-link" href="/ru/calculator/">Рассчитать стоимость →</a></article><article class="feature-card"><h3>От 9 900 ₽</h3><p>Можно начать с компактного сайта специалиста или агентства и расширять его по мере роста.</p><a class="text-link" href="#contact">Обсудить проект →</a></article><article class="feature-card"><h3>Для международных клиентов</h3><p>Добавим языки, SEO по локациям и отслеживание заявок из разных рынков.</p><a class="text-link" href="/ru/tools/">Бесплатные инструменты →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Вопросы о сайте<br>для недвижимости.</h2></div><p>Что стоит продумать риелтору или агентству до запуска нового сайта.</p></div><div class="features-grid"><article class="feature-card"><h3>Что должно быть на сайте риелтора?</h3><p>Карточки объектов, фото, цена и локация, информация об агенте, удобные контакты и понятная мобильная версия.</p></article><article class="feature-card"><h3>Можно сделать каталог объектов?</h3><p>Да. У объектов могут быть собственные страницы, галереи, характеристики и отдельные формы заявки.</p></article><article class="feature-card"><h3>Можно продвигать районы в поиске?</h3><p>Да. Создаём полезные страницы под города, районы, жилые комплексы и типы недвижимости.</p></article><article class="feature-card"><h3>Сколько стоит сайт?</h3><p>Стартовая цена — от 9 900 ₽. Итог зависит от каталога, языков, SEO, CRM и других функций.</p></article></div></div></section>
<!-- /REALTORS_SEO_V1 -->'''
    },
    'ka': {
        'path': ROOT/'ka/realtors/index.html',
        'url': 'https://beqson.com/ka/realtors/',
        'title': 'უძრავი ქონების სააგენტოსა და აგენტის ვებსაიტი — BEQSON',
        'desc': 'ვებსაიტები უძრავი ქონების აგენტებისა და სააგენტოებისთვის: ობიექტები, ლოკალური SEO, მრავალენოვანი გვერდები, განაცხადები და CRM. ფასი 299 ₾-დან.',
        'og_locale': 'ka_GE',
        'og_image': 'https://beqson.com/assets/concepts/ka/realtors-og.jpg',
        'alt': 'უძრავი ქონების სააგენტოსა და აგენტის ვებსაიტი — BEQSON',
        'h1_old': 'უძრავი ქონება,<br>რომლის ნახვაც მოგინდება.',
        'h1_new': 'ვებსაიტები უძრავი ქონების<br>აგენტებისა და სააგენტოებისთვის.',
        'lead_old': 'საიტი აგენტისთვის ან სააგენტოსთვის, სადაც ფოტოები, ობიექტის დეტალები და პროფესიული გამოცდილება დამაჯერებელ პრეზენტაციას ქმნის.',
        'lead_new': 'ვქმნით უძრავი ქონების საიტებს ობიექტების გვერდებით, ლოკაციებზე ორიენტირებული SEO-თი, მრავალენოვანი სტრუქტურით და თითოეული ობიექტიდან მარტივი განაცხადით.',
        'breadcrumb_home': 'მთავარი', 'breadcrumb_industry': 'უძრავი ქონება',
        'service_name': 'უძრავი ქონების ვებსაიტების შექმნა და SEO',
        'service_type': 'უძრავი ქონების ვებსაიტის დიზაინი, დეველოპმენტი და SEO',
        'faq': [
            ('რა უნდა ჰქონდეს უძრავი ქონების კარგ ვებსაიტს?', 'ობიექტების ცალკე გვერდები ფოტოებით, ფასითა და ლოკაციით, აგენტის ინფორმაცია, მარტივი კონტაქტი, მობილური ვერსია და გვერდები იმ უბნებისა თუ ტიპებისთვის, რომლებზეც მუშაობთ.'),
            ('შესაძლებელია ობიექტების კატალოგი და ცალკე განაცხადები?', 'დიახ. თითოეულ ობიექტს შეიძლება ჰქონდეს საკუთარი გვერდი და განაცხადი ფორმით, WhatsApp-ით, Telegram-ით ან email-ით, CRM-ში შესაბამისი კონტექსტის გადაცემით.'),
            ('აკეთებთ SEO-ს უძრავი ქონებისთვის?', 'დიახ. შესაძლებელია ქალაქების, უბნების, კომპლექსებისა და ქონების ტიპების გვერდების შექმნა, მეტამონაცემებისა და შიდა ბმულების გამართვა. კონკრეტულ პოზიციებს არ ვპირდებით.'),
            ('რა ღირს უძრავი ქონების ვებსაიტი?', 'BEQSON-ის საწყისი ფასი იწყება 299 ₾-დან კომპაქტური საიტისთვის. კატალოგი, დამატებითი ენები, CRM და გაფართოებული SEO ზრდის პროექტის მოცულობას.')
        ],
        'section': '''<!-- REALTORS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">უძრავი ქონების ვებსაიტი</p><h2>ინტერესიდან ობიექტამდე<br>და რეალურ განაცხადამდე.</h2></div><p>უძრავი ქონების საიტმა უნდა აჩვენოს ობიექტი ხარისხიანად, დაეხმაროს მომხმარებელს დეტალების სწრაფად გაგებაში და მარტივად მიიყვანოს ნახვის მოთხოვნამდე.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>ობიექტების გვერდები</h3><p>ფოტოები, ფასი, უბანი, მახასიათებლები, უპირატესობები და კონკრეტული მოქმედება — კითხვა ან ნახვის დაჯავშნა.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>SEO უბნებისა და ტიპებისთვის</h3><p>ცალკე გვერდები ქალაქებისთვის, უბნებისთვის, საცხოვრებელი კომპლექსებისა და ქონების ტიპებისთვის.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>მრავალენოვანი სტრუქტურა</h3><p>ქართული, ინგლისური, რუსული და სხვა ენები ადგილობრივ და საერთაშორისო მყიდველებთან მუშაობაში გეხმარებათ.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>განაცხადები და CRM</h3><p>ფორმები, WhatsApp, Telegram, ანალიტიკა და CRM აჩვენებს, რომელი ობიექტიდან მოვიდა თითოეული ლიდი.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ძიება → ობიექტი → განაცხადი</p><h2>მარტივი გზა Google-დან<br>ნახვის მოთხოვნამდე.</h2><p class="lead">ვქმნით გვერდებს რეალური ლოკაციებისა და მოთხოვნების მიხედვით და თითოეულ ობიექტს ვუკავშირებთ მარტივ საკონტაქტო მოქმედებას.</p></div><ol class="channel-list"><li><span>01</span><p>SEO-გვერდები ქალაქებისა და უბნებისთვის</p></li><li><span>02</span><p>განაცხადი კონკრეტული ობიექტის კონტექსტით</p></li><li><span>03</span><p>CRM და განაცხადების წყაროს ანალიტიკა</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">საწყისი ფასები</p><h2>დაიწყეთ მარტივად.<br>კატალოგი ეტაპობრივად გაზარდეთ.</h2></div><p>უძრავი ქონების საიტის საწყისი ფასი არის <strong>299 ₾-დან</strong>. მანამდე შეგიძლიათ უფასოდ შეამოწმოთ არსებული საიტი ან გამოთვალოთ ახალი პროექტის ღირებულება.</p></div><div class="features-grid"><article class="feature-card"><h3>უფასო SEO აუდიტი</h3><p>შეამოწმეთ ტექნიკური SEO, მეტამონაცემები და მთავარი პრობლემები.</p><a class="text-link" href="/ka/audit/">საიტის შემოწმება →</a></article><article class="feature-card"><h3>ღირებულების კალკულატორი</h3><p>მიიღეთ შეფასება გვერდების, SEO-ს, CRM-ის, ენებისა და სხვა ფუნქციების მიხედვით.</p><a class="text-link" href="/ka/calculator/">ღირებულების გამოთვლა →</a></article><article class="feature-card"><h3>299 ₾-დან</h3><p>დაიწყეთ კომპაქტური აგენტის ან სააგენტოს საიტით და გააფართოვეთ საჭიროების მიხედვით.</p><a class="text-link" href="#contact">პროექტის განხილვა →</a></article><article class="feature-card"><h3>საერთაშორისო კლიენტებისთვის</h3><p>დავამატებთ ენებს, ლოკაციის SEO-ს და სხვადასხვა ბაზრიდან განაცხადების ანალიტიკას.</p><a class="text-link" href="/ka/tools/">უფასო ინსტრუმენტები →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>კითხვები უძრავი ქონების<br>ვებსაიტზე.</h2></div><p>მთავარი საკითხები აგენტებისა და სააგენტოებისთვის ახალი საიტის დაწყებამდე.</p></div><div class="features-grid"><article class="feature-card"><h3>რა უნდა ჰქონდეს უძრავი ქონების საიტს?</h3><p>ობიექტების გვერდები, ფოტოები, ფასი, ლოკაცია, აგენტის ინფორმაცია, მარტივი კონტაქტი და კარგი მობილური ვერსია.</p></article><article class="feature-card"><h3>შესაძლებელია ობიექტების კატალოგი?</h3><p>დიახ. თითოეულ ობიექტს შეიძლება ჰქონდეს საკუთარი გალერეა, დეტალები და განაცხადის ფორმა.</p></article><article class="feature-card"><h3>შესაძლებელია უბნების SEO?</h3><p>დიახ. ვქმნით სასარგებლო გვერდებს ქალაქების, უბნების, კომპლექსებისა და ქონების ტიპებისთვის.</p></article><article class="feature-card"><h3>რა ღირს საიტი?</h3><p>საწყისი ფასი 299 ₾-დან იწყება. საბოლოო ღირებულება დამოკიდებულია კატალოგზე, ენებზე, SEO-ზე, CRM-სა და სხვა ფუნქციებზე.</p></article></div></div></section>
<!-- /REALTORS_SEO_V1 -->'''
    }
}

def schema(c, lang):
    faq = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c['faq']]
    graph = [
        {"@type":"Organization","@id":"https://beqson.com/#organization","name":"BEQSON Digital Studio","url":"https://beqson.com/","logo":"https://beqson.com/assets/beqson-mark-v3.png","email":"digitalstudiobeqson@gmail.com","telephone":"+995551739333","sameAs":["https://t.me/digital_studio_beqson"]},
        {"@type":"WebPage","@id":c['url']+'#webpage',"url":c['url'],"name":c['title'],"description":c['desc'],"inLanguage":lang,"publisher":{"@id":"https://beqson.com/#organization"}},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":c['breadcrumb_home'],"item":f"https://beqson.com/{lang}/"},{"@type":"ListItem","position":2,"name":c['breadcrumb_industry'],"item":c['url']}]},
        {"@type":"Service","name":c['service_name'],"description":c['desc'],"provider":{"@id":"https://beqson.com/#organization"},"url":c['url'],"serviceType":c['service_type']},
        {"@type":"FAQPage","mainEntity":faq}
    ]
    return json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, separators=(',',':'))

def set_meta(html, c, lang):
    html = re.sub(r'<title>.*?</title>', f'<title>{c["title"]}</title>', html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{c["desc"]}">', html, count=1)
    html = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', '<link rel="alternate" hreflang="x-default" href="https://beqson.com/en/realtors/">', html, count=1)
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
    marker = '<section class="contact-section section" id="contact">'
    if '<!-- REALTORS_SEO_V1 -->' not in html:
        if marker not in html:
            raise RuntimeError(f'contact marker not found in {p}')
        html = html.replace(marker, c['section']+'\n'+marker, 1)
    p.write_text(html, encoding='utf-8')
    print('updated', p.relative_to(ROOT))

for lang,c in CFG.items():
    patch(lang,c)
