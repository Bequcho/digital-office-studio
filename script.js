'use strict';
document.documentElement.classList.add('js');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
if (menuButton && navigation) {
  const closeMenu = (returnFocus = navigation.contains(document.activeElement)) => {
    navigation.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', menuButton.dataset.openLabel);
    if (returnFocus) menuButton.focus();
  };
  menuButton.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') !== 'true';
    navigation.classList.toggle('is-open', expanded);
    menuButton.setAttribute('aria-expanded', String(expanded));
    menuButton.setAttribute('aria-label', expanded ? menuButton.dataset.closeLabel : menuButton.dataset.openLabel);
    // The disclosure links precede the toggle in DOM order; enter them on opening.
    if (expanded) navigation.querySelector('a')?.focus();
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
  window.matchMedia('(min-width: 1181px)').addEventListener('change', event => {
    // Keep keyboard focus visible when the desktop links become a hidden disclosure.
    const focusedLink = navigation.contains(document.activeElement);
    const focusedToggle = document.activeElement === menuButton;
    closeMenu(!event.matches && focusedLink);
    if (event.matches && focusedToggle) navigation.querySelector('a')?.focus();
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
