import fs from "node:fs";
import path from "node:path";
import {execFileSync} from "node:child_process";

const root = path.resolve(import.meta.dirname, "..");
const langs = ["ru", "en", "ka"];

const translations = {
  ru: {
    title: "BEQSON Motion Lab — интерактивный веб-дизайн и анимация",
    description: "Интерактивный концепт BEQSON: от каркаса сайта до визуального дизайна, интернет-магазина и AI-консультанта. Анимация и веб-интерфейсы на CSS и JavaScript.",
    back: "← Все проекты", home: "Главная", skip: "Перейти к содержанию",
    eyebrow: "BEQSON / INTERACTIVE EXPERIENCE",
    heading: "От идеи до сайта,",
    accent: "который оживает.",
    lead: "Пройдите четыре этапа и посмотрите, как простой набросок превращается в современный сайт, интернет-магазин и интерфейс AI-консультанта.",
    try: "Смотреть анимацию ↓", portfolio: "Все проекты ↗",
    conceptNote: "Самостоятельный интерактивный концепт студии BEQSON. Интерфейсы магазина и чата на этой странице демонстрационные.",
    floatA: "Motion UI", floatB: "Made to interact",
    storyEyebrow: "01 / КАК ЭТО УСТРОЕНО",
    storyTitle: "Одна идея. Четыре превращения.",
    storyLead: "Прокручивайте страницу: макет слева будет меняться вместе с этапами справа. В сценах магазина и AI можно нажимать кнопки.",
    sample: "Интерактивный макет",
    sampleTag: "Без реальных оплат и AI-запросов",
    browser: ["beqson.com/idea", "beqson.com/design", "beqson.com/shop", "beqson.com/assistant"],
    pill: ["Каркас", "Дизайн", "Магазин", "AI"],
    designNav: "СТУДИЯ", designNavRight: "Проекты · Контакты", designHeading: "Идея встречает дизайн.", designText: "Ясная структура и фирменный стиль для вашего бизнеса.", designAction: "Узнать больше",
    shopNav: "NOVA STORE", shopNavRight: "Каталог · О нас",
    shopHeading: "Продажи начинаются здесь", products: ["Форма и стиль", "Тёплые детали", "Вещи для дома"],
    cartLabel: "Товаров в корзине", addCart: "Добавить товар в корзину +",
    aiName: "BEQSON AI Consultant", aiOnline: "Демо диалога · онлайн",
    aiGreeting: "Привет! Что вы хотели бы создать?",
    aiUser: "Нужен красивый интернет-магазин.",
    aiAnswer: "Начнём с каталога, карточек товаров и удобного оформления заказа. Затем подберём подходящие интеграции.",
    aiQ1: "А если нужен сайт услуг?", aiA1: "Для услуг подойдут понятные страницы, форма заявки и быстрые способы связи с вашей командой.",
    aiQ2: "Можно подключить AI?", aiA2: "Да, можно обсудить чат-консультанта, его базу знаний и способы связи с менеджером.",
    steps: [
      {number:"01 / STRUCTURE",title:"Сначала — понятный каркас",body:"Определяем, что важно посетителю. Создаём структуру, расставляем акценты и проектируем удобный путь к действию.",tag:"Структура и UX"},
      {number:"02 / VISUAL",title:"Добавляем характер и движение",body:"Подбираем цвета, типографику, изображения и микроанимации. Макет превращается в интерфейс с узнаваемым стилем.",tag:"Веб-дизайн и Motion UI"},
      {number:"03 / COMMERCE",title:"Превращаем сайт в витрину",body:"Показываем товары, категории, корзину и сценарий заказа. Нажмите кнопку добавления товара внутри демо.",tag:"Интерактивный E-Commerce"},
      {number:"04 / ASSISTANT",title:"Добавляем диалог с AI",body:"Показываем, как консультант мог бы отвечать на вопросы посетителя. Кнопки в макете переключают подготовленные ответы — это не подключённая AI-модель.",tag:"Прототип AI-интерфейса"}
    ],
    capabilityEyebrow:"02 / ЧТО ПОКАЗЫВАЕТ КЕЙС", capabilityTitle:"Красиво — и технически продуманно.",
    capabilities:[
      {icon:"↗",title:"Motion UI",text:"Анимация переходов и появления элементов при прокрутке."},
      {icon:"⌘",title:"JavaScript",text:"Рабочие переключения сцен, кнопки и локальная корзина."},
      {icon:"▣",title:"Responsive Design",text:"Композиция адаптируется к компьютеру, планшету и телефону."},
      {icon:"◉",title:"Accessibility",text:"Клавиатура, читаемые подписи и поддержка уменьшения движения."}
    ],
    finalEyebrow:"03 / ВАШ СЛЕДУЮЩИЙ ПРОЕКТ", finalTitle:"Сделаем что-то запоминающееся для вашего бизнеса?",
    finalLead:"Этот Motion Lab — собственный демонстрационный проект BEQSON. Можем обсудить похожий подход для сайта, магазина или AI-консультанта.",
    finalContact:"Обсудить проект ↗", finalShop:"Создание интернет-магазина ↗", finalAI:"AI-консультант ↗",
    footer:"BEQSON Motion Lab · Независимый демонстрационный проект",
  },
  en: {
    title:"BEQSON Motion Lab — Interactive Web Design & Animation",
    description:"An interactive BEQSON concept: a website transforms from wireframe to visual design, online store and AI consultant interface. Motion UI with CSS and JavaScript.",
    back:"← All Projects", home:"Home", skip:"Skip to content",
    eyebrow:"BEQSON / INTERACTIVE EXPERIENCE",
    heading:"From an idea to",
    accent:"a website in motion.",
    lead:"Explore four stages as a simple wireframe evolves into a polished website, an online store and an AI consultant interface.",
    try:"Explore the animation ↓", portfolio:"All projects ↗",
    conceptNote:"An independent interactive concept by BEQSON. The store and chat interfaces on this page are illustrations, not live commercial systems.",
    floatA:"Motion UI",floatB:"Made to interact",
    storyEyebrow:"01 / THE JOURNEY", storyTitle:"One idea. Four transformations.",
    storyLead:"Scroll through the stages: the preview on the left changes as you go. Try the interactive controls in the store and AI scenes.",
    sample:"Interactive prototype",sampleTag:"No real checkout or live AI requests",
    browser:["beqson.com/idea","beqson.com/design","beqson.com/shop","beqson.com/assistant"],
    pill:["Wireframe","Design","Store","AI"],
    designNav:"STUDIO",designNavRight:"Projects · Contact",designHeading:"Where ideas meet design.",designText:"Clear structure and a distinct style for your business.",designAction:"Learn more",
    shopNav:"NOVA STORE",shopNavRight:"Catalog · About",
    shopHeading:"Your next storefront",products:["Everyday form","Warm details","Objects for living"],
    cartLabel:"Items in cart",addCart:"Add an item to cart +",
    aiName:"BEQSON AI Consultant",aiOnline:"Scripted chat demo · online",
    aiGreeting:"Hello! What would you like to create?",
    aiUser:"I need a beautiful online store.",
    aiAnswer:"Let's start with a catalog, product pages and a simple ordering flow. Then we can assess the right integrations.",
    aiQ1:"What about a service website?",aiA1:"A clear service site can include dedicated pages, an enquiry form and quick ways to contact your team.",
    aiQ2:"Can I add an AI assistant?",aiA2:"Yes, we can plan a chat consultant, its knowledge base and the handoff to a human team.",
    steps:[
      {number:"01 / STRUCTURE",title:"Start with a clear wireframe",body:"Identify what visitors need. Outline the page hierarchy, key messages and a straightforward path to action.",tag:"Structure and UX"},
      {number:"02 / VISUAL",title:"Give the experience a visual identity",body:"Bring together color, typography, imagery and subtle motion to build a memorable interface.",tag:"Web Design and Motion UI"},
      {number:"03 / COMMERCE",title:"Turn the site into a storefront",body:"Explore product categories, a shopping cart and an example ordering journey. Try the add-to-cart button in the preview.",tag:"Interactive E-Commerce"},
      {number:"04 / ASSISTANT",title:"Let visitors start a conversation",body:"See how a consultant interface might answer common questions. The preview buttons switch scripted answers; no AI model is connected here.",tag:"AI Interface Prototype"}
    ],
    capabilityEyebrow:"02 / WHAT THIS DEMONSTRATES",capabilityTitle:"Visually engaging. Thoughtfully built.",
    capabilities:[
      {icon:"↗",title:"Motion UI",text:"Scroll-driven reveals and smooth interface transitions."},
      {icon:"⌘",title:"JavaScript",text:"Functional scene switching, buttons and a local demo cart."},
      {icon:"▣",title:"Responsive Design",text:"Layouts that adapt to desktop, tablet and mobile."},
      {icon:"◉",title:"Accessibility",text:"Keyboard access, clear labels and reduced-motion support."}
    ],
    finalEyebrow:"03 / YOUR NEXT PROJECT",finalTitle:"Let's make something memorable for your business.",
    finalLead:"Motion Lab is a self-initiated BEQSON concept. Let's explore a similar approach for your website, online store or AI consultant.",
    finalContact:"Discuss a project ↗",finalShop:"Build an online store ↗",finalAI:"AI consultant ↗",
    footer:"BEQSON Motion Lab · Independent demonstration concept",
  },
  ka: {
    title:"BEQSON Motion Lab — ინტერაქტიული ვებდიზაინი და ანიმაცია",
    description:"BEQSON-ის ინტერაქტიული კონცეფცია: ვებსაიტის მონახაზიდან ვიზუალურ დიზაინამდე, ონლაინმაღაზიამდე და AI კონსულტანტის ინტერფეისამდე. CSS და JavaScript ანიმაცია.",
    back:"← ყველა პროექტი",home:"მთავარი",skip:"შინაარსზე გადასვლა",
    eyebrow:"BEQSON / INTERACTIVE EXPERIENCE",
    heading:"იდეიდან ვებსაიტამდე,",
    accent:"რომელიც ცოცხლდება.",
    lead:"გაიარეთ ოთხი ეტაპი და ნახეთ, როგორ იქცევა მარტივი მონახაზი დახვეწილ ვებსაიტად, ონლაინმაღაზიად და AI კონსულტანტის ინტერფეისად.",
    try:"ანიმაციის ნახვა ↓",portfolio:"ყველა პროექტი ↗",
    conceptNote:"BEQSON-ის დამოუკიდებელი ინტერაქტიული კონცეფცია. ამ გვერდზე მაღაზიისა და ჩატის ინტერფეისები სადემონსტრაციოა.",
    floatA:"Motion UI",floatB:"Made to interact",
    storyEyebrow:"01 / როგორ მუშაობს",storyTitle:"ერთი იდეა. ოთხი გარდაქმნა.",
    storyLead:"ჩამოსქროლეთ გვერდი: მარცხნივ მაკეტი ეტაპობრივად შეიცვლება. მაღაზიისა და AI-ის სცენებში ღილაკებიც შეგიძლიათ მოსინჯოთ.",
    sample:"ინტერაქტიული პროტოტიპი",sampleTag:"რეალური გადახდებისა და AI მოთხოვნების გარეშე",
    browser:["beqson.com/idea","beqson.com/design","beqson.com/shop","beqson.com/assistant"],
    pill:["მონახაზი","დიზაინი","მაღაზია","AI"],
    designNav:"სტუდია",designNavRight:"პროექტები · კონტაქტი",designHeading:"სადაც იდეა დიზაინად იქცევა.",designText:"მკაფიო სტრუქტურა და გამორჩეული სტილი თქვენი ბიზნესისთვის.",designAction:"გაიგეთ მეტი",
    shopNav:"NOVA STORE",shopNavRight:"კატალოგი · ჩვენ შესახებ",
    shopHeading:"თქვენი ონლაინვიტრინა",products:["ყოველდღიური სტილი","თბილი დეტალები","ნივთები სახლისთვის"],
    cartLabel:"კალათაში პროდუქტი",addCart:"პროდუქტის კალათაში დამატება +",
    aiName:"BEQSON AI Consultant",aiOnline:"სცენარით შექმნილი ჩატის დემო · ონლაინ",
    aiGreeting:"გამარჯობა! რისი შექმნა გსურთ?",
    aiUser:"ლამაზი ონლაინმაღაზია მჭირდება.",
    aiAnswer:"დავიწყოთ კატალოგით, პროდუქტის გვერდებით და მარტივი შეკვეთით. შემდეგ შევარჩევთ საჭირო ინტეგრაციებს.",
    aiQ1:"თუ მომსახურების საიტი მჭირდება?",aiA1:"მომსახურების საიტს შეიძლება ჰქონდეს გასაგები გვერდები, განაცხადის ფორმა და გუნდთან სწრაფი დაკავშირება.",
    aiQ2:"AI ასისტენტის დამატება შეიძლება?",aiA2:"დიახ, შეგვიძლია ჩატის, ცოდნის ბაზისა და მენეჯერთან გადამისამართების დაგეგმვა.",
    steps:[
      {number:"01 / STRUCTURE",title:"ჯერ — გასაგები სტრუქტურა",body:"ვარკვევთ, რა სჭირდება მომხმარებელს. ვაწყობთ გვერდების იერარქიას და მოქმედებამდე მისასვლელ მარტივ გზას.",tag:"სტრუქტურა და UX"},
      {number:"02 / VISUAL",title:"შემდეგ — ვიზუალური ხასიათი",body:"ფერებს, ტიპოგრაფიას, სურათებსა და მსუბუქ ანიმაციას ვაერთიანებთ გამორჩეულ ინტერფეისში.",tag:"ვებდიზაინი და Motion UI"},
      {number:"03 / COMMERCE",title:"ვებსაიტი ონლაინვიტრინად იქცევა",body:"ვაჩვენებთ პროდუქტებს, კატეგორიებს, კალათასა და შეკვეთის მაგალითს. მოსინჯეთ პროდუქტის დამატების ღილაკი.",tag:"ინტერაქტიული E-Commerce"},
      {number:"04 / ASSISTANT",title:"მომხმარებელთან დიალოგი იწყება",body:"ნახეთ, როგორ შეიძლება კონსულტანტი პასუხობდეს კითხვებს. ღილაკები მზა პასუხებს ცვლის; რეალური AI მოდელი აქ არ არის დაკავშირებული.",tag:"AI ინტერფეისის პროტოტიპი"}
    ],
    capabilityEyebrow:"02 / რას აჩვენებს ეს პროექტი",capabilityTitle:"ლამაზი ვიზუალი და გააზრებული ტექნოლოგია.",
    capabilities:[
      {icon:"↗",title:"Motion UI",text:"სქროლზე რეაგირებადი ანიმაცია და რბილი გადასვლები."},
      {icon:"⌘",title:"JavaScript",text:"სცენების გადართვა, ღილაკები და სადემონსტრაციო კალათა."},
      {icon:"▣",title:"Responsive Design",text:"კომპიუტერის, პლანშეტისა და ტელეფონისთვის მორგებული დიზაინი."},
      {icon:"◉",title:"Accessibility",text:"კლავიატურით მართვა, წაკითხვადი ტექსტი და შემცირებული ანიმაცია."}
    ],
    finalEyebrow:"03 / თქვენი მომავალი პროექტი",finalTitle:"შევქმნათ დასამახსოვრებელი გამოცდილება თქვენი ბიზნესისთვის.",
    finalLead:"Motion Lab არის BEQSON-ის დამოუკიდებელი კონცეფცია. განვიხილოთ მსგავსი მიდგომა თქვენი ვებსაიტის, მაღაზიის ან AI კონსულტანტისთვის.",
    finalContact:"პროექტის განხილვა ↗",finalShop:"ონლაინმაღაზიის შექმნა ↗",finalAI:"AI კონსულტანტი ↗",
    footer:"BEQSON Motion Lab · დამოუკიდებელი სადემონსტრაციო კონცეფცია",
  }
};

