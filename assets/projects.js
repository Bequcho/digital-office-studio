document.addEventListener('DOMContentLoaded',()=>{const buttons=[...document.querySelectorAll('[data-project-filter]')],cards=[...document.querySelectorAll('[data-project-cat]')];buttons.forEach(b=>b.addEventListener('click',()=>{buttons.forEach(x=>x.classList.remove('active'));b.classList.add('active');const f=b.dataset.projectFilter;cards.forEach(c=>c.hidden=!(f==='all'||c.dataset.projectCat===f));}));});

/* Load the optional BEQSON AI Consultant link without changing existing page flows. */
(() => {
  if (document.querySelector('script[data-beqson-ai-launcher]')) return;
  const el = document.createElement('script');
  el.dataset.beqsonAiLauncher = '1';
  el.src = '/assets/ai-launcher.js?v=2';
  document.head.appendChild(el);
})();
