import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const languages = ['ru', 'en', 'ka'];
const copy = {
  ru: {
    title:'BEQSON Commerce Motion — интерактивная 3D-витрина',
    description:'Интерактивное E-Commerce демо BEQSON: вращение 3D-товара, смена цвета, увеличение, анимация корзины и адаптивный интерфейс. Без настоящих платежей.',
    skip:'К содержанию', back:'← Наши проекты', service:'Создание интернет-магазина',
    eyebrow:'BEQSON / COMMERCE MOTION', heading:'Товар, который', accent:'хочется рассмотреть.',
    intro:'Попробуйте современную витрину: вращайте товар, выбирайте цвет, приближайте детали и добавляйте его в корзину. Каждый жест продуман.',
    action:'Испытать витрину', concept:'Демонстрационный концепт BEQSON · HALO ONE — вымышленный товар. Реальных продаж и оплат нет.',
    tags:['3D-взаимодействие','Варианты цвета','Живая корзина'],
    sectionTag:'01 / ИНТЕРАКТИВНЫЙ ТОВАР', sceneLabel:'HALO ONE / 360° EXPERIENCE', stageHelp:'Проведите мышью или пальцем, чтобы повернуть',
    rotate:'Автовращение', pause:'Остановить вращение', zoom:'Приблизить', resetZoom:'Уменьшить',
    badge:'CONCEPT PRODUCT · 360°', productType:'Портативная акустика', productName:'HALO ONE',
    productDesc:'Дизайнерская Bluetooth-колонка для демонстрации интерактивной карточки товара. Внимание к форме, цвету и деталям интерфейса.',
    colorTitle:'Выберите отделку', colors:['Ледяной синий','Графит','Тёплый песок'],
    label:'Демо-цена', quantity:'Количество', add:'Добавить в корзину', added:'Добавлено в корзину',
    note:'Это интерактивный макет магазина, не реальный товар. Оформление не создаёт заказ.',
    cart:'Корзина', close:'Закрыть корзину', empty:'В корзине пока пусто', emptyDesc:'Выберите отделку и добавьте HALO ONE.',
    total:'Итого', remove:'Убрать', checkout:'Продолжить оформление (демо)',
    success:'Демонстрация оформления завершена', successBody:'Отлично! Так может выглядеть последний шаг покупки. Платёж не списан, заказ никому не отправлен.',
    goBack:'Продолжить просмотр', plus:'Увеличить количество', minus:'Уменьшить количество',
    toast:'Товар добавлен', footerTag:'02 / ЗА КУЛИСАМИ', footerTitle:'Витрина, которая вовлекает.',
    footerDesc:'Этот независимый концепт показывает возможности анимации товаров, выбора вариантов и сценариев корзины для E-Commerce. Реальный магазин можно соединить с Shopify или WooCommerce.',
    footerCta:'Обсудить интернет-магазин', portfolio:'Остальные проекты',
    facts:['Управление мышью и пальцем','Три визуальных варианта','Анимация корзины','Адаптация для мобильных'],
    footerNote:'BEQSON Commerce Motion · Самостоятельный демонстрационный проект'
  },
  en: {
    title:'BEQSON Commerce Motion — Interactive 3D Storefront',
    description:'An interactive BEQSON E-Commerce demo: rotate a 3D product, switch colors, zoom in, add to a motion-enhanced cart. Responsive concept, no real payments.',
    skip:'Skip to content', back:'← All projects', service:'Online store development',
    eyebrow:'BEQSON / COMMERCE MOTION', heading:'A product worth', accent:'a closer look.',
    intro:'Explore a modern storefront: spin the product, choose a finish, zoom in and add it to your cart. Every interaction has a purpose.',
    action:'Try the storefront', concept:'A BEQSON demonstration concept · HALO ONE is a fictional product. No real orders or payments.',
    tags:['3D interaction','Color variants','Live demo cart'],
    sectionTag:'01 / INTERACTIVE PRODUCT', sceneLabel:'HALO ONE / 360° EXPERIENCE', stageHelp:'Drag with your mouse or finger to rotate',
    rotate:'Auto rotation', pause:'Pause rotation', zoom:'Zoom in', resetZoom:'Zoom out',
    badge:'CONCEPT PRODUCT · 360°', productType:'Portable audio', productName:'HALO ONE',
    productDesc:'A design-led Bluetooth speaker created to demonstrate a modern product page. Explore material, color and thoughtful motion details.',
    colorTitle:'Select finish', colors:['Arctic blue','Graphite','Warm sand'],
    label:'Demo price', quantity:'Quantity', add:'Add to cart', added:'Added to cart',
    note:'This is an interactive store concept, not a real product. Checkout does not place an order.',
    cart:'Shopping cart', close:'Close cart', empty:'Your cart is empty', emptyDesc:'Choose a finish and add your HALO ONE.',
    total:'Subtotal', remove:'Remove', checkout:'Continue to checkout (demo)',
    success:'Demo checkout complete', successBody:'Nice! This is how a purchase completion could feel. No payment was taken and no order was sent.',
    goBack:'Continue exploring', plus:'Increase quantity', minus:'Decrease quantity',
    toast:'Added to cart', footerTag:'02 / BEHIND THE SCENES', footerTitle:'Commerce designed to engage.',
    footerDesc:'This independent concept demonstrates interactive product views, variants and cart microinteractions. A production store can be integrated with Shopify or WooCommerce.',
    footerCta:'Discuss an online store', portfolio:'More projects',
    facts:['Mouse & touch controls','Three visual finishes','Animated demo cart','Responsive layout'],
    footerNote:'BEQSON Commerce Motion · Independent demonstration concept'
  },
  ka: {
    title:'BEQSON Commerce Motion — ინტერაქტიული 3D ვიტრინა',
    description:'BEQSON-ის E-Commerce დემო: 3D პროდუქტის დატრიალება, ფერის შეცვლა, გადიდება და ანიმაციური კალათა. ადაპტიური კონცეფცია რეალური გადახდების გარეშე.',
    skip:'შინაარსზე გადასვლა', back:'← ყველა პროექტი', service:'ონლაინმაღაზიის შექმნა',
    eyebrow:'BEQSON / COMMERCE MOTION', heading:'პროდუქტი, რომლის', accent:'დათვალიერებაც გსურთ.',
    intro:'გამოსცადეთ თანამედროვე ონლაინვიტრინა: დაატრიალეთ პროდუქტი, აირჩიეთ ფერი, გაადიდეთ დეტალები და დაამატეთ კალათაში.',
    action:'ვიტრინის გამოცდა', concept:'BEQSON-ის სადემონსტრაციო კონცეფცია · HALO ONE გამოგონილი პროდუქტია. რეალური შეკვეთები და გადახდები არ სრულდება.',
    tags:['3D ინტერაქცია','ფერის ვარიანტები','ინტერაქტიული კალათა'],
    sectionTag:'01 / ინტერაქტიული პროდუქტი', sceneLabel:'HALO ONE / 360° EXPERIENCE', stageHelp:'დაატრიალეთ მაუსით ან თითით',
    rotate:'ავტობრუნვა', pause:'ბრუნვის შეჩერება', zoom:'გადიდება', resetZoom:'შემცირება',
    badge:'კონცეპტუალური პროდუქტი · 360°', productType:'პორტატული აუდიო', productName:'HALO ONE',
    productDesc:'დიზაინერული Bluetooth დინამიკი, შექმნილი თანამედროვე პროდუქტის გვერდის დემონსტრაციისთვის. გაეცანით ფორმას, ფერსა და ანიმაციას.',
    colorTitle:'აირჩიეთ ფერი', colors:['ყინულისფერი ლურჯი','გრაფიტი','თბილი ქვიშა'],
    label:'დემო ფასი', quantity:'რაოდენობა', add:'კალათაში დამატება', added:'დამატებულია კალათაში',
    note:'ეს არის მაღაზიის ინტერაქტიული მაკეტი და არა რეალური პროდუქტი. გადახდა და შეკვეთა არ სრულდება.',
    cart:'კალათა', close:'კალათის დახურვა', empty:'კალათა ცარიელია', emptyDesc:'აირჩიეთ ფერი და დაამატეთ HALO ONE.',
    total:'ჯამი', remove:'წაშლა', checkout:'გაფორმების გაგრძელება (დემო)',
    success:'დემო შეკვეთა დასრულებულია', successBody:'ასე შეიძლება გამოიყურებოდეს შეძენის ბოლო ნაბიჯი. თანხა არ ჩამოგეჭრათ და შეკვეთა არ გაგზავნილა.',
    goBack:'დათვალიერების გაგრძელება', plus:'რაოდენობის გაზრდა', minus:'რაოდენობის შემცირება',
    toast:'კალათაში დაემატა', footerTag:'02 / შესაძლებლობები', footerTitle:'ვიტრინა, რომელიც იზიდავს.',
    footerDesc:'დამოუკიდებელი კონცეფცია აჩვენებს 3D პროდუქტს, ფერების არჩევასა და კალათის ანიმაციას. რეალური მაღაზიის შექმნა შესაძლებელია Shopify-ს ან WooCommerce-ის გამოყენებით.',
    footerCta:'ონლაინმაღაზიის განხილვა', portfolio:'სხვა პროექტები',
    facts:['მაუსით და თითით მართვა','სამი ფერის ვარიანტი','ანიმაციური კალათა','მობილურზე მორგება'],
    footerNote:'BEQSON Commerce Motion · დამოუკიდებელი სადემონსტრაციო კონცეფცია'
  }
};

