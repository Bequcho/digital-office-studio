(() => {
  'use strict';

  const SUPABASE_URL = 'https://htzfhxhpnxduxjcfhhdx.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_gWtCN4v2ToGvJcJjTgtomQ_C1y7SEuW';
  const ADMIN_EMAIL = 'digitalstudiobeqson@gmail.com';
  const STATUS = [
    ['new','Новые'],['contacted','Связались'],['proposal','Предложение'],['won','Клиент'],['in_progress','В работе'],['completed','Завершено'],['lost','Потеряно']
  ];

  const { createClient } = window.supabase;
  const db = createClient(SUPABASE_URL, SUPABASE_KEY, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
  });

  const $ = (s) => document.querySelector(s);
  const authView = $('#auth-view');
  const appView = $('#app-view');
  const authForm = $('#auth-form');
  const authEmail = $('#auth-email');
  const authPassword = $('#auth-password');
  const authStatus = $('#auth-status');
  const signupBtn = $('#signup-btn');
  const logoutBtn = $('#logout-btn');
  const refreshBtn = $('#refresh-btn');
  const search = $('#search');
  const board = $('#board');
  const stats = $('#stats');
  const leadDialog = $('#lead-dialog');
  const leadDetail = $('#lead-detail');

  let leads = [];
  let selectedId = null;

  boot();

  async function boot() {
    const { data: { session } } = await db.auth.getSession();
    await handleSession(session);
    db.auth.onAuthStateChange((_event, nextSession) => handleSession(nextSession));
  }

  async function handleSession(session) {
    const email = session?.user?.email?.toLowerCase();
    if (!session || email !== ADMIN_EMAIL) {
      if (session && email !== ADMIN_EMAIL) await db.auth.signOut();
      authView.hidden = false;
      appView.hidden = true;
      return;
    }
    authView.hidden = true;
    appView.hidden = false;
    await loadLeads();
  }

  authForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    setAuthStatus('Входим…');
    const email = authEmail.value.trim().toLowerCase();
    const password = authPassword.value;
    if (email !== ADMIN_EMAIL) return setAuthStatus('Для этого кабинета разрешён только администратор BEQSON.', true);
    const { error } = await db.auth.signInWithPassword({ email, password });
    if (error) setAuthStatus(humanAuthError(error.message), true);
  });

  signupBtn.addEventListener('click', async () => {
    const email = authEmail.value.trim().toLowerCase();
    const password = authPassword.value;
    if (email !== ADMIN_EMAIL) return setAuthStatus('Создание доступа разрешено только для аккаунта BEQSON.', true);
    if (password.length < 8) return setAuthStatus('Пароль должен быть минимум 8 символов.', true);
    setAuthStatus('Создаём доступ…');
    const { error } = await db.auth.signUp({
      email, password,
      options: { emailRedirectTo: 'https://beqson.com/crm/' }
    });
    if (error) return setAuthStatus(humanAuthError(error.message), true);
    setAuthStatus('Готово. Проверьте письмо Supabase и подтвердите email. Затем вернитесь сюда и войдите.');
  });

  logoutBtn.addEventListener('click', () => db.auth.signOut());
  refreshBtn.addEventListener('click', loadLeads);
  search.addEventListener('input', render);

  async function loadLeads() {
    refreshBtn.disabled = true;
    refreshBtn.textContent = 'Обновляем…';
    const { data, error } = await db.from('leads').select('*').order('created_at', { ascending: false });
    refreshBtn.disabled = false;
    refreshBtn.textContent = 'Обновить';
    if (error) return toast('Не удалось загрузить заявки');
    leads = data || [];
    render();
  }

  function render() {
    const q = search.value.trim().toLowerCase();
    const visible = leads.filter(l => !q || [l.name,l.contact,l.niche,l.company,l.message,l.website].some(v => String(v || '').toLowerCase().includes(q)));
    renderStats(visible);
    board.innerHTML = '';
    for (const [key, label] of STATUS) {
      const col = document.createElement('section');
      col.className = 'column';
      const rows = visible.filter(l => l.status === key);
      col.innerHTML = `<div class="column-head"><h2>${label}</h2><span class="count">${rows.length}</span></div><div class="card-list"></div>`;
      const list = col.querySelector('.card-list');
      if (!rows.length) {
        list.innerHTML = '<div class="empty">Пока пусто</div>';
      } else {
        rows.forEach(lead => list.appendChild(makeCard(lead)));
      }
      board.appendChild(col);
    }
  }

  function renderStats(rows) {
    const won = rows.filter(x => ['won','in_progress','completed'].includes(x.status)).length;
    const fresh = rows.filter(x => x.status === 'new').length;
    const active = rows.filter(x => ['contacted','proposal','won','in_progress'].includes(x.status)).length;
    stats.innerHTML = [
      ['Всего заявок', rows.length], ['Новые', fresh], ['Активные', active], ['Клиенты', won]
    ].map(([label,val]) => `<article class="stat-card"><small>${label}</small><strong>${val}</strong></article>`).join('');
  }

  function makeCard(lead) {
    const el = document.createElement('article');
    el.className = 'lead-card';
    const date = new Intl.DateTimeFormat('ru-RU', {day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'}).format(new Date(lead.created_at));
    el.innerHTML = `<h3>${esc(lead.name)}</h3><p>${esc(lead.contact)}</p><p>${esc(lead.niche || 'Без ниши')}</p><div class="lead-meta"><span>${esc(lead.budget || 'Бюджет не указан')}</span><span>${date}</span></div>`;
    el.addEventListener('click', () => openLead(lead.id));
    return el;
  }

  function openLead(id) {
    const lead = leads.find(x => x.id === id);
    if (!lead) return;
    selectedId = id;
    const statusButtons = STATUS.map(([key,label]) => `<button type="button" class="status-btn ${lead.status === key ? 'active' : ''}" data-status="${key}">${label}</button>`).join('');
    leadDetail.innerHTML = `
      <div class="detail-title"><p class="eyebrow">LEAD DETAILS</p><h2>${esc(lead.name)}</h2><p class="muted">${esc(lead.niche || 'Без категории')}</p></div>
      <div class="detail-grid">
        ${detail('Контакт', lead.contact)}
        ${detail('Бюджет', lead.budget)}
        ${detail('Сайт', lead.website, true)}
        ${detail('Язык', (lead.language || '').toUpperCase())}
        ${detail('Источник', lead.source)}
        ${detail('Страница', lead.page_url, true)}
        ${detail('Referrer', lead.referrer, true)}
        ${detail('UTM', [lead.utm_source,lead.utm_medium,lead.utm_campaign].filter(Boolean).join(' / ') || '—')}
      </div>
      <div class="detail-message">${esc(lead.message || 'Сообщение не указано')}</div>
      <div class="status-row">${statusButtons}</div>
      <div class="notes-wrap"><label>Внутренняя заметка</label><textarea id="lead-notes" placeholder="Что обсудили, следующий шаг…">${esc(lead.internal_notes || '')}</textarea><button type="button" class="primary save-note" id="save-note">Сохранить заметку</button></div>`;

    leadDetail.querySelectorAll('[data-status]').forEach(btn => btn.addEventListener('click', () => updateStatus(id, btn.dataset.status)));
    $('#save-note').addEventListener('click', () => saveNote(id));
    leadDialog.showModal();
  }

  async function updateStatus(id, status) {
    const { error } = await db.from('leads').update({ status }).eq('id', id);
    if (error) return toast('Не удалось изменить статус');
    await db.from('lead_events').insert({ lead_id:id, event_type:'status_changed', details:{ status } });
    const lead = leads.find(x => x.id === id);
    if (lead) lead.status = status;
    toast('Статус обновлён');
    render();
    openLead(id);
  }

  async function saveNote(id) {
    const notes = $('#lead-notes').value.trim();
    const { error } = await db.from('leads').update({ internal_notes: notes || null }).eq('id', id);
    if (error) return toast('Не удалось сохранить заметку');
    const lead = leads.find(x => x.id === id);
    if (lead) lead.internal_notes = notes || null;
    await db.from('lead_events').insert({ lead_id:id, event_type:'note_updated', details:{} });
    toast('Заметка сохранена');
  }

  function detail(label, value, link=false) {
    const v = value || '—';
    if (link && /^https?:\/\//i.test(v)) return `<div class="detail-item"><small>${label}</small><a href="${escAttr(v)}" target="_blank" rel="noopener noreferrer">${esc(v)}</a></div>`;
    return `<div class="detail-item"><small>${label}</small><span>${esc(v)}</span></div>`;
  }

  function setAuthStatus(text, error=false) {
    authStatus.textContent = text;
    authStatus.className = `status ${error ? 'err' : 'ok'}`;
  }

  function humanAuthError(message) {
    if (/invalid login credentials/i.test(message)) return 'Неверный email или пароль.';
    if (/email not confirmed/i.test(message)) return 'Сначала подтвердите email по письму Supabase.';
    if (/already registered/i.test(message)) return 'Аккаунт уже создан. Используйте «Войти».';
    return message;
  }

  function toast(text) {
    document.querySelector('.toast')?.remove();
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = text;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2200);
  }

  function esc(value) {
    return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }
  function escAttr(value) { return esc(value).replace(/`/g,'&#96;'); }
})();
