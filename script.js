'use strict';
document.documentElement.classList.add('js');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
if (menuButton && navigation) {
  const closeMenu = (returnFocus = false) => {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    if (returnFocus) menuButton.focus();
  };
  menuButton.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') !== 'true';
    navigation.classList.toggle('is-open', expanded);
    menuButton.setAttribute('aria-expanded', String(expanded));
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
  window.matchMedia('(min-width: 1001px)').addEventListener('change', event => {
    if (event.matches) closeMenu();
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
