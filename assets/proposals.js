(() => {
  'use strict';
  const SUPABASE_URL = 'https://htzfhxhpnxduxjcfhhdx.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_gWtCN4v2ToGvJcJjTgtomQ_C1y7SEuW';
  const ADMIN_EMAIL = 'digitalstudiobeqson@gmail.com';
  const { createClient } = window.supabase;
  const db = createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } });
  const $ = s => document.querySelector(s);
  const leadList = $('#lead-list');
  const leadSearch = $('#lead-search');
  const packageSelect = $('#package');
  const amount = $('#amount');
  const currency = $('#currency');
  const timeline = $('#timeline');
  const scope = $('#scope');
  const payment = $('#payment');
  const notes = $('#notes');
  const save = $('#save');
  const printBtn = $('#print');
  const statusEl = $('#status');
  const logout = $('#logout');

  let leads = [];
  let selected = null;
  let currentProposal = null;

  const defaults = {
    Start: {
      price: 250,
      scope: ['Одностраничный сайт-визитка', 'Адаптация под мобильные устройства', 'Форма заявки и контакты', 'Базовая SEO-настройка', 'Подключение аналитики']
    },
    Growth: {
      price: 490,
      scope: ['Многостраничный сайт', 'SEO-структура и локальное продвижение', 'Google / Yandex Business', 'CRM для заявок', 'WhatsApp / Telegram / email интеграции', 'Аналитика и отслеживание конверсий']
    },
    Pro: {
      price: 890,
      scope: ['Премиальный многостраничный сайт', 'Расширенное SEO и локальная выдача', 'CRM и автоматизация лидов', 'Интеграции с мессенджерами и формами', 'Аналитика и рекламная инфраструктура', 'Приоритетная настройка и запуск']
    }
  };

  boot();

  async function boot() {
    const { data: { session } } = await db.auth.getSession();
    const email = session?.user?.email?.toLowerCase();
    if (!session || email !== ADMIN_EMAIL) {
      location.href = '/crm/';
      return;
    }
    await loadLeads();
  }

  async function loadLeads() {
    const { data, error } = await db.from('leads').select('*').order('created_at', { ascending: false });
    if (error) return setStatus('Не удалось загрузить заявки', true);
    leads = data || [];
    renderLeads();
    if (leads.length) selectLead(leads[0].id);
  }

  function renderLeads() {
    const q = leadSearch.value.trim().toLowerCase();
    const rows = leads.filter(l => !q || [l.name,l.contact,l.niche,l.company].some(v => String(v || '').toLowerCase().includes(q)));
    leadList.innerHTML = '';
    rows.forEach(l => {
      const el = document.createElement('div');
      el.className = 'lead-item' + (selected?.id === l.id ? ' active' : '');
      el.innerHTML = `<b>${esc(l.name)}</b><span>${esc(l.niche || 'Без ниши')} · ${esc(l.recommended_package || 'Start')} · ${l.lead_score || 0}/100</span>`;
      el.onclick = () => selectLead(l.id);
      leadList.appendChild(el);
    });
  }

  async function selectLead(id) {
    selected = leads.find(l => l.id === id);
    if (!selected) return;
    renderLeads();
    const { data } = await db.from('proposals').select('*').eq('lead_id', id).order('created_at', { ascending: false }).limit(1).maybeSingle();
    currentProposal = data || null;
    const pkg = currentProposal?.package_name || selected.recommended_package || 'Start';
    packageSelect.value = ['Start','Growth','Pro'].includes(pkg) ? pkg : 'Start';
    const def = defaults[packageSelect.value];
    amount.value = currentProposal?.amount ?? def.price;
    currency.value = currentProposal?.currency || 'USD';
    timeline.value = currentProposal?.timeline || '7–14 рабочих дней';
    scope.value = currentProposal?.scope?.length ? currentProposal.scope.join('\n') : def.scope.join('\n');
    payment.value = currentProposal?.payment_terms || '50% предоплата, 50% после завершения и согласования проекта.';
    notes.value = currentProposal?.notes || '';
    renderPreview();
  }

  function renderPreview() {
    if (!selected) return;
    $('#p-name').textContent = selected.name || 'Клиент';
    $('#p-meta').textContent = [selected.niche, selected.company, selected.website].filter(Boolean).join(' · ') || selected.contact || '—';
    $('#p-package').textContent = packageSelect.value;
    const symbol = currency.value === 'USD' ? '$' : currency.value === 'EUR' ? '€' : '₾';
    $('#p-price').textContent = `${symbol}${Number(amount.value || 0).toLocaleString('ru-RU')}`;
    $('#p-timeline').textContent = timeline.value || '—';
    $('#p-payment').textContent = payment.value || '—';
    $('#p-notes').textContent = notes.value || '';
    const items = scope.value.split('\n').map(x => x.trim()).filter(Boolean);
    $('#p-scope').innerHTML = items.map(x => `<li>${esc(x)}</li>`).join('');
  }

  async function saveProposal() {
    if (!selected) return setStatus('Сначала выберите клиента', true);
    save.disabled = true;
    save.textContent = 'Сохраняем…';
    const payload = {
      lead_id: selected.id,
      language: selected.language || 'ru',
      package_name: packageSelect.value,
      amount: Number(amount.value || 0),
      currency: currency.value,
      scope: scope.value.split('\n').map(x => x.trim()).filter(Boolean),
      timeline: timeline.value.trim() || null,
      payment_terms: payment.value.trim() || null,
      notes: notes.value.trim() || null,
      status: 'draft'
    };

    let result;
    if (currentProposal?.id) result = await db.from('proposals').update(payload).eq('id', currentProposal.id).select().single();
    else result = await db.from('proposals').insert(payload).select().single();

    save.disabled = false;
    save.textContent = 'Сохранить предложение';
    if (result.error) return setStatus('Не удалось сохранить предложение', true);
    currentProposal = result.data;
    await db.from('lead_events').insert({ lead_id: selected.id, event_type: 'proposal_saved', details: { proposal_id: currentProposal.id, package: payload.package_name, amount: payload.amount, currency: payload.currency } });
    setStatus('Предложение сохранено');
  }

  leadSearch.addEventListener('input', renderLeads);
  packageSelect.addEventListener('change', () => {
    const def = defaults[packageSelect.value];
    amount.value = def.price;
    scope.value = def.scope.join('\n');
    renderPreview();
  });
  [amount,currency,timeline,scope,payment,notes].forEach(el => el.addEventListener('input', renderPreview));
  save.addEventListener('click', saveProposal);
  printBtn.addEventListener('click', () => { renderPreview(); window.print(); });
  logout.addEventListener('click', async () => { await db.auth.signOut(); location.href = '/crm/'; });

  function setStatus(text, err=false) {
    statusEl.textContent = text;
    statusEl.style.color = err ? '#ff8d8d' : '#58d5a0';
  }
  function esc(v) { return String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
})();
