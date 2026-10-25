/* Kakheti Wine House Shopify 360 preview. Does not alter native product forms. */
(() => {
  'use strict';
  const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)');
  const instances = [];
  let lastFrame = 0;

  const renderAngle = instance => {
    instance.rotor.style.transform = `rotateX(-6deg) rotateY(${instance.angle.toFixed(2)}deg)`;
  };
  function init(root) {
    if (root.dataset.kwsReady === 'true') return;
    const dialog = root.querySelector('[data-kws-dialog]');
    const gallery = document.querySelector('main media-gallery');
    if (!dialog || !gallery || typeof dialog.showModal !== 'function') return;
    root.dataset.kwsReady = 'true';

    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'kws-gallery-trigger';
    trigger.textContent = root.dataset.kwsTriggerLabel;
    gallery.appendChild(trigger);

    const body = root.querySelector('[data-kws-body]');
    const neck = root.querySelector('[data-kws-neck]');
    for (let step = 0; step < 24; step++) {
      const facet = document.createElement('span');
      facet.className = 'kws-facet';
      facet.style.setProperty('--step', step);
      facet.style.setProperty('--shade', `${Math.round(63 + 34 * Math.max(0, Math.cos(step * Math.PI / 12)))}%`);
      body.appendChild(facet);
    }
    for (let step = 0; step < 16; step++) {
      const facet = document.createElement('span');
      facet.className = 'kws-neck-facet';
      facet.style.setProperty('--step', step);
      neck.appendChild(facet);
    }

    const instance = {
      dialog, root,
      scene: root.querySelector('[data-kws-scene]'),
      drag: root.querySelector('[data-kws-drag]'),
      rotor: root.querySelector('[data-kws-rotor]'),
      canvas: root.querySelector('[data-kws-webgl]'),
      modelURL: root.dataset.kwsModelUrl,
      webgl: null, webglStarted: false,
      spinning: !prefersReduced.matches,
      angle: -23, dragInfo: null, resumeAt: 0,
      mode: 'model', zoomed: false,
    };
    renderAngle(instance);
    instances.push(instance);
    const spin = root.querySelector('[data-kws-spin]');
    const zoom = root.querySelector('[data-kws-zoom]');
    const locale = (document.documentElement.lang || 'en').toLowerCase();
    const language = locale.startsWith('ka') ? 'ka' : locale.startsWith('ru') ? 'ru' : 'en';
    const copy = {
      en: { back: 'Rear label', rearAlt: 'AI-designed back of the wine bottle',
        note: 'Original front photograph, AI-designed rear label and reconstructed glass sides. The rear label is a design concept.' },
      ru: { back: 'Задняя сторона', rearAlt: 'Созданная задняя сторона бутылки вина',
        note: 'Спереди — оригинальное фото, сзади — созданная дизайнерская контрэтикетка, по бокам — 3D-реконструкция. Задняя этикетка является концептом.' },
      ka: { back: 'უკანა მხარე', rearAlt: 'ბოთლის კონცეპტუალური უკანა ეტიკეტი',
        note: 'წინ — ორიგინალი ფოტო, უკან — AI-ით შექმნილი ეტიკეტის კონცეფცია; გვერდები 3D რეკონსტრუქციაა.' },
    }[language];
    const photo = root.querySelector('.kws-original');
    const frontSrc = photo?.getAttribute('src') || '';
    const frontSrcset = photo?.getAttribute('srcset');
    // Both assets are in the SAME Shopify draft theme; the GLB carries a
    // version query parameter while the additional rear JPG is loaded by path.
    const backSrc = String(instance.modelURL || '').replace(/\.glb(?:\?[^#]*)?$/, '-back.jpg');
    if (backSrc !== instance.modelURL && photo) {
      const backTab = document.createElement('button');
      backTab.type = 'button';
      backTab.dataset.kwsMode = 'back';
      backTab.textContent = copy.back;
      backTab.setAttribute('aria-pressed', 'false');
      root.querySelector('.kws-tabs')?.appendChild(backTab);
    }
    const disclosure = root.querySelector('.kws-disclosure');
    if (disclosure) disclosure.textContent = copy.note;

    const selectMode = mode => {
      instance.mode = mode;
      dialog.classList.toggle('is-photo', mode === 'photo' || mode === 'back');
      if (photo && (mode === 'photo' || mode === 'back')) {
        if (mode === 'back') {
          photo.removeAttribute('srcset');
          photo.alt = copy.rearAlt;
          if (photo.getAttribute('src') !== backSrc) photo.src = backSrc;
        } else {
          if (frontSrcset !== null) photo.setAttribute('srcset', frontSrcset);
          if (photo.getAttribute('src') !== frontSrc) photo.src = frontSrc;
        }
      }
      root.querySelectorAll('[data-kws-mode]').forEach(item => {
        const active = item.dataset.kwsMode === mode;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      });
    };
    photo?.addEventListener('error', () => {
      // A missing concept asset should never leave a broken image in the UI.
      if (instance.mode === 'back') selectMode('photo');
    });

    const photoFallback = error => {
      // Never expose the old CSS cardboard-style bottle if the browser lacks
      // WebGL2 or if the real model fails to load. A real photo is more honest.
      console.warn('Kakheti 3D preview: showing original product photo', error);
      instance.webglStarted = true;
      instance.scene.classList.add('is-webgl-unavailable');
      const messages = {
        en: {trigger: 'View bottle photos', note: '3D is unavailable in this browser. You can view the real front photo and the AI-designed rear label concept.'},
        ru: {trigger: 'Посмотреть бутылку', note: 'В этом браузере 3D недоступно. Можно посмотреть настоящее фото спереди и созданную заднюю этикетку.'},
        ka: {trigger: 'ბოთლის ფოტოები', note: 'ამ ბრაუზერში 3D მიუწვდომელია. შეგიძლიათ იხილოთ ორიგინალი წინა ფოტო და შექმნილი უკანა ეტიკეტი.'},
      }[language];
      trigger.textContent = messages.trigger;
      const info = root.querySelector('.kws-disclosure');
      if (info) info.textContent = messages.note;
      const modelButton = root.querySelector('[data-kws-mode="model"]');
      if (modelButton) {
        modelButton.disabled = true;
        modelButton.title = messages.note;
      }
      selectMode('photo');
    };

    const open = () => {
      if (dialog.open) return;
      dialog.showModal();
      instance.drag.focus({ preventScroll: true });
      if (!instance.webglStarted && window.Kakheti3DViewer && instance.modelURL) {
        instance.webglStarted = true;
        window.Kakheti3DViewer.create(instance.canvas, instance.modelURL)
          .then(renderer => {
            instance.webgl = renderer;
            instance.scene.classList.add('is-webgl-ready');
          })
          .catch(photoFallback);
      } else if (!instance.webglStarted) {
        photoFallback(new Error('3D renderer or model URL unavailable'));
      }
    };
    const close = () => {
      if (dialog.open) dialog.close();
      trigger.focus({ preventScroll: true });
    };
    trigger.addEventListener('click', open);
    root.querySelectorAll('[data-kws-close]').forEach(button => button.addEventListener('click', close));
    dialog.addEventListener('click', event => { if (event.target === dialog) close(); });

    root.querySelectorAll('[data-kws-mode]').forEach(button => button.addEventListener('click', () => {
      if (!button.disabled) selectMode(button.dataset.kwsMode);
    }));
    spin.addEventListener('click', () => {
      instance.spinning = !instance.spinning;
      instance.resumeAt = 0;
      spin.setAttribute('aria-pressed', String(instance.spinning));
      spin.textContent = `${instance.spinning ? '❚❚' : '↻'} ${spin.dataset.label}`;
    });
    zoom.addEventListener('click', () => {
      instance.zoomed = !instance.zoomed;
      instance.scene.classList.toggle('is-zoomed', instance.zoomed);
      zoom.setAttribute('aria-pressed', String(instance.zoomed));
      zoom.textContent = `${instance.zoomed ? '−' : '+'} ${zoom.dataset.label}`;
    });
    spin.setAttribute('aria-pressed', String(instance.spinning));
    zoom.setAttribute('aria-pressed', 'false');

    instance.drag.addEventListener('pointerdown', event => {
      if (event.pointerType === 'mouse' && event.button !== 0) return;
      instance.dragInfo = { pointerId: event.pointerId, x: event.clientX, angle: instance.angle };
      instance.resumeAt = Infinity;
      instance.drag.classList.add('is-dragging');
      try { instance.drag.setPointerCapture(event.pointerId); } catch {}
      event.preventDefault();
    });
    instance.drag.addEventListener('pointermove', event => {
      const drag = instance.dragInfo;
      if (!drag || drag.pointerId !== event.pointerId) return;
      instance.angle = drag.angle + (event.clientX - drag.x) * .7;
      renderAngle(instance);
    });
    function endDrag(event) {
      const drag = instance.dragInfo;
      if (!drag || drag.pointerId !== event.pointerId) return;
      instance.dragInfo = null;
      instance.drag.classList.remove('is-dragging');
      instance.resumeAt = performance.now() + 1400;
      try { if (instance.drag.hasPointerCapture(event.pointerId)) instance.drag.releasePointerCapture(event.pointerId); } catch {}
    }
    instance.drag.addEventListener('pointerup', endDrag);
    instance.drag.addEventListener('pointercancel', endDrag);
    instance.drag.addEventListener('keydown', event => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault();
      instance.angle += event.key === 'ArrowLeft' ? -15 : 15;
      instance.resumeAt = performance.now() + 1200;
      renderAngle(instance);
    });
  }
  const loop = now => {
    const dt = lastFrame ? Math.min(50, now - lastFrame) : 0;
    lastFrame = now;
    if (!document.hidden) {
      for (const instance of instances) {
        if (instance.dialog.open && instance.mode === 'model') {
          if (instance.spinning && !instance.dragInfo && now >= instance.resumeAt) {
            instance.angle += dt * .016;
            renderAngle(instance);
          }
          if (instance.webgl) instance.webgl.render(instance.angle, instance.zoomed);
        }
      }
    }
    requestAnimationFrame(loop);
  };
  document.querySelectorAll('[data-kws-root]').forEach(init);
  requestAnimationFrame(loop);
})();

