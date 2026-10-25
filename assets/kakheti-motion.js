/* BEQSON wine concept: illustrative 3D bottles and a client-only demo cart. */
(() => {
  'use strict';

  const lang = document.documentElement.lang === 'ka' ? 'ka' : document.documentElement.lang === 'en' ? 'en' : 'ru';
  const words = {
    ru: { catalogHint:'НОВОЕ · Откройте любое вино — вращайте 3D-бутылку, увеличивайте её и попробуйте интерактивную корзину.', cart:'Корзина', threeD:'3D-бутылка', photo:'Оригинальное фото', pause:'Остановить', play:'Вращать', zoom:'Приблизить', unzoom:'Отдалить', hint:'Потяните мышью или пальцем, чтобы повернуть', note:'3D-модель — художественная визуализация. Точный вид этикетки показан на фото.', quantity:'Количество', add:'Добавить в демо-корзину', added:'Добавлено в корзину', empty:'Ваша демо-корзина пока пуста', total:'Итого', remove:'Удалить', checkout:'Завершить демо-заказ', complete:'Демо-заказ завершён', completeText:'Это демонстрация: заказ никуда не отправлен, оплата не производится.', keep:'Продолжить просмотр', disclaimer:'Демонстрационный проект BEQSON. Реальные заказы не принимаются.', close:'Закрыть корзину', minus:'Уменьшить количество', plus:'Увеличить количество', spin:'Интерактивное вращение бутылки' },
    en: { catalogHint:'NEW · Explore any wine to rotate and zoom its 3D bottle, then try the interactive demo cart.', cart:'Cart', threeD:'3D bottle', photo:'Actual product photo', pause:'Pause', play:'Rotate', zoom:'Zoom in', unzoom:'Zoom out', hint:'Drag with your mouse or finger to rotate', note:'The 3D bottle is an artistic visualization. See the photo for the actual label.', quantity:'Quantity', add:'Add to demo cart', added:'Added to cart', empty:'Your demo cart is empty', total:'Total', remove:'Remove', checkout:'Complete demo checkout', complete:'Demo checkout complete', completeText:'This is a demo. No order is placed and no payment is made.', keep:'Keep browsing', disclaimer:'A BEQSON concept. No real orders are accepted.', close:'Close cart', minus:'Decrease quantity', plus:'Increase quantity', spin:'Interactive bottle rotation' },
    ka: { catalogHint:'სიახლე · გახსენით ნებისმიერი ღვინო, დაატრიალეთ და გაადიდეთ 3D ბოთლი, სცადეთ დემო კალათაც.', cart:'კალათა', threeD:'3D ბოთლი', photo:'ნამდვილი ფოტო', pause:'შეჩერება', play:'ბრუნვა', zoom:'გადიდება', unzoom:'დაპატარავება', hint:'გადაატრიალეთ მაუსით ან თითით', note:'3D ბოთლი მხატვრული ვიზუალიზაციაა. ეტიკეტის ზუსტი სახე იხილეთ ფოტოზე.', quantity:'რაოდენობა', add:'დემო კალათაში დამატება', added:'დამატებულია', empty:'დემო კალათა ცარიელია', total:'ჯამი', remove:'წაშლა', checkout:'დემო შეკვეთის დასრულება', complete:'დემო შეკვეთა დასრულდა', completeText:'ეს დემოა — შეკვეთა არ იგზავნება და თანხა არ იჭრება.', keep:'დათვალიერების გაგრძელება', disclaimer:'BEQSON-ის დემო პროექტი. რეალური შეკვეთები არ მიიღება.', close:'კალათის დახურვა', minus:'რაოდენობის შემცირება', plus:'რაოდენობის გაზრდა', spin:'ბოთლის ინტერაქტიული ბრუნვა' },
  }[lang];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const money = amount => `${amount.toFixed(2)} GEL`;
  const escapeHTML = value => String(value).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
  const bottleStates = new Map();
  const catalog = new Map();
  const items = new Map();
  let lastTime = 0;
  let activePointer = null;
  let restoreFocus = null;

  const catalogHint = document.createElement('p');
  catalogHint.className = 'kwh-catalog-hint';
  catalogHint.textContent = words.catalogHint;
  document.querySelector('#cellar .filters')?.insertAdjacentElement('beforebegin', catalogHint);

  const header = document.querySelector('.head-inner');
  const cartButton = document.createElement('button');
  cartButton.className = 'kwh-cart-toggle';
  cartButton.type = 'button';
  cartButton.setAttribute('aria-label', words.cart);
  cartButton.innerHTML = `<svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 4h2l2.3 10.5h11.5l2-8H6"/><circle cx="9" cy="20" r="1.3"/><circle cx="18" cy="20" r="1.3"/></svg><span>${escapeHTML(words.cart)}</span><b data-wine-count>0</b>`;
  header.appendChild(cartButton);

  const drawer = document.createElement('div');
  drawer.className = 'kwh-cart-overlay';
  drawer.hidden = true;
  drawer.innerHTML = `<div class="kwh-cart-shade" data-cart-close></div><aside class="kwh-cart-drawer" role="dialog" aria-modal="true" aria-label="${escapeHTML(words.cart)}" tabindex="-1"><div class="kwh-cart-heading"><h2>${escapeHTML(words.cart)} <span data-wine-drawer-count>0</span></h2><button type="button" data-cart-close aria-label="${escapeHTML(words.close)}">×</button></div><div class="kwh-cart-list" data-wine-lines></div><div class="kwh-cart-footer" data-wine-cart-footer><div class="kwh-cart-sum"><span>${escapeHTML(words.total)}</span><strong data-wine-total>0.00 GEL</strong></div><button class="kwh-checkout" type="button" data-wine-checkout>${escapeHTML(words.checkout)}</button><small>${escapeHTML(words.disclaimer)}</small></div></aside>`;
  document.body.appendChild(drawer);
  const drawerPanel = drawer.querySelector('.kwh-cart-drawer');
  const cartLines = drawer.querySelector('[data-wine-lines]');
  const footer = drawer.querySelector('[data-wine-cart-footer]');

  const toast = document.createElement('div');
  toast.className = 'kwh-cart-toast';
  toast.setAttribute('role','status');
  document.body.appendChild(toast);
  let toastTimeout;
  const showToast = message => {
    toast.textContent = message;
    toast.classList.add('is-active');
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => toast.classList.remove('is-active'), 2200);
  };

  function setAngle(state, next) {
    state.angle = ((next % 360) + 360) % 360;
    state.rotor.style.transform = `rotateX(-7deg) rotateY(${state.angle.toFixed(2)}deg)`;
  }
  function updateSpin(state) {
    state.spinButton.setAttribute('aria-pressed', String(state.spinning));
    state.spinButton.textContent = state.spinning ? `❚❚ ${words.pause}` : `↻ ${words.play}`;
  }
  function updateZoom(state) {
    state.stage.classList.toggle('is-zoomed', state.zoomed);
    state.zoomButton.textContent = `${state.zoomed ? '−' : '+'} ${state.zoomed ? words.unzoom : words.zoom}`;
    state.zoomButton.setAttribute('aria-pressed', String(state.zoomed));
  }

  document.querySelectorAll('.wine-dialog').forEach(dialog => {
    const id = dialog.id.slice(5);
    const title = dialog.querySelector('.dialog-content h2')?.textContent?.trim() || 'Kakheti Wine House';
    const price = Number(dialog.querySelector('.dialog-price')?.textContent?.replace(/[^\d.]/g, '')) || 0;
    const img = dialog.querySelector('.dialog-visual img');
    const opener = document.querySelector(`[data-open-wine="${id}"]`);
    const kind = opener?.closest('.wine-card')?.dataset.cats.includes('red') ? 'red' : 'amber';
    const year = title.match(/20\d{2}/)?.[0] || '2023';
    const labelName = title.replace(/\s*20\d{2}\s*/, '').trim();
    catalog.set(id, {id,title,price,kind,image:img.src});

    const visual = dialog.querySelector('.dialog-visual');
    visual.classList.add('kwh-visual-enhanced');
    visual.dataset.kind = kind;
    const view = document.createElement('div');
    view.className = 'kwh-motion-view';
    view.innerHTML = `<div class="kwh-view-tabs" role="group" aria-label="Product view"><button type="button" class="is-active" data-wine-mode="3d" aria-pressed="true">↻ ${escapeHTML(words.threeD)}</button><button type="button" data-wine-mode="photo" aria-pressed="false">▧ ${escapeHTML(words.photo)}</button></div><div class="kwh-model-stage" data-wine-stage><div class="kwh-model-ring" aria-hidden="true"></div><div class="kwh-model-drag" data-wine-drag role="img" tabindex="0" aria-label="${escapeHTML(words.spin)}"><div class="kwh-bottle-rotor" data-wine-rotor><div class="kwh-bottle-body" data-wine-body></div><div class="kwh-bottle-neck" data-wine-neck></div><div class="kwh-bottle-shoulder" aria-hidden="true"></div><div class="kwh-bottle-cork" aria-hidden="true"></div><div class="kwh-label-front"><span class="kwh-label-brand">KAKHETI<br>WINE HOUSE</span><i></i><strong>${escapeHTML(labelName)}</strong><small>${escapeHTML(year)} · 750 ML</small></div><div class="kwh-label-back">KWH<br><small>KAKHETI · GEORGIA</small></div></div></div><p class="kwh-model-hint">${escapeHTML(words.hint)}</p><div class="kwh-model-actions"><button type="button" data-wine-spin aria-pressed="false"></button><button type="button" data-wine-zoom aria-pressed="false"></button></div></div><p class="kwh-render-disclose">${escapeHTML(words.note)}</p>`;
    visual.insertBefore(view, img);
    const body = view.querySelector('[data-wine-body]');
    const neck = view.querySelector('[data-wine-neck]');
    for(let i=0;i<24;i++) {
      const facet=document.createElement('span');
      facet.className='kwh-bottle-facet';
      facet.style.setProperty('--step', i);
      facet.style.setProperty('--shade', `${Math.round(65+33*Math.max(0,Math.cos(i*Math.PI/12)))}%`);
      body.appendChild(facet);
    }
    for(let i=0;i<16;i++) {
      const facet=document.createElement('span');
      facet.className='kwh-neck-facet';
      facet.style.setProperty('--step', i);
      neck.appendChild(facet);
    }
    const state={dialog,stage:view.querySelector('[data-wine-stage]'),drag:view.querySelector('[data-wine-drag]'),rotor:view.querySelector('[data-wine-rotor]'),spinButton:view.querySelector('[data-wine-spin]'),zoomButton:view.querySelector('[data-wine-zoom]'),angle:-22,spinning:!reduced.matches,zoomed:false,dragging:false,resumeAt:0,mode:'3d',quantity:1};
    bottleStates.set(id,state);
    setAngle(state,-22);updateSpin(state);updateZoom(state);

    view.querySelectorAll('[data-wine-mode]').forEach(button => button.addEventListener('click',()=>{
      state.mode=button.dataset.wineMode;
      visual.classList.toggle('is-photo',state.mode==='photo');
      view.querySelectorAll('[data-wine-mode]').forEach(b=>{
        b.classList.toggle('is-active',b===button);
        b.setAttribute('aria-pressed',String(b===button));
      });
    }));
    state.spinButton.addEventListener('click',()=>{state.spinning=!state.spinning;state.resumeAt=0;updateSpin(state)});
    state.zoomButton.addEventListener('click',()=>{state.zoomed=!state.zoomed;updateZoom(state)});
    state.drag.addEventListener('pointerdown',event=>{
      if(event.pointerType==='mouse'&&event.button!==0)return;
      if(activePointer)return;
      state.dragging=true;
      state.resumeAt=Infinity;
      activePointer={state,id:event.pointerId,x:event.clientX,angle:state.angle};
      state.stage.classList.add('is-dragging');
      try{state.drag.setPointerCapture(event.pointerId)}catch{}
      event.preventDefault();
    });
    state.drag.addEventListener('keydown',event=>{
      if(event.key!=='ArrowLeft'&&event.key!=='ArrowRight')return;
      event.preventDefault();
      setAngle(state,state.angle+(event.key==='ArrowLeft'?-15:15));
      state.resumeAt=performance.now()+1300;
    });

    const buy=document.createElement('div');
    buy.className='kwh-product-buy';
    buy.innerHTML=`<div class="kwh-buy-count"><span>${escapeHTML(words.quantity)}</span><div><button type="button" data-wine-qty="-1" aria-label="${escapeHTML(words.minus)}">−</button><b data-wine-qty-value>1</b><button type="button" data-wine-qty="1" aria-label="${escapeHTML(words.plus)}">+</button></div></div><button class="kwh-product-add" type="button" data-wine-add>${escapeHTML(words.add)} <span aria-hidden="true">↗</span></button>`;
    dialog.querySelector('.dialog-price').insertAdjacentElement('afterend',buy);
    buy.querySelectorAll('[data-wine-qty]').forEach(button=>button.addEventListener('click',()=>{
      state.quantity=Math.min(12,Math.max(1,state.quantity+Number(button.dataset.wineQty)));
      buy.querySelector('[data-wine-qty-value]').textContent=state.quantity;
    }));
    buy.querySelector('[data-wine-add]').addEventListener('click',event=>{
      const next=(items.get(id)||0)+state.quantity;
      items.set(id,next);
      renderCart();
      animateFly(event.currentTarget);
      showToast(words.added);
      // A native modal dialog sits above every ordinary overlay. Close it
      // before showing our demo cart so the drawer remains fully interactive.
      setTimeout(() => { if (dialog.open) dialog.close(); openCart(); }, reduced.matches ? 120 : 720);
    });
  });

  window.addEventListener('pointermove',event=>{
    if(!activePointer||event.pointerId!==activePointer.id)return;
    setAngle(activePointer.state,activePointer.angle+(event.clientX-activePointer.x)*.7);
  });
  function finishDrag(event){
    if(!activePointer||event.pointerId!==activePointer.id)return;
    const {state,id}=activePointer;
    activePointer=null;
    state.dragging=false;
    state.stage.classList.remove('is-dragging');
    state.resumeAt=performance.now()+1350;
    if(state.drag.hasPointerCapture?.(id))state.drag.releasePointerCapture(id);
  }
  window.addEventListener('pointerup',finishDrag);
  window.addEventListener('pointercancel',finishDrag);

  function animate(now){
    const dt=lastTime?Math.min(50,now-lastTime):0;
    lastTime=now;
    const active=document.querySelector('.wine-dialog[open]');
    if(active&&!document.hidden){
      const state=bottleStates.get(active.id.slice(5));
      if(state?.mode==='3d'&&state.spinning&&!state.dragging&&now>=state.resumeAt)setAngle(state,state.angle+dt*.018);
    }
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);

  function count(){return [...items.values()].reduce((sum,qty)=>sum+qty,0)}
  function renderCart(){
    const n=count();
    cartButton.querySelector('[data-wine-count]').textContent=n;
    drawer.querySelector('[data-wine-drawer-count]').textContent=n;
    footer.hidden=n===0;
    if(!n){cartLines.innerHTML=`<div class="kwh-cart-empty">${escapeHTML(words.empty)}</div>`;return}
    let total=0;
    cartLines.innerHTML=[...items].map(([id,qty])=>{
      const wine=catalog.get(id);
      if(!wine)return '';
      total+=qty*wine.price;
      return `<article class="kwh-cart-item"><img src="${escapeHTML(wine.image)}" alt="" width="64" height="78"><div><strong>${escapeHTML(wine.title)}</strong><small>${money(wine.price)} · ${qty}</small><div class="kwh-cart-step"><button data-cart-change="-1" data-wine-id="${id}" aria-label="${escapeHTML(words.minus)}">−</button><span>${qty}</span><button data-cart-change="1" data-wine-id="${id}" aria-label="${escapeHTML(words.plus)}">+</button><button class="kwh-cart-remove" data-cart-remove="${id}">${escapeHTML(words.remove)}</button></div></div></article>`;
    }).join('');
    drawer.querySelector('[data-wine-total]').textContent=money(total);
  }
  function openCart(){
    restoreFocus=document.activeElement;
    renderCart();
    drawer.hidden=false;
    document.body.classList.add('kwh-cart-is-open');
    drawerPanel.focus();
  }
  function closeCart(){
    drawer.hidden=true;
    document.body.classList.remove('kwh-cart-is-open');
    restoreFocus?.focus({preventScroll:true});
  }
  cartButton.addEventListener('click',openCart);
  drawer.addEventListener('click',event=>{
    if(event.target.closest('[data-cart-close]')){closeCart();return}
    const remove=event.target.closest('[data-cart-remove]');
    if(remove){items.delete(remove.dataset.cartRemove);renderCart();return}
    const change=event.target.closest('[data-cart-change]');
    if(change){const id=change.dataset.wineId;const next=(items.get(id)||0)+Number(change.dataset.cartChange);if(next<=0)items.delete(id);else items.set(id,next);renderCart()}
  });
  drawer.querySelector('[data-wine-checkout]').addEventListener('click',()=>{
    items.clear();renderCart();
    cartLines.innerHTML=`<div class="kwh-cart-finished"><strong>✓ ${escapeHTML(words.complete)}</strong><p>${escapeHTML(words.completeText)}</p><button type="button" data-cart-close>${escapeHTML(words.keep)}</button></div>`;
    cartLines.querySelector('button').focus();
  });
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape'&&!drawer.hidden){event.preventDefault();closeCart();return}
    if(event.key!=='Tab'||drawer.hidden)return;
    const els=[...drawerPanel.querySelectorAll('button,a,[tabindex]:not([tabindex="-1"])')].filter(el=>!el.disabled&&el.getClientRects().length);
    const first=els[0],last=els[els.length-1];
    if(event.shiftKey&&(document.activeElement===first||document.activeElement===drawerPanel)){event.preventDefault();last?.focus()}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus()}
  });
  function animateFly(button){
    if(reduced.matches)return;
    const from=button.getBoundingClientRect(),to=cartButton.getBoundingClientRect();
    const dot=document.createElement('span');
    dot.className='kwh-flying-cork';dot.textContent='+';
    dot.style.left=`${from.left+from.width/2}px`;dot.style.top=`${from.top+from.height/2}px`;
    document.body.appendChild(dot);
    if(!dot.animate){dot.remove();return}
    const dx=to.left+to.width/2-from.left-from.width/2,dy=to.top+to.height/2-from.top-from.height/2;
    const motion=dot.animate([{transform:'translate(0,0) scale(1)',opacity:1},{transform:`translate(${dx*.4}px,${Math.min(-80,dy*.5)}px) scale(1.3)`,opacity:1},{transform:`translate(${dx}px,${dy}px) scale(.15)`,opacity:.25}],{duration:720,easing:'cubic-bezier(.2,.7,.2,1)'});
    motion.onfinish=()=>dot.remove();motion.oncancel=()=>dot.remove();
  }
  renderCart();
})();
