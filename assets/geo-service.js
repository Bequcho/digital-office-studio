(() => {
  'use strict';
  const form = document.getElementById('geo-self-form');
  const result = document.getElementById('geo-result');
  if (!form || !result) return;
  const inputs = Array.from(form.querySelectorAll('input[type="checkbox"]'));
  const site = document.getElementById('geo-website');
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const missing = inputs.filter(input => !input.checked);
    const count = inputs.length - missing.length;
    document.getElementById('geo-score').textContent = count + ' / ' + inputs.length;
    const ul = document.getElementById('geo-advice');
    ul.replaceChildren();
    const items = missing.length ? missing.map(input => input.dataset.advice) : [document.body.dataset.allGood];
    for (const advice of items) {
      const li = document.createElement('li');
      li.textContent = advice;
      ul.appendChild(li);
    }
    const language = document.body.dataset.lang || 'en';
    const intro = {ru:'Здравствуйте! Интересует GEO Audit BEQSON.',ka:'გამარჯობა! მაინტერესებს BEQSON GEO Audit.',en:'Hello! I am interested in BEQSON GEO Audit.'}[language];
    const website = site.value.trim();
    const lines = [intro, website ? 'Website: ' + website : '', 'Self-check: ' + count + '/' + inputs.length, ...items.map(v => '- ' + v)].filter(Boolean);
    document.getElementById('geo-send').href = 'https://wa.me/995551739333?text=' + encodeURIComponent(lines.join('\n'));
    result.hidden = false;
    result.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth', block:'nearest'});
  });
})();
