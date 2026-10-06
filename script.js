
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');
if (burger) {
  burger.addEventListener('click', () => nav.classList.toggle('open'));
}
document.querySelectorAll('#nav a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));

const translations = {
  ru: {
    pageTitle: 'BEQSON — сайты, SEO и поток клиентов для сервисного бизнеса',
    metaDescription: 'BEQSON создаёт сайты, настраивает локальное SEO, Google/Яндекс, CRM и систему заявок для сервисного бизнеса.',
    ogTitle: 'BEQSON Digital Studio',
    ogDescription: 'Сайт + SEO + локальный поиск + CRM + заявки.',
    consultLabel: 'Получить консультацию',
    navServices: 'Направления', navPricing: 'Цены', navGrowth: 'Рост клиентов', navCase: 'Кейс', navContacts: 'Контакты',
    heroKicker: 'Сайты • SEO • CRM • реклама',
    heroTitle: 'Цифровой офис<br>и привлечение клиентов<br><span class="hero-accent">для бизнеса</span>',
    heroText: 'Создаём сайты, подключаем CRM, автоматизируем заявки и помогаем привлекать клиентов из Google, Яндекса и рекламы.',
    heroBtnPrimary: 'Получить консультацию →', heroBtnSecondary: 'Посмотреть направления',
    micro1: '✓ Сайт под ключ', micro2: '✓ Локальное SEO', micro3: '✓ Заявки в WhatsApp / CRM',
    value1Title: 'Сайт + SEO основа', value1Text: 'Современный сайт, готовый к продвижению',
    value2Title: 'Google / Yandex', value2Text: 'Карты и локальный поиск',
    value3Title: 'CRM и автоматизация', value3Text: 'Заявки, воронка и напоминания',
    value4Title: 'Запуск рекламы', value4Text: 'Google / Яндекс / Meta',
    servicesKicker: 'Наши направления', servicesTitle: 'Направления, с которыми мы работаем', servicesText: 'Для каждой ниши — свой сайт, оффер, SEO и воронка заявок.',
    niche1Title: 'Адвокаты', niche1Text: 'Сайт, заявки, доверие и репутация',
    niche2Title: 'Стоматологи', niche2Text: 'Больше записей и новых пациентов',
    niche3Title: 'Частные врачи / клиники', niche3Text: 'Онлайн-запись и поток пациентов',
    niche4Title: 'Риелторы', niche4Text: 'Больше обращений и качественных лидов',
    niche5Title: 'Бухгалтеры / налоговые консультанты', niche5Text: 'Заявки на консультации и B2B-клиенты',
    niche6Title: 'Ремонт / строительство / дизайнеры', niche6Text: 'Больше проектов и целевых обращений',
    niche7Title: 'Автосервисы / детейлинг', niche7Text: 'Онлайн-запись и стабильный поток клиентов',
    niche8Title: 'Отели / апартаменты / туризм', niche8Text: 'Больше прямых заявок и бронирований',
    pricingKicker: 'Тарифы', pricingTitle: 'Пакеты и цены', pricingText: 'Прозрачные решения под разные задачи и бюджет.',
    price1Sub: 'Для старта и базовых задач', price2Sub: 'Для стабильного роста', price3Sub: 'Для полной системы',
    oneTime: 'разово', choosePlan: 'Выбрать пакет', recommended: 'Рекомендуем',
    price1b1: 'Одностраничный сайт-визитка', price1b2: 'Базовая структура', price1b3: 'Форма заявки', price1b4: 'WhatsApp / Telegram', price1b5: 'Базовое SEO',
    price2b1: 'Многостраничный сайт', price2b2: 'SEO-структура', price2b3: 'До 3 SEO-страниц', price2b4: 'Google / Yandex setup', price2b5: 'Аналитика и формы',
    price3b1: 'Сайт + CRM', price3b2: 'До 8 SEO-страниц', price3b3: 'Мультиязычность', price3b4: 'Автоматизация заявок', price3b5: 'Подготовка к рекламе',
    monthly: 'Сопровождение и развитие — <b>от $60 / месяц</b>',
    growthKicker: 'Как мы растим клиентов', growthTitle: 'Не просто сайт — система привлечения заявок', growthText: 'Мы делаем так, чтобы бизнес находили, ему доверяли и оставляли заявку.',
    flow1Title: 'SEO-страницы', flow1Text: 'Под реальные поисковые запросы',
    flow2Title: 'Google / Яндекс', flow2Text: 'Профили и локальная видимость',
    flow3Title: 'Карты', flow3Text: 'Попадаем в локальный поиск',
    flow4Title: 'Реклама', flow4Text: 'Google / Meta / Яндекс',
    flow5Title: 'Автоворонка', flow5Text: 'Формы, WhatsApp, CRM',
    flow6Title: 'Аналитика', flow6Text: 'Смотрим что работает и улучшаем',
    result1Title: 'Больше лидов из поиска', result1Text: 'Google, Яндекс и карты',
    result2Title: '24/7 приём заявок', result2Text: 'Сайт и формы работают постоянно',
    result3Title: 'Одна система вместо хаоса', result3Text: 'Сайт, реклама, заявки и клиенты',
    caseKicker: 'Кейс', caseTitle: 'LevaniLaw.ge — цифровой офис для адвоката', caseText: 'С нуля собрали сайт, страницы услуг, русскую / грузинскую / английскую структуру, Google Business, Search Console, Яндекс Вебмастер, локальное SEO и WhatsApp.', caseBtn: 'Посмотреть кейс →',
    ctaKicker: 'Начнём?', ctaTitle: 'Соберём цифровую систему под вашу нишу', ctaText: 'Подберём сайт, упаковку и инструменты роста под ваш бизнес.', ctaBtn: 'Обсудить проект →',
    footerText: 'Websites • SEO • Local Search • Client Acquisition',
    waMessage: 'Здравствуйте! Хочу обсудить проект с BEQSON',
    waConsultMessage: 'Здравствуйте! Хочу получить консультацию BEQSON',
    emailSubject: 'Консультация BEQSON'
  },
  ka: {
    pageTitle: 'BEQSON — ვებსაიტები, SEO და კლიენტების მოზიდვა სერვისული ბიზნესისთვის',
    metaDescription: 'BEQSON ქმნის ვებსაიტებს, აწყობს ლოკალურ SEO-ს, Google/Yandex პროფილებს, CRM-ს და განაცხადების სისტემას სერვისული ბიზნესისთვის.',
    ogTitle: 'BEQSON Digital Studio',
    ogDescription: 'ვებსაიტი + SEO + ლოკალური ძიება + CRM + განაცხადები.',
    consultLabel: 'მიიღეთ კონსულტაცია',
    navServices: 'მიმართულებები', navPricing: 'ფასები', navGrowth: 'კლიენტების ზრდა', navCase: 'ქეისი', navContacts: 'კონტაქტი',
    heroKicker: 'ვებგვერდები • SEO • CRM • რეკლამა',
    heroTitle: 'ციფრული ოფისი<br>და კლიენტების მოზიდვა<br><span class="hero-accent">ბიზნესისთვის</span>',
    heroText: 'ვქმნით ვებსაიტებს, ვაერთებთ CRM-ს, ვაავტომატიზებთ განაცხადებს და გეხმარებით Google-იდან, Yandex-იდან და რეკლამიდან კლიენტების მოზიდვაში.',
    heroBtnPrimary: 'მიიღეთ კონსულტაცია →', heroBtnSecondary: 'მიმართულებების ნახვა',
    micro1: '✓ ვებსაიტი გასაღებით', micro2: '✓ ლოკალური SEO', micro3: '✓ განაცხადები WhatsApp / CRM-ში',
    value1Title: 'ვებსაიტი + SEO საფუძველი', value1Text: 'თანამედროვე ვებსაიტი, მზად продвижებისთვის',
    value2Title: 'Google / Yandex', value2Text: 'რუკები და ლოკალური ძიება',
    value3Title: 'CRM და ავტომატიზაცია', value3Text: 'განაცხადები, ძაბრი და შეხსენებები',
    value4Title: 'რეკლამის გაშვება', value4Text: 'Google / Yandex / Meta',
    servicesKicker: 'ჩვენი მიმართულებები', servicesTitle: 'ნიშები, რომლებთანაც ვმუშაობთ', servicesText: 'ყოველი ნიშისთვის — საკუთარი ვებსაიტი, შეთავაზება, SEO და განაცხადების სისტემა.',
    niche1Title: 'ადვოკატები', niche1Text: 'ვებსაიტი, განაცხადები, ნდობა და რეპუტაცია',
    niche2Title: 'სტომატოლოგები', niche2Text: 'მეტი ჩაწერა და ახალი პაციენტები',
    niche3Title: 'კერძო ექიმები / კლინიკები', niche3Text: 'ონლაინ ჩაწერა და პაციენტების ნაკადი',
    niche4Title: 'რიელტორები', niche4Text: 'მეტი მიმართვა და ხარისხიანი ლიდები',
    niche5Title: 'ბუღალტრები / საგადასახადო კონსულტანტები', niche5Text: 'საკონსულტაციო განაცხადები და B2B კლიენტები',
    niche6Title: 'რემონტი / მშენებლობა / დიზაინერები', niche6Text: 'მეტი პროექტი და მიზნობრივი მიმართვები',
    niche7Title: 'ავტოსერვისები / დეტეილინგი', niche7Text: 'ონლაინ ჩაწერა და კლიენტების სტაბილური ნაკადი',
    niche8Title: 'სასტუმროები / აპარტამენტები / ტურიზმი', niche8Text: 'მეტი პირდაპირი მოთხოვნა და ჯავშანი',
    pricingKicker: 'ტარიფები', pricingTitle: 'პაკეტები და ფასები', pricingText: 'გამჭვირვალე გადაწყვეტილებები სხვადასხვა ამოცანისა და ბიუჯეტისთვის.',
    price1Sub: 'სტარტისთვის და საბაზისო ამოცანებისთვის', price2Sub: 'სტაბილური ზრდისთვის', price3Sub: 'სრული სისტემისთვის',
    oneTime: 'ერთჯერადად', choosePlan: 'პაკეტის არჩევა', recommended: 'გირჩევთ',
    price1b1: 'ერთგვერდიანი საიტი-ვიზიტკა', price1b2: 'საბაზისო სტრუქტურა', price1b3: 'განაცხადის ფორმა', price1b4: 'WhatsApp / Telegram', price1b5: 'საბაზისო SEO',
    price2b1: 'მრავალგვერდიანი საიტი', price2b2: 'SEO სტრუქტურა', price2b3: 'მდე 3 SEO-გვერდი', price2b4: 'Google / Yandex დაყენება', price2b5: 'ანალიტიკა და ფორმები',
    price3b1: 'საიტი + CRM', price3b2: 'მდე 8 SEO-გვერდი', price3b3: 'მულტენოვანება', price3b4: 'განაცხადების ავტომატიზაცია', price3b5: 'რეკლამისთვის მომზადება',
    monthly: 'მხარდაჭერა და განვითარება — <b>$60 / თვიდან</b>',
    growthKicker: 'როგორ ვიზრდით კლიენტებს', growthTitle: 'არა უბრალოდ საიტი — განაცხადების მოზიდვის სისტემა', growthText: 'ვაკეთებთ ისე, რომ ბიზნესი იპოვონ, ენდონ და განაცხადი დატოვონ.',
    flow1Title: 'SEO-გვერდები', flow1Text: 'რეალური საძიებო მოთხოვნებისთვის',
    flow2Title: 'Google / Yandex', flow2Text: 'პროფილები და ლოკალური ხილვადობა',
    flow3Title: 'რუკები', flow3Text: 'ლოკალურ ძიებაში მოხვედრა',
    flow4Title: 'რეკლამა', flow4Text: 'Google / Meta / Yandex',
    flow5Title: 'ავტომატური ძაბრი', flow5Text: 'ფორმები, WhatsApp, CRM',
    flow6Title: 'ანალიტიკა', flow6Text: 'ვაკვირდებით, რა მუშაობს და ვაუმჯობესებთ',
    result1Title: 'მეტი ლიდი ძიებიდან', result1Text: 'Google, Yandex და რუკები',
    result2Title: '24/7 განაცხადების მიღება', result2Text: 'საიტი და ფორმები მუდმივად მუშაობს',
    result3Title: 'ერთი სისტემა ქაოსის ნაცვლად', result3Text: 'საიტი, რეკლამა, განაცხადები და კლიენტები',
    caseKicker: 'ქეისი', caseTitle: 'LevaniLaw.ge — ციფრული ოფისი ადვოკატისთვის', caseText: 'ნულიდან ავაწყვეთ საიტი, მომსახურების გვერდები, რუსული / ქართული / ინგლისური სტრუქტურა, Google Business, Search Console, Yandex Webmaster, ლოკალური SEO და WhatsApp.', caseBtn: 'ქეისის ნახვა →',
    ctaKicker: 'დავიწყოთ?', ctaTitle: 'ავაწყობთ ციფრულ სისტემას თქვენი ნიშისთვის', ctaText: 'შევარჩევთ ვებსაიტს, შეფუთვას და ზრდის ინსტრუმენტებს თქვენი ბიზნესისთვის.', ctaBtn: 'პროექტის განხილვა →',
    footerText: 'ვებსაიტები • SEO • ლოკალური ძიება • კლიენტების მოზიდვა',
    waMessage: 'გამარჯობა! მსურს BEQSON-თან პროექტის განხილვა',
    waConsultMessage: 'გამარჯობა! მსურს BEQSON-ის კონსულტაცია',
    emailSubject: 'კონსულტაცია BEQSON'
  },
  en: {
    pageTitle: 'BEQSON — websites, SEO and client acquisition for service businesses',
    metaDescription: 'BEQSON builds websites, sets up local SEO, Google/Yandex profiles, CRM and lead systems for service businesses.',
    ogTitle: 'BEQSON Digital Studio',
    ogDescription: 'Website + SEO + local search + CRM + leads.',
    consultLabel: 'Get a consultation',
    navServices: 'Services', navPricing: 'Pricing', navGrowth: 'Client growth', navCase: 'Case study', navContacts: 'Contacts',
    heroKicker: 'Websites • SEO • CRM • Ads',
    heroTitle: 'Digital office<br>and client acquisition<br><span class="hero-accent">for business</span>',
    heroText: 'We build websites, connect CRM, automate leads and help businesses attract clients from Google, Yandex and ads.',
    heroBtnPrimary: 'Get a consultation →', heroBtnSecondary: 'View industries',
    micro1: '✓ Turnkey website', micro2: '✓ Local SEO', micro3: '✓ Leads in WhatsApp / CRM',
    value1Title: 'Website + SEO foundation', value1Text: 'A modern website ready for promotion',
    value2Title: 'Google / Yandex', value2Text: 'Maps and local search',
    value3Title: 'CRM & automation', value3Text: 'Leads, pipeline and reminders',
    value4Title: 'Ad launch', value4Text: 'Google / Yandex / Meta',
    servicesKicker: 'Our industries', servicesTitle: 'Industries we work with', servicesText: 'Each niche gets its own website, offer, SEO and lead funnel.',
    niche1Title: 'Lawyers', niche1Text: 'Website, leads, trust and reputation',
    niche2Title: 'Dentists', niche2Text: 'More bookings and new patients',
    niche3Title: 'Private doctors / clinics', niche3Text: 'Online booking and patient flow',
    niche4Title: 'Realtors', niche4Text: 'More inquiries and better leads',
    niche5Title: 'Accountants / tax consultants', niche5Text: 'Consultation leads and B2B clients',
    niche6Title: 'Renovation / construction / designers', niche6Text: 'More projects and targeted inquiries',
    niche7Title: 'Auto services / detailing', niche7Text: 'Online bookings and a stable client flow',
    niche8Title: 'Hotels / apartments / tourism', niche8Text: 'More direct requests and bookings',
    pricingKicker: 'Pricing', pricingTitle: 'Packages and pricing', pricingText: 'Transparent solutions for different goals and budgets.',
    price1Sub: 'For launch and basic needs', price2Sub: 'For steady growth', price3Sub: 'For a full system',
    oneTime: 'one-time', choosePlan: 'Choose plan', recommended: 'Recommended',
    price1b1: 'One-page business card website', price1b2: 'Basic structure', price1b3: 'Lead form', price1b4: 'WhatsApp / Telegram', price1b5: 'Basic SEO',
    price2b1: 'Multi-page website', price2b2: 'SEO structure', price2b3: 'Up to 3 SEO pages', price2b4: 'Google / Yandex setup', price2b5: 'Analytics and forms',
    price3b1: 'Website + CRM', price3b2: 'Up to 8 SEO pages', price3b3: 'Multilingual', price3b4: 'Lead automation', price3b5: 'Ad-ready setup',
    monthly: 'Support and growth — <b>from $60 / month</b>',
    growthKicker: 'How we grow clients', growthTitle: 'Not just a website — a lead generation system', growthText: 'We make sure businesses are found, trusted and contacted.',
    flow1Title: 'SEO pages', flow1Text: 'Built for real search intent',
    flow2Title: 'Google / Yandex', flow2Text: 'Profiles and local visibility',
    flow3Title: 'Maps', flow3Text: 'Appear in local search',
    flow4Title: 'Ads', flow4Text: 'Google / Meta / Yandex',
    flow5Title: 'Automated funnel', flow5Text: 'Forms, WhatsApp, CRM',
    flow6Title: 'Analytics', flow6Text: 'Track what works and improve it',
    result1Title: 'More leads from search', result1Text: 'Google, Yandex and maps',
    result2Title: '24/7 lead capture', result2Text: 'Your website and forms work all the time',
    result3Title: 'One system instead of chaos', result3Text: 'Website, ads, leads and clients in one place',
    caseKicker: 'Case study', caseTitle: 'LevaniLaw.ge — a digital office for a lawyer', caseText: 'We built the site from scratch, created service pages, a Russian / Georgian / English structure, Google Business, Search Console, Yandex Webmaster, local SEO and WhatsApp.', caseBtn: 'View case study →',
    ctaKicker: 'Ready?', ctaTitle: 'We will build a digital system for your niche', ctaText: 'We will choose the right website, positioning and growth tools for your business.', ctaBtn: 'Discuss the project →',
    footerText: 'Websites • SEO • Local Search • Client Acquisition',
    waMessage: 'Hello! I would like to discuss a project with BEQSON',
    waConsultMessage: 'Hello! I would like to get a consultation from BEQSON',
    emailSubject: 'BEQSON consultation'
  }
};

function setConsultLinks(t) {
  const waMain = 'https://wa.me/995551739333?text=' + encodeURIComponent(t.waMessage || 'Hello');
  const waConsult = 'https://wa.me/995551739333?text=' + encodeURIComponent(t.waConsultMessage || t.waMessage || 'Hello');
  document.querySelectorAll('.js-wa-link').forEach((link, index) => {
    link.href = index === 0 ? waConsult : waMain;
  });
  const emailHref = 'mailto:digitalstudiobeqson@gmail.com?subject=' + encodeURIComponent(t.emailSubject || 'BEQSON consultation');
  document.querySelectorAll('.js-email-link').forEach(link => link.href = emailHref);
}

function applyLanguage(lang) {
  const t = translations[lang] || translations.ru;
  document.documentElement.lang = lang;
  document.title = t.pageTitle;
  const titleTag = document.getElementById('page-title');
  const metaDescription = document.getElementById('meta-description');
  const ogTitle = document.getElementById('og-title');
  const ogDescription = document.getElementById('og-description');
  if (titleTag) titleTag.textContent = t.pageTitle;
  if (metaDescription) metaDescription.setAttribute('content', t.metaDescription);
  if (ogTitle) ogTitle.setAttribute('content', t.ogTitle);
  if (ogDescription) ogDescription.setAttribute('content', t.ogDescription);

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key] !== undefined) el.textContent = t[key];
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const key = el.getAttribute('data-i18n-html');
    if (t[key] !== undefined) el.innerHTML = t[key];
  });

  document.querySelectorAll('.flag-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });

  setConsultLinks(t);
  localStorage.setItem('beqson-lang', lang);
}

document.querySelectorAll('.flag-btn').forEach(btn => {
  btn.addEventListener('click', () => applyLanguage(btn.dataset.lang));
});

const savedLang = localStorage.getItem('beqson-lang') || 'ru';
applyLanguage(savedLang);
