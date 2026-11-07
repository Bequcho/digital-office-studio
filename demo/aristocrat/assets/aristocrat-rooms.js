(() => {
  'use strict';
  const galleries = JSON.parse(document.getElementById('room-gallery-data').textContent);
  const dialog = document.querySelector('[data-room-gallery]');
  const photo = dialog.querySelector('.gallery-image');
  const heading = document.getElementById('room-gallery-title');
  const caption = document.getElementById('room-gallery-caption');
  const counter = dialog.querySelector('.gallery-count');
  let group;
  let current = 0;
  let opener;
  let revision = 0;
  let touch;
  const show = index => {
    const items = galleries[group].photos;
    current = (index + items.length) % items.length;
    const item = items[current];
    const request = ++revision;
    dialog.classList.add('is-changing');
    photo.src = '/demo/aristocrat/assets/' + item.src;
    photo.alt = item.alt;
    caption.textContent = item.caption;
    counter.textContent = `${current + 1} / ${items.length}`;
    photo.decode().catch(() => {}).finally(() => {
      if (request === revision) dialog.classList.remove('is-changing');
    });
  };
  document.querySelectorAll('[data-room-set]').forEach(button => {
    button.addEventListener('click', () => {
      group = button.dataset.roomSet;
      opener = button;
      heading.textContent = galleries[group].title;
      show(Number(button.dataset.roomIndex));
      dialog.showModal();
      document.body.classList.add('gallery-open');
      dialog.querySelector('.gallery-close').focus();
    });
  });
  dialog.querySelector('.gallery-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.gallery-prev').addEventListener('click', () => show(current - 1));
  dialog.querySelector('.gallery-next').addEventListener('click', () => show(current + 1));
  dialog.addEventListener('keydown', event => {
    const move = { ArrowLeft: current - 1, ArrowRight: current + 1, Home: 0, End: galleries[group].photos.length - 1 };
    if (Object.hasOwn(move, event.key)) {
      event.preventDefault();
      show(move[event.key]);
    }
  });
  photo.addEventListener('touchstart', event => {
    touch = event.touches.length === 1 ? { x: event.touches[0].clientX, y: event.touches[0].clientY } : null;
  }, { passive: true });
  photo.addEventListener('touchend', event => {
    if (!touch || !event.changedTouches.length) return;
    const dx = event.changedTouches[0].clientX - touch.x;
    const dy = event.changedTouches[0].clientY - touch.y;
    touch = null;
    if (Math.abs(dx) >= 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(current + (dx < 0 ? 1 : -1));
  }, { passive: true });
  photo.addEventListener('touchcancel', () => { touch = null; }, { passive: true });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('gallery-open');
    touch = null;
    opener?.focus({ preventScroll: true });
  });
})();
