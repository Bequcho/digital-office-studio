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
    // The disclosure links precede the toggle in DOM order; enter them on opening.
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
    // Keep keyboard focus visible when the desktop links become a hidden disclosure.
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

  const lang = (document.documentElement.lang || 'ru').toLowerCase();
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
      label: 'ვებსაიტები • SEO • CRM • რეკლამა',
      title1: 'ციფრული ოფისი',
      title2: 'და კლიენტების მოზიდვა',
      title3: 'ბიზნესისთვის',
      description: 'ვქმნით ვებსაიტებს, ვაერთებთ CRM-ს, ვაავტომატიზებთ განაცხადებს და ვეხმარებით ბიზნესს Google-იდან, Yandex-იდან და რეკლამიდან კლიენტების მოზიდვაში.',
      primary: 'მიიღეთ კონსულტაცია →',
      secondary: 'ნახეთ მიმართულებები',
      aria: 'BEQSON-ის ძირითადი შესაძლებლობები',
      imageAlt: 'BEQSON — ციფრული ოფისი, CRM, განაცხადები და ანალიტიკა',
      features: [
        ['globe','ვებსაიტი + SEO საფუძველი','თანამედროვე ვებსაიტი, მზად წინსვლისთვის'],
        ['pin','Google / Yandex','რუკები და ლოკალური ძიება'],
        ['gear','CRM და ავტომატიზაცია','განაცხადები, გაყიდვების ძაბრი და შეხსენებები'],
        ['chart','რეკლამის გაშვება','Google / Yandex / Meta']
      ]
    }
  };

  const c = content[lang] || content.ru;
  const sprite = '/digital-office-studio/assets/icons.svg';
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
        <div class="classic-hero-visual">
          <img src="/digital-office-studio/assets/images/hero-main.webp" alt="${c.imageAlt}" width="1600" height="900" fetchpriority="high" loading="eager">
        </div>
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
