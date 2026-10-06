# Исходные изображения и локализованные макеты

Для каждого направления создано собственное изображение с помощью image_gen. На него наложен интерфейс из `mockups.json` и `mockups.css`, отрисованный Chromium через `build_mockups.py`. Текст не генерируется моделью изображения: используются локальные Manrope, Noto Sans Georgian и PT Serif, поэтому надписи точно соответствуют GE (`ka`), RU и EN.

Имена LEX, DENTA, VITA, ESTATE, BALANCE, FORMA, APEX и AURA условные. Изображения представляют дизайн-концепции, а не реальные клиентские проекты. Все фото и шрифты лежат локально; при открытии сайта внешние сервисы не вызываются.

Иллюстрации сохранены в `assets/concepts/art/`. При повторной сборке они используются без нового обращения к image_gen. Экспорт: 1536×1024, 768×512 и 480×320 и 320×213 в AVIF/WebP; для Open Graph — JPEG 1200×800. Ранние файлы `assets/concepts/<slug>.webp` оставлены доступными для прежних ссылок.

PT Serif получен из `@fontsource/pt-serif` версии 5.3.0, лицензия SIL OFL сохранена в `assets/fonts/pt-serif-OFL.txt`.

## Запросы для исходных иллюстраций

Общие условия: photorealistic premium website hero photograph, landscape 3:2, high resolution; edge-to-edge photograph; no lettering, text, watermark, branding or website UI; magazine-quality natural textures.

### lawyers

An elegant boutique lawyer's study, dark graphite walls, champagne brass desk lamp, a sculptural carved walnut desk with neatly stacked neutral legal books and one cream document folder, city-facing window, quiet architectural afternoon light. No people. Serious warm understated luxury. Wide editorial interior photograph.

### dentists

A bright boutique dental practice treatment room, pearl white walls, muted sage-green cabinetry, modern dental chair and professional dental equipment, daylight, a delicate leafy plant, impeccably clean Scandinavian interior. No people. Wide editorial architectural photograph.

### clinics

A welcoming modern medical consultation interior, midnight blue accent wall with soft pearl white furnishings, elegant comfortable chair, examination couch and a subtle unmarked medical instrument cabinet, a large window and leafy plant, refined private clinic, warm daylight. No people. Wide editorial architectural photograph.

### realtors

An extraordinary modern residential villa interior, olive and warm sand tones, large floor-to-ceiling windows opening to a verdant hillside, cream linen sofa, natural wood, architectural sunlight. Premium real estate editorial photography, credible lived-in calm luxury. No people. Wide photograph.

### accountants

A refined accountant's navy-blue and walnut office desk with copper lamp, laptop screen showing an abstract spreadsheet of lines with NO readable text, neat paper sheets without text and a brass pen, navy background, daylight, credible thoughtful boutique financial consultancy. No people. Wide editorial still life photograph.

### construction

A beautifully finished contemporary limestone living room, warm terracotta sculptural armchair, built-in oak cabinetry, large natural stone surfaces, modern pendant light, architectural shadows, handmade tactile materials, premium interior designer portfolio photography. No people. Wide photograph.

### autoservices

A pristine black premium sports coupe seen from front three-quarter angle in a professional dark titanium automotive detailing workshop, cool architectural linear light reflections, tiny acid-lime accents on tool cabinet, crisp glossy paint finish, no badges, no logos, no readable plates, no people. Wide editorial automotive photograph.

### hotels

A serene boutique hotel terrace on the Georgian Black Sea coast, linen lounge chairs, turquoise sea on horizon, sculptural Mediterranean stone railings and graceful olive branches, morning sunlight, boutique travel editorial photography with warm linen and sea green colors. No people. Wide photograph.
