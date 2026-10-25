#!/usr/bin/env python3
"""Build localized, SEO-ready BEQSON Family Voices portfolio case pages."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "meta-static-ads"
BASE = "https://beqson.com"
ASSET = "/assets/meta-ads/"

CONCEPTS = [
    {
        "key":"voice",
        "title":"Preserve Their Voice",
        "designs":[
            ("preserve_their_voice_A_warm_connection", "Warm Connection"),
            ("preserve_their_voice_B_cinematic_portrait", "Cinematic Portrait"),
        ],
    },
    {
        "key":"gift",
        "title":"A Gift That Lasts",
        "designs":[
            ("02_gift_A_family_moment", "Family Moment"),
            ("02_gift_B_heirloom_still_life", "Heirloom Still Life"),
        ],
    },
    {
        "key":"audio",
        "title":"Read the Story. Hear the Voice.",
        "designs":[
            ("03_read_hear_A_lifestyle", "Read & Listen"),
            ("03_read_hear_B_product_story", "Product Story"),
        ],
    },
]

COPY = {
 "en":{
    "title":"Family Voices — Meta Static Ads Design | BEQSON Digital Studio",
    "description":"Six premium Meta static ad concepts in 4:5 and 9:16. An independent, unofficial BEQSON spec campaign inspired by family storytelling and keepsakes.",
    "nav_home":"Home","nav_projects":"Projects","nav_services":"Services","nav_contact":"Contact",
    "kicker":"BEQSON CREATIVE STUDIO / INDEPENDENT CONCEPT 2026",
    "headline":"Family Voices.","headline_accent":"Stories that stay with us.",
    "hero":"An emotional static-ad exploration of memory, voice and the gifts that connect generations. Three strategic ideas, six distinctive compositions, and twelve platform-ready adaptations.",
    "disclosure":"Unofficial portfolio project · Not commissioned or endorsed by Remento",
    "metric_1":"Creative concepts","metric_2":"Distinct ad designs","metric_3":"Final exports",
    "overview_tag":"01 / PROJECT OVERVIEW","overview_heading":"Designed to make a feeling tangible.",
    "overview":"Family Voices is an independent speculative advertising project created by BEQSON Digital Studio. Inspired by the Remento product idea—preserving spoken family stories alongside a printed keepsake—the campaign explores how emotional storytelling can translate into clear, premium static ads for social feeds and vertical placements. No work was commissioned by Remento, and these ads have not been used in a campaign.",
    "challenge_tag":"02 / CREATIVE CHALLENGE","challenge_heading":"Emotion first. Product clarity close behind.",
    "challenge_1_title":"The creative challenge","challenge_1":"Communicate an intangible benefit—the irreplaceable sound of a loved one's voice—within a static frame that can be understood in seconds. Each direction needed a simple hook, expressive imagery, legible typography and a focused call to action.",
    "challenge_2_title":"Audience and emotional insight","challenge_2":"Hypothetical audience: adult children looking for meaningful gifts for parents, families documenting grandparents' memories, and people who value personal archives. Creative hypothesis: specificity and genuine human connection can make the message resonate more deeply than generic nostalgia. This is a design assumption, not audience research or a tested claim.",
    "direction_tag":"03 / CREATIVE DIRECTION","direction_heading":"Warmth, tactility and restraint.",
    "direction":"A consistent editorial system anchors all six ads: warm cinematic photography, paper and linen textures, serif headlines with modern sans-serif supporting copy, elegant spacing, and a quiet palette of ivory, walnut, olive, cocoa and muted gold. Distinct compositions explore intimate portraiture, real family connection, premium gifting and product demonstration.",
    "concepts_tag":"04 / ADVERTISING CONCEPTS","concepts_heading":"Three angles. Two treatments each.",
    "concepts_sub":"A different emotional or functional reason to care in every group—not simply a change of color or crop.",
    "voice_desc":"The human voice becomes the emotional centerpiece. One treatment uses a shared family moment; the other focuses on a grandfather's quiet storytelling presence.",
    "gift_desc":"A keepsake as a considered, deeply personal gift. The two treatments contrast the emotional moment of giving with a tactile premium product still life.",
    "audio_desc":"The product mechanism made visible: a printed memory and the possibility of hearing the original voice. QR and audio-player elements are illustrative, not working product screens.",
    "design_label":"Independent art direction · 4:5 feed layout",
    "gallery_tag":"05 / FINAL STATIC ADS","gallery_heading":"The six finished feed creatives.",
    "gallery_sub":"Final artboards exported at 1080 × 1350 px. Open any image to inspect the full-resolution design.",
    "adapt_tag":"06 / FORMAT ADAPTATION","adapt_heading":"Designed for feed and full screen.",
    "adapt_sub":"Each visual direction was separately arranged for 1080 × 1920 px vertical placements, with headline, CTA and disclosure kept clear of the main interface zones where practical. Final media placements should always be previewed inside the ad platform.",
    "process_tag":"07 / DESIGN WORKFLOW","process_heading":"A repeatable creative production process.",
    "process":[("01","Message & insight","Define one emotional promise, a simple advertising hook and a clear CTA for each concept."),("02","Visual exploration","Art-direct AI-assisted source photography and curate natural, believable scenes."),("03","Type & composition","Set every line of copy deterministically; refine contrast, hierarchy and illustrative overlays."),("04","Adapt & quality-check","Build separate 4:5 and 9:16 layouts; verify dimensions, readability, faces, artifacts and spelling.")],
    "tools_tag":"08 / TOOLS & SKILLS","tools_heading":"AI-assisted imagery. Human-led decisions.",
    "tools_intro":"The artwork uses generative photography with manual layout and final export. Relevant skills demonstrated:",
    "tools":["Static ad design","Creative direction","Concept development","Visual storytelling","AI-assisted imagery","Typography","Responsive art direction","Meta placement adaptation","Image compositing","Quality assurance"],
    "note":"Disclosure: All family scenes and pictured books are AI-generated illustrations. Remento is referenced only as inspiration for an independent spec campaign. The QR graphics and audio-player views are nonfunctional demonstration elements. There are no campaign budgets, CTR, ROAS, client approvals or performance claims.",
    "final_tag":"09 / FINAL GALLERY","final_heading":"Twelve exports. One cohesive story.",
    "final_text":"Six ad designs, each in two placements. The source artwork and platform adaptations form a reusable creative system suitable for sharing in a job application or as an example of BEQSON's approach.",
    "cta_tag":"10 / WORK WITH BEQSON","cta_heading":"Need static ads that feel as good as they look?",
    "cta_text":"BEQSON develops AI-assisted, human-art-directed static creative for emerging brands, e-commerce and service businesses. Tell us about your product, audience and creative brief.",
    "cta_mail":"Discuss an ad project","cta_back":"View all BEQSON projects",
    "related":"Explore more from BEQSON","related_links":[("Kakheti Wine House — E-commerce","kakheti-wine-house"),("BEQSON Motion Lab","motion-lab"),("AI Consultant","ai-consultant")],
    "footer":"© BEQSON Digital Studio · Independent speculative creative study",
 },
 "ru":{
    "title":"Family Voices — дизайн статичной рекламы Meta | BEQSON Digital Studio",
    "description":"Шесть премиальных концепций статичной рекламы Meta в форматах 4:5 и 9:16. Независимый демонстрационный проект BEQSON о семейных историях.",
    "nav_home":"Главная","nav_projects":"Проекты","nav_services":"Услуги","nav_contact":"Связаться",
    "kicker":"BEQSON CREATIVE STUDIO / НЕЗАВИСИМЫЙ КОНЦЕПТ 2026",
    "headline":"Family Voices.","headline_accent":"Истории, которые остаются с нами.",
    "hero":"Эмоциональная рекламная серия о памяти, голосе и подарках, объединяющих поколения. Три идеи, шесть разных композиций и двенадцать адаптаций под Meta Ads.",
    "disclosure":"Неофициальный проект для портфолио · Не заказан и не одобрен Remento",
    "metric_1":"Рекламные концепции","metric_2":"Разных дизайнов","metric_3":"Готовых изображений",
    "overview_tag":"01 / О ПРОЕКТЕ","overview_heading":"Дизайн, который передаёт чувство.",
    "overview":"Family Voices — самостоятельный демонстрационный рекламный проект студии BEQSON. Вдохновившись идеей Remento — сохранять устные истории семьи вместе с печатной книгой, — мы исследовали, как превращать эмоциональную идею в понятные премиальные статичные объявления для ленты и Stories. Remento не заказывала эти материалы; объявления не запускались в рекламных кампаниях.",
    "challenge_tag":"02 / КРЕАТИВНАЯ ЗАДАЧА","challenge_heading":"Сначала эмоция. Затем ясность продукта.",
    "challenge_1_title":"Креативная задача","challenge_1":"За несколько секунд показать невидимую ценность — возможность услышать голос близкого человека. Каждый вариант должен содержать одну сильную идею, естественную фотографию, читаемый заголовок и понятный призыв к действию.",
    "challenge_2_title":"Аудитория и инсайт","challenge_2":"Предполагаемая аудитория: взрослые дети, ищущие значимый подарок родителям, семьи, сохраняющие воспоминания бабушек и дедушек, и люди, которым важны семейные архивы. Наша творческая гипотеза: конкретные человеческие моменты работают выразительнее общей ностальгии. Это гипотеза дизайна, а не подтверждённое исследование.",
    "direction_tag":"03 / АРТ-ДИРЕКШН","direction_heading":"Тепло, фактура и сдержанность.",
    "direction":"Единая визуальная система объединяет все шесть работ: тёплая кинематографичная фотография, фактуры бумаги и льна, выразительная антиква для заголовков, современный гротеск для пояснений и палитра слоновой кости, ореха, оливкового, какао и приглушённого золота.",
    "concepts_tag":"04 / КОНЦЕПЦИИ","concepts_heading":"Три идеи. Два исполнения каждой.",
    "concepts_sub":"Для каждой идеи — своя эмоция или функция, а не простая замена цвета.",
    "voice_desc":"Голос как эмоциональный центр истории. Первый вариант показывает тёплый разговор, второй — камерный портрет дедушки, который делится воспоминаниями.",
    "gift_desc":"Книга памяти как по-настоящему личный подарок. Эмоциональный момент вручения контрастирует с премиальной предметной композицией.",
    "audio_desc":"Объяснение механики: печатная история и возможность услышать оригинальную запись. QR-графика и экран аудиоплеера — демонстрационные, нерабочие элементы.",
    "design_label":"Независимый арт-дирекшн · Формат ленты 4:5",
    "gallery_tag":"05 / ГОТОВЫЕ ОБЪЯВЛЕНИЯ","gallery_heading":"Шесть финальных макетов для ленты.",
    "gallery_sub":"Размер каждого изображения — 1080 × 1350 пикселей. Нажмите, чтобы открыть полный размер.",
    "adapt_tag":"06 / АДАПТАЦИЯ ФОРМАТОВ","adapt_heading":"Для ленты и вертикального экрана.",
    "adapt_sub":"Каждое исполнение отдельно адаптировано под 1080 × 1920 пикселей. Заголовки, CTA и важные элементы размещены с учётом типичных интерфейсных зон. Перед реальным запуском рекомендуется проверить макеты в рекламном кабинете.",
    "process_tag":"07 / РАБОЧИЙ ПРОЦЕСС","process_heading":"Повторяемый процесс производства креативов.",
    "process":[("01","Идея и сообщение","Определяем эмоциональное обещание, рекламный заголовок и CTA."),("02","Визуальный поиск","Создаём и отбираем естественные исходные изображения с поддержкой AI."),("03","Типографика и композиция","Набираем текст отдельно, настраиваем контраст и визуальную иерархию."),("04","Адаптация и проверка","Экспортируем 4:5 и 9:16, проверяем размеры, орфографию и артефакты.")],
    "tools_tag":"08 / ИНСТРУМЕНТЫ И НАВЫКИ","tools_heading":"AI в визуалах. Решения — за арт-директором.",
    "tools_intro":"Изображения созданы с помощью генерации и доведены отдельной вёрсткой. Мы демонстрируем навыки:",
    "tools":["Дизайн статичной рекламы","Арт-дирекшн","Разработка концепций","Визуальный сторителлинг","AI-графика","Типографика","Адаптация форматов","Meta Ads layouts","Композиция","Контроль качества"],
    "note":"Важное уточнение: семейные сцены и книги на изображениях созданы с помощью AI. Название Remento используется исключительно как контекст независимого демонстрационного проекта. QR и экраны плеера не функциональны. Бюджеты, CTR, ROAS, одобрение заказчика и результаты рекламных кампаний не заявляются.",
    "final_tag":"09 / ИТОГОВАЯ ГАЛЕРЕЯ","final_heading":"Двенадцать файлов. Одна история.",
    "final_text":"Шесть самостоятельных рекламных макетов, каждый в двух форматах. Материалы можно изучить в портфолио и использовать как пример нашего творческого подхода.",
    "cta_tag":"10 / СОТРУДНИЧЕСТВО","cta_heading":"Нужны статичные объявления, которые запоминаются?",
    "cta_text":"BEQSON создаёт рекламу с AI-assisted визуалами и полноценным арт-дирекшном для брендов, интернет-магазинов и сервисных компаний. Расскажите нам о продукте и задаче.",
    "cta_mail":"Обсудить рекламный проект","cta_back":"Все проекты BEQSON",
    "related":"Другие проекты BEQSON","related_links":[("Kakheti Wine House — E-commerce","kakheti-wine-house"),("BEQSON Motion Lab","motion-lab"),("AI-консультант","ai-consultant")],
    "footer":"© BEQSON Digital Studio · Независимый демонстрационный проект",
 },
 "ka":{
    "title":"Family Voices — Meta სტატიკური რეკლამის დიზაინი | BEQSON",
    "description":"Meta Ads-ის ექვსი პრემიუმ ვიზუალური კონცეფცია 4:5 და 9:16 ფორმატებში. BEQSON-ის დამოუკიდებელი სადემონსტრაციო პროექტი ოჯახურ ისტორიებზე.",
    "nav_home":"მთავარი","nav_projects":"პროექტები","nav_services":"სერვისები","nav_contact":"კონტაქტი",
    "kicker":"BEQSON CREATIVE STUDIO / დამოუკიდებელი კონცეფცია 2026",
    "headline":"Family Voices.","headline_accent":"ისტორიები, რომლებიც ჩვენთან რჩება.",
    "hero":"ემოციური სარეკლამო სერია მოგონებების, საყვარელი ხმებისა და თაობების დამაკავშირებელი საჩუქრების შესახებ. სამი იდეა, ექვსი განსხვავებული დიზაინი და თორმეტი ადაპტაცია Meta Ads-ისთვის.",
    "disclosure":"არაოფიციალური პორტფოლიოს პროექტი · Remento-ს არ შეუკვეთავს და არ დაუმტკიცებია",
    "metric_1":"კრეატიული კონცეფცია","metric_2":"განსხვავებული დიზაინი","metric_3":"საბოლოო ფაილი",
    "overview_tag":"01 / პროექტის შესახებ","overview_heading":"დიზაინი, რომელიც ემოციას გადმოსცემს.",
    "overview":"Family Voices არის BEQSON Digital Studio-ს დამოუკიდებელი სადემონსტრაციო პროექტი. Remento-ს იდეით შთაგონებულებმა — ოჯახის ზეპირი ისტორიების შენარჩუნება ბეჭდურ წიგნთან ერთად — შევისწავლეთ, როგორ შეიძლება ემოციური გზავნილის გადატანა პრემიუმ სტატიკურ რეკლამაში. Remento ჩვენი დამკვეთი არ ყოფილა და ეს ნამუშევრები რეალურ კამპანიებში არ გამოყენებულა.",
    "challenge_tag":"02 / კრეატიული ამოცანა","challenge_heading":"ჯერ ემოცია, შემდეგ პროდუქტის სიცხადე.",
    "challenge_1_title":"კრეატიული ამოცანა","challenge_1":"რამდენიმე წამში უნდა გადმოგვეცა უხილავი ღირებულება — ახლობლის ხმის ხელახლა მოსმენის შესაძლებლობა. თითოეულ დიზაინს სჭირდებოდა ერთი ძლიერი იდეა, ბუნებრივი ფოტო, მკაფიო სათაური და მოქმედებისკენ მოწოდება.",
    "challenge_2_title":"აუდიტორია და ინსაიტი","challenge_2":"სავარაუდო აუდიტორია: ზრდასრული შვილები, რომლებიც მშობლებისთვის მნიშვნელოვან საჩუქარს ეძებენ; ოჯახები, რომლებიც ბებია-ბაბუის მოგონებებს ინახავენ; ადამიანები, ვისთვისაც ოჯახური არქივები მნიშვნელოვანია. ჩვენი კრეატიული ჰიპოთეზაა, რომ რეალური ადამიანური მომენტები ზოგად ნოსტალგიაზე ძლიერია. ეს არ არის დადასტურებული კვლევა.",
    "direction_tag":"03 / ვიზუალური მიმართულება","direction_heading":"სითბო, ფაქტურა და თავშეკავებულობა.",
    "direction":"ექვსივე ნამუშევარს აერთიანებს თბილი კინემატოგრაფიული ფოტოგრაფია, ქაღალდისა და სელის ფაქტურა, ელეგანტური სერიფული სათაურები, თანამედროვე დამატებითი ტექსტი და ბუნებრივი პალიტრა: სპილოსძვლისფერი, კაკლისფერი, ზეთისხილისფერი და ჩამქრალი ოქროსფერი.",
    "concepts_tag":"04 / სარეკლამო კონცეფციები","concepts_heading":"სამი იდეა. ორი შესრულება თითოეულისთვის.",
    "concepts_sub":"ყველა მიმართულებას საკუთარი ემოციური ან ფუნქციური აქცენტი აქვს — ეს მხოლოდ ფერის შეცვლა არ არის.",
    "voice_desc":"ხმა, როგორც მოგონების ემოციური ცენტრი. ერთი ვარიანტი ოჯახურ საუბარს აჩვენებს, მეორე — ბაბუის ინტიმურ პორტრეტს.",
    "gift_desc":"მოგონებების წიგნი, როგორც ღრმა პირადი საჩუქარი. ერთი დიზაინი ჩუქების მომენტზეა, მეორე — პრემიუმ პროდუქტის ფოტოკომპოზიციაზე.",
    "audio_desc":"პროდუქტის იდეის ვიზუალური ახსნა: დაბეჭდილი ისტორია და ორიგინალური ხმის მოსმენა. QR და აუდიოპლეერის ეკრანი მხოლოდ საილუსტრაციო, არაფუნქციური ელემენტებია.",
    "design_label":"დამოუკიდებელი არტ-დირექშენი · 4:5 ფორმატი",
    "gallery_tag":"05 / საბოლოო რეკლამები","gallery_heading":"ექვსი დასრულებული ვიზუალი ლენტისთვის.",
    "gallery_sub":"თითოეული მაკეტის ზომაა 1080 × 1350 პიქსელი. დააჭირეთ სრული ზომით სანახავად.",
    "adapt_tag":"06 / ფორმატების ადაპტაცია","adapt_heading":"ლენტისთვის და ვერტიკალური ეკრანისთვის.",
    "adapt_sub":"თითოეული დიზაინი ცალკე მომზადდა 1080 × 1920 ფორმატში. მთავარი სათაურები და CTA გათვლილია გავრცელებულ ინტერფეისის ზონებზე. რეალურ გაშვებამდე საჭიროა სარეკლამო პლატფორმაში გადამოწმება.",
    "process_tag":"07 / სამუშაო პროცესი","process_heading":"გამეორებადი კრეატიული წარმოების პროცესი.",
    "process":[("01","იდეა და გზავნილი","ვადგენთ ემოციურ დაპირებას, სათაურსა და CTA-ს."),("02","ვიზუალური კვლევა","AI-ის დახმარებით ვქმნით და ვარჩევთ ბუნებრივ ფოტოებს."),("03","ტიპოგრაფია და კომპოზიცია","ტექსტს ცალკე ვაწყობთ, ვაუმჯობესებთ კონტრასტსა და იერარქიას."),("04","ადაპტაცია და შემოწმება","ვამზადებთ 4:5 და 9:16 ფაილებს; ვამოწმებთ ზომებს, ტექსტსა და დეტალებს.")],
    "tools_tag":"08 / ინსტრუმენტები და უნარები","tools_heading":"AI ვიზუალებში. გადაწყვეტილებები — არტ-დირექციაში.",
    "tools_intro":"საწყისი ფოტოები შექმნილია გენერაციული მეთოდით, ხოლო ტექსტი და კომპოზიცია დამუშავებულია ცალკე. ნაჩვენებია უნარები:",
    "tools":["სტატიკური რეკლამის დიზაინი","არტ-დირექშენი","კონცეფციის განვითარება","ვიზუალური თხრობა","AI გამოსახულებები","ტიპოგრაფია","ფორმატების ადაპტაცია","Meta Ads layouts","კომპოზიცია","ხარისხის კონტროლი"],
    "note":"განმარტება: ოჯახური სცენები და წიგნები AI-ით შექმნილი ილუსტრაციებია. Remento მოხსენიებულია მხოლოდ დამოუკიდებელი პორტფოლიოს კონცეფციის კონტექსტში. QR და აუდიოპლეერის ეკრანები არაფუნქციურია. არ არსებობს რეკლამის ბიუჯეტის, CTR-ის, ROAS-ის, დამკვეთის დამტკიცების ან კამპანიის შედეგების პრეტენზია.",
    "final_tag":"09 / საბოლოო გალერეა","final_heading":"თორმეტი ფაილი. ერთი საერთო ისტორია.",
    "final_text":"ექვსი სარეკლამო დიზაინი ორ-ორ ფორმატში. ეს მასალები ასახავს BEQSON-ის კრეატიულ მიდგომას.",
    "cta_tag":"10 / თანამშრომლობა","cta_heading":"გჭირდებათ სტატიკური რეკლამა, რომელიც ემახსოვრებათ?",
    "cta_text":"BEQSON ქმნის AI-ის დახმარებით შემუშავებულ, არტ-დირექციით დამუშავებულ სარეკლამო ვიზუალებს ბრენდების, ონლაინმაღაზიებისა და მომსახურების ბიზნესებისთვის. მოგვიყევით თქვენი პროდუქტისა და ამოცანის შესახებ.",
    "cta_mail":"რეკლამის პროექტის განხილვა","cta_back":"BEQSON-ის ყველა პროექტი",
    "related":"BEQSON-ის სხვა პროექტები","related_links":[("Kakheti Wine House — E-commerce","kakheti-wine-house"),("BEQSON Motion Lab","motion-lab"),("AI კონსულტანტი","ai-consultant")],
    "footer":"© BEQSON Digital Studio · დამოუკიდებელი სადემონსტრაციო პროექტი",
 },
}


def e(s): return escape(str(s), quote=True)


def ad_img(name, aspect, alt, eager=False):
    width, height = (1080, 1350) if aspect == "4x5" else (1080, 1920)
    path = f"{ASSET}{name}_{aspect}.webp"
    return (f'<a href="{path}" target="_blank" rel="noopener" aria-label="{e(alt)}">'
            f'<img src="{path}" width="{width}" height="{height}" alt="{e(alt)}"'
            f' loading="{"eager" if eager else "lazy"}" decoding="async"></a>')


def header(lang, c):
    return f'''<header class="site-header"><div class="shell header-inner">
      <a class="brand" href="/{lang}/"><img src="/assets/beqson-mark-v3.png" width="42" height="42" alt=""><span><b>BEQSON</b><small>DIGITAL STUDIO</small></span></a>
      <nav class="main-nav" aria-label="Navigation"><a href="/{lang}/">{e(c['nav_home'])}</a><a href="/{lang}/projects/">{e(c['nav_projects'])}</a><a href="/{lang}/#services">{e(c['nav_services'])}</a></nav>
      <div class="header-tools"><div class="languages"><a href="/en/{SLUG}/" hreflang="en">EN</a><a href="/ka/{SLUG}/" hreflang="ka">KA</a><a href="/ru/{SLUG}/" hreflang="ru">RU</a></div><a class="button primary" href="mailto:digitalstudiobeqson@gmail.com?subject=Meta%20Static%20Ads%20Design">{e(c['nav_contact'])}</a></div>
    </div></header>'''


def sec_header(c, tag, heading, sub=""):
    return (f'<div class="meta-section-heading"><div><div class="meta-kicker">{e(c[tag])}</div>'
            f'<h2>{e(c[heading])}</h2></div>{f"<p>{e(c[sub])}</p>" if sub else ""}</div>')


def card_gallery(c, lang):
    intro = sec_header(c, "concepts_tag", "concepts_heading", "concepts_sub")
    desc_keys = ["voice_desc", "gift_desc", "audio_desc"]
    parts = []
    for i, concept in enumerate(CONCEPTS):
        figures=[]
        for name, label in concept['designs']:
            alt=f"{concept['title']} — {label}, independent BEQSON spec ad"
            figures.append(f'<figure>{ad_img(name,"4x5",alt)}<figcaption>{e(label)} · 4:5</figcaption></figure>')
        parts.append(f'''<article class="meta-concept"><div class="meta-concept-copy"><span class="meta-concept-no">CONCEPT 0{i+1}</span>
         <h3>{e(concept['title'])}</h3><p>{e(c[desc_keys[i]])}</p><span class="meta-concept-caption">{e(c['design_label'])}</span></div>
         <div class="meta-pair">{''.join(figures)}</div></article>''')
    return intro+''.join(parts)


def ad_gallery(aspect):
    cards=[]
    for concept in CONCEPTS:
        for filename,label in concept["designs"]:
            alt=f"{concept['title']} – {label} – {aspect} BEQSON independent ad spec"
            size="1080 × 1350" if aspect == "4x5" else "1080 × 1920"
            cards.append(f'<div class="meta-ad"><figure>{ad_img(filename,aspect,alt)}<figcaption><span>{e(label)}</span><small>{size}</small></figcaption></figure></div>')
    return ''.join(cards)


def page(lang):
    c=COPY[lang]
    canonical=f"{BASE}/{lang}/{SLUG}/"
    og=f"{BASE}{ASSET}family-voices-og.jpg"
    structured={"@context":"https://schema.org","@type":"CreativeWork","name":"Family Voices — Meta Static Ads Spec Campaign",
        "description":c["description"],"url":canonical,"inLanguage":lang,"dateCreated":"2026-10-26",
        "author":{"@type":"Organization","name":"BEQSON Digital Studio","url":BASE},
        "image":[f"{BASE}{ASSET}family-voices-cover.jpg"],"isBasedOn":{"@type":"WebPage","name":"Remento product idea","url":"https://www.remento.co/"}}
    hreflang=''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}/{l}/{SLUG}/">' for l in ('en','ka','ru'))
    hreflang+=f'<link rel="alternate" hreflang="x-default" href="{BASE}/en/{SLUG}/">'
    process=''.join(f'<div><b>{e(n)}</b><h3>{e(title)}</h3><p>{e(detail)}</p></div>' for n,title,detail in c['process'])
    tags=''.join(f'<li>{e(x)}</li>' for x in c['tools'])
    related=''.join(f'<a href="/{lang}/{slug}/">{e(name)} ↗</a>' for name,slug in c['related_links'])
    h=f'''<!doctype html><html lang="{lang}"><head>
      <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
      <title>{e(c['title'])}</title><meta name="description" content="{e(c['description'])}"><meta name="robots" content="index,follow,max-image-preview:large">
      <meta name="theme-color" content="#06172f"><link rel="canonical" href="{canonical}">{hreflang}
      <meta property="og:type" content="article"><meta property="og:site_name" content="BEQSON Digital Studio"><meta property="og:title" content="{e(c['title'])}">
      <meta property="og:description" content="{e(c['description'])}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{og}">
      <meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
      <link rel="icon" href="/assets/favicon-v3.png?v=3" type="image/png"><link rel="stylesheet" href="/styles.css?v=12-clutch-trust"><link rel="stylesheet" href="/assets/meta-portfolio.css?v=1">
      <script type="application/ld+json">{json.dumps(structured,ensure_ascii=False,separators=(',',':'))}</script></head>
      <body class="meta-case-page" id="top">{header(lang,c)}<main id="main">
      <section class="meta-hero"><div class="meta-shell"><span class="meta-status">{e(c['disclosure'])}</span>
      <div class="meta-kicker" style="margin-top:28px">{e(c['kicker'])}</div><h1>{e(c['headline'])}<em>{e(c['headline_accent'])}</em></h1><p class="meta-lead">{e(c['hero'])}</p>
      <a class="meta-hero-visual" href="{ASSET}family-voices-cover.jpg" target="_blank" rel="noopener"><img src="{ASSET}family-voices-cover.jpg" alt="BEQSON Family Voices independent spec campaign cover" width="1600" height="900" fetchpriority="high"></a>
      <div class="meta-proof-row"><div><b>03</b><span>{e(c['metric_1'])}</span></div><div><b>06</b><span>{e(c['metric_2'])}</span></div><div><b>12</b><span>{e(c['metric_3'])}</span></div></div></div></section>
      <section class="meta-section" id="overview"><div class="meta-shell">{sec_header(c,'overview_tag','overview_heading')}<p class="meta-text">{e(c['overview'])}</p></div></section>
      <section class="meta-section" id="challenge"><div class="meta-shell">{sec_header(c,'challenge_tag','challenge_heading')}<div class="meta-insight-grid"><div class="meta-insight-card"><span class="meta-kicker">CHALLENGE</span><h3>{e(c['challenge_1_title'])}</h3><p>{e(c['challenge_1'])}</p></div><div class="meta-insight-card"><span class="meta-kicker">INSIGHT</span><h3>{e(c['challenge_2_title'])}</h3><p>{e(c['challenge_2'])}</p></div></div></div></section>
      <section class="meta-section" id="direction"><div class="meta-shell">{sec_header(c,'direction_tag','direction_heading')}<p class="meta-text">{e(c['direction'])}</p></div></section>
      <section class="meta-section" id="concepts"><div class="meta-shell">{card_gallery(c,lang)}</div></section>
      <section class="meta-section" id="feed"><div class="meta-shell">{sec_header(c,'gallery_tag','gallery_heading','gallery_sub')}<div class="meta-gallery">{ad_gallery('4x5')}</div></div></section>
      <section class="meta-section" id="stories"><div class="meta-shell">{sec_header(c,'adapt_tag','adapt_heading','adapt_sub')}<div class="meta-story-grid">{ad_gallery('9x16')}</div></div></section>
      <section class="meta-section" id="workflow"><div class="meta-shell">{sec_header(c,'process_tag','process_heading')}<div class="meta-process">{process}</div></div></section>
      <section class="meta-section" id="skills"><div class="meta-shell">{sec_header(c,'tools_tag','tools_heading')}<p class="meta-text">{e(c['tools_intro'])}</p><ul class="meta-tags">{tags}</ul><p class="meta-note" style="margin-top:30px">{e(c['note'])}</p></div></section>
      <section class="meta-section" id="final-gallery"><div class="meta-shell">{sec_header(c,'final_tag','final_heading')}<p class="meta-text">{e(c['final_text'])}</p></div></section>
      <section class="meta-section" id="contact"><div class="meta-shell"><div class="meta-contact"><span class="meta-kicker">{e(c['cta_tag'])}</span><h2>{e(c['cta_heading'])}</h2><p>{e(c['cta_text'])}</p><div class="meta-actions">
      <a class="meta-action primary" href="mailto:digitalstudiobeqson@gmail.com?subject=Meta%20Static%20Ad%20Creative%20Design">{e(c['cta_mail'])} ↗</a>
      <a class="meta-action" href="/{lang}/projects/">{e(c['cta_back'])} ↗</a></div>
      <div class="meta-kicker" style="margin-top:48px">{e(c['related'])}</div><div class="meta-related">{related}</div>
      </div></div></section></main><footer class="meta-footer"><div class="meta-shell"><span>{e(c['footer'])}</span><a href="https://beqson.com/">beqson.com</a><a href="mailto:digitalstudiobeqson@gmail.com">digitalstudiobeqson@gmail.com</a></div></footer>
      </body></html>'''
    target=ROOT/lang/SLUG
    target.mkdir(parents=True,exist_ok=True)
    (target/"index.html").write_text(h,encoding="utf-8")
    print(f"Built {target.relative_to(ROOT)}/index.html ({len(h)} chars)")


if __name__=="__main__":
    for language in ("en","ru","ka"):
        page(language)
