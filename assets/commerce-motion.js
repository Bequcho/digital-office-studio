/* Commerce Motion: real UI interactions with a fictional, client-side-only cart. */
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const copy = JSON.parse($('#cm-copy').textContent);
  const tones = ['arctic', 'graphite', 'sand'];
  const stage = $('[data-stage]');
  const rotor = $('[data-rotor]');
  const turntable = $('[data-turntable]');
  const cartButton = $('[data-open-cart]');
  const panel = $('[data-cart-panel]');
  const backdrop = $('[data-backdrop]');
  const cartContent = $('[data-cart-content]');
  const cartBottom = $('[data-cart-bottom]');
  const toast = $('[data-toast]');
  const autoButton = $('[data-rotate]');
  const zoomButton = $('[data-zoom]');
  const addButton = $('[data-add]');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const price = 189;
  let activeTone = 'arctic';
  let quantity = 1;
  let entries = [];
  let angle = -24;
  let spinning = !reduced.matches;
  let zoomed = false;
  let dragging = false;
  let startX = 0;
  let startAngle = 0;
  let dragPointer = -1;
  let lastTime = 0;
  let resumeTimer = 0;
  let toastTimer = 0;
  let restoreFocus = null;

  // CSS3D cylinder: 24 facets, circular end caps and true front/rear markings.
  const facets = $('[data-facets]');
  for (let i=0; i<24; i++) {
    const span = document.createElement('span');
    span.className = 'cm-facet';
    span.style.setProperty('--i', i);
    // Lighting varies around the circumference, so facets read as a cylinder.
    const frontFacing = Math.cos(i * Math.PI / 12);
    span.style.filter = `brightness(${(.58 + .40 * Math.max(0, frontFacing)).toFixed(2)})`;
    span.setAttribute('aria-hidden', 'true');
    facets.appendChild(span);
  }

  function setAngle(deg) {
    angle = ((deg % 360) + 360) % 360;
    rotor.style.setProperty('--angle', `${angle.toFixed(2)}deg`);
  }
  function animate(now) {
    const delta = lastTime ? Math.min(40, now - lastTime) : 0;
    lastTime = now;
    if (spinning && !dragging && !document.hidden && !reduced.matches) setAngle(angle + delta * .011);
    requestAnimationFrame(animate);
  }
  if (!reduced.matches) requestAnimationFrame(animate);

  function updateAutoButton() {
    autoButton.setAttribute('aria-pressed', String(spinning));
    autoButton.innerHTML = `${spinning ? '❚❚' : '↻'} <span>${spinning ? copy.pause : copy.rotate}</span>`;
  }
  function updateZoomButton() {
    zoomButton.setAttribute('aria-pressed', String(zoomed));
    zoomButton.innerHTML = `${zoomed ? '−' : '＋'} <span>${zoomed ? copy.resetZoom : copy.zoom}</span>`;
    stage.classList.toggle('is-zoomed', zoomed);
  }
  autoButton.addEventListener('click', () => {
    clearTimeout(resumeTimer);
    spinning = !spinning;
    updateAutoButton();
  });
  zoomButton.addEventListener('click', () => {zoomed = !zoomed;updateZoomButton();});
  updateAutoButton();

  turntable.addEventListener('pointerdown', event => {
    if (event.button !== 0 && event.pointerType === 'mouse') return;
    dragging = true;
    dragPointer = event.pointerId;
    startX = event.clientX;
    startAngle = angle;
    stage.classList.add('is-dragging');
    clearTimeout(resumeTimer);
    turntable.setPointerCapture(event.pointerId);
  });
  turntable.addEventListener('pointermove', event => {
    if (!dragging || event.pointerId !== dragPointer) return;
    setAngle(startAngle + (event.clientX - startX) * .85);
  });
  const endDrag = event => {
    if (!dragging || event.pointerId !== dragPointer) return;
    dragging = false;
    dragPointer = -1;
    stage.classList.remove('is-dragging');
    if (turntable.hasPointerCapture(event.pointerId)) turntable.releasePointerCapture(event.pointerId);
  };
  turntable.addEventListener('pointerup', endDrag);
  turntable.addEventListener('pointercancel', endDrag);
  turntable.addEventListener('lostpointercapture', () => {dragging=false;stage.classList.remove('is-dragging');});
  turntable.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();setAngle(angle + (event.key === 'ArrowLeft' ? -15 : 15));
    }
  });

  function setTone(tone) {
    activeTone = tone;
    stage.dataset.tone = tone;
    $$('[data-tone].cm-swatch').forEach((swatch,index) => {
      const active = swatch.dataset.tone === tone;
      swatch.classList.toggle('is-active', active);
      swatch.setAttribute('aria-pressed', String(active));
      if (active) $('[data-selected-color]').textContent = copy.colors[index];
    });
    turntable.setAttribute('aria-label', `HALO ONE — ${copy.colors[tones.indexOf(tone)]}`);
  }
  $$('.cm-swatch').forEach(button => button.addEventListener('click', () => setTone(button.dataset.tone)));
  $('[data-qty-minus]').addEventListener('click', () => {quantity=Math.max(1,quantity-1);$('[data-qty]').textContent=quantity;});
  $('[data-qty-plus]').addEventListener('click', () => {quantity=Math.min(9,quantity+1);$('[data-qty]').textContent=quantity;});
  const cash = n => `$${n.toFixed(2)}`;
  const escapeHTML = v => String(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
  function cartCount() {return entries.reduce((sum,item) => sum + item.qty,0);}
  function updateCart() {
    const count = cartCount();
    $$('[data-cart-count]').forEach(node => node.textContent = count);
    if (!count) {
      cartContent.innerHTML = `<div class="cm-empty"><strong>${escapeHTML(copy.empty)}</strong><p>${escapeHTML(copy.emptyDesc)}</p></div>`;
      cartBottom.hidden = true;
      return;
    }
    cartBottom.hidden = false;
    cartContent.innerHTML = entries.map(item => {
      const name = copy.colors[tones.indexOf(item.tone)];
      return `<article class="cm-cart-line"><div class="cm-cart-thumb" data-tone="${item.tone}" aria-hidden="true"><span></span></div><div class="cm-cart-info"><strong>HALO ONE</strong><small>${escapeHTML(name)} · ${cash(price*item.qty)}</small><div class="cm-cart-tools"><button type="button" data-adjust="-1" data-key="${item.tone}" aria-label="${escapeHTML(copy.minus)}">−</button><span>${item.qty}</span><button type="button" data-adjust="1" data-key="${item.tone}" aria-label="${escapeHTML(copy.plus)}">+</button><button type="button" data-remove="${item.tone}">${escapeHTML(copy.remove)}</button></div></div></article>`;
    }).join('');
    $('[data-cart-total]').textContent = cash(count*price);
  }

  function showToast(message) {
    toast.textContent = message;
    toast.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 2600);
  }
  function animateToCart() {
    if (reduced.matches) return;
    const start = addButton.getBoundingClientRect();
    const end = cartButton.getBoundingClientRect();
    const fly = document.createElement('span');
    fly.className = 'cm-fly';fly.textContent='+';
    fly.style.left=`${start.left+start.width/2-15}px`;
    fly.style.top=`${start.top+start.height/2-15}px`;
    document.body.appendChild(fly);
    if (!fly.animate) {fly.remove();return;}
    const dx = end.left+end.width/2-(start.left+start.width/2);
    const dy = end.top+end.height/2-(start.top+start.height/2);
    const animation = fly.animate([
      {transform:'translate(0,0) scale(1)',opacity:1,offset:0},
      {transform:`translate(${dx*.38}px,${Math.min(-130,dy*.5)}px) scale(1.4)`,opacity:1,offset:.45},
      {transform:`translate(${dx}px,${dy}px) scale(.18)`,opacity:.3,offset:1}
    ],{duration:760,easing:'cubic-bezier(.2,.65,.2,1)'});
    animation.onfinish = () => fly.remove();
    animation.oncancel = () => fly.remove();
  }
  addButton.addEventListener('click', () => {
    let item = entries.find(entry => entry.tone === activeTone);
    if (item) item.qty += quantity;
    else entries.push({tone:activeTone,qty:quantity});
    updateCart();
    animateToCart();
    showToast(copy.toast);
    addButton.classList.add('is-added');
    $('[data-add-label]').textContent=copy.added;
    setTimeout(() => {addButton.classList.remove('is-added');$('[data-add-label]').textContent=copy.add;},1200);
  });

  function openCart() {
    restoreFocus = document.activeElement;
    updateCart();
    backdrop.hidden=false;panel.hidden=false;
    document.body.style.overflow='hidden';
    panel.focus();
  }
  function closeCart() {
    backdrop.hidden=true;panel.hidden=true;
    document.body.style.overflow='';
    restoreFocus?.focus({preventScroll:true});
  }
  cartButton.addEventListener('click',openCart);
  $('[data-close-cart]').addEventListener('click',closeCart);
  backdrop.addEventListener('click',closeCart);
  panel.addEventListener('click', event => {
    const remove = event.target.closest('[data-remove]');
    const adjust = event.target.closest('[data-adjust]');
    if (remove) entries=entries.filter(item=>item.tone!==remove.dataset.remove);
    if (adjust) {
      const item=entries.find(entry=>entry.tone===adjust.dataset.key);
      if (item) item.qty=Math.max(0,item.qty+Number(adjust.dataset.adjust));
      entries=entries.filter(item=>item.qty>0);
    }
    if (remove || adjust) updateCart();
  });
  $('[data-checkout]').addEventListener('click', () => {
    entries=[];updateCart();
    cartContent.innerHTML=`<div class="cm-cart-success"><div class="cm-success-mark">✓</div><h3>${escapeHTML(copy.success)}</h3><p>${escapeHTML(copy.successBody)}</p><button type="button" data-finish>${escapeHTML(copy.goBack)}</button></div>`;
    cartContent.querySelector('[data-finish]').addEventListener('click', closeCart);
    cartContent.querySelector('[data-finish]').focus();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !panel.hidden) closeCart();
    if (event.key !== 'Tab' || panel.hidden) return;
    const focusable=$$('button, a, [tabindex]:not([tabindex="-1"])').filter(el => panel.contains(el) && !el.disabled && el.getClientRects().length);
    if (!focusable.length) {event.preventDefault();panel.focus();return;}
    const first=focusable[0],last=focusable[focusable.length-1];
    if (event.shiftKey && (document.activeElement===first || document.activeElement===panel)) {event.preventDefault();last.focus();}
    else if (!event.shiftKey && document.activeElement===last) {event.preventDefault();first.focus();}
  });
  updateCart();
})();
