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

    const selectMode = mode => {
      instance.mode = mode;
      dialog.classList.toggle('is-photo', mode === 'photo');
      root.querySelectorAll('[data-kws-mode]').forEach(item => {
        const active = item.dataset.kwsMode === mode;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      });
    };

    const photoFallback = error => {
      // Never expose the old CSS cardboard-style bottle if the browser lacks
      // WebGL2 or if the real model fails to load. A real photo is more honest.
      console.warn('Kakheti 3D preview: showing original product photo', error);
      instance.webglStarted = true;
      instance.scene.classList.add('is-webgl-unavailable');
      const locale = (document.documentElement.lang || 'en').toLowerCase();
      const language = locale.startsWith('ka') ? 'ka' : locale.startsWith('ru') ? 'ru' : 'en';
      const messages = {
        en: {trigger: 'View bottle photo', note: '3D is not available in this browser. Showing the original product photograph.'},
        ru: {trigger: 'Посмотреть фото', note: 'В этом браузере 3D недоступно. Показываем настоящую фотографию бутылки.'},
        ka: {trigger: 'ბოთლის ფოტოს ნახვა', note: 'ამ ბრაუზერში 3D მიუწვდომელია. ნაჩვენებია ბოთლის ნამდვილი ფოტო.'},
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

