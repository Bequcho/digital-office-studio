from pathlib import Path
import re, json

CONFIG = {
'en': {
 'path':'en/autoservices/index.html',
 'title':'Auto Repair & Detailing Website Design + SEO | BEQSON',
 'desc':'Website design for auto repair shops and detailing studios: service pages, local SEO, before-and-after work, booking flows, analytics and CRM-ready enquiries.',
 'h1':'Auto service website design<br>built to drive bookings.',
 'lead':'Websites for auto repair shops and detailing studios with service-focused SEO, strong proof of work, local search visibility and a fast path from Google to booking.',
 'og_alt':'Auto service and detailing website design by BEQSON',
 'service_name':'Auto service and detailing website design and SEO',
 'service_type':'Auto service website design, development and SEO',
 'crumb':'Auto service / detailing',
 'home':'Home',
 'inlang':'en',
 'price':'$149',
 'features':[
   ('Service pages that match search intent','Create focused pages for diagnostics, maintenance, paint correction, ceramic coating, PPF, polishing and the services you actually sell.'),
   ('Before-and-after proof','Show real vehicles, the problem, process, materials and finished result so visitors can judge quality before they contact you.'),
   ('Local SEO + vehicle brands','Build search visibility around your city, neighbourhood, services and the vehicle brands or categories you specialise in.'),
   ('Booking + CRM-ready leads','Collect the service, car model, preferred date and contact details, then pass each enquiry into a measurable lead workflow.')
 ],
 'path_title':'From local search to a booked car.',
 'path_lead':'Turn service and location searches into clear proof, fast contact and trackable bookings.',
 'steps':['Google search for a service, car brand and location','Service page + real work + trust signals','Booking request, WhatsApp or call captured in CRM'],
 'seo_eyebrow':'SEO FOR AUTO SERVICES',
 'seo_title':'Promote the services people actually search for.',
 'seo_intro':'A strong auto business website should not rank only for your company name. We structure pages around real commercial intent so each important service can become an entry point from search.',
 'seo_cards':[
   ('Service SEO','Separate landing pages for detailing, polishing, ceramic coating, diagnostics, maintenance and other high-value services.'),
   ('Local SEO','City and service-area signals, map/profile consistency and location-focused content for customers searching nearby.'),
   ('Brand specialisation','Where it is genuine, create useful pages around the makes, vehicle types or specialist equipment your workshop works with.')
 ],
 'price_title':'Launch pricing for auto businesses',
 'price_text':'A focused starter website begins from $149. Larger service catalogues, multilingual pages, advanced SEO, booking flows and CRM integrations are scoped separately.',
 'audit':'Run free SEO Audit', 'calc':'Estimate website cost',
 'faq_title':'Auto service website FAQ',
 'faqs':[
   ('What should an auto repair or detailing website include?','Clear service pages, real work examples, location and opening hours, contact options, trust signals and a fast way to request a booking or quote.'),
   ('Can you create separate pages for each service?','Yes. High-value services such as detailing, polishing, ceramic coating, PPF, diagnostics or maintenance can each have focused pages for stronger search intent and conversion.'),
   ('Do you provide local SEO for auto services?','Yes. We can structure service and location pages, improve metadata and internal linking, and prepare the website for local search. Specific rankings are never guaranteed.'),
   ('Can enquiries go into a CRM?','Yes. Forms can collect the requested service, vehicle information and contact details and feed them into a CRM-ready workflow for follow-up and source tracking.')
 ]
},
'ru': {
 'path':'ru/autoservices/index.html',
 'title':'Сайт для автосервиса и детейлинга + SEO | BEQSON',
 'desc':'Создание сайтов для автосервисов и детейлинг-студий: страницы услуг, локальное SEO, работы до/после, запись, аналитика и заявки в CRM.',
 'h1':'Сайт для автосервиса,<br>который приводит записи.',
 'lead':'Создаём сайты для автосервисов и детейлинг-студий: отдельные страницы услуг, локальное SEO, сильная демонстрация работ и быстрый путь из Google к записи.',
 'og_alt':'Создание сайта для автосервиса и детейлинга — BEQSON',
 'service_name':'Создание сайта и SEO для автосервиса и детейлинга',
 'service_type':'Создание и SEO-продвижение сайтов для автосервисов и детейлинг-студий',
 'crumb':'Автосервисы / детейлинг',
 'home':'Главная',
 'inlang':'ru',
 'price':'9 900 ₽',
 'features':[
   ('Страницы конкретных услуг','Отдельно показываем диагностику, обслуживание, полировку, керамику, защитные плёнки и другие услуги, которые реально продаёт сервис.'),
   ('Работы «до / после»','Реальные автомобили, задача, процесс, материалы и результат помогают доказать качество ещё до звонка.'),
   ('Локальное SEO + марки авто','Продвигаем услуги по городу и району, а при реальной специализации — по маркам и категориям автомобилей.'),
   ('Запись + заявки в CRM','Собираем услугу, модель автомобиля, желаемую дату и контакт клиента, чтобы обращения не терялись и измерялись по источникам.')
 ],
 'path_title':'Из локального поиска — к записи автомобиля.',
 'path_lead':'Превращаем запросы по услуге и локации в доказательство качества, быстрый контакт и измеримую запись.',
 'steps':['Поиск услуги, марки автомобиля и города','Страница услуги + реальные работы + доверие','Запись, WhatsApp или звонок с фиксацией заявки'],
 'seo_eyebrow':'SEO ДЛЯ АВТОБИЗНЕСА',
 'seo_title':'Продвигаем не «автосервис вообще», а конкретные услуги.',
 'seo_intro':'Сильный сайт должен находиться не только по названию компании. Структурируем страницы под коммерческие запросы, чтобы каждая важная услуга могла приводить клиента из поиска.',
 'seo_cards':[
   ('SEO услуг','Отдельные посадочные под детейлинг, полировку, керамику, PPF, диагностику, ТО и другие приоритетные направления.'),
   ('Локальное SEO','Город, район, зона обслуживания, согласованные данные в картах и контент под тех, кто ищет сервис рядом.'),
   ('Специализация по авто','Если она реальная — создаём полезные страницы под марки, типы автомобилей или специализированное оборудование сервиса.')
 ],
 'price_title':'Стартовая цена для автобизнеса',
 'price_text':'Сфокусированный стартовый сайт — от 9 900 ₽. Большой каталог услуг, мультиязычность, расширенное SEO, онлайн-запись и CRM-интеграции рассчитываются отдельно.',
 'audit':'Бесплатный SEO-аудит', 'calc':'Рассчитать стоимость сайта',
 'faq_title':'Частые вопросы об автосервисных сайтах',
 'faqs':[
   ('Что должно быть на сайте автосервиса или детейлинга?','Понятные страницы услуг, реальные примеры работ, адрес и часы работы, способы связи, факторы доверия и быстрый путь к записи или запросу цены.'),
   ('Можно ли сделать отдельную страницу для каждой услуги?','Да. Детейлинг, полировка, керамика, защитная плёнка, диагностика, ТО и другие важные услуги могут получить отдельные SEO-страницы.'),
   ('Вы делаете локальное SEO для автосервисов?','Да. Можем выстроить страницы услуг и локаций, метаданные и внутренние ссылки и подготовить сайт к локальному поиску. Конкретные позиции в Google не гарантируются.'),
   ('Можно отправлять заявки сразу в CRM?','Да. Форма может собирать услугу, автомобиль и контакты клиента и передавать заявку в CRM-сценарий для дальнейшей работы и учёта источника.')
 ]
},
'ka': {
 'path':'ka/autoservices/index.html',
 'title':'ავტოსერვისისა და დეტეილინგის ვებსაიტი + SEO | BEQSON',
 'desc':'ვებსაიტები ავტოსერვისებისა და დეტეილინგის სტუდიებისთვის: სერვისების გვერდები, ლოკალური SEO, ნამუშევრები, ჩაწერა, ანალიტიკა და CRM-ready ლიდები.',
 'h1':'ავტოსერვისის ვებსაიტი,<br>რომელსაც ჩაწერები მოაქვს.',
 'lead':'ვქმნით საიტებს ავტოსერვისებისა და დეტეილინგის სტუდიებისთვის — ცალკე სერვისების გვერდებით, ლოკალური SEO-თი, რეალური ნამუშევრებით და Google-იდან ჩაწერამდე მოკლე გზით.',
 'og_alt':'ავტოსერვისისა და დეტეილინგის ვებსაიტის შექმნა — BEQSON',
 'service_name':'ავტოსერვისისა და დეტეილინგის ვებსაიტის შექმნა და SEO',
 'service_type':'ავტოსერვისისა და დეტეილინგის ვებსაიტის შექმნა, განვითარება და SEO',
 'crumb':'ავტოსერვისი / დეტეილინგი',
 'home':'მთავარი',
 'inlang':'ka',
 'price':'299 ₾',
 'features':[
   ('ცალკე გვერდები სერვისებისთვის','დიაგნოსტიკა, ტექნიკური მომსახურება, პოლირება, კერამიკა, დამცავი ფირი და სხვა რეალური სერვისები ცალ-ცალკე და გასაგებად.'),
   ('ნამუშევრები „მანამდე / შემდეგ“','რეალური ავტომობილები, პრობლემა, პროცესი, გამოყენებული მასალები და შედეგი ხარისხს კონტაქტამდე აჩვენებს.'),
   ('ლოკალური SEO + ავტომარკები','სერვისებს ქალაქისა და რაიონის მიხედვით ვაწყობთ, ხოლო რეალური სპეციალიზაციის შემთხვევაში — ავტომარკებისა და კატეგორიების მიხედვითაც.'),
   ('ჩაწერა + CRM-ready ლიდები','ვაგროვებთ სერვისს, ავტომობილის მოდელს, სასურველ თარიღსა და კონტაქტს, რათა არცერთი მოთხოვნა არ დაიკარგოს.')
 ],
 'path_title':'ლოკალური ძიებიდან — ავტომობილის ჩაწერამდე.',
 'path_lead':'სერვისისა და ლოკაციის ძიებას ვაქცევთ ხარისხის მტკიცებულებად, სწრაფ კონტაქტად და გაზომვად ჩაწერად.',
 'steps':['სერვისის, ავტომარკისა და ქალაქის ძიება','სერვისის გვერდი + რეალური ნამუშევრები + ნდობა','ჩაწერა, WhatsApp ან ზარი — მოთხოვნის დაფიქსირებით'],
 'seo_eyebrow':'SEO ავტობიზნესისთვის',
 'seo_title':'ვაწინაურებთ კონკრეტულ სერვისებს და არა მხოლოდ კომპანიის სახელს.',
 'seo_intro':'ძლიერი საიტი მხოლოდ ბრენდის სახელით არ უნდა იძებნებოდეს. გვერდებს კომერციული მოთხოვნების მიხედვით ვაწყობთ, რათა თითოეულ მნიშვნელოვან სერვისს Google-იდან კლიენტის მოყვანა შეეძლოს.',
 'seo_cards':[
   ('სერვისების SEO','ცალკე გვერდები დეტეილინგის, პოლირების, კერამიკის, PPF-ის, დიაგნოსტიკის, ტექნიკური მომსახურებისა და სხვა მიმართულებებისთვის.'),
   ('ლოკალური SEO','ქალაქი, რაიონი, მომსახურების არეალი, რუკების მონაცემების თანმიმდევრულობა და კონტენტი ახლომდებარე კლიენტებისთვის.'),
   ('ავტომარკების სპეციალიზაცია','თუ ეს რეალური უპირატესობაა, ვქმნით სასარგებლო გვერდებს კონკრეტული მარკების, ავტომობილის ტიპებისა ან სპეციალიზებული აღჭურვილობისთვის.')
 ],
 'price_title':'საწყისი ფასი ავტობიზნესისთვის',
 'price_text':'ფოკუსირებული საწყისი საიტი — 299 ₾-დან. დიდი სერვისების კატალოგი, რამდენიმე ენა, გაფართოებული SEO, ონლაინ ჩაწერა და CRM ინტეგრაციები ცალკე ფასდება.',
 'audit':'უფასო SEO აუდიტი', 'calc':'საიტის ღირებულების გამოთვლა',
 'faq_title':'ხშირი კითხვები ავტოსერვისის საიტებზე',
 'faqs':[
   ('რა უნდა იყოს ავტოსერვისის ან დეტეილინგის საიტზე?','გასაგები სერვისების გვერდები, რეალური ნამუშევრები, მისამართი და სამუშაო საათები, საკონტაქტო გზები, ნდობის ელემენტები და სწრაფი ჩაწერა ან ფასის მოთხოვნა.'),
   ('შეიძლება თითოეული სერვისისთვის ცალკე გვერდი გაკეთდეს?','დიახ. დეტეილინგს, პოლირებას, კერამიკას, დამცავ ფირს, დიაგნოსტიკას, ტექნიკურ მომსახურებას და სხვა მნიშვნელოვან სერვისებს შეიძლება ჰქონდეს საკუთარი SEO გვერდი.'),
   ('აკეთებთ ლოკალურ SEO-ს ავტოსერვისებისთვის?','დიახ. შეგვიძლია დავაწყოთ სერვისებისა და ლოკაციების გვერდები, მეტამონაცემები და შიდა ბმულები და მოვამზადოთ საიტი ლოკალური ძიებისთვის. კონკრეტული პოზიციები გარანტირებული არ არის.'),
   ('შეიძლება მოთხოვნები პირდაპირ CRM-ში გადავიდეს?','დიახ. ფორმა აგროვებს სერვისს, ავტომობილის მონაცემებსა და კლიენტის კონტაქტს და გადასცემს მოთხოვნას CRM-ready პროცესში შემდგომი მუშაობისა და წყაროს აღრიცხვისთვის.')
 ]
}
}

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def build_schema(lang,c):
    base=f'https://beqson.com/{lang}/autoservices/'
    faq=[]
    for q,a in c['faqs']:
        faq.append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
    graph={
      '@context':'https://schema.org',
      '@graph':[
        {'@type':'Organization','@id':'https://beqson.com/#organization','name':'BEQSON Digital Studio','url':'https://beqson.com/','logo':'https://beqson.com/assets/beqson-mark-v3.png','email':'digitalstudiobeqson@gmail.com','telephone':'+995551739333','sameAs':['https://t.me/digital_studio_beqson']},
        {'@type':'WebPage','@id':base+'#webpage','url':base,'name':c['title'],'description':c['desc'],'inLanguage':c['inlang'],'publisher':{'@id':'https://beqson.com/#organization'}},
        {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':c['home'],'item':f'https://beqson.com/{lang}/'},{'@type':'ListItem','position':2,'name':c['crumb'],'item':base}]},
        {'@type':'Service','name':c['service_name'],'description':c['desc'],'provider':{'@id':'https://beqson.com/#organization'},'url':base,'serviceType':c['service_type']},
        {'@type':'FAQPage','mainEntity':faq}
      ]
    }
    return json.dumps(graph, ensure_ascii=False, separators=(',',':'))

def build_sections(lang,c):
    feature_html=''.join(f'<article class="feature-card"><span class="feature-number">0{i}</span><span class="icon-tile small"><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#{icon}"></use></svg></span><h3>{h}</h3><p>{p}</p></article>' for i,((h,p),icon) in enumerate(zip(c['features'],['layers','sparkle','map','check']),1))
    steps=''.join(f'<li><span>0{i}</span><p>{s}</p><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg></li>' for i,s in enumerate(c['steps'],1))
    seo_cards=''.join(f'<article class="feature-card"><span class="feature-number">0{i}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(c['seo_cards'],1))
    faq_cards=''.join(f'<article class="feature-card"><h3>{q}</h3><p>{a}</p></article>' for q,a in c['faqs'])
    if lang=='ru': detail='Что важно именно<br>для автосервиса и детейлинга.'; detailp='Соединяем сильную визуальную подачу с поисковой структурой и понятной записью.'; price_label='BEQSON / СТАРТ'; faq_eye='FAQ'; price_btn='Обсудить проект'
    elif lang=='ka': detail='რა არის მნიშვნელოვანი<br>ავტოსერვისისა და დეტეილინგისთვის.'; detailp='ვაერთიანებთ ძლიერ ვიზუალურ პრეზენტაციას, საძიებო სტრუქტურასა და მარტივ ჩაწერას.'; price_label='BEQSON / START'; faq_eye='FAQ'; price_btn='პროექტის განხილვა'
    else: detail='What matters for<br>auto service & detailing.'; detailp='Combine strong visual proof with search-focused structure and a simple booking path.'; price_label='BEQSON / LAUNCH'; faq_eye='FAQ'; price_btn='Discuss your project'
    return f'''<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">BEQSON / DETAIL</p><h2>{detail}</h2></div><p>{detailp}</p></div><div class="features-grid">{feature_html}</div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">SEO · LOCAL · BOOKINGS</p><h2>{c['path_title']}</h2><p class="lead">{c['path_lead']}</p></div><ol class="channel-list">{steps}</ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">{c['seo_eyebrow']}</p><h2>{c['seo_title']}</h2></div><p>{c['seo_intro']}</p></div><div class="features-grid">{seo_cards}</div><div class="actions" style="margin-top:28px"><a class="button primary" href="/{lang}/audit/">{c['audit']}</a><a class="text-link" href="/{lang}/calculator/">{c['calc']}<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow"></use></svg></a></div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">{price_label}</p><h2>{c['price_title']}</h2><p class="lead">{c['price_text']}</p><a class="button primary" href="#contact">{price_btn}</a></div><ol class="channel-list"><li><span>01</span><p>Start — {c['price']}</p></li><li><span>02</span><p>{c['audit']}</p></li><li><span>03</span><p>{c['calc']}</p></li></ol></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">{faq_eye}</p><h2>{c['faq_title']}</h2></div></div><div class="features-grid">{faq_cards}</div></div></section>
'''

def patch(lang,c):
    p=Path(c['path']); s=p.read_text(encoding='utf-8')
    s=re.sub(r'<title>.*?</title>',f'<title>{c["title"]}</title>',s,count=1)
    s=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{c["desc"]}">',s,count=1)
    s=s.replace(f'<link rel="alternate" hreflang="x-default" href="https://beqson.com/ka/autoservices/">',f'<link rel="alternate" hreflang="x-default" href="https://beqson.com/en/autoservices/">')
    s=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{c["title"]}">',s,count=1)
    s=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{c["desc"]}">',s,count=1)
    s=re.sub(r'<meta property="og:image:alt" content="[^"]*">',f'<meta property="og:image:alt" content="{c["og_alt"]}">',s,count=1)
    s=re.sub(r'<meta name="twitter:image:alt" content="[^"]*">',f'<meta name="twitter:image:alt" content="{c["og_alt"]}">',s,count=1)
    schema=build_schema(lang,c)
    s=re.sub(r'<script type="application/ld\+json">.*?</script>',f'<script type="application/ld+json">{schema}</script>',s,count=1,flags=re.S)
    # Hero text: replace first H1 and following lead only in the hero area.
    hero_start=s.index('<section class="industry-hero">')
    hero_end=s.index('</section>',hero_start)+10
    hero=s[hero_start:hero_end]
    hero=re.sub(r'<h1>.*?</h1>',f'<h1>{c["h1"]}</h1>',hero,count=1,flags=re.S)
    hero=re.sub(r'<p class="lead">.*?</p>',f'<p class="lead">{c["lead"]}</p>',hero,count=1,flags=re.S)
    s=s[:hero_start]+hero+s[hero_end:]
    new_sections=build_sections(lang,c)
    s,n=re.subn(r'<section class="section industry-features">.*?(?=<section class="contact-section section" id="contact">)',new_sections,s,count=1,flags=re.S)
    if n!=1: raise RuntimeError(f'{lang}: content sections not replaced')
    p.write_text(s,encoding='utf-8')

for lang,c in CONFIG.items(): patch(lang,c)
print('updated', ', '.join(c['path'] for c in CONFIG.values()))
