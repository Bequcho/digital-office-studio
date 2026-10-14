from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]

CFG = {
    'en': {
        'path': ROOT/'en/hotels/index.html',
        'url': 'https://beqson.com/en/hotels/',
        'title': 'Hotel Website Design & Direct Booking SEO | BEQSON',
        'desc': 'Website design for hotels, apartments and tourism businesses: room pages, destination SEO, multilingual structure, direct booking enquiries, analytics and CRM.',
        'og_locale': 'en_US',
        'og_image': 'https://beqson.com/assets/concepts/en/hotels-og.jpg',
        'alt': 'Hotel and apartment website design by BEQSON',
        'h1_old': 'A place guests<br>want to experience.',
        'h1_new': 'Hotel website design<br>built for direct enquiries.',
        'lead_old': 'An atmospheric website for a hotel, apartment or travel business. Help guests picture their stay and make it easy to ask about availability.',
        'lead_new': 'Websites for hotels, apartments and tourism businesses with room or property pages, destination SEO, multilingual content and clear direct enquiry or booking paths.',
        'breadcrumb_home': 'Home', 'breadcrumb_industry': 'Hotels / apartments / tourism',
        'service_name': 'Hotel, apartment and tourism website design and SEO',
        'service_type': 'Hotel website design, development and SEO',
        'faq': [
            ('What should a hotel website include?', 'Clear room or property pages, strong photography, amenities, location information, mobile-friendly navigation, availability or enquiry actions and trust-building details.'),
            ('Can you add direct booking or availability enquiries?', 'Yes. We can create direct enquiry and reservation forms, connect messenger channels and, where a provider supports it, integrate or link an existing booking engine.'),
            ('Do you provide SEO for hotels and apartments?', 'Yes. We can build pages around destinations, accommodation types and relevant local searches, improve metadata and internal linking, and prepare the site for search. Specific rankings are never guaranteed.'),
            ('How much does a hotel website cost?', 'Our international launch pricing starts from $149 for a focused starter website. Multiple room types, languages, booking integrations, CRM and advanced SEO increase the final scope.')
        ],
        'section': '''<!-- HOTELS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">HOTEL WEBSITE DESIGN</p><h2>Help guests picture the stay<br>and take the next step.</h2></div><p>A hospitality website should combine atmosphere with practical information: where to stay, what is included, why the location matters and how to enquire or book directly.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Room & property pages</h3><p>Photography, amenities, occupancy, location details and clear calls to enquire or book for every room, apartment or accommodation type.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Direct booking paths</h3><p>Reservation enquiries, WhatsApp, email or an existing booking engine can be connected so guests have a simple direct route from the website.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>Destination & local SEO</h3><p>Useful pages for destinations, neighbourhoods, accommodation types and travel intent create more relevant entry points from search.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Languages, analytics & CRM</h3><p>Multilingual pages, enquiry source tracking and CRM-ready lead capture help hospitality businesses understand where direct demand comes from.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">SEARCH → STAY → ENQUIRY</p><h2>A shorter route from Google<br>to a direct conversation.</h2><p class="lead">Attract relevant searches, present the stay clearly and give visitors an easy direct action without forcing them to hunt for contact details.</p></div><ol class="channel-list"><li><span>01</span><p>Destination and accommodation SEO pages</p></li><li><span>02</span><p>Room or property pages with clear availability actions</p></li><li><span>03</span><p>Analytics, enquiry source tracking and CRM-ready leads</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">LAUNCH PRICING</p><h2>Start with the essentials.<br>Expand as direct demand grows.</h2></div><p>International launch pricing starts from <strong>$149</strong>. Before contacting us, you can audit an existing site or estimate a new hospitality project for free.</p></div><div class="features-grid"><article class="feature-card"><h3>Free SEO Audit</h3><p>Check technical SEO, metadata and priority issues on an existing hotel or apartment website.</p><a class="text-link" href="/en/audit/">Run audit →</a></article><article class="feature-card"><h3>Website Cost Calculator</h3><p>Estimate pages, languages, SEO, CRM and booking-related features.</p><a class="text-link" href="/en/calculator/">Calculate cost →</a></article><article class="feature-card"><h3>Start from $149</h3><p>Launch a focused hospitality website and expand room types, destinations and integrations later.</p><a class="text-link" href="#contact">Discuss project →</a></article><article class="feature-card"><h3>International-ready</h3><p>Add languages and local search pages for guests from different markets.</p><a class="text-link" href="/en/tools/">Explore free tools →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Hotel website<br>questions.</h2></div><p>Practical answers for hotels, apartments and tourism businesses planning a stronger direct web presence.</p></div><div class="features-grid"><article class="feature-card"><h3>What should a hotel website include?</h3><p>Room or property pages, strong visuals, amenities, location details, mobile usability and clear enquiry or booking actions.</p></article><article class="feature-card"><h3>Can you add direct booking?</h3><p>We can build direct enquiry flows and connect supported third-party booking engines or reservation links where available.</p></article><article class="feature-card"><h3>Can the site target destinations in Google?</h3><p>Yes. We can structure useful pages around destinations, neighbourhoods and accommodation types as part of the SEO plan.</p></article><article class="feature-card"><h3>How much does it cost?</h3><p>International launch pricing starts from $149. Languages, room types, booking integrations, CRM and SEO scope determine the final price.</p></article></div></div></section>
<!-- /HOTELS_SEO_V1 -->'''
    },
    'ru': {
        'path': ROOT/'ru/hotels/index.html',
        'url': 'https://beqson.com/ru/hotels/',
        'title': 'Создание сайтов для отелей и апартаментов — BEQSON',
        'desc': 'Создание сайтов для отелей, апартаментов и туризма: номера и объекты, локальное SEO, прямые заявки на бронирование, несколько языков, аналитика и CRM. От 9 900 ₽.',
        'og_locale': 'ru_RU',
        'og_image': 'https://beqson.com/assets/concepts/ru/hotels-og.jpg',
        'alt': 'Создание сайтов для отелей и апартаментов — BEQSON',
        'h1_old': 'Место, в которое<br>хочется приехать.',
        'h1_new': 'Создание сайтов<br>для отелей и апартаментов.',
        'lead_old': 'Атмосферный сайт для отеля, апартаментов или туристического проекта. Помогаем гостю представить отдых и легко связаться для бронирования.',
        'lead_new': 'Сайты для отелей, апартаментов и туристического бизнеса: страницы номеров и объектов, SEO по локациям, несколько языков и понятный путь к прямой заявке или бронированию.',
        'breadcrumb_home': 'Главная', 'breadcrumb_industry': 'Отели / апартаменты / туризм',
        'service_name': 'Создание сайтов и SEO для отелей, апартаментов и туризма',
        'service_type': 'Создание, разработка и SEO сайтов для отелей и апартаментов',
        'faq': [
            ('Что должно быть на сайте отеля?', 'Страницы номеров или объектов с фотографиями, удобствами и условиями, информация о локации, мобильная версия и заметные кнопки заявки или бронирования.'),
            ('Можно ли принимать прямые заявки на бронирование?', 'Да. Можно сделать форму заявки, связать сайт с WhatsApp и email, а при наличии подходящего сервиса — подключить или дать прямую ссылку на существующий booking engine.'),
            ('Вы делаете SEO для отелей и апартаментов?', 'Да. Можно создавать страницы под направления, районы, типы размещения и локальные запросы, улучшать метаданные и перелинковку. Конкретные позиции в поиске не гарантируются.'),
            ('Сколько стоит сайт для отеля?', 'Стартовая цена BEQSON начинается от 9 900 ₽ за компактный сайт. Количество номеров, языки, интеграции бронирования, CRM и расширенное SEO увеличивают объём проекта.')
        ],
        'section': '''<!-- HOTELS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">САЙТ ДЛЯ ОТЕЛЯ</p><h2>Помогаем гостю представить отдых<br>и сделать следующий шаг.</h2></div><p>Сайт отеля должен соединять атмосферу и практичность: показать номера, преимущества локации, условия проживания и дать понятный способ обратиться напрямую.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>Номера и объекты</h3><p>Фото, удобства, вместимость, особенности, локация и отдельная кнопка заявки или бронирования для каждого варианта размещения.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>Прямые заявки</h3><p>Форма бронирования, WhatsApp, email или существующий сервис бронирования дают гостю простой прямой путь с сайта.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>SEO по направлениям</h3><p>Страницы под города, районы, курорты и типы размещения создают дополнительные точки входа из поиска.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>Языки, аналитика и CRM</h3><p>Мультиязычность, отслеживание источников и CRM помогают понимать, откуда приходят прямые обращения.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ПОИСК → ПРОЖИВАНИЕ → ЗАЯВКА</p><h2>Короче путь от Google<br>до прямого обращения.</h2><p class="lead">Привлекаем подходящий поисковый трафик, понятно показываем варианты проживания и даём гостю простой способ связаться напрямую.</p></div><ol class="channel-list"><li><span>01</span><p>SEO-страницы направлений и типов размещения</p></li><li><span>02</span><p>Страницы номеров с понятной заявкой на доступность</p></li><li><span>03</span><p>Аналитика, источники обращений и CRM</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">СТАРТОВЫЕ ЦЕНЫ</p><h2>Начните с основы.<br>Расширяйте сайт по мере роста.</h2></div><p>Стартовая цена сайта для отеля или апартаментов — <strong>от 9 900 ₽</strong>. Перед заказом можно бесплатно проверить текущий сайт или рассчитать новый проект.</p></div><div class="features-grid"><article class="feature-card"><h3>Бесплатный SEO-аудит</h3><p>Проверим техническое SEO, метаданные и основные проблемы текущего сайта.</p><a class="text-link" href="/ru/audit/">Проверить сайт →</a></article><article class="feature-card"><h3>Калькулятор стоимости</h3><p>Оцените проект с учётом страниц, языков, SEO, CRM и функций бронирования.</p><a class="text-link" href="/ru/calculator/">Рассчитать стоимость →</a></article><article class="feature-card"><h3>От 9 900 ₽</h3><p>Можно начать с компактного сайта объекта размещения и постепенно добавлять номера, направления и интеграции.</p><a class="text-link" href="#contact">Обсудить проект →</a></article><article class="feature-card"><h3>Для иностранных гостей</h3><p>Добавим языковые версии и страницы под разные рынки и направления.</p><a class="text-link" href="/ru/tools/">Бесплатные инструменты →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>Вопросы о сайте<br>для отеля.</h2></div><p>Что стоит продумать отелю, апартаментам или туристическому проекту перед запуском.</p></div><div class="features-grid"><article class="feature-card"><h3>Что должно быть на сайте отеля?</h3><p>Номера или объекты, фотографии, удобства, информация о локации, мобильная версия и понятная заявка или бронирование.</p></article><article class="feature-card"><h3>Можно принимать прямые заявки?</h3><p>Да. Сделаем формы и мессенджеры, а при наличии подходящего сервиса подключим или свяжем сайт с booking engine.</p></article><article class="feature-card"><h3>Можно продвигаться по локациям?</h3><p>Да. В SEO-структуру можно включить страницы городов, районов, курортов и типов размещения.</p></article><article class="feature-card"><h3>Сколько стоит сайт?</h3><p>Стартовая цена — от 9 900 ₽. Языки, количество номеров, интеграции, CRM и SEO определяют итоговый объём.</p></article></div></div></section>
<!-- /HOTELS_SEO_V1 -->'''
    },
    'ka': {
        'path': ROOT/'ka/hotels/index.html',
        'url': 'https://beqson.com/ka/hotels/',
        'title': 'სასტუმროებისა და აპარტამენტების ვებსაიტების შექმნა — BEQSON',
        'desc': 'ვებსაიტების შექმნა სასტუმროებისთვის, აპარტამენტებისა და ტურიზმისთვის: ნომრების გვერდები, ლოკალური SEO, პირდაპირი ჯავშნის მოთხოვნები, ენები, ანალიტიკა და CRM. 299 ₾-დან.',
        'og_locale': 'ka_GE',
        'og_image': 'https://beqson.com/assets/concepts/ka/hotels-og.jpg',
        'alt': 'სასტუმროებისა და აპარტამენტების ვებსაიტების შექმნა — BEQSON',
        'h1_old': 'ადგილი, რომლის<br>მონახულებაც გსურთ.',
        'h1_new': 'ვებსაიტების შექმნა<br>სასტუმროებისა და აპარტამენტებისთვის.',
        'lead_old': 'ატმოსფერული საიტი სასტუმროს, აპარტამენტების ან ტურისტული პროექტისთვის. სტუმარს ვეხმარებით წარმოიდგინოს დასვენება და მარტივად დაგიკავშირდეთ.',
        'lead_new': 'საიტები სასტუმროებისთვის, აპარტამენტებისა და ტურისტული ბიზნესისთვის — ნომრების გვერდებით, ლოკალური SEO-თი, მრავალენოვანი სტრუქტურით და პირდაპირი ჯავშნის ან მოთხოვნის მარტივი გზით.',
        'breadcrumb_home': 'მთავარი', 'breadcrumb_industry': 'სასტუმროები / აპარტამენტები / ტურიზმი',
        'service_name': 'სასტუმროებისა და აპარტამენტების ვებსაიტების შექმნა და SEO',
        'service_type': 'სასტუმროებისა და აპარტამენტების ვებსაიტების დიზაინი, შექმნა და SEO',
        'faq': [
            ('რა უნდა იყოს სასტუმროს ვებსაიტზე?', 'ნომრების ან ობიექტების გვერდები ფოტოებით, პირობებითა და ლოკაციით, მობილური ვერსია და მკაფიო ღილაკები მოთხოვნის ან ჯავშნისთვის.'),
            ('შეიძლება პირდაპირი ჯავშნის მოთხოვნების მიღება?', 'დიახ. შესაძლებელია ფორმის, WhatsApp-ისა და email-ის დაკავშირება, ხოლო შესაბამისი სერვისის არსებობის შემთხვევაში — არსებული booking engine-ის ინტეგრაცია ან პირდაპირი ბმული.'),
            ('აკეთებთ SEO-ს სასტუმროებისა და აპარტამენტებისთვის?', 'დიახ. შესაძლებელია გვერდების შექმნა ქალაქების, რაიონების, კურორტებისა და განთავსების ტიპებისთვის, მეტამონაცემებისა და შიდა ბმულების გაუმჯობესება. კონკრეტული პოზიციები გარანტირებული არ არის.'),
            ('რა ღირს სასტუმროს ვებსაიტი?', 'BEQSON-ის სასტარტო ფასი იწყება 299 ₾-დან კომპაქტური საიტისთვის. ენები, ნომრების რაოდენობა, ჯავშნის ინტეგრაციები, CRM და გაფართოებული SEO ზრდის პროექტის მოცულობას.')
        ],
        'section': '''<!-- HOTELS_SEO_V1 -->
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">სასტუმროს ვებსაიტი</p><h2>აჩვენეთ სტუმარს გამოცდილება<br>და გაუმარტივეთ შემდეგი ნაბიჯი.</h2></div><p>სასტუმროს საიტი უნდა აერთიანებდეს ატმოსფეროსა და პრაქტიკულ ინფორმაციას: ნომრები, ლოკაცია, პირობები და პირდაპირი კონტაქტის ან ჯავშნის მარტივი გზა.</p></div><div class="features-grid"><article class="feature-card"><span class="feature-number">01</span><h3>ნომრები და ობიექტები</h3><p>ფოტოები, პირობები, ტევადობა, ლოკაცია და ცალკე მოთხოვნის ან ჯავშნის მოქმედება თითოეული ვარიანტისთვის.</p></article><article class="feature-card"><span class="feature-number">02</span><h3>პირდაპირი მოთხოვნები</h3><p>ფორმა, WhatsApp, email ან არსებული ჯავშნის სერვისი სტუმარს საიტიდან პირდაპირი მოქმედების მარტივ გზას აძლევს.</p></article><article class="feature-card"><span class="feature-number">03</span><h3>ლოკალური და ტურისტული SEO</h3><p>ქალაქების, რაიონების, კურორტებისა და განთავსების ტიპების გვერდები ქმნის დამატებით შესასვლელებს საძიებო სისტემიდან.</p></article><article class="feature-card"><span class="feature-number">04</span><h3>ენები, ანალიტიკა და CRM</h3><p>მრავალენოვანი გვერდები, წყაროების მონიტორინგი და CRM დაგეხმარებათ გაიგოთ, საიდან მოდის პირდაპირი მოთხოვნები.</p></article></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">ძიება → განთავსება → მოთხოვნა</p><h2>მოკლე გზა Google-იდან<br>პირდაპირ კონტაქტამდე.</h2><p class="lead">ვიზიდავთ შესაბამის საძიებო ტრაფიკს, მკაფიოდ ვაჩვენებთ განთავსების ვარიანტებს და სტუმარს ვაძლევთ პირდაპირი კონტაქტის მარტივ გზას.</p></div><ol class="channel-list"><li><span>01</span><p>SEO გვერდები მიმართულებებისა და განთავსების ტიპებისთვის</p></li><li><span>02</span><p>ნომრების გვერდები ხელმისაწვდომობის მკაფიო მოთხოვნით</p></li><li><span>03</span><p>ანალიტიკა, მოთხოვნის წყაროები და CRM</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">სასტარტო ფასები</p><h2>დაიწყეთ საჭირო საფუძვლით.<br>გააფართოეთ საიტი ზრდასთან ერთად.</h2></div><p>სასტუმროს ან აპარტამენტების საიტის სასტარტო ფასი არის <strong>299 ₾-დან</strong>. შეკვეთამდე შეგიძლიათ უფასოდ შეამოწმოთ არსებული საიტი ან გამოთვალოთ ახალი პროექტი.</p></div><div class="features-grid"><article class="feature-card"><h3>უფასო SEO აუდიტი</h3><p>შეამოწმეთ ტექნიკური SEO, მეტამონაცემები და მიმდინარე საიტის მთავარი პრობლემები.</p><a class="text-link" href="/ka/audit/">საიტის შემოწმება →</a></article><article class="feature-card"><h3>ღირებულების კალკულატორი</h3><p>შეაფასეთ პროექტი გვერდების, ენების, SEO-ს, CRM-ისა და ჯავშნის ფუნქციების მიხედვით.</p><a class="text-link" href="/ka/calculator/">ღირებულების გამოთვლა →</a></article><article class="feature-card"><h3>299 ₾-დან</h3><p>დაიწყეთ კომპაქტური საიტით და მოგვიანებით დაამატეთ ნომრები, მიმართულებები და ინტეგრაციები.</p><a class="text-link" href="#contact">პროექტის განხილვა →</a></article><article class="feature-card"><h3>უცხოელი სტუმრებისთვის</h3><p>დავამატებთ ენებს და საძიებო გვერდებს სხვადასხვა ბაზრისა და მიმართულებისთვის.</p><a class="text-link" href="/ka/tools/">უფასო ინსტრუმენტები →</a></article></div></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">FAQ</p><h2>კითხვები სასტუმროს<br>ვებსაიტზე.</h2></div><p>რა უნდა გაითვალისწინოს სასტუმრომ, აპარტამენტებმა ან ტურისტულმა ბიზნესმა ახალი საიტის გაშვებამდე.</p></div><div class="features-grid"><article class="feature-card"><h3>რა უნდა იყოს სასტუმროს საიტზე?</h3><p>ნომრები ან ობიექტები, ფოტოები, პირობები, ლოკაცია, მობილური ვერსია და მკაფიო მოთხოვნა ან ჯავშანი.</p></article><article class="feature-card"><h3>შეიძლება პირდაპირი ჯავშნის მოთხოვნები?</h3><p>დიახ. დავამატებთ ფორმებსა და მესენჯერებს, ხოლო შესაბამისი სერვისის არსებობისას booking engine-ს დავუკავშირებთ.</p></article><article class="feature-card"><h3>შეიძლება ლოკაციებზე SEO?</h3><p>დიახ. SEO სტრუქტურაში შეიძლება შევიდეს ქალაქები, რაიონები, კურორტები და განთავსების ტიპები.</p></article><article class="feature-card"><h3>რა ღირს საიტი?</h3><p>სასტარტო ფასი არის 299 ₾-დან. ენები, ნომრები, ინტეგრაციები, CRM და SEO განსაზღვრავს საბოლოო მოცულობას.</p></article></div></div></section>
<!-- /HOTELS_SEO_V1 -->'''
    }
}