const esc = x => String(x).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function render(lang, t) {
  const alternates=languages.map(code=>`<link rel="alternate" hreflang="${code}" href="https://beqson.com/${code}/commerce-motion/">`).join('');
  const nav=languages.map(code=>`<a href="/${code}/commerce-motion/" lang="${code}" hreflang="${code}" ${code===lang?'aria-current="page"':''}>${code==='ka'?'GE':code.toUpperCase()}</a>`).join('');
  const choices=t.colors.map((name,index)=>`<button type="button" class="cm-swatch${index===0?' is-active':''}" data-tone="${['arctic','graphite','sand'][index]}" aria-label="${esc(name)}" aria-pressed="${index===0?'true':'false'}"><span></span><small>${esc(name)}</small></button>`).join('');
  return `<!doctype html>
<html lang="${lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#061326">
<title>${esc(t.title)}</title><meta name="description" content="${esc(t.description)}">
<link rel="canonical" href="https://beqson.com/${lang}/commerce-motion/">${alternates}
<meta property="og:type" content="website"><meta property="og:title" content="${esc(t.title)}"><meta property="og:description" content="${esc(t.description)}"><meta property="og:url" content="https://beqson.com/${lang}/commerce-motion/"><meta property="og:image" content="https://beqson.com/assets/project-covers/beqson-commerce-motion.svg">
<link rel="icon" href="/assets/favicon-v3.png"><link rel="stylesheet" href="/assets/commerce-motion.css?v=2"><script src="/assets/commerce-motion.js?v=2" defer></script>
</head><body class="cm-page" data-lang="${lang}">
<a class="cm-skip" href="#main">${esc(t.skip)}</a>
<header class="cm-header"><div class="cm-shell cm-topline"><a class="cm-logo" href="/${lang}/">BEQSON<span>.</span><small>DIGITAL STUDIO</small></a><nav class="cm-nav" aria-label="Navigation"><a class="cm-back" href="/${lang}/projects/">${esc(t.back)}</a><div class="cm-langs">${nav}</div><button class="cm-cart-btn" type="button" data-open-cart aria-label="${esc(t.cart)}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M2 4h3l2.2 11.5h11.5l2.3-8H6"/><circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/></svg><span data-cart-count>0</span></button></nav></div></header>
<main id="main"><section class="cm-hero"><div class="cm-shell cm-hero-grid"><div class="cm-hero-content"><p class="cm-eyebrow">${esc(t.eyebrow)}</p><h1>${esc(t.heading)}<br><em>${esc(t.accent)}</em></h1><p class="cm-intro">${esc(t.intro)}</p><div class="cm-hero-links"><a class="cm-btn cm-btn-primary" href="#demo">${esc(t.action)} <span aria-hidden="true">↘</span></a><a class="cm-inline-link" href="/${lang}/shopify/">${esc(t.service)} ↗</a></div><p class="cm-concept">ⓘ ${esc(t.concept)}</p></div><div class="cm-hero-art" aria-hidden="true"><div class="cm-hero-orbit"></div><span class="cm-hero-word">COMMERCE<br><b>IN MOTION</b></span><div class="cm-hero-shape"><i></i><b>HALO</b></div><span class="cm-hero-chip">DRAG · ROTATE · EXPLORE</span></div></div><div class="cm-shell cm-tags">${t.tags.map(x=>`<span>✦ ${esc(x)}</span>`).join('')}</div></section>
<section class="cm-demo-section" id="demo"><div class="cm-shell"><p class="cm-eyebrow">${esc(t.sectionTag)}</p><div class="cm-product-layout">
<div class="cm-stage" data-stage data-tone="arctic"><div class="cm-stage-top"><span><i class="cm-live-dot"></i>${esc(t.sceneLabel)}</span><span class="cm-rotate-mark">↻ 360°</span></div><div class="cm-stage-aura" aria-hidden="true"></div><div class="cm-stage-rings" aria-hidden="true"></div>
<div class="cm-turntable" data-turntable role="img" tabindex="0" aria-label="${esc(t.productName)} — ${esc(t.stageHelp)}">
<div class="cm-rotor" data-rotor><div class="cm-facets" data-facets></div><div class="cm-top-cap"></div><div class="cm-base-cap"></div><div class="cm-front-mark"><span class="cm-brand-stamp">H<br><small>HALO</small></span><span class="cm-light-indicator"></span></div><div class="cm-back-mark">HALO / 01</div></div>
</div><div class="cm-podium" aria-hidden="true"><div class="cm-podium-ring"></div></div><div class="cm-stage-bottom"><span>${esc(t.stageHelp)}</span><div class="cm-stage-controls"><button type="button" class="cm-icon-btn" data-rotate aria-pressed="true">❚❚ <span>${esc(t.pause)}</span></button><button type="button" class="cm-icon-btn" data-zoom aria-pressed="false">＋ <span>${esc(t.zoom)}</span></button></div></div></div>
<aside class="cm-product-details"><p class="cm-badge">${esc(t.badge)}</p><p class="cm-type">${esc(t.productType)}</p><h2>${esc(t.productName)}<span>®</span></h2><p class="cm-detail-copy">${esc(t.productDesc)}</p><div class="cm-divider"></div><div class="cm-choice-title"><strong>${esc(t.colorTitle)}</strong><span data-selected-color>${esc(t.colors[0])}</span></div><div class="cm-swatches" role="group" aria-label="${esc(t.colorTitle)}">${choices}</div><div class="cm-divider"></div><div class="cm-purchase"><div><small>${esc(t.label)}</small><strong>$189<span>.00</span></strong></div><div class="cm-qty"><label for="cm-qty">${esc(t.quantity)}</label><div><button type="button" data-qty-minus aria-label="${esc(t.minus)}">−</button><output id="cm-qty" data-qty>1</output><button type="button" data-qty-plus aria-label="${esc(t.plus)}">+</button></div></div></div><button class="cm-add" type="button" data-add><span class="cm-add-symbol">+</span><span data-add-label>${esc(t.add)}</span><span aria-hidden="true">↗</span></button><p class="cm-purchase-note">${esc(t.note)}</p></aside>
</div></div></section>
<section class="cm-after"><div class="cm-shell"><div><p class="cm-eyebrow">${esc(t.footerTag)}</p><h2>${esc(t.footerTitle)}</h2><p>${esc(t.footerDesc)}</p><div class="cm-features">${t.facts.map(x=>`<span>✓ ${esc(x)}</span>`).join('')}</div><div class="cm-footer-links"><a class="cm-btn cm-btn-primary" href="/${lang}/shopify/">${esc(t.footerCta)} ↗</a><a class="cm-inline-link" href="/${lang}/projects/">${esc(t.portfolio)} ↗</a></div></div><div class="cm-after-visual" aria-hidden="true"><div class="cm-after-orbit"></div><b>360°</b><small>COMMERCE EXPERIENCE</small></div></div></section></main>
<footer class="cm-footer"><div class="cm-shell"><a href="/${lang}/">BEQSON DIGITAL STUDIO</a><span>${esc(t.footerNote)}</span></div></footer>
<div class="cm-cart-backdrop" data-backdrop hidden></div><aside class="cm-cart-panel" data-cart-panel role="dialog" aria-modal="true" aria-labelledby="cm-cart-title" tabindex="-1" hidden><div class="cm-cart-head"><h2 id="cm-cart-title">${esc(t.cart)} <span data-cart-count>0</span></h2><button type="button" data-close-cart aria-label="${esc(t.close)}">×</button></div><div class="cm-cart-content" data-cart-content></div><div class="cm-cart-bottom" data-cart-bottom hidden><div><span>${esc(t.total)}</span><strong data-cart-total>$0.00</strong></div><button class="cm-checkout" type="button" data-checkout>${esc(t.checkout)} →</button><small>${esc(t.note)}</small></div></aside>
<div class="cm-toast" role="status" aria-live="polite" data-toast></div>
<script type="application/json" id="cm-copy">${JSON.stringify({colors:t.colors,cart:t.cart,close:t.close,empty:t.empty,emptyDesc:t.emptyDesc,remove:t.remove,plus:t.plus,minus:t.minus,success:t.success,successBody:t.successBody,goBack:t.goBack,toast:t.toast,rotate:t.rotate,pause:t.pause,zoom:t.zoom,resetZoom:t.resetZoom,added:t.added,add:t.add}).replaceAll('<','\\u003c')}</script>
</body></html>`;
}

for (const lang of languages) {
  const file=path.join(root,lang,'commerce-motion','index.html');
  fs.mkdirSync(path.dirname(file),{recursive:true});
  fs.writeFileSync(file,render(lang,copy[lang]));
  process.stdout.write(`Generated ${file}\n`);
}