const esc = value => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const keys = ["wireframe", "design", "store", "ai"];

function render(lang, t) {
  const langLinks = langs.map(code => `<a href="/${code}/motion-lab/" hreflang="${code}" lang="${code}" ${code === lang ? 'aria-current="page"' : ""}>${code === "ka" ? "GE" : code.toUpperCase()}</a>`).join("");
  const alternate = langs.map(code => `<link rel="alternate" hreflang="${code}" href="https://beqson.com/${code}/motion-lab/">`).join("");
  const pills = t.pill.map((label, i) => `<button class="ml-stage-pill" type="button" data-ml-target="${keys[i]}" ${i===0 ? 'aria-current="step"' : ""}>${String(i+1).padStart(2,"0")} · ${esc(label)}</button>`).join("");
  const steps = t.steps.map((step, i) => `<article id="step-${keys[i]}" class="ml-step ${i===0 ? "is-active" : ""}" data-ml-step="${keys[i]}" data-url="${esc(t.browser[i])}"><span class="ml-step-number">${esc(step.number)}</span><h3>${esc(step.title)}</h3><p>${esc(step.body)}</p><span class="ml-step-tag">${esc(step.tag)}</span></article>`).join("\n");
  const caps = t.capabilities.map(cap => `<article class="ml-capability" data-reveal><b aria-hidden="true">${esc(cap.icon)}</b><h3>${esc(cap.title)}</h3><p>${esc(cap.text)}</p></article>`).join("");
  const products = t.products.map((label, i) => `<article class="ml-product"><div class="ml-product-photo ml-product-photo--${["one","two","three"][i]}" aria-hidden="true"></div><div class="ml-product-label">${esc(label)}</div><div class="ml-product-price">${["$48","$65","$39"][i]}</div></article>`).join("");

  return `<!doctype html>
<html lang="${lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#050d1e">
  <title>${esc(t.title)}</title>
  <meta name="description" content="${esc(t.description)}">
  <link rel="canonical" href="https://beqson.com/${lang}/motion-lab/">
  ${alternate}
  <meta property="og:type" content="website">
  <meta property="og:title" content="${esc(t.title)}">
  <meta property="og:description" content="${esc(t.description)}">
  <meta property="og:url" content="https://beqson.com/${lang}/motion-lab/">
  <meta property="og:image" content="https://beqson.com/assets/project-covers/beqson-motion-lab.svg">
  <link rel="icon" href="/assets/favicon-v3.png">
  <link rel="stylesheet" href="/assets/motion-lab.css?v=1">
  <script defer src="/assets/motion-lab.js?v=1"></script>
</head>
<body class="ml-page">
  <a class="ml-skip" href="#main">${esc(t.skip)}</a>
  <header class="ml-topbar"><div class="ml-shell">
    <a class="ml-brand" href="/${lang}/" aria-label="BEQSON">BEQSON<span>.</span></a>
    <nav class="ml-top-actions" aria-label="Site navigation">
      <a class="ml-back" href="/${lang}/projects/">${esc(t.back)}</a>
      <div class="ml-languages" aria-label="Language">${langLinks}</div>
    </nav>
  </div></header>
  <main id="main">
    <section class="ml-hero">
      <div class="ml-orb ml-orb--one" aria-hidden="true"></div><div class="ml-orb ml-orb--two" aria-hidden="true"></div>
      <div class="ml-shell">
        <div data-reveal>
          <div class="ml-eyebrow">${esc(t.eyebrow)}</div>
          <h1>${esc(t.heading)}<br><em>${esc(t.accent)}</em></h1>
          <p class="ml-lead">${esc(t.lead)}</p>
          <div class="ml-hero-actions"><a class="ml-button ml-button--primary" href="#story">${esc(t.try)}</a><a class="ml-button ml-button--secondary" href="/${lang}/projects/">${esc(t.portfolio)}</a></div>
          <p class="ml-disclaimer"><span aria-hidden="true">ⓘ</span>${esc(t.conceptNote)}</p>
        </div>
        <div class="ml-hero-showcase" aria-hidden="true">
          <div class="ml-hero-ring"></div><div class="ml-hero-ring ml-hero-ring--small"></div>
          <div class="ml-holo"><div class="ml-holo-header"><i></i><i></i><i></i></div><div class="ml-holo-main"><div class="ml-holo-mark">BEQSON<br><b>MOTION LAB</b></div><div class="ml-holo-line"></div><div class="ml-holo-line short"></div><div class="ml-holo-cards"><i></i><i></i><i></i></div></div></div>
          <span class="ml-float-chip ml-float-chip--a"><i></i>${esc(t.floatA)}</span><span class="ml-float-chip ml-float-chip--b"><i></i>${esc(t.floatB)}</span>
        </div>
      </div>
    </section>
    <section id="story" class="ml-story">
      <div class="ml-shell">
        <div class="ml-section-intro" data-reveal><div class="ml-eyebrow">${esc(t.storyEyebrow)}</div><h2>${esc(t.storyTitle)}</h2><p>${esc(t.storyLead)}</p></div>
        <div class="ml-story-layout">
          <div class="ml-preview-column">
            <div class="ml-preview-wrap">
              <div class="ml-preview" data-ml-preview data-stage="wireframe">
                <div class="ml-browser-bar"><span class="ml-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="ml-address" data-ml-address>${esc(t.browser[0])}</span></div>
                <div class="ml-browser-body">
                  <div class="ml-scene ml-scene--wireframe" data-ml-scene="wireframe" aria-hidden="false">
                    <div class="ml-wf-bar"><i class="ml-wf-logo"></i><i class="ml-wf-nav"></i></div>
                    <div class="ml-wf-hero"><div><div class="ml-wf-line large"></div><div class="ml-wf-line"></div><div class="ml-wf-line short"></div><div class="ml-wf-button"></div></div><div class="ml-wf-picture" aria-hidden="true">◇</div></div>
                    <div class="ml-wf-grid"><div class="ml-wf-box"><i></i><b></b></div><div class="ml-wf-box"><i></i><b></b></div><div class="ml-wf-box"><i></i><b></b></div></div>
                  </div>
                  <div class="ml-scene ml-scene--design" data-ml-scene="design" aria-hidden="true">
                    <div class="ml-design-nav">BEQSON / ${esc(t.designNav)} <span>${esc(t.designNavRight)}</span></div>
                    <div class="ml-design-hero"><div><h3>${esc(t.designHeading)}</h3><p>${esc(t.designText)}</p><span class="ml-design-cta">${esc(t.designAction)} ↗</span></div><div class="ml-design-illustration" aria-hidden="true"></div></div>
                    <div class="ml-design-bottom" aria-hidden="true"><i></i><i></i><i></i></div>
                  </div>
                  <div class="ml-scene ml-scene--store" data-ml-scene="store" aria-hidden="true">
                    <div class="ml-store-nav">${esc(t.shopNav)} <span>${esc(t.shopNavRight)}</span></div>
                    <div class="ml-store-hero"><h3>${esc(t.shopHeading)}</h3><span class="ml-cart-count" aria-live="polite"><span aria-hidden="true">🛒 </span><span data-ml-cart data-label="${esc(t.cartLabel)}" aria-label="${esc(t.cartLabel)}: 0">0</span></span></div>
                    <div class="ml-products">${products}</div>
                    <button type="button" class="ml-add-cart" data-ml-add>${esc(t.addCart)}</button>
                  </div>
                  <div class="ml-scene ml-scene--ai" data-ml-scene="ai" aria-hidden="true">
                    <div class="ml-ai-top"><span class="ml-ai-avatar" aria-hidden="true">AI</span><span class="ml-ai-name">${esc(t.aiName)}<small>${esc(t.aiOnline)}</small></span></div>
                    <div class="ml-chat"><div class="ml-bubble ml-bubble--assistant">${esc(t.aiGreeting)}</div><div class="ml-bubble ml-bubble--user">${esc(t.aiUser)}</div><div class="ml-bubble ml-bubble--assistant" data-ml-ai-response aria-live="polite">${esc(t.aiAnswer)}</div></div>
                    <div class="ml-ai-actions"><button type="button" class="ml-ai-question" data-ml-question data-answer="${esc(t.aiA1)}">${esc(t.aiQ1)}</button><button type="button" class="ml-ai-question" data-ml-question data-answer="${esc(t.aiA2)}">${esc(t.aiQ2)}</button></div>
                  </div>
                </div>
              </div>
            </div>
            <div class="ml-demo-label"><strong>${esc(t.sample)}</strong><span>${esc(t.sampleTag)}</span></div>
            <nav class="ml-stage-pills" aria-label="Animation stages">${pills}</nav>
          </div>
          <div class="ml-steps">${steps}</div>
        </div>
      </div>
    </section>
    <section class="ml-capabilities"><div class="ml-shell"><div class="ml-eyebrow">${esc(t.capabilityEyebrow)}</div><h2 data-reveal>${esc(t.capabilityTitle)}</h2><div class="ml-capabilities-grid">${caps}</div></div></section>
    <section class="ml-final"><div class="ml-shell" data-reveal><div class="ml-eyebrow" style="justify-content:center">${esc(t.finalEyebrow)}</div><h2>${esc(t.finalTitle)}</h2><p>${esc(t.finalLead)}</p><div class="ml-hero-actions"><a class="ml-button ml-button--primary" href="mailto:digitalstudiobeqson@gmail.com?subject=BEQSON%20Motion%20Lab">${esc(t.finalContact)}</a><a class="ml-button ml-button--secondary" href="/${lang}/shopify/">${esc(t.finalShop)}</a><a class="ml-button ml-button--secondary" href="/${lang}/ai-consultant/">${esc(t.finalAI)}</a></div></div></section>
  </main>
  <footer class="ml-footer"><div class="ml-shell"><span>© 2026 BEQSON · ${esc(t.footer)}</span><a href="/${lang}/">${esc(t.home)} ↗</a></div></footer>
</body>
</html>`;
}

for (const lang of langs) {
  const dir = path.join(root, lang, "motion-lab");
  fs.mkdirSync(dir, {recursive:true});
  fs.writeFileSync(path.join(dir,"index.html"), render(lang, translations[lang]));
  console.log(`Built ${lang}/motion-lab/index.html`);
}

// Reuse BEQSON's authoritative SEO rules instead of maintaining duplicate
// schema and social metadata for this interactive standalone experience.
execFileSync("python3", [path.join(root, "tools", "finalize_motion_lab.py")], {stdio:"inherit"});
