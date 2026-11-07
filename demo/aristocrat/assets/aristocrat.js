(() => {
  'use strict';
  const header = document.querySelector('[data-header]');
  const toggle = header.querySelector('.menu-toggle');
  const nav = header.querySelector('.navigation');
  const closeMenu = (restoreFocus = false) => {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'მენიუს გახსნა');
    nav.classList.remove('is-open');
    document.body.classList.remove('menu-open');
    if (restoreFocus) toggle.focus();
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'მენიუს დახურვა' : 'მენიუს გახსნა');
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
  });
  nav.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('click', event => {
    if (!header.contains(event.target)) closeMenu();
  });
  header.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu(true);
    if (event.key !== 'Tab' || toggle.getAttribute('aria-expanded') !== 'true') return;
    const last = nav.querySelector('a:last-child');
    if (event.shiftKey && document.activeElement === toggle) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); toggle.focus();
    }
  });
  const desktop = matchMedia('(min-width: 901px)');
  desktop.addEventListener('change', () => closeMenu());

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  if (!reducedMotion.matches && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
    document.documentElement.classList.add('js-motion');
    reducedMotion.addEventListener('change', event => {
      if (event.matches) {
        document.documentElement.classList.remove('js-motion');
        observer.disconnect();
      }
    });
  }

  const dialog = document.querySelector('.photo-dialog');
  if (!dialog) return;
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const controls = [...dialog.querySelectorAll('button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])')]
      .filter(element => element.getClientRects().length > 0);
    const first = controls[0];
    const last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); first.focus();
    }
  });
  if (dialog.hasAttribute('data-room-gallery')) return;
  const galleryImage = dialog.querySelector('.gallery-image');
  const count = dialog.querySelector('.gallery-count');
  const photos = [
    ['room-spacious-double.webp', 'საოჯახო სტუდიო ორადგილიანი და ერთადგილიანი საწოლებით'],
    ['room-double.webp', 'ნომერი ორადგილიანი საწოლითა და ხის ავეჯით'],
    ['room-twin-cozy.webp', 'ორი ერთადგილიანი საწოლი თბილად განათებულ ნომერში']
  ];
  let current = 0;
  let opener;
  const showPhoto = index => {
    current = (index + photos.length) % photos.length;
    galleryImage.src = '/demo/aristocrat/assets/' + photos[current][0];
    galleryImage.alt = photos[current][1];
    count.textContent = `${current + 1} / ${photos.length}`;
  };
  document.querySelectorAll('[data-gallery]').forEach(button => {
    button.addEventListener('click', () => {
      opener = button;
      showPhoto(Number(button.dataset.gallery));
      dialog.showModal();
      document.body.classList.add('gallery-open');
      dialog.querySelector('.gallery-close').focus();
    });
  });
  dialog.querySelector('.gallery-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.gallery-prev').addEventListener('click', () => showPhoto(current - 1));
  dialog.querySelector('.gallery-next').addEventListener('click', () => showPhoto(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showPhoto(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('gallery-open');
    opener?.focus({ preventScroll: true });
  });
})();
