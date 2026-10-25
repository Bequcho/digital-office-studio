#!/usr/bin/env python3
"""Add Family Voices case to existing hand-curated home/project galleries.

These pages are intentionally updated in place with single-anchor edits, to
preserve their existing SEO markup, integrations, and unrelated sections.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "/assets/meta-ads/family-voices-cover.jpg"

COPY = {
    "en":{
        "badge":"Independent spec","name":"Family Voices — Emotional Meta Static Ads",
        "desc":"Six distinct, premium editorial ad designs for a family storytelling concept, with twelve 4:5 and 9:16 exports. Unofficial work, not commissioned by Remento.",
        "cta":"Explore the case","all_old":"Explore all 16 projects","all_new":"Explore all 17 projects",
        "list_title":"Family Voices — Meta Static Ads Design (Independent Spec)",
        "list_desc":"Three emotional messaging concepts, six original static ads and adaptations for feed and vertical Meta placements. An independent BEQSON exploration, not a Remento client project.",
        "list_cta":"View full case",
    },
    "ru":{
        "badge":"Независимый концепт","name":"Family Voices — эмоциональная реклама Meta Ads",
        "desc":"Шесть оригинальных рекламных макетов о семейных воспоминаниях и двенадцать экспортов 4:5 и 9:16. Неофициальная работа, не заказанная Remento.",
        "cta":"Смотреть кейс","all_old":"Все 16 проектов","all_new":"Все 17 проектов",
        "list_title":"Family Voices — дизайн статичной рекламы Meta (концепт)",
        "list_desc":"Три эмоциональные рекламные идеи, шесть оригинальных креативов и адаптации для ленты и вертикального формата. Самостоятельный проект BEQSON, а не заказ Remento.",
        "list_cta":"Открыть кейс",
    },
    "ka":{
        "badge":"დამოუკიდებელი კონცეფცია","name":"Family Voices — ემოციური Meta Ads დიზაინი",
        "desc":"ექვსი ორიგინალური რეკლამა ოჯახურ მოგონებებზე და თორმეტი 4:5 / 9:16 ფაილი. არაოფიციალური ნამუშევარი, რომელიც Remento-ს არ შეუკვეთავს.",
        "cta":"კეისის ნახვა","all_old":"ყველა 16 პროექტის ნახვა","all_new":"ყველა 17 პროექტის ნახვა",
        "list_title":"Family Voices — Meta სტატიკური რეკლამის დიზაინი (კონცეფცია)",
        "list_desc":"სამი ემოციური იდეა, ექვსი ორიგინალური დიზაინი და ადაპტაციები Meta-ის ლენტისა და ვერტიკალური ფორმატებისთვის. BEQSON-ის დამოუკიდებელი პროექტი, არა Remento-ს შეკვეთა.",
        "list_cta":"სრული კეისის ნახვა",
    }
}


def update_once(path, target, replacement):
    body = path.read_text(encoding="utf-8")
    if body.count(target)!=1:
        raise RuntimeError(f"Expected one exact anchor, found {body.count(target)}: {path}")
    path.write_text(body.replace(target,replacement,1),encoding="utf-8")


for lang,c in COPY.items():
    case=f"/{lang}/meta-static-ads/"
    home=ROOT/lang/"index.html"
    raw=home.read_text(encoding="utf-8")
    if case in raw: raise RuntimeError(f"Already inserted: {home}")
    card=f'''<a class="beqson-work-card beqson-work-card--featured" href="{case}"><span class="beqson-work-art"><img src="{IMAGE}" alt="BEQSON Family Voices — Meta static ad portfolio cover" width="1600" height="900" loading="lazy" decoding="async"></span><span class="beqson-work-copy"><span class="beqson-work-meta"><span class="beqson-work-badge">{escape(c['badge'])}</span><span class="beqson-work-cat">META ADS / DESIGN</span></span><strong class="beqson-work-name">{escape(c['name'])}</strong><span class="beqson-work-desc">{escape(c['desc'])}</span><span class="beqson-work-cta">{escape(c['cta'])} <span aria-hidden="true">↗</span></span></span></a>'''
    anchor=f'<a class="beqson-work-card" href="/{lang}/commerce-motion/">'
    update_once(home,anchor,card+anchor)
    update_once(home,c["all_old"],c["all_new"])
    print("Home card registered:",home.relative_to(ROOT))

    listing=ROOT/lang/"projects/index.html"
    raw=listing.read_text(encoding="utf-8")
    if case in raw: raise RuntimeError(f"Already inserted: {listing}")
    project=f'''<article class="project-card" id="family-voices" data-project-cat="design"><div class="project-visual"><img src="{IMAGE}" alt="Family Voices — six Meta static advertising concepts by BEQSON" width="1600" height="900" loading="lazy" decoding="async"></div><div class="project-body"><div class="project-topline"><span class="project-badge">{escape(c['badge'])}</span><span class="project-cat">META ADS / DESIGN</span></div><h2>{escape(c['list_title'])}</h2><p>{escape(c['list_desc'])}</p><ul class="project-tags"><li>Static Ads</li><li>Creative Direction</li><li>4:5 &amp; 9:16</li><li>AI-Assisted Design</li></ul><a class="project-link" href="{case}">{escape(c['list_cta'])} ↗</a></div></article>'''
    update_once(listing,'<div class="projects-grid">','<div class="projects-grid">'+project)
    print("Project catalogue registered:",listing.relative_to(ROOT))
