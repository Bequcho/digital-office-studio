/* Reference-derived light passes with an idle gap; original artwork stays static. */
(() => {
  'use strict';
  const brand = document.querySelector('.bq-brand');
  if (!brand) return;
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  const paths = [...brand.querySelectorAll('[data-light]')];
  const svg = brand.querySelector('.bq-contour');
  const pause = 3000;
  let data, loading = false, failed = false, active = false, parked = false;
  let frame = 0, timer = 0, phase = 'running', elapsed = 0, started = 0, previous = -1;
  const clearLight = () => {
    paths.forEach(path => path.removeAttribute('d'));
    svg.style.opacity = '';
  };
  const suspend = () => {
    if (active) elapsed += performance.now() - started;
    active = false;
    cancelAnimationFrame(frame); clearTimeout(timer); frame = timer = 0;
    brand.dataset.motion = media.matches || failed ? 'static' : 'paused';
  };
  const beginPass = () => {
    timer = 0;
    if (!active || document.hidden || media.matches) { suspend(); return; }
    phase = 'running'; elapsed = 0; previous = -1; started = performance.now();
    brand.dataset.motion = 'running'; frame = requestAnimationFrame(paint);
  };
  const paint = now => {
    frame = 0;
    if (!active) return;
    if (document.hidden || media.matches) { suspend(); return; }
    const time = elapsed + now - started, duration = data.duration * 1000;
    if (time >= duration) {
      clearLight(); phase = 'pause'; elapsed = 0; started = now;
      brand.dataset.motion = 'static'; timer = setTimeout(beginPass, pause);
      return;
    }
    const index = Math.min(145, Math.max(0, Math.floor(time * data.fps / 1000)));
    if (index !== previous) {
      paths.forEach((path, i) => path.setAttribute('d', data.frames[index][i]));
      previous = index;
    }
    const opacity = String(Math.min(1, (duration - time) / 350));
    if (svg.style.opacity !== opacity) svg.style.opacity = opacity;
    frame = requestAnimationFrame(paint);
  };
  const resume = async () => {
    if (parked || document.hidden || media.matches || active || failed || loading) return;
    if (!data) {
      loading = true;
      try {
        const response = await fetch('/assets/brand/beqson-contours.json?v=1');
        if (!response.ok) throw new Error('Light data unavailable');
        data = await response.json();
        if (data.frames?.length !== 146 || data.fps !== 30 || !Number.isFinite(data.duration) || data.duration <= 0) throw new Error('Invalid light data');
      } catch (_) {
        failed = true; clearLight(); brand.dataset.motion = 'static'; return;
      } finally { loading = false; }
    }
    if (parked || document.hidden || media.matches || active) return;
    active = true; started = performance.now();
    brand.dataset.motion = phase === 'running' ? 'running' : 'static';
    if (phase === 'running') frame = requestAnimationFrame(paint);
    else timer = setTimeout(beginPass, Math.max(0, pause - elapsed));
  };
  document.addEventListener('visibilitychange', () => document.hidden ? suspend() : resume());
  window.addEventListener('pagehide', () => { parked = true; suspend(); });
  window.addEventListener('pageshow', () => { parked = false; resume(); });
  media.addEventListener('change', () => {
    if (media.matches) {
      suspend(); clearLight(); phase = 'running'; elapsed = 0; previous = -1;
      brand.dataset.motion = 'static';
    } else resume();
  });
  resume();
})();

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
