'use strict';
document.documentElement.classList.add('js');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
if (menuButton && navigation) {
  const closeMenu = (returnFocus = navigation.contains(document.activeElement)) => {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', menuButton.dataset.openLabel);
    if (returnFocus) menuButton.focus();
  };
  menuButton.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') !== 'true';
    navigation.classList.toggle('is-open', expanded);
    menuButton.setAttribute('aria-expanded', String(expanded));
    menuButton.setAttribute('aria-label', expanded ? menuButton.dataset.closeLabel : menuButton.dataset.openLabel);
    if (expanded) navigation.querySelector('a')?.focus();
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('click', event => {
    if (!navigation.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && navigation.classList.contains('is-open')) closeMenu(true);
  });
  window.matchMedia('(min-width: 1181px)').addEventListener('change', event => {
    const focusedLink = navigation.contains(document.activeElement);
    const focusedToggle = document.activeElement === menuButton;
    closeMenu(!event.matches && focusedLink);
    if (event.matches && focusedToggle) navigation.querySelector('a')?.focus();
  });
}
const lightbox = document.querySelector('.lightbox');
if (lightbox && typeof lightbox.showModal === 'function') {
  const modalImage = lightbox.querySelector('img');
  const modalTitle = lightbox.querySelector('[data-modal-title]');
  let trigger = null;
  document.querySelectorAll('[data-lightbox]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = link;
      const title = link.dataset.lightboxTitle || '';
      modalImage.src = link.href;
      modalImage.alt = title;
      modalTitle.textContent = title;
      lightbox.showModal();
      document.body.classList.add('modal-open');
      lightbox.querySelector('.lightbox-scroll').scrollTo(0, 0);
    });
  });
  lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
  lightbox.addEventListener('click', event => {
    if (event.target === lightbox) {
      const bounds = lightbox.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) lightbox.close();
    }
  });
  lightbox.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    if (trigger) trigger.focus({preventScroll: true});
  });
}

