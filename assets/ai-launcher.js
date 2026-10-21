/* BEQSON AI Consultant: lightweight, lazy-loaded on-site chat panel. */
(() => {
  'use strict';
  const id = 'beqson-ai-assistant-link';
  const panelId = 'beqson-ai-panel';
  const href = 'https://k4h7xqtesbe9.run.agentplace.io/';
  const copy = {
    ka: { label: 'ჰკითხეთ AI-ს', heading: 'BEQSON AI კონსულტანტი', open: 'სრულ ეკრანზე გახსნა', close: 'ჩატის დახურვა', aria: 'გახსენით BEQSON-ის AI ჩატი' },
    ru: { label: 'Спросить AI', heading: 'AI-консультант BEQSON', open: 'Открыть на весь экран', close: 'Закрыть чат', aria: 'Открыть AI-консультанта BEQSON' },
    en: { label: 'Ask AI', heading: 'BEQSON AI Consultant', open: 'Open full screen', close: 'Close chat', aria: 'Open BEQSON AI chat' }
  };
  function mount() {
    if (!document.body || document.getElementById(id)) return;
    const lang = (document.documentElement.lang || '').toLowerCase().split('-')[0];
    const words = copy[lang] || copy.en;
    if (!document.getElementById('beqson-ai-launcher-styles')) {
      const style = document.createElement('style');
      style.id = 'beqson-ai-launcher-styles';
      style.textContent = "#beqson-ai-assistant-link {\n position:fixed; right:22px; bottom:calc(22px + env(safe-area-inset-bottom, 0px)); z-index:2147483001;\n display:inline-flex; justify-content:center; align-items:center; gap:10px; min-height:48px;\n max-width:calc(100vw - 28px); padding:11px 17px; border:1px solid rgba(99,189,255,.65);\n border-radius:999px; background:linear-gradient(135deg,#0c2141 0%,#0e3564 60%,#173e76 100%);\n box-shadow:0 10px 28px rgba(3,12,35,.36),0 0 21px rgba(43,152,255,.32),inset 0 1px 0 rgba(255,255,255,.2);\n color:#f5faff; font:800 13px/1.25 Manrope,Georgian,Arial,sans-serif; letter-spacing:.01em;\n text-decoration:none; white-space:nowrap; cursor:pointer; appearance:none; -webkit-tap-highlight-color:transparent;\n transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;\n}\n#beqson-ai-assistant-link:hover {transform:translateY(-3px);border-color:#9cdcff;box-shadow:0 15px 34px rgba(3,12,35,.38),0 0 25px rgba(43,152,255,.52)}\n#beqson-ai-assistant-link:focus-visible, #beqson-ai-panel button:focus-visible,#beqson-ai-panel a:focus-visible {outline:3px solid #8cd8ff;outline-offset:3px}\n#beqson-ai-assistant-link .beqson-ai-sparkle {\n display:inline-flex;align-items:center;justify-content:center;width:25px;height:25px;\n border-radius:50%;color:#c9efff;background:rgba(81,174,255,.2);font-size:20px;line-height:1;\n}\nbody:has(.bls-launcher) #beqson-ai-assistant-link {bottom:calc(92px + env(safe-area-inset-bottom, 0px))}\nbody.beqson-ai-open #beqson-ai-assistant-link {visibility:hidden}\nbody:has(.beqson-lead-system.is-open) #beqson-ai-assistant-link,\nbody:has(.beqson-lead-system.is-open) #beqson-ai-panel,\nbody.modal-open #beqson-ai-assistant-link,\nbody:has(dialog[open]) #beqson-ai-assistant-link {display:none!important}\n#beqson-ai-panel[hidden]{display:none!important}\n#beqson-ai-panel{\n position:fixed;right:22px;bottom:calc(158px + env(safe-area-inset-bottom, 0px));z-index:2147483002;\n display:flex;flex-direction:column;overflow:hidden;width:min(425px,calc(100vw - 32px));\n height:min(660px,calc(100dvh - 178px - env(safe-area-inset-bottom, 0px)));\n min-height:300px;border:1px solid rgba(115,194,255,.65);border-radius:23px;\n background:#061327; box-shadow:0 25px 70px rgba(1,9,28,.6),0 0 30px rgba(56,146,255,.2);\n color:#f5faff;font:500 14px/1.4 Manrope,Georgian,Arial,sans-serif;\n}\n#beqson-ai-panel .beqson-ai-head{\n display:flex;align-items:center;gap:10px;flex:0 0 auto;min-height:57px;padding:10px 12px 10px 17px;\n background:linear-gradient(110deg,#102b50,#0c1f3d);border-bottom:1px solid rgba(130,187,255,.3);\n}\n#beqson-ai-panel .beqson-ai-dot{display:block;flex:0 0 auto;width:9px;height:9px;border-radius:50%;background:#53e6a8;box-shadow:0 0 0 5px rgba(83,230,168,.09)}\n#beqson-ai-panel .beqson-ai-heading{flex:1;min-width:0;margin:0;color:#f5faff;font-size:13px;font-weight:800;line-height:1.35;overflow-wrap:anywhere}\n#beqson-ai-panel .beqson-ai-action{\n flex:0 0 auto;display:inline-flex;justify-content:center;align-items:center;\n min-width:35px;min-height:35px;padding:4px;border:1px solid rgba(150,204,255,.32);\n border-radius:10px;background:rgba(255,255,255,.06);color:#e9f5ff;\n text-decoration:none;font:700 22px/1 Arial,sans-serif;cursor:pointer;\n}\n#beqson-ai-panel .beqson-ai-action:hover{background:rgba(80,165,255,.18)}\n#beqson-ai-panel .beqson-ai-frame{display:block;flex:1 1 auto;width:100%;min-height:0;border:0;background:#061327}\n#beqson-ai-panel .beqson-ai-foot{\n display:flex;align-items:center;justify-content:center;flex:0 0 auto;\n padding:6px 12px;background:#091a32;border-top:1px solid rgba(130,187,255,.22);\n}\n#beqson-ai-panel .beqson-ai-foot a{font-size:11px;color:#a7d9ff;text-decoration:underline;text-underline-offset:3px}\n@media (max-width:600px) {\n #beqson-ai-assistant-link {right:13px;bottom:calc(17px + env(safe-area-inset-bottom,0px));padding:10px 14px;min-height:48px;font-size:12px}\n body:has(.bls-launcher) #beqson-ai-assistant-link {bottom:calc(79px + env(safe-area-inset-bottom,0px))}\n #beqson-ai-assistant-link .beqson-ai-sparkle{width:24px;height:24px}\n #beqson-ai-panel {\n   right:10px;bottom:calc(10px + env(safe-area-inset-bottom,0px));width:calc(100vw - 20px);\n   height:calc(100dvh - 20px - env(safe-area-inset-bottom,0px));max-height:none;min-height:0;\n   border-radius:19px;\n }\n #beqson-ai-panel .beqson-ai-head{min-height:53px}\n}\n@media (prefers-reduced-motion:reduce){#beqson-ai-assistant-link{transition:none}#beqson-ai-assistant-link:hover{transform:none}}";
      document.head.appendChild(style);
    }
    const trigger = document.createElement('button');
    trigger.id = id;
    trigger.type = 'button';
    trigger.setAttribute('aria-label', words.aria);
    trigger.setAttribute('aria-controls', panelId);
    trigger.setAttribute('aria-expanded', 'false');
    trigger.title = words.aria;
    const sparkle = document.createElement('span');
    sparkle.className = 'beqson-ai-sparkle';
    sparkle.setAttribute('aria-hidden', 'true');
    sparkle.textContent = '✦';
    const label = document.createElement('span');
    label.textContent = words.label;
    trigger.append(sparkle, label);

    const panel = document.createElement('section');
    panel.id = panelId;
    panel.hidden = true;
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'false');
    panel.setAttribute('aria-label', words.heading);
    const head = document.createElement('div');
    head.className = 'beqson-ai-head';
    const dot = document.createElement('span');
    dot.className = 'beqson-ai-dot';
    dot.setAttribute('aria-hidden', 'true');
    const heading = document.createElement('strong');
    heading.className = 'beqson-ai-heading';
    heading.textContent = words.heading;
    const fullscreen = document.createElement('a');
    fullscreen.className = 'beqson-ai-action';
    fullscreen.href = href;
    fullscreen.target = '_blank';
    fullscreen.rel = 'noopener noreferrer';
    fullscreen.textContent = '↗';
    fullscreen.title = words.open;
    fullscreen.setAttribute('aria-label', words.open);
    const closeButton = document.createElement('button');
    closeButton.className = 'beqson-ai-action';
    closeButton.type = 'button';
    closeButton.textContent = '×';
    closeButton.title = words.close;
    closeButton.setAttribute('aria-label', words.close);
    head.append(dot, heading, fullscreen, closeButton);

    const foot = document.createElement('div');
    foot.className = 'beqson-ai-foot';
    const fullLink = document.createElement('a');
    fullLink.href = href;
    fullLink.target = '_blank';
    fullLink.rel = 'noopener noreferrer';
    fullLink.textContent = words.open;
    foot.appendChild(fullLink);
    panel.appendChild(head);
    panel.appendChild(foot);

    let initialized = false;
    function openChat() {
      if (!initialized) {
        const frame = document.createElement('iframe');
        frame.className = 'beqson-ai-frame';
        frame.title = words.heading;
        frame.src = href;
        frame.setAttribute('allow', 'microphone; clipboard-write');
        frame.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
        panel.insertBefore(frame, foot);
        initialized = true;
      }
      panel.hidden = false;
      document.body.classList.add('beqson-ai-open');
      trigger.setAttribute('aria-expanded', 'true');
      closeButton.focus({ preventScroll: true });
    }
    function closeChat() {
      if (panel.hidden) return;
      panel.hidden = true;
      document.body.classList.remove('beqson-ai-open');
      trigger.setAttribute('aria-expanded', 'false');
      trigger.focus({ preventScroll: true });
    }
    trigger.addEventListener('click', () => panel.hidden ? openChat() : closeChat());
    closeButton.addEventListener('click', closeChat);
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !panel.hidden) closeChat();
    });
    document.addEventListener('pointerdown', event => {
      if (!panel.hidden && !panel.contains(event.target) && !trigger.contains(event.target)) {
        closeChat();
      }
    });
    document.body.append(trigger, panel);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount, { once: true });
  } else {
    mount();
  }
})();
