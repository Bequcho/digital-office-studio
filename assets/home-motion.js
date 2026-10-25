/* BEQSON Homepage Motion — tiny dependency-free enhancement. */
(() => {
  'use strict';
  if (!document.querySelector('.classic-hero') || !document.querySelector('.beqson-work')) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduceMotion.matches || !('IntersectionObserver' in window)) return;

  // Mark only individual content pieces, preserving the section's own layout.
  const revealSelectors = [
    '.classic-hero-kicker', '.classic-hero h1', '.classic-hero-copy > p',
    '.classic-hero-actions', '.classic-value-card',
    '#services .section-heading > *', '#services .industry-card',
    '.audit-home-card', '.growth-section .section-heading > *',
    '.growth-section .step-card', '.growth-note',
    '.pricing-section .section-heading > *', '.price-card', '.pricing-bottom',
    '.beqson-work-heading > *', '.beqson-work-card', '.beqson-work-bottom',
    '.faq-grid > *', '.clutch-trust-card', '.contact-grid > *'
  ];

  const items = Array.from(document.querySelectorAll(revealSelectors.join(',')));
  if (!items.length) return;

  const groups = new Map();
  for (const item of items) {
    const group = item.closest('.classic-hero-copy, .classic-value-grid, .industry-grid, .steps-grid, .pricing-grid, .beqson-work-grid, .section-heading, .beqson-work-heading, .faq-grid, .contact-grid');
    if (group) {
      const index = groups.get(group) || 0;
      item.style.setProperty('--bq-delay', `${Math.min(index, 5) * 65}ms`);
      groups.set(group, index + 1);
    }
    item.classList.add('bq-reveal');
  }

  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('bq-visible');
      observer.unobserve(entry.target);
    }
  }, { rootMargin: '0px 0px -6% 0px', threshold: .06 });

  for (const item of items) observer.observe(item);
  document.documentElement.classList.add('bq-motion-ready');

  // Pointer-driven lighting and tilt only on devices that genuinely hover.
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  if (!finePointer.matches) return;

  document.querySelectorAll('.beqson-work-card').forEach(card => {
    let frame = 0;
    let latestX = 0;
    let latestY = 0;

    const paint = () => {
      frame = 0;
      const bounds = card.getBoundingClientRect();
      if (!bounds.width || !bounds.height) return;
      const x = Math.max(0, Math.min(1, (latestX - bounds.left) / bounds.width));
      const y = Math.max(0, Math.min(1, (latestY - bounds.top) / bounds.height));
      card.style.setProperty('--bq-pointer-x', `${(x * 100).toFixed(1)}%`);
      card.style.setProperty('--bq-pointer-y', `${(y * 100).toFixed(1)}%`);
      card.style.setProperty('--bq-tilt-x', `${((.5 - y) * 5).toFixed(2)}deg`);
      card.style.setProperty('--bq-tilt-y', `${((x - .5) * 5).toFixed(2)}deg`);
    };

    card.addEventListener('pointermove', event => {
      if (event.pointerType && event.pointerType !== 'mouse') return;
      latestX = event.clientX;
      latestY = event.clientY;
      if (!frame) frame = requestAnimationFrame(paint);
    }, { passive: true });

    card.addEventListener('pointerleave', () => {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      for (const property of ['--bq-pointer-x', '--bq-pointer-y', '--bq-tilt-x', '--bq-tilt-y']) {
        card.style.removeProperty(property);
      }
    });
  });
})();