/* Classic homepage hero restored from the approved reference. */
(() => {
  const oldHero = document.querySelector('.home-banner');
  const oldValue = document.querySelector('.value-section');
  if (!oldHero || !oldValue) return;

  const lang = (document.documentElement.lang || 'ka').toLowerCase();
  const content = {
    ru: {
      label: 'САЙТЫ • SEO • CRM • РЕКЛАМА',
      title1: 'Цифровой офис',
      title2: 'и привлечение клиентов',
      title3: 'для бизнеса',
      description: 'Создаём сайты, подключаем CRM, автоматизируем заявки и помогаем привлекать клиентов из Google, Яндекса и рекламы.',
      primary: 'Получить консультацию →',
      secondary: 'Посмотреть направления',
      aria: 'Ключевые возможности BEQSON',
      imageAlt: 'BEQSON — цифровой офис, CRM, заявки и аналитика',
      features: [
        ['globe','Сайт + SEO основа','Современный сайт, готовый к продвижению'],
        ['pin','Google / Yandex','Карты и локальный поиск'],
        ['gear','CRM и автоматизация','Заявки, воронка и напоминания'],
        ['chart','Запуск рекламы','Google / Яндекс / Meta']
      ]
    },
    en: {
      label: 'WEBSITES • SEO • CRM • ADS',
      title1: 'Digital office',
      title2: 'and client acquisition',
      title3: 'for business',
      description: 'We build websites, connect CRM, automate leads and help businesses attract clients from Google, Yandex and ads.',
      primary: 'Get a consultation →',
      secondary: 'View industries',
      aria: 'Key BEQSON capabilities',
      imageAlt: 'BEQSON — digital office, CRM, leads and analytics',
      features: [
        ['globe','Website + SEO foundation','A modern site ready for promotion'],
        ['pin','Google / Yandex','Maps and local search'],
        ['gear','CRM & automation','Leads, pipeline and reminders'],
        ['chart','Ad launch','Google / Yandex / Meta']
      ]
    },
    ka: {
      label: 'ვებგვერდები • SEO • CRM • რეკლამა',
      title1: 'ციფრული ოფისი',
      title2: 'და კლიენტების მოზიდვა',
      title3: 'ბიზნესისთვის',
      description: 'ვქმნით ვებგვერდებს, ვაერთებთ CRM-ს, ვაავტომატიზებთ მომართვების დამუშავებას და ვეხმარებით ბიზნესს კლიენტების მოზიდვაში Google-იდან, Yandex-იდან და რეკლამიდან.',
      primary: 'კონსულტაციის მიღება →',
      secondary: 'მიმართულებების ნახვა',
      aria: 'BEQSON-ის ძირითადი შესაძლებლობები',
      imageAlt: 'BEQSON — ციფრული ოფისი, CRM, მომართვები და სტატისტიკა',
      features: [
        ['globe','ვებგვერდი + SEO საფუძველი','თანამედროვე ვებგვერდი, საძიებო სისტემებისთვის მზად'],
        ['pin','Google / Yandex','რუკები და ადგილობრივი ძიება'],
        ['gear','CRM და ავტომატიზაცია','მომართვები, გაყიდვების ეტაპები და შეხსენებები'],
        ['chart','რეკლამის დაწყება','Google / Yandex / Meta']
      ]
    }
  };

  const c = content[lang] || content.ka;
  const sprite = '/assets/icons.svg';
  const featureIcon = icon => {
    if (icon === 'gear') {
      return `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Z"></path><path d="m19 13.5 1.3 1-.9 2.1-1.6-.2a7.8 7.8 0 0 1-1.4 1.4l.2 1.6-2.1.9-1-1.3a7.6 7.6 0 0 1-2 0l-1 1.3-2.1-.9.2-1.6a7.8 7.8 0 0 1-1.4-1.4l-1.6.2-.9-2.1 1.3-1a7.6 7.6 0 0 1 0-2l-1.3-1 .9-2.1 1.6.2a7.8 7.8 0 0 1 1.4-1.4l-.2-1.6 2.1-.9 1 1.3a7.6 7.6 0 0 1 2 0l1-1.3 2.1.9-.2 1.6a7.8 7.8 0 0 1 1.4 1.4l1.6-.2.9 2.1-1.3 1a7.6 7.6 0 0 1 0 2Z"></path></svg>`;
    }
    return `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="${sprite}#${icon}"></use></svg>`;
  };

  const hero = `
    <section class="classic-hero" aria-labelledby="classic-hero-title">
      <div class="shell classic-hero-grid">
        <div class="classic-hero-copy">
          <span class="classic-hero-kicker">${c.label}</span>
          <h1 id="classic-hero-title"><span>${c.title1}</span><span>${c.title2}</span><span class="classic-hero-accent">${c.title3}</span></h1>
          <p>${c.description}</p>
          <div class="classic-hero-actions">
            <a class="classic-btn primary" href="#contact">${c.primary}</a>
            <a class="classic-btn secondary" href="#services">${c.secondary}</a>
          </div>
        </div>
        ${lang === 'ka' || lang === 'en' || lang === 'ru' ? '' : `<div class="classic-hero-visual">
          <img src="/assets/images/hero-main.webp" alt="${c.imageAlt}" width="1600" height="900" fetchpriority="high" loading="eager">
        </div>`}
      </div>
    </section>`;

  const values = `
    <section class="classic-valuebar" aria-label="${c.aria}">
      <div class="shell classic-value-grid">
        ${c.features.map(([icon,title,text]) => `
          <div class="classic-value-card">
            <span class="classic-feature-icon">${featureIcon(icon)}</span>
            <span><b>${title}</b><small>${text}</small></span>
          </div>`).join('')}
      </div>
    </section>`;

  oldHero.outerHTML = hero;
  oldValue.outerHTML = values;
})();