def schema(c, lang):
    graph = [
        {'@type':'Organization','@id':'https://beqson.com/#organization','name':'BEQSON Digital Studio','url':'https://beqson.com/','logo':'https://beqson.com/assets/beqson-mark-v3.png','email':'digitalstudiobeqson@gmail.com','telephone':'+995551739333','sameAs':['https://t.me/digital_studio_beqson']},
        {'@type':'WebPage','@id':c['url']+'#webpage','url':c['url'],'name':c['title'],'description':c['desc'],'inLanguage':lang,'publisher':{'@id':'https://beqson.com/#organization'}},
        {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':c['breadcrumb_home'],'item':f'https://beqson.com/{lang}/'},{'@type':'ListItem','position':2,'name':c['breadcrumb_industry'],'item':c['url']}]},
        {'@type':'Service','name':c['service_name'],'description':c['desc'],'provider':{'@id':'https://beqson.com/#organization'},'url':c['url'],'serviceType':c['service_type']},
        {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in c['faq']]}
    ]
    return json.dumps({'@context':'https://schema.org','@graph':graph}, ensure_ascii=False, separators=(',',':'))

def set_meta(html, c, lang):
    html = re.sub(r'<title>.*?</title>', f'<title>{c["title"]}</title>', html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{c["desc"]}">', html, count=1)
    html = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', '<link rel="alternate" hreflang="x-default" href="https://beqson.com/en/hotels/">', html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{c["title"]}">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{c["desc"]}">', html, count=1)
    html = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{c["alt"]}">', html, count=1)
    html = re.sub(r'<meta name="twitter:image:alt" content="[^"]*">', f'<meta name="twitter:image:alt" content="{c["alt"]}">', html, count=1)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">'+schema(c,lang)+'</script>', html, count=1, flags=re.S)
    return html

def patch(lang, c):
    p = c['path']
    html = p.read_text(encoding='utf-8')
    if '<!-- HOTELS_SEO_V1 -->' in html:
        print('already updated', p.relative_to(ROOT))
        return
    html = set_meta(html, c, lang)
    if c['h1_old'] not in html or c['lead_old'] not in html:
        raise RuntimeError(f'Hero source text not found in {p}')
    html = html.replace(c['h1_old'], c['h1_new'], 1)
    html = html.replace(c['lead_old'], c['lead_new'], 1)
    start = html.find('<section class="section industry-features">')
    end = html.find('<section class="contact-section section"', start)
    if start < 0 or end < 0:
        raise RuntimeError(f'Industry feature/contact markers not found in {p}')
    html = html[:start] + c['section'] + '\n' + html[end:]
    p.write_text(html, encoding='utf-8')
    print('updated', p.relative_to(ROOT))

for lang,c in CFG.items():
    patch(lang,c)
