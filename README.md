# BEQSON — Premium · GE / RU / EN

Готовый статический сайт для https://bequcho.github.io/digital-office-studio/.
Для публикации не нужно устанавливать Node.js, Python или запускать сборку: все HTML-страницы уже созданы.

## Обновить сайт в GitHub

1. Используйте обновлённые файлы текущей сборки, включая новые языковые папки внутри `assets/concepts/` и шрифты WOFF2.
2. Откройте существующий репозиторий `bequcho/digital-office-studio` и его корневую папку.
3. При ручной загрузке нажмите **Add file → Upload files**. Перетащите **файлы сайта**, включая папки `assets`, `ru`, `ka`, `en` и `tools`. Главный `index.html` должен оказаться непосредственно в корне репозитория. Также сохраните пустой файл `.nojekyll`.
4. Сохраните изменения в ветке, из которой публикуется ваш сайт, с заменой файлов с такими же именами. Для прежней настройки это `main`.
5. Дождитесь успешной публикации в **Actions** и откройте https://bequcho.github.io/digital-office-studio/ru/. При старом отображении обновите страницу сочетанием **Ctrl + F5**.

Если GitHub Pages уже настроен, повторная настройка обычно не нужна. Для публикации из ветки: **Settings → Pages → Deploy from a branch → main → /(root) → Save**.

Старые изображения, которые остались в репозитории от v7, работе новой версии не мешают. Все используемые v8 файлы входят в архив.

## Что внутри

- 3 главные языковые страницы: `/ru/`, `/ka/`, `/en/`.
- 8 страниц направлений на каждом языке — 24 новые отраслевые страницы.
- Русская главная также доступна из корня, с canonical на `/ru/`.
- Страница ошибки `404.html`.
- 8 индивидуальных визуальных концепций × 3 языка: 24 локализованных макета, AVIF/WebP в четырёх размерах и JPEG для Open Graph.
- Локальные шрифты Manrope и Noto Sans Georgian в WOFF2; PT Serif для макетов. Лицензии включены.
- SVG-иконки с объёмным оформлением, графические флаги, адаптивное меню.
- Увеличение макетов, FAQ, прямые ссылки на WhatsApp, Telegram и email.
- `canonical`, `hreflang`, Open Graph, JSON-LD и обновлённая карта сайта.
- Файл `QA-REPORT.md` с результатами проверки.

## Направления и адреса

| Направление | Русская страница |
| --- | --- |
| Адвокаты | https://bequcho.github.io/digital-office-studio/ru/lawyers/ |
| Стоматологи | https://bequcho.github.io/digital-office-studio/ru/dentists/ |
| Частные врачи / клиники | https://bequcho.github.io/digital-office-studio/ru/clinics/ |
| Риелторы | https://bequcho.github.io/digital-office-studio/ru/realtors/ |
| Бухгалтеры / налоговые консультанты | https://bequcho.github.io/digital-office-studio/ru/accountants/ |
| Ремонт / строительство / дизайнеры | https://bequcho.github.io/digital-office-studio/ru/construction/ |
| Автосервисы / детейлинг | https://bequcho.github.io/digital-office-studio/ru/autoservices/ |
| Отели / апартаменты / туризм | https://bequcho.github.io/digital-office-studio/ru/hotels/ |

Грузинская и английская версии имеют те же адреса направлений внутри `/ka/` и `/en/`. Переключение флагом сохраняет выбранное направление.

## Контакты и цены

- WhatsApp: +995 551 73 93 33.
- Telegram: @digital_studio_beqson.
- Email: digitalstudiobeqson@gmail.com.
- Start — $250, Growth — $490, Pro — $890.
- Сопровождение — от $60 в месяц.

Сайт студии связывает посетителя с вами через выбранный мессенджер или почтовую программу. Не имитирует отправку заявок и не сохраняет персональные данные в браузере. Услуги CRM, аналитики, форм и бронирования описаны как возможная комплектация клиентских проектов; их подключение согласуется отдельно.

Макеты LEX, DENTA, VITA, ESTATE, BALANCE, FORMA, APEX и AURA — демонстрационные дизайн-концепции с оригинальными изображениями, созданными с помощью ИИ. Это изображения, а не отдельные работающие сайты этих условных компаний. Названия в макетах условные; русский, грузинский и английский текст отрисован настоящими локальными шрифтами. Язык изображения соответствует языку страницы. Финальные тексты клиентского сайта адаптируются под заказчика. Реальный проект LevaniLaw представлен отдельно, без выдуманных результатов и отзывов.

Все 24 изображения доступны в [MOCKUPS.md](MOCKUPS.md). GE использует существующую папку `/ka/`; адреса `/ru/`, `/ka/`, `/en/` сохранены.

## Карта сайта

https://bequcho.github.io/digital-office-studio/sitemap.xml

Карта содержит 27 основных страниц: три главные и 24 страницы направлений. После публикации можно отправить обновлённый sitemap в уже используемые панели поисковых систем. `robots.txt` включён в архив; при размещении GitHub Pages в подпапке правила обхода домена определяет его корневой robots.txt.

## Редактирование исходников

- `styles.css` — весь дизайн и адаптивность.
- `script.js` — меню и увеличение макетов.
- `tools/content.json` — основные тексты на трёх языках.
- `tools/industries.json` — содержание восьми направлений.
- `tools/build.py` — генератор статических страниц на стандартном Python 3.
- `tools/IMAGE-PROMPTS.md` — полные запросы для восьми изображений.
- `assets/concepts/ka/`, `ru/`, `en/` — локализованные AVIF/WebP и JPEG для социальных сетей.
- `tools/mockups.json` и `tools/mockups.css` — тексты и восемь визуальных стилей макетов.
- `tools/build_mockups.py` — воспроизводимый экспорт изображений через Chromium.
- `tools/test_site.py` — проверка маршрутов, ресурсов, якорей и SEO-разметки.
- `tools/audit_browser.py` — проверка адаптивности и поведения в браузере.

После изменения JSON-текстов можно пересоздать HTML командой из папки сайта:

```bash
python3 tools/build.py
```

Для обычной загрузки в GitHub эта команда не требуется. Если будете подключать новый домен, в генераторе нужно обновить `BASE_URL`, пересобрать HTML и карту сайта, затем настроить домен в GitHub Pages.

## Локальная разработка и проверки

Из `/workspace/digital-office-studio` запустите сервер с корнем `/workspace`, чтобы сохранить адресный префикс GitHub Pages:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory /workspace
```

Для проверки статических страниц достаточно стандартного Python:

```bash
python3 tools/test_site.py
```

Пересоздание макетов требует Chromium, Pillow и Playwright. Пакеты нужны только разработчику; опубликованный сайт остаётся полностью статическим. Все исходные иллюстрации уже сохранены локально, повторная генерация с помощью ИИ не требуется:

```bash
python3 -m venv /workspace/beqson-tools
/workspace/beqson-tools/bin/pip install -r tools/requirements-mockups.txt
/workspace/beqson-tools/bin/python tools/build_mockups.py
python3 tools/build.py
/workspace/beqson-tools/bin/python tools/audit_browser.py --output /tmp/beqson-audit
```

Chromium определяется автоматически; при необходимости задайте `CHROMIUM_PATH`. Для дополнительной проверки axe-core передайте `--axe /path/to/axe.min.js`. Результаты текущего аудита — в [QA-REPORT.md](QA-REPORT.md).

## Документация GitHub

Инструкция сверена с официальными страницами 6 октября 2026 года:

- https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
