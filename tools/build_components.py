"""Shared page sections with localized editorial data.

JSON values containing markup are trusted, repository-owned HTML fragments
(e.g. <br>, <strong>, &amp;), not user input. Layout is defined only here.
"""
import json
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
HOME = json.loads((TOOLS / 'home_sections.json').read_text(encoding='utf-8'))
INDUSTRY = json.loads((TOOLS / 'industry_sections.json').read_text(encoding='utf-8'))
LEAD_STYLE = '<link rel="stylesheet" href="/assets/lead-system.css?v=1">'
LEAD_SCRIPT = '<script src="/assets/lead-system.js?v=2" defer></script>'


def home_promos(lang):
    return ''.join(
        f'<section class="audit-home-strip{" calculator-home-strip" if c["calculator"] else ""}"><div class="shell"><div class="audit-home-card"><div><span class="audit-home-kicker">{c["kicker"]}</span><h2>{c["heading"]}</h2><p>{c["text"]}</p></div><a class="audit-home-btn" href="{c["href"]}">{c["label"]}</a></div></div></section>'
        for c in HOME[lang]['promos'])


def home_industries(lang, base):
    d = HOME[lang]['industries']
    cards = ''.join(
        f'<a class="legacy-niche" href="{base}{lang}/{c["slug"]}/"><img alt="{c["alt"]}" loading="lazy" decoding="async" src="{base}assets/images/{c["image"]}"><div><h3>{c["heading"]}</h3><p>{c["text"]}</p></div></a>'
        for c in d['cards'])
    return f'<section class="legacy-industries" id="services"><div class="legacy-industries-inner"><div class="legacy-section-head"><span class="legacy-kicker">{d["kicker"]}</span><h2>{d["heading"]}</h2><p>{d["text"]}</p></div><div class="legacy-niche-grid">{cards}</div></div></section>'


def home_projects(lang):
    d = HOME[lang]['projects']
    cards = ''.join(
        f'<a class="home-project-card" href="{c["href"]}"><span>{c["tag"]}</span><strong>{c["heading"]}</strong><small>{c["text"]}</small></a>'
        for c in d['cards'])
    a = d['cta']
    return f'<section class="home-projects-strip"><div class="shell"><div class="home-projects-head"><div><p class="eyebrow">PORTFOLIO</p><h2>{d["heading"]}</h2></div><p>{d["text"]}</p></div><div class="home-projects-grid">{cards}</div><a class="{a["class"]}" href="{a["href"]}">{a["label"]}</a></div></section>'


def home_trust(lang):
    d = HOME[lang]['clutch']
    return f'<section class="clutch-trust-strip" aria-label="{d["label"]}"><div class="shell"><a class="clutch-trust-card" href="https://clutch.co/profile/beqson-digital-studio" target="_blank" rel="noopener noreferrer" aria-label="{d["linkLabel"]}"><div class="clutch-trust-copy"><span class="clutch-trust-kicker">{d["kicker"]}</span><strong>{d["heading"]}</strong><span>{d["text"]}</span></div><span class="clutch-wordmark" aria-hidden="true">Clutch<span class="clutch-dot">•</span></span><span class="clutch-arrow" aria-hidden="true">{d["cta"]}</span></a></div></section>'


def feature_section(d):
    cards = []
    for c in d['cards']:
        number = f'<span class="feature-number">{c["number"]}</span>' if 'number' in c else ''
        link = f'<a class="text-link" href="{c["link"]["href"]}">{c["link"]["label"]}</a>' if 'link' in c else ''
        if 'icon' in c:
            number += f'<span class="icon-tile small"><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#{c["icon"]}"></use></svg></span>'
        cards.append(f'<article class="feature-card">{number}<h3>{c["heading"]}</h3><p>{c["text"]}</p>{link}</article>')
    intro = f'<p>{d["intro"]}</p>' if d['intro'] is not None else ''
    actions = ''
    if 'actions' in d:
        links = ''.join(f'<a class="{a["class"]}" href="{a["href"]}">{a["label"]}</a>' for a in d['actions'])
        actions = f'<div class="actions" style="margin-top:28px">{links}</div>'
    return f'<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">{d["kicker"]}</p><h2>{d["heading"]}</h2></div>{intro}</div><div class="features-grid">{"".join(cards)}</div>{actions}</div></section>'


def path_section(d):
    link = ''
    if 'link' in d:
        a = d['link']
        attrs = ' target="_blank" rel="noopener"' if a['external'] else ''
        link = f'<a class="{a.get("class", "text-link")}" href="{a["href"]}"{attrs}>{a["label"]}</a>'
    arrow = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/icons.svg#arrow-up"></use></svg>' if d.get('channelArrows') else ''
    channels = ''.join(f'<li><span>{i:02}</span><p>{text}</p>{arrow}</li>' for i, text in enumerate(d['channels'], 1))
    return f'<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">{d["kicker"]}</p><h2>{d["heading"]}</h2><p class="lead">{d["intro"]}</p>{link}</div><ol class="channel-list">{channels}</ol></div></section>'


def has_generic_sections(slug):
    return not INDUSTRY.get(slug, {}).get('replaceGeneric', False)


def industry_details(lang, slug, placement):
    config = INDUSTRY.get(slug)
    if not config or config['placement'] != placement:
        return ''
    sections = [path_section(d) if d['kind'] == 'path' else feature_section(d) for d in config[lang]]
    body = '\n'.join(sections)
    marker = config['marker']
    return (f'<!-- {marker} -->\n{body}\n<!-- /{marker} -->' if marker else body) + '\n'
