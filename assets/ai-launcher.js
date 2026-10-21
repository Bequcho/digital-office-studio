/* BEQSON AI Consultant: unobtrusive outbound launcher, no embedded third-party scripts. */
(() => {
  'use strict';
  const id = 'beqson-ai-assistant-link';
  const href = 'https://k4h7xqtesbe9.run.agentplace.io/';
  const copy = {
    ka: { label: 'ჰკითხეთ AI-ს', aria: 'გახსენით BEQSON-ის AI კონსულტანტი ახალ ჩანართში' },
    ru: { label: 'Спросить AI', aria: 'Открыть AI-консультанта BEQSON в новой вкладке' },
    en: { label: 'Ask AI', aria: 'Open BEQSON AI Consultant in a new tab' }
  };
  function mount() {
    if (!document.body || document.getElementById(id)) return;
    const lang = (document.documentElement.lang || '').toLowerCase().split('-')[0];
    const words = copy[lang] || copy.en;
    if (!document.getElementById('beqson-ai-launcher-styles')) {
      const style = document.createElement('style');
      style.id = 'beqson-ai-launcher-styles';
      style.textContent = "#beqson-ai-assistant-link {\n  position: fixed;\n  right: 22px;\n  bottom: calc(22px + env(safe-area-inset-bottom, 0px));\n  z-index: 65;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  gap: 10px;\n  max-width: calc(100vw - 28px);\n  min-height: 48px;\n  padding: 11px 17px;\n  border: 1px solid rgba(99, 189, 255, .65);\n  border-radius: 999px;\n  background: linear-gradient(135deg, #0c2141 0%, #0e3564 60%, #173e76 100%);\n  box-shadow: 0 10px 28px rgba(3, 12, 35, .36), 0 0 21px rgba(43, 152, 255, .32), inset 0 1px 0 rgba(255, 255, 255, .20);\n  color: #f5faff;\n  font: 800 13px/1.25 Manrope, Georgian, Arial, sans-serif;\n  letter-spacing: .01em;\n  text-decoration: none;\n  white-space: nowrap;\n  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;\n  -webkit-tap-highlight-color: transparent;\n}\n#beqson-ai-assistant-link:hover {\n  transform: translateY(-3px);\n  border-color: #9cdcff;\n  box-shadow: 0 15px 34px rgba(3, 12, 35, .38), 0 0 25px rgba(43, 152, 255, .52);\n}\n#beqson-ai-assistant-link:focus-visible {\n  outline: 3px solid #8cd8ff;\n  outline-offset: 4px;\n}\n#beqson-ai-assistant-link .beqson-ai-sparkle {\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  width: 25px;\n  height: 25px;\n  border-radius: 50%;\n  color: #c9efff;\n  background: rgba(81, 174, 255, .20);\n  font-size: 20px;\n  line-height: 1;\n}\nbody.modal-open #beqson-ai-assistant-link,\nbody:has(dialog[open]) #beqson-ai-assistant-link { display: none; }\n@media (max-width: 600px) {\n  #beqson-ai-assistant-link { right: 13px; bottom: calc(17px + env(safe-area-inset-bottom, 0px)); padding: 10px 14px; min-height: 48px; font-size: 12px; }\n  #beqson-ai-assistant-link .beqson-ai-sparkle { width: 24px; height: 24px; }\n}\n@media (prefers-reduced-motion: reduce) {\n  #beqson-ai-assistant-link { transition: none; }\n  #beqson-ai-assistant-link:hover { transform: none; }\n}";
      document.head.appendChild(style);
    }
    const link = document.createElement('a');
    link.id = id;
    link.href = href;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.setAttribute('aria-label', words.aria);
    link.title = words.aria;
    const sparkle = document.createElement('span');
    sparkle.className = 'beqson-ai-sparkle';
    sparkle.setAttribute('aria-hidden', 'true');
    sparkle.textContent = '✦';
    const label = document.createElement('span');
    label.textContent = words.label;
    link.append(sparkle, label);
    document.body.appendChild(link);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount, { once: true });
  } else {
    mount();
  }
})();
