import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const translations = {
  ru: {
    badge: "Концепт студии", category: "WEB / MOTION", title: "BEQSON Motion Lab — сайт, который оживает",
    short: "Интерактивный путь от каркаса сайта до дизайна, магазина и AI-чата. Анимация прокрутки и работающие демо-кнопки.",
    detail: "Авторский интерактивный проект BEQSON: при прокрутке сайт проходит четыре этапа — каркас, визуальный дизайн, интернет-магазин и AI-интерфейс. Анимации созданы на CSS и JavaScript. Работают переключение сцен, демонстрационная корзина и сценарные ответы чата. Проект адаптирован для мобильных устройств и учитывает настройки уменьшения движения. Реальных оплат и запросов к AI нет.",
    tags: ["Motion UI", "JavaScript", "CSS animation", "UX", "Responsive"],
    link: "Открыть интерактивную демонстрацию", homeLink: "Посмотреть анимацию"
  },
  en: {
    badge: "Studio concept", category: "WEB / MOTION", title: "BEQSON Motion Lab — a website in motion",
    short: "An interactive journey from wireframe to web design, storefront and AI chat. Scroll animations and working demo controls.",
    detail: "A self-initiated BEQSON interactive concept. As visitors scroll, a website evolves through four stages: wireframe, visual design, online store and AI interface. Built using CSS animations and JavaScript, with working scene navigation, a demo cart and scripted chat replies. Responsive and respects reduced-motion settings. There are no real payments or live AI calls.",
    tags: ["Motion UI", "JavaScript", "CSS animation", "UX", "Responsive"],
    link: "Open interactive demonstration", homeLink: "Explore the animation"
  },
  ka: {
    badge: "სტუდიის კონცეფცია", category: "WEB / MOTION", title: "BEQSON Motion Lab — გაცოცხლებული ვებსაიტი",
    short: "ინტერაქტიული გზა მონახაზიდან დიზაინამდე, ონლაინმაღაზიამდე და AI ჩატამდე. სქროლის ანიმაცია და მოქმედი დემო ღილაკები.",
    detail: "BEQSON-ის დამოუკიდებელი ინტერაქტიული კონცეფცია. გვერდის სქროლისას ვებსაიტი ოთხ ეტაპს გადის: მონახაზი, ვიზუალური დიზაინი, ონლაინმაღაზია და AI ინტერფეისი. CSS და JavaScript ანიმაცია, სცენების გადართვა, სადემონსტრაციო კალათა და წინასწარ მომზადებული ჩატის პასუხები. დიზაინი მორგებულია მობილურ მოწყობილობებზე და ითვალისწინებს შემცირებული მოძრაობის პარამეტრს. რეალური გადახდები და AI მოთხოვნები არ სრულდება.",
    tags: ["Motion UI", "JavaScript", "CSS animation", "UX", "Responsive"],
    link: "ინტერაქტიული დემოს გახსნა", homeLink: "ანიმაციის ნახვა"
  }
};

const esc = value => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");

for (const [lang, t] of Object.entries(translations)) {
  const homeFile = path.join(root, lang, "index.html");
  const portfolioFile = path.join(root, lang, "projects", "index.html");
  const homeCard = `<a class="beqson-work-card" href="/${lang}/motion-lab/"><span class="beqson-work-art"><img src="/assets/project-covers/beqson-motion-lab.svg" alt="" loading="lazy" decoding="async"></span><span class="beqson-work-copy"><span class="beqson-work-meta"><span class="beqson-work-badge">${esc(t.badge)}</span><span class="beqson-work-cat">${esc(t.category)}</span></span><strong class="beqson-work-name">${esc(t.title)}</strong><span class="beqson-work-desc">${esc(t.short)}</span><span class="beqson-work-cta">${esc(t.homeLink)} <span aria-hidden="true">↗</span></span></span></a>`;
  const portfolioCard = `<article class="project-card" id="motion-lab" data-project-cat="web"><div class="project-visual"><img src="/assets/project-covers/beqson-motion-lab.svg" alt="BEQSON Motion Lab interactive website preview" width="1600" height="1000" loading="lazy" decoding="async"></div><div class="project-body"><div class="project-topline"><span class="project-badge">${esc(t.badge)}</span><span class="project-cat">${esc(t.category)}</span></div><h2>${esc(t.title)}</h2><p>${esc(t.detail)}</p><ul class="project-tags">${t.tags.map(tag => `<li>${esc(tag)}</li>`).join("")}</ul><div class="project-actions" role="group" aria-label="BEQSON Motion Lab"><a class="project-action project-action--demo" href="/${lang}/motion-lab/"><span>${esc(t.link)}</span><span class="project-action-arrow" aria-hidden="true">↗</span></a></div></div></article>`;

  let home = fs.readFileSync(homeFile, "utf8");
  if (!home.includes(`href="/${lang}/motion-lab/"`)) {
    const insertionPoint = `<a class="beqson-work-card beqson-work-card--ai" href="/${lang}/ai-consultant/"`;
    if (!home.includes(insertionPoint)) throw Error(`Homepage insertion marker missing for ${lang}`);
    home = home.replace(insertionPoint, homeCard + insertionPoint);
  }
  const homeTotal = (home.match(/<a class="beqson-work-card\b/g) || []).length;
  home = home.replace(/(<a class="beqson-work-all"[^>]*>[^<]*?)\d+(\s)/, `$1${homeTotal}$2`);
  fs.writeFileSync(homeFile, home);

  let portfolio = fs.readFileSync(portfolioFile, "utf8");
  if (!portfolio.includes('id="motion-lab"')) {
    const insertionPoint = '<article class="project-card" id="forme-home"';
    if (!portfolio.includes(insertionPoint)) throw Error(`Portfolio insertion marker missing for ${lang}`);
    portfolio = portfolio.replace(insertionPoint, portfolioCard + insertionPoint);
  }
  fs.writeFileSync(portfolioFile, portfolio);
  const total = (portfolio.match(/<article class="project-card"/g) || []).length;
  if (total !== homeTotal) throw Error(`Portfolio count does not match homepage for ${lang}: ${homeTotal} vs ${total}`);
  process.stdout.write(`${lang}: ${total} projects with Motion Lab\n`);
}
