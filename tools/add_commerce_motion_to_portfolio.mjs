import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const cover = "/assets/project-covers/beqson-commerce-motion.svg";
const copy = {
  ru: {
    badge: "Концепт студии", category: "E-COMMERCE / 3D", title: "Commerce Motion — интерактивная витрина",
    short: "Объёмный товар вращается на 360°, меняет цвет и приближается. Анимированная корзина с количеством и итоговой ценой.",
    description: "Авторская витрина BEQSON с CSS 3D и JavaScript: плавное вращение объёмного товара мышью или пальцем, автоматическая анимация, приближение, три варианта отделки и анимированное добавление в корзину. Можно менять количество, удалять позиции и завершать демонстрационный сценарий оформления. Адаптировано для мобильных экранов и трёх языков. HALO ONE — вымышленный товар; реальных платежей и заказов нет.",
    homeLink: "Открыть 3D-витрину", link: "Попробовать интерактивный магазин",
  },
  en: {
    badge: "Studio concept", category: "E-COMMERCE / 3D", title: "Commerce Motion — interactive storefront",
    short: "A 360° product rotates, changes color and zooms in. Animated cart with quantities and live totals.",
    description: "A self-initiated BEQSON e-commerce showcase built with CSS 3D and JavaScript: smooth auto-rotation, mouse/touch dragging, zoom, three material finishes and an animated add-to-cart journey. Visitors can change quantities, remove products and complete a simulated checkout. Responsive and available in three languages. HALO ONE is a fictional concept product; no payments or real orders are processed.",
    homeLink: "Explore 3D storefront", link: "Try interactive store",
  },
  ka: {
    badge: "სტუდიის კონცეფცია", category: "E-COMMERCE / 3D", title: "Commerce Motion — ინტერაქტიული ვიტრინა",
    short: "360° ბრუნვადი პროდუქტი, ფერის შეცვლა, დეტალების გადიდება და ანიმირებული კალათა რაოდენობითა და ჯამური ფასით.",
    description: "BEQSON-ის დამოუკიდებელი E-Commerce კონცეფცია CSS 3D-ითა და JavaScript-ით: პროდუქტის ავტომატური ბრუნვა, მართვა მაუსით ან შეხებით, გადიდება, სამი ფერი და კალათაში დამატების ანიმაცია. შესაძლებელია რაოდენობის შეცვლა, პროდუქტების წაშლა და შესყიდვის სადემონსტრაციო სცენარის დასრულება. ადაპტირებულია მობილურისთვის და ხელმისაწვდომია სამ ენაზე. HALO ONE გამოგონილი პროდუქტია — რეალური გადახდები და შეკვეთები არ სრულდება.",
    homeLink: "3D ვიტრინის ნახვა", link: "ინტერაქტიული მაღაზიის ნახვა",
  },
};

const esc = s => String(s).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");

for (const [lang, t] of Object.entries(copy)) {
  const url = `/${lang}/commerce-motion/`;
  const homeFile = path.join(root, lang, "index.html");
  const projectsFile = path.join(root, lang, "projects", "index.html");
  const homeCard = `<a class="beqson-work-card" href="${url}"><span class="beqson-work-art"><img src="${cover}" alt="" loading="lazy" decoding="async"></span><span class="beqson-work-copy"><span class="beqson-work-meta"><span class="beqson-work-badge">${esc(t.badge)}</span><span class="beqson-work-cat">${esc(t.category)}</span></span><strong class="beqson-work-name">${esc(t.title)}</strong><span class="beqson-work-desc">${esc(t.short)}</span><span class="beqson-work-cta">${esc(t.homeLink)} <span aria-hidden="true">↗</span></span></span></a>`;
  const projectCard = `<article class="project-card" id="commerce-motion" data-project-cat="commerce"><div class="project-visual"><img src="${cover}" alt="BEQSON Commerce Motion interactive e-commerce showcase" width="1600" height="1000" loading="lazy" decoding="async"></div><div class="project-body"><div class="project-topline"><span class="project-badge">${esc(t.badge)}</span><span class="project-cat">${esc(t.category)}</span></div><h2>${esc(t.title)}</h2><p>${esc(t.description)}</p><ul class="project-tags"><li>CSS 3D</li><li>JavaScript</li><li>Product UX</li><li>E-Commerce</li><li>Responsive</li></ul><div class="project-actions" role="group" aria-label="Commerce Motion"><a class="project-action project-action--demo" href="${url}"><span>${esc(t.link)}</span><span class="project-action-arrow" aria-hidden="true">↗</span></a></div></div></article>`;

  let home = fs.readFileSync(homeFile, "utf8");
  if (!home.includes(`href="${url}"`)) {
    const marker = `<a class="beqson-work-card" href="/${lang}/motion-lab/"`;
    if (!home.includes(marker)) throw Error(`Missing Motion Lab homepage marker: ${lang}`);
    home = home.replace(marker, homeCard + marker);
  }
  const homeTotal = (home.match(/<a class="beqson-work-card\b/g) ?? []).length;
  home = home.replace(/(<a class="beqson-work-all"[^>]*>[^<]*?)\d+(\s)/, `$1${homeTotal}$2`);
  fs.writeFileSync(homeFile, home);

  let projects = fs.readFileSync(projectsFile, "utf8");
  if (!projects.includes('id="commerce-motion"')) {
    const marker = '<article class="project-card" id="motion-lab"';
    if (!projects.includes(marker)) throw Error(`Missing Motion Lab portfolio marker: ${lang}`);
    projects = projects.replace(marker, projectCard.replace('data-project-cat="commerce"', 'data-project-cat="web"') + marker);
  }
  fs.writeFileSync(projectsFile, projects);
  const projectTotal = (projects.match(/<article class="project-card"/g) ?? []).length;
  if (projectTotal !== homeTotal) throw Error(`Project-card counts differ: ${lang} homepage=${homeTotal} portfolio=${projectTotal}`);
  process.stdout.write(`${lang}: ${projectTotal} portfolio projects\n`);
}
