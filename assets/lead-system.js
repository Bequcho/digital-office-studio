(() => {
  'use strict';

  const VERSION = '1.1.0';
  const EMAIL_ENDPOINT = window.BEQSON_EMAIL_ENDPOINT || 'https://formsubmit.co/ajax/digitalstudiobeqson@gmail.com';
  const CRM_ENDPOINT = window.BEQSON_CRM_ENDPOINT || 'https://htzfhxhpnxduxjcfhhdx.supabase.co/functions/v1/create-lead';
  const CRM_ANON_KEY = window.BEQSON_CRM_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh0emZoeGhwbnhkdXhqY2ZoaGR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE4MTQ0MDEsImV4cCI6MjEwNzM5MDQwMX0.t9CAGKuI8--1PkZIyjnbmjFaz9BooiYlm-FE3RVRP9I';
  const lang = (document.documentElement.lang || 'en').toLowerCase().slice(0, 2);

  const copy = {
    ru: {
      launcher: 'Обсудить проект', eyebrow: 'BEQSON LEAD SYSTEM', title: 'Расскажите о вашем проекте',
      text: 'Коротко опишите задачу — мы посмотрим нишу и предложим следующий шаг.',
      name: 'Ваше имя', namePh: 'Например, Алексей', contact: 'Как с вами связаться', contactPh: 'WhatsApp, Telegram или email',
      business: 'Сфера бизнеса', businessPh: 'Выберите направление', website: 'Сайт или соцсеть', websitePh: 'https://... (если есть)',
      goal: 'Что хотите улучшить?', goalPh: 'Новый сайт, SEO, заявки, CRM, автоматизация...', budget: 'Ориентир по бюджету', budgetPh: 'Пока не определён',
      submit: 'Отправить заявку', sending: 'Отправляем…', successTitle: 'Заявка отправлена',
      successText: 'Спасибо. Мы получили данные и свяжемся с вами удобным способом.',
      error: 'Не удалось отправить заявку. Напишите нам в WhatsApp или Telegram.', close: 'Закрыть',
      consent: 'Отправляя форму, вы разрешаете использовать данные только для ответа на ваш запрос.', direct: 'Или напишите напрямую',
      budgetOptions: ['До $300', '$300–500', '$500–900', '$900+', 'Пока не определён'],
      industries: ['Адвокат / юрист', 'Стоматология', 'Частный врач / клиника', 'Недвижимость', 'Бухгалтерия / налоги', 'Строительство / дизайн', 'Автосервис / детейлинг', 'Отель / туризм', 'Другая сфера']
    },
    ka: {
      launcher: 'პროექტის განხილვა', eyebrow: 'BEQSON LEAD SYSTEM', title: 'მოგვიყევით თქვენი პროექტის შესახებ',
      text: 'მოკლედ აღწერეთ ამოცანა — გადავხედავთ სფეროს და შემოგთავაზებთ შემდეგ ნაბიჯს.',
      name: 'თქვენი სახელი', namePh: 'მაგალითად, გიორგი', contact: 'როგორ დაგიკავშირდეთ', contactPh: 'WhatsApp, Telegram ან email',
      business: 'ბიზნესის სფერო', businessPh: 'აირჩიეთ მიმართულება', website: 'ვებსაიტი ან სოციალური ქსელი', websitePh: 'https://... (თუ გაქვთ)',
      goal: 'რისი გაუმჯობესება გსურთ?', goalPh: 'ახალი საიტი, SEO, ლიდები, CRM, ავტომატიზაცია...', budget: 'სავარაუდო ბიუჯეტი', budgetPh: 'ჯერ არ არის განსაზღვრული',
      submit: 'განაცხადის გაგზავნა', sending: 'იგზავნება…', successTitle: 'განაცხადი გაიგზავნა',
      successText: 'გმადლობთ. მონაცემები მივიღეთ და თქვენთვის მოსახერხებელი გზით დაგიკავშირდებით.',
      error: 'განაცხადის გაგზავნა ვერ მოხერხდა. მოგვწერეთ WhatsApp-ში ან Telegram-ში.', close: 'დახურვა',
      consent: 'ფორმის გაგზავნით გვაძლევთ უფლებას, მონაცემები გამოვიყენოთ მხოლოდ თქვენს მოთხოვნაზე პასუხისთვის.', direct: 'ან მოგვწერეთ პირდაპირ',
      budgetOptions: ['$300-მდე', '$300–500', '$500–900', '$900+', 'ჯერ არ არის განსაზღვრული'],
      industries: ['ადვოკატი / იურისტი', 'სტომატოლოგია', 'კერძო ექიმი / კლინიკა', 'უძრავი ქონება', 'ბუღალტერია / გადასახადები', 'მშენებლობა / დიზაინი', 'ავტოსერვისი / დეტეილინგი', 'სასტუმრო / ტურიზმი', 'სხვა სფერო']
    },
    en: {
      launcher: 'Discuss a project', eyebrow: 'BEQSON LEAD SYSTEM', title: 'Tell us about your project',
      text: 'Briefly describe the task — we will review your niche and suggest the next step.',
      name: 'Your name', namePh: 'For example, Alex', contact: 'How can we reach you?', contactPh: 'WhatsApp, Telegram or email',
      business: 'Business industry', businessPh: 'Choose an industry', website: 'Website or social page', websitePh: 'https://... (if available)',
      goal: 'What would you like to improve?', goalPh: 'New website, SEO, leads, CRM, automation...', budget: 'Approximate budget', budgetPh: 'Not decided yet',
      submit: 'Send request', sending: 'Sending…', successTitle: 'Request sent',
      successText: 'Thank you. We received your details and will contact you using your preferred channel.',
      error: 'We could not send the request. Please contact us via WhatsApp or Telegram.', close: 'Close',
      consent: 'By submitting, you allow us to use this data only to respond to your request.', direct: 'Or message us directly',
      budgetOptions: ['Up to $300', '$300–500', '$500–900', '$900+', 'Not decided yet'],
      industries: ['Lawyer / legal', 'Dentistry', 'Private doctor / clinic', 'Real estate', 'Accounting / tax', 'Construction / design', 'Auto service / detailing', 'Hotel / tourism', 'Other']
    }
  };

  const t = copy[lang] || copy.en;
  const root = document.createElement('div');
  root.className = 'beqson-lead-system';
  root.dataset.version = VERSION;

  const optionHtml = (items, placeholder) =>
    `<option value="" selected disabled>${escapeHtml(placeholder)}</option>` +
    items.map(item => `<option value="${escapeHtml(item)}">${escapeHtml(item)}</option>`).join('');

  root.innerHTML = `
    <button class="bls-launcher" type="button" aria-haspopup="dialog" aria-controls="beqson-lead-dialog">
      <span class="bls-launcher-dot" aria-hidden="true"></span>
      <span>${escapeHtml(t.launcher)}</span>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
    </button>
    <div class="bls-backdrop" hidden></div>
    <section class="bls-modal" id="beqson-lead-dialog" role="dialog" aria-modal="true" aria-labelledby="beqson-lead-title" hidden>
      <button class="bls-close" type="button" aria-label="${escapeHtml(t.close)}">×</button>
      <div class="bls-glow bls-glow-a" aria-hidden="true"></div>
      <div class="bls-glow bls-glow-b" aria-hidden="true"></div>
      <div class="bls-modal-head">
        <span class="bls-eyebrow">${escapeHtml(t.eyebrow)}</span>
        <h2 id="beqson-lead-title">${escapeHtml(t.title)}</h2>
        <p>${escapeHtml(t.text)}</p>
      </div>
      <form class="bls-form" novalidate>
        <div class="bls-grid">
          <label><span>${escapeHtml(t.name)}</span><input name="name" type="text" autocomplete="name" placeholder="${escapeHtml(t.namePh)}" required maxlength="80"></label>
          <label><span>${escapeHtml(t.contact)}</span><input name="contact" type="text" autocomplete="email" placeholder="${escapeHtml(t.contactPh)}" required maxlength="120"></label>
          <label><span>${escapeHtml(t.business)}</span><select name="industry" required>${optionHtml(t.industries, t.businessPh)}</select></label>
          <label><span>${escapeHtml(t.budget)}</span><select name="budget">${optionHtml(t.budgetOptions, t.budgetPh)}</select></label>
          <label class="bls-wide"><span>${escapeHtml(t.website)}</span><input name="website" type="url" inputmode="url" placeholder="${escapeHtml(t.websitePh)}" maxlength="240"></label>
          <label class="bls-wide"><span>${escapeHtml(t.goal)}</span><textarea name="message" rows="4" placeholder="${escapeHtml(t.goalPh)}" required maxlength="1600"></textarea></label>
        </div>
        <input class="bls-honey" type="text" name="company_fax" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="bls-submit-row">
          <button class="bls-submit" type="submit"><span>${escapeHtml(t.submit)}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
          <p class="bls-consent">${escapeHtml(t.consent)}</p>
        </div>
        <div class="bls-status" role="status" aria-live="polite"></div>
      </form>
      <div class="bls-direct">
        <span>${escapeHtml(t.direct)}</span>
        <a href="https://wa.me/995551739333" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <a href="https://t.me/digital_studio_beqson" target="_blank" rel="noopener noreferrer">Telegram</a>
      </div>
    </section>
  `;

  document.body.appendChild(root);

  const launcher = root.querySelector('.bls-launcher');
  const modal = root.querySelector('.bls-modal');
  const backdrop = root.querySelector('.bls-backdrop');
  const closeBtn = root.querySelector('.bls-close');
  const form = root.querySelector('.bls-form');
  const submit = root.querySelector('.bls-submit');
  const status = root.querySelector('.bls-status');
  let previousFocus = null;

  launcher.addEventListener('click', openModal);
  closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', closeModal);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !modal.hidden) closeModal();
  });

  form.addEventListener('submit', async event => {
    event.preventDefault();
    status.className = 'bls-status';
    status.textContent = '';

    if (!form.reportValidity()) return;
    if (form.elements.company_fax.value) return;

    setSubmitting(true);
    const payload = Object.fromEntries(new FormData(form).entries());
    const attribution = getAttribution();
    delete payload.company_fax;

    const shared = {
      language: lang,
      page_url: location.href,
      page_path: location.pathname,
      page_title: document.title,
      referrer: document.referrer || 'direct',
      first_source: attribution.source,
      utm_source: attribution.utm_source,
      utm_medium: attribution.utm_medium,
      utm_campaign: attribution.utm_campaign,
      submitted_at: new Date().toISOString(),
      lead_system_version: VERSION
    };

    const emailPayload = {
      ...payload,
      ...shared,
      _subject: `BEQSON lead · ${payload.industry || 'Website enquiry'} · ${lang.toUpperCase()}`
    };

    const crmPayload = {
      name: payload.name,
      contact: payload.contact,
      niche: payload.industry || '',
      website: payload.website || '',
      message: payload.message || '',
      budget: payload.budget || '',
      language: lang,
      source: attribution.source || 'website_form',
      page_url: location.href,
      referrer: document.referrer || 'direct',
      utm_source: attribution.utm_source,
      utm_medium: attribution.utm_medium,
      utm_campaign: attribution.utm_campaign,
      consent: true
    };

    try {
      const [crmResult, emailResult] = await Promise.allSettled([
        postJson(CRM_ENDPOINT, crmPayload, {
          apikey: CRM_ANON_KEY,
          Authorization: `Bearer ${CRM_ANON_KEY}`
        }),
        postJson(EMAIL_ENDPOINT, emailPayload)
      ]);

      if (crmResult.status !== 'fulfilled') throw crmResult.reason || new Error('CRM submission failed');

      status.className = 'bls-status is-success';
      status.innerHTML = `<strong>${escapeHtml(t.successTitle)}</strong><span>${escapeHtml(t.successText)}</span>`;
      form.reset();
      emitEvent('lead_submit_success', {
        industry: payload.industry || '',
        language: lang,
        crm: 'saved',
        email: emailResult.status === 'fulfilled' ? 'sent' : 'failed'
      });
    } catch (error) {
      console.error('BEQSON lead submit error', error);
      status.className = 'bls-status is-error';
      status.textContent = t.error;
      emitEvent('lead_submit_error', { language: lang });
    } finally {
      setSubmitting(false);
    }
  });

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    const href = link.href || '';
    if (href.includes('wa.me/')) emitEvent('contact_click', { channel: 'whatsapp', page: location.pathname });
    if (href.includes('t.me/')) emitEvent('contact_click', { channel: 'telegram', page: location.pathname });
    if (href.startsWith('mailto:')) emitEvent('contact_click', { channel: 'email', page: location.pathname });
  }, { passive: true });

  async function postJson(url, body, extraHeaders = {}) {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json', ...extraHeaders },
      body: JSON.stringify(body)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.success === false) {
      const error = new Error(`Request failed: ${response.status}`);
      error.status = response.status;
      error.data = data;
      throw error;
    }
    return data;
  }

  function openModal() {
    previousFocus = document.activeElement;
    modal.hidden = false;
    backdrop.hidden = false;
    document.documentElement.classList.add('bls-lock');
    requestAnimationFrame(() => root.classList.add('is-open'));
    setTimeout(() => modal.querySelector('input, select, textarea, button')?.focus(), 80);
    emitEvent('lead_form_open', { language: lang, page: location.pathname });
  }

  function closeModal() {
    root.classList.remove('is-open');
    document.documentElement.classList.remove('bls-lock');
    setTimeout(() => {
      modal.hidden = true;
      backdrop.hidden = true;
    }, 180);
    previousFocus?.focus?.();
  }

  function setSubmitting(state) {
    submit.disabled = state;
    const label = submit.querySelector('span');
    if (label) label.textContent = state ? t.sending : t.submit;
  }

  function getAttribution() {
    const url = new URL(location.href);
    const existing = safeParse(sessionStorage.getItem('beqson_attribution'));
    let source = 'direct';
    if (document.referrer) {
      try { source = new URL(document.referrer).hostname || 'referral'; } catch (_) { source = 'referral'; }
    }
    const detected = {
      source,
      utm_source: url.searchParams.get('utm_source') || '',
      utm_medium: url.searchParams.get('utm_medium') || '',
      utm_campaign: url.searchParams.get('utm_campaign') || ''
    };
    const value = existing || detected;
    if (!existing) {
      try { sessionStorage.setItem('beqson_attribution', JSON.stringify(value)); } catch (_) {}
    }
    return value;
  }

  function emitEvent(name, detail = {}) {
    const payload = { event: `beqson_${name}`, ...detail };
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
    window.dispatchEvent(new CustomEvent('beqson:analytics', { detail: payload }));
  }

  function safeParse(value) {
    try { return value ? JSON.parse(value) : null; } catch (_) { return null; }
  }

  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }
})();