/* Georgian homepage language polish. The hero slogan itself is intentionally unchanged. */
(() => {
  const lang = (document.documentElement.lang || '').toLowerCase();
  const isKaHome = lang === 'ka' && /\/ka\/(?:index\.html)?$/.test(window.location.pathname);
  if (!isKaHome) return;

  const replacements = new Map([
    ['კონსულტაცია','კონსულტაციის მიღება'],
    ['ნიშები, რომლებთანაც ვმუშაობთ','სფეროები, რომლებშიც ვმუშაობთ'],
    ['ყოველი ნიშისთვის — საკუთარი ვებსაიტი, შეთავაზება, SEO და განაცხადების სისტემა.','თითოეული სფეროსთვის — საკუთარი ვებგვერდი, შეთავაზება, SEO და მომართვების მართვის სისტემა.'],
    ['ვებსაიტი, განაცხადები, ნდობა და რეპუტაცია','ვებგვერდი, მომართვები, ნდობა და რეპუტაცია'],
    ['ონლაინ ჩაწერა და პაციენტების ნაკადი','ინტერნეტით ჩაწერა და პაციენტების სტაბილური ნაკადი'],
    ['რიელტორები','უძრავი ქონების აგენტები'],
    ['მეტი მიმართვა და ხარისხიანი ლიდები','მეტი მომართვა და დაინტერესებული კლიენტები'],
    ['საკონსულტაციო განაცხადები და B2B კლიენტები','კონსულტაციაზე მეტი მოთხოვნა და ბიზნესკლიენტები'],
    ['რემონტი / მშენებლობა / დიზაინერები','რემონტი / მშენებლობა / დიზაინი'],
    ['ავტოსერვისები / დეტეილინგი','ავტოსერვისები / ავტომობილის მოვლა'],
    ['ონლაინ ჩაწერა და კლიენტების სტაბილური ნაკადი','ინტერნეტით ჩაწერა და კლიენტების სტაბილური ნაკადი'],
    ['სასტუმროები / აპარტამენტები / ტურიზმი','სასტუმროები / ბინები / ტურიზმი'],
    ['ლამაზი დიზაინი მკაფიო მიზნით.','ლამაზი და მიზანმიმართული.'],
    ['ვქმნით გზას თქვენი ბიზნესის გაცნობიდან მომართვამდე. თითოეული ეტაპის შედეგი შეგვიძლია გავზომოთ და გავაუმჯობესოთ.','ვაწყობთ გზას თქვენი ბიზნესის პირველად გაცნობიდან მომართვამდე. თითოეულ ეტაპს ვზომავთ და საჭიროებისამებრ ვაუმჯობესებთ.'],
    ['ვიკვლევთ ბიზნესს','ვიცნობთ თქვენს ბიზნესს'],
    ['ვეცნობით სერვისებს, აუდიტორიასა და თქვენს უპირატესობებს.','ვეცნობით მომსახურებებს, აუდიტორიასა და მიზეზებს, რის გამოც კლიენტმა თქვენ უნდა აგირჩიოთ.'],
    ['ვქმნით საიტს','ვქმნით ვებგვერდს'],
    ['ვაყალიბებთ შეთავაზებას და კონტაქტამდე მარტივ გზას.','ვაყალიბებთ შეთავაზებას და ვქმნით დაკავშირების მარტივ გზას.'],
    ['ვამზადებთ ძიებისთვის','ვემზადებით ძიებისთვის'],
    ['ვქმნით სერვისების გვერდებს, მეტამონაცემებსა და რუკების პროფილებს.','ვქმნით მომსახურებების გვერდებს, მეტამონაცემებსა და რუკებზე ბიზნესის გვერდებს.'],
    ['ვუმატებთ საკონტაქტო არხებსა და მომართვების აღრიცხვას.','ვამატებთ საკონტაქტო არხებს და მომართვების აღრიცხვის სისტემას.'],
    ['ვარჩევთ არხებს და რეკლამას შეთანხმებული ბიუჯეტით ვტესტავთ.','ვარჩევთ არხებს და რეკლამას შეთანხმებული ბიუჯეტით ვამოწმებთ.'],
    ['ვაკვირდებით მომართვების წყაროებს და ვაუმჯობესებთ შედეგებს.','ვაკვირდებით, საიდან მოდის მომართვები, და ვაუმჯობესებთ სუსტ ეტაპებს.'],
    ['03 / მკაფიო საწყისი ნაბიჯი','03 / მარტივი დასაწყისი'],
    ['აირჩიეთ მასშტაბი.','აირჩიეთ სამუშაოს მოცულობა.'],
    ['სამი პაკეტი — პირველი საიტიდან მომართვების მართვის სისტემამდე.','სამი შეთავაზება — პირველი ვებგვერდიდან მომართვების მართვის სრულ სისტემამდე.'],
    ['01 / START','01 / საწყისი'],
    ['Start','საწყისი'],
    ['პირველი თავდაჯერებული ნაბიჯი','პირველი საიმედო ნაბიჯი'],
    ['ერთგვერდიანი სავიზიტო საიტი','ერთგვერდიანი ვებგვერდი'],
    ['მობილურზე მორგებული ვერსია','მობილურ მოწყობილობებზე მორგება'],
    ['საბაზისო SEO-გამართვა','საბაზისო SEO გამართვა'],
    ['პაკეტის განხილვა','შეთავაზების განხილვა'],
    ['რეკომენდებული','ჩვენი არჩევანი'],
    ['Growth','ზრდა'],
    ['მრავალგვერდიანი საიტი','მრავალგვერდიანი ვებგვერდი'],
    ['3-მდე SEO-გვერდი','3-მდე SEO გვერდი'],
    ['სერვისებზე მორგებული სტრუქტურა','მომსახურებებზე მორგებული სტრუქტურა'],
    ['Google / Yandex-ის გამართვა','Google-ისა და Yandex-ის გამართვა'],
    ['ანალიტიკა და მომართვის ფორმები','სტატისტიკა და მომართვის ფორმები'],
    ['03 / PRO','03 / სრული'],
    ['Pro','სრული'],
    ['ერთიანი სისტემისთვის','ერთიანი ციფრული სისტემისთვის'],
    ['საიტი და CRM-ის ინტეგრაცია','ვებგვერდი და CRM-ის დაკავშირება'],
    ['8-მდე SEO-გვერდი','8-მდე SEO გვერდი'],
    ['მომართვების ავტომატიზაცია','მომართვების ავტომატური დამუშავება'],
    ['რეკლამისთვის მომზადება','რეკლამის გასაშვებად მომზადება'],
    ['ფასები მოცემულია USD-ში. სამუშაოს მოცულობას დაწყებამდე ვათანხმებთ. დომენი, ფასიანი სერვისები და სარეკლამო ბიუჯეტი საჭიროებისამებრ ცალკე იფარება.','ფასები მითითებულია აშშ დოლარში. სამუშაოს საბოლოო მოცულობას დაწყებამდე ვათანხმებთ. დომენის, ფასიანი ონლაინ მომსახურებებისა და რეკლამის ხარჯები, საჭიროების შემთხვევაში, ცალკე იფარება.'],
    ['$60-დან / თვე','თვეში $60-დან'],
    ['თბილისელი ადვოკატის საიტი: პირადი ბრენდი, პრაქტიკის მიმართულებები და მარტივი კონტაქტი. სამი ენობრივი ვერსია ადგილობრივი და საერთაშორისო აუდიტორიისთვის.','თბილისელი ადვოკატის ვებგვერდი: პროფესიული სახე, პრაქტიკის მიმართულებები და დაკავშირების მარტივი გზა. სამი ენობრივი ვერსია — ადგილობრივი და საერთაშორისო აუდიტორიისთვის.'],
    ['RU / KA / EN','ქართული / რუსული / ინგლისური'],
    ['საიტი და სერვისების გვერდები','ვებგვერდი და მომსახურებების გვერდები'],
    ['საიტის გახსნა','ვებგვერდის გახსნა'],
    ['LAWYER / TBILISI','ადვოკატი / თბილისი'],
    ['FAQ','ხშირი კითხვები'],
    ['შესაძლებელია განსხვავებული სტილი?','შეიძლება ვებგვერდი სხვა სტილში გაკეთდეს?'],
    ['დიახ. კონცეფციები შესაძლო მიმართულებებს აჩვენებს. ფერებს, შრიფტს, ფოტოებსა და სტრუქტურას თქვენს ბიზნესზე ვარგებთ.','დიახ. წარმოდგენილი ნიმუშები შესაძლო მიმართულებებს აჩვენებს. ფერებს, შრიფტს, ფოტოებსა და სტრუქტურას თქვენს ბიზნესს ვარგებთ.'],
    ['იმუშავებს საიტი ტელეფონზე?','იმუშავებს ვებგვერდი ტელეფონზე?'],
    ['დიახ. საიტი ერგება ტელეფონს, პლანშეტსა და კომპიუტერს. გადმოცემამდე ვამოწმებთ ეკრანის ძირითად ზომებსა და ნავიგაციას.','დიახ. ვებგვერდი ერგება ტელეფონს, პლანშეტსა და კომპიუტერს. გადმოცემამდე ვამოწმებთ სხვადასხვა ეკრანზე გამოსახვასა და მენიუს მუშაობას.'],
    ['რა არის საჭირო დასაწყებად?','რა გვჭირდება დასაწყებად?'],
    ['ბიზნესის სახელი, სერვისები, კონტაქტები და თქვენი მიზნები. ფოტოები, ლოგო და ტექსტები დაგვეხმარება, თუმცა მასალების ჩამონათვალს ერთადაც განვსაზღვრავთ.','ბიზნესის სახელი, მომსახურებების ჩამონათვალი, საკონტაქტო მონაცემები და თქვენი მიზნები. ფოტოები, ლოგო და მზა ტექსტები დაგვეხმარება, თუმცა საჭირო მასალებს ერთადაც განვსაზღვრავთ.'],
    ['იძლევით კლიენტების ზრდის გარანტიას?','იძლევით თუ არა კლიენტების რაოდენობის ზრდის გარანტიას?'],
    ['მომართვების ფიქსირებულ რაოდენობას არ გპირდებით. შედეგი დამოკიდებულია ბაზარზე, ბიუჯეტზე, შეთავაზებასა და მომართვებზე რეაგირებაზე. ვათანხმებთ კონკრეტულ ნაბიჯებს და შედეგებს მონაცემებით ვაფასებთ.','მომართვების ფიქსირებულ რაოდენობას არ ვპირდებით. შედეგი დამოკიდებულია ბაზარზე, ბიუჯეტზე, შეთავაზებასა და მომართვებზე რეაგირებაზე. წინასწარ ვათანხმებთ კონკრეტულ სამუშაოებს და შედეგებს მონაცემებით ვაფასებთ.'],
    ['თქვენი იმიჯი —','თქვენი ციფრული სახე —'],
    ['გვიამბეთ, რას საქმიანობთ და რისი გაუმჯობესება გსურთ. შევარჩევთ საიტის ფორმატსა და შემდეგ ნაბიჯს.','გვიამბეთ, რას საქმიანობთ და რისი გაუმჯობესება გსურთ. შევარჩევთ ვებგვერდის შესაფერის სახეს და შემდეგ ნაბიჯს.'],
    ['აირჩიეთ კომუნიკაციის მოსახერხებელი გზა','აირჩიეთ თქვენთვის მოსახერხებელი საკონტაქტო გზა'],
    ['Email','ელფოსტა'],
    ['© 2026 Digital Studio','© 2026 ციფრული სტუდია'],
    ['გამორჩეული საიტები. მიზნობრივი სისტემები.','ვებგვერდები ხასიათით. სისტემები კონკრეტული მიზნით.'],
    ['ზემოთ','გვერდის დასაწყისში']
  ]);

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const raw = node.nodeValue;
    const trimmed = raw.trim();
    if (!trimmed || !replacements.has(trimmed)) continue;
    node.nodeValue = raw.replace(trimmed, replacements.get(trimmed));
  }

  const pageTitle = 'BEQSON — ვებგვერდები, SEO და კლიენტების მოზიდვა';
  const pageDescription = 'BEQSON-ის ციფრული სტუდია ქმნის ინდივიდუალურ ვებგვერდებს, აწყობს ადგილობრივ SEO-ს და კლიენტების მომართვების მართვის სისტემებს რვა ბიზნესმიმართულებისთვის ქართულ, რუსულ და ინგლისურ ენებზე.';
  document.title = pageTitle;
  [
    ['meta[name="description"]', pageDescription],
    ['meta[property="og:title"]', pageTitle],
    ['meta[property="og:description"]', pageDescription],
    ['meta[property="og:image:alt"]', pageTitle],
    ['meta[name="twitter:image:alt"]', pageTitle]
  ].forEach(([selector, value]) => document.querySelector(selector)?.setAttribute('content', value));

  document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
    try {
      const data = JSON.parse(script.textContent);
      const graph = data['@graph'];
      if (!Array.isArray(graph)) return;
      graph.forEach(item => {
        if (item['@type'] === 'WebPage' && item.inLanguage === 'ka') {
          item.name = pageTitle;
          item.description = pageDescription;
        }
      });
      script.textContent = JSON.stringify(data);
    } catch (_) {}
  });

  document.querySelector('.languages')?.setAttribute('aria-label', 'ენა');
  document.querySelectorAll('[aria-label="Email"]').forEach(el => {
    el.setAttribute('aria-label', 'ელფოსტა');
    el.setAttribute('title', 'ელფოსტა');
  });

  const genericMessage = 'გამარჯობა! მსურს BEQSON-თან ვებგვერდის შექმნის განხილვა.';
  document.querySelectorAll('a[href^="https://wa.me/995551739333"]').forEach(link => {
    const plan = link.closest('.price-card')?.querySelector('h3')?.textContent.trim();
    const message = plan ? `${genericMessage} მაინტერესებს შეთავაზება „${plan}“.` : genericMessage;
    link.href = `https://wa.me/995551739333?text=${encodeURIComponent(message)}`;
  });
  document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
    const subject = 'BEQSON — ვებგვერდის პროექტი';
    link.href = `mailto:digitalstudiobeqson@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(genericMessage)}`;
  });
})();
