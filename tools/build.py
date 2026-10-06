#!/usr/bin/env python3
"""Rebuild all static BEQSON pages. Python 3, standard library only."""
from pathlib import Path
import json, html, itertools
from urllib.parse import quote, urlsplit
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parent.parent
CONTENT = json.loads((ROOT/'tools/content.json').read_text())
INDUSTRIES = json.loads((ROOT/'tools/industries.json').read_text())
BASE_URL = 'https://bequcho.github.io/digital-office-studio/'
EMAIL='digitalstudiobeqson@gmail.com'
PHONE='995551739333'
LANGS=('ru','ka','en')

def esc(value): return html.escape(str(value), quote=True)
def lines(value): return esc(value).replace('\n','<br>')
PATHS={
 'arrow':'<path d="M4 12h15m-6-6 6 6-6 6"/>',
 'arrow-up':'<path d="M6 18 18 6M6 6h12v12"/>',
 'check':'<path d="m5 12 4 4L19 6"/>',
 'close':'<path d="m6 6 12 12M6 18 18 6"/>',
 'menu':'<path d="M4 7h16M4 12h16M4 17h16"/>',
 'plus':'<path d="M12 5v14M5 12h14"/>',
 'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18Z"/>',
 'pin':'<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 0 1 14 0Z"/><circle cx="12" cy="10" r="2.4"/>',
 'layers':'<path d="m12 3 10 5-10 5L2 8l10-5Zm-10 9 10 5 10-5M2 16l10 5 10-5"/>',
 'trend':'<path d="M4 19V5m0 14h17M7 14l4-4 4 2 6-7M16 5h5v5"/>',
 'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
 'plan':'<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M4 9h16M9 9v11M7 6.5h.01M10 6.5h.01"/>',
 'message':'<path d="M20 14a4 4 0 0 1-4 4H9l-5 3V7a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v7Z"/><path d="M8 8h8m-8 5h5"/>',
 'megaphone':'<path d="m4 9 7-2 9-4v17l-9-4-7-2V9Zm3 6 2 6h4l-2-5M11 7v9"/>',
 'chart':'<path d="M3 21h19M6 17v-5m6 5V7m6 10V3"/>',
 'scales':'<path d="M12 3v18m-6 0h12M4 7h16M6 7l-4 7h8L6 7Zm12 0-4 7h8l-4-7Z"/>',
 'tooth':'<path d="M12 5C8 1 3 3 4 8c1 4 2 5 2 9 0 6 3 5 4 0 .8-4 3.2-4 4 0 1 5 4 6 4 0 0-4 1-5 2-9 1-5-4-7-8-3Z"/><path d="m9 4 4 3"/>',
 'heart':'<path d="M20 4c-3-3-6-1-8 2-2-3-5-5-8-2-5 5 2 11 8 16 6-5 13-11 8-16Z"/><path d="M7 11h3l2-3 2 6 2-3h2"/>',
 'home':'<path d="m3 10 9-7 9 7M5 9v12h14V9M10 21v-7h4v7"/>',
 'calculator':'<rect x="5" y="2" width="14" height="20" rx="3"/><path d="M8 6h8M8 11h1m6 0h1M8 15h1m6 0h1M8 19h1m6 0h1"/>',
 'ruler':'<path d="m16 3 5 5L8 21l-5-5L16 3Zm-3 3 3 3m-6 0 2 2m-5 1 3 3m-6 0 2 2"/>',
 'car':'<path d="m4 9 3-6h10l3 6M3 9h18v10H3V9Zm2 10v2m14-2v2M6 13h2m8 0h2M9 16h6"/>',
 'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
 'rocket':'<path d="M9 15c-2-7 5-12 12-12 0 7-5 14-12 12Zm0 0-3 3M8 8H4l-2 5 6 1m2 2 1 6 5-2v-4M5 16l-3 6 6-3"/><circle cx="16" cy="8" r="2"/>',
 'crown':'<path d="m3 6 5 5 4-7 4 7 5-5-3 13H6L3 6Zm3 10h12"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 6 9 7 9-7"/>',
 'telegram':'<path d="M22 3 18 21l-7-6-4 4 1-7L2 9l20-6ZM8 12 18 6l-7 9"/>',
 'whatsapp':'<path d="m3 21 1.5-5A9 9 0 1 1 8 20L3 21Z"/><path d="m8 7 2 3-1 1c1 2 2 3 4 4l1-1 3 1c-1 4-5 2-8-1-3-3-4-5-1-7Z"/>',
 'sparkle':'<path d="m12 2 3 7 7 3-7 3-3 7-3-7-7-3 7-3 3-7Z"/>',
 'zoom':'<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6M7 10h6m-3-3v6"/>'}

def icon(name,cls=''):
 sprite=urlsplit(BASE_URL).path+'assets/icons.svg'
 return f'<svg class="icon {cls}" viewBox="0 0 24 24" aria-hidden="true"><use href="{sprite}#{name}"></use></svg>'
def tile(name,tone='',small=False):
 return f'<span class="icon-tile {tone} {"small" if small else ""}">{icon(name)}</span>'
def flag(lang):
 shapes={
 'ru':'<path fill="#fff" d="M0 0h30v20H0z"/><path fill="#2456bc" d="M0 7h30v7H0z"/><path fill="#db3946" d="M0 14h30v6H0z"/>',
 'ka':'<path fill="#fff" d="M0 0h30v20H0z"/><path stroke="#d82d3a" stroke-width="3.5" d="M15 0v20M0 10h30"/><path stroke="#d82d3a" stroke-width="1.6" d="M6 2v5M3.5 4.5h5m-2.5 8v5M3.5 15h5M24 2v5m-2.5-2.5h5M24 12.5v5M21.5 15h5"/>',
 'en':'<path fill="#20346b" d="M0 0h30v20H0z"/><path stroke="#fff" stroke-width="5" d="m0 0 30 20M30 0 0 20"/><path stroke="#d82d3a" stroke-width="2" d="m0 0 30 20M30 0 0 20"/><path stroke="#fff" stroke-width="7" d="M15 0v20M0 10h30"/><path stroke="#d82d3a" stroke-width="4" d="M15 0v20M0 10h30"/>'}
 return f'<svg viewBox="0 0 30 20" aria-hidden="true">{shapes[lang]}</svg>'
def contacts(lang,industry=None):
 c=CONTENT[lang];message=c['waText']+((' '+c['industryMessage']+': '+industry[lang]['name']+'.') if industry else '')
 return [('whatsapp','WhatsApp','+995 551 73 93 33','https://wa.me/'+PHONE+'?text='+quote(message)),('telegram','Telegram','@digital_studio_beqson','https://t.me/digital_studio_beqson'),('mail','Email',EMAIL,'mailto:'+EMAIL+'?subject='+quote(c['mailSubject'])+'&body='+quote(message))]
def link_attrs(url):return ' target="_blank" rel="noopener noreferrer"' if url.startswith('https:') else ''
def header(lang,base,slug=None,force_home=False):
 c=CONTENT[lang];home=f'{base}{lang}/';flags='';nav=''
 for l in LANGS:
  href=f'{base}{l}/'+(slug+'/' if slug else '')
  flags+=f'<a class="flag-link {"active" if l==lang else ""}" href="{href}" lang="{l}" hreflang="{l}" aria-label="{CONTENT[l]["name"]}" title="{CONTENT[l]["name"]}"'+(' aria-current="page"' if l==lang else '')+f'>{flag(l)}</a>'
 for label,anchor in zip(c['nav'],('services','growth','pricing','case')):
  nav+=f'<a href="{home if (slug or force_home) else ""}#{anchor}">{label}</a>'
 socials=''.join(f'<a class="social {kind}" href="{esc(url)}" aria-label="{name}" title="{name}"{link_attrs(url)}>{icon(kind)}</a>' for kind,name,text,url in contacts(lang))
 return f'''<a class="skip" href="#main">{c['skip']}</a>
<header class="site-header"><div class="shell header-inner">
<a class="brand" href="{home}"><img src="{base}assets/logo.svg" width="42" height="42" alt=""><span><b>BEQSON</b><small>DIGITAL STUDIO</small></span></a>
<nav class="main-nav" id="main-nav" aria-label="{c['menu']}">{nav}<div class="mobile-contacts">{socials}</div></nav>
<div class="header-tools"><div class="languages" aria-label="Language">{flags}</div><div class="consult-group"><a class="consult-label" href="#contact">{c['consult']}</a><div class="socials">{socials}</div></div><button class="menu-toggle" type="button" aria-label="{c['menu']}" data-open-label="{c['menu']}" data-close-label="{c['close']}" aria-controls="main-nav" aria-expanded="false">{icon('menu')}</button></div>
</div></header>'''
def footer(lang,base):
 c=CONTENT[lang]
 return f'''<footer class="site-footer"><div class="shell footer-inner"><a class="footer-brand" href="{base}{lang}/">BEQSON<span>© 2026 Digital Studio</span></a><p>{c['footer']}</p><a class="text-link" href="#top">{c['backTop']} {icon('arrow-up')}</a></div></footer>'''
def contact_section(lang,industry=None):
 c=CONTENT[lang];links=''
 for kind,name,value,url in contacts(lang,industry):
  links+=f'<a class="contact-link" href="{esc(url)}"{link_attrs(url)}>{tile(kind,small=True)}<span><b>{name}</b><small>{value}</small></span>{icon("arrow-up")}</a>'
 return f'''<section class="contact-section section" id="contact"><div class="shell contact-grid"><div><p class="eyebrow">{c['contactKicker']}</p><h2>{lines(c['contactTitle'])}</h2><p class="lead">{c['contactText']}</p></div><div class="contact-options"><p>{c['contactPrompt']}</p>{links}</div></div></section>'''
def head(lang,base,title,description,slug=None,noindex=False):
 c=CONTENT[lang];canonical=BASE_URL+('404.html' if noindex else lang+'/'+(slug+'/' if slug else ''));image=BASE_URL+'assets/'+(f'concepts/{lang}/{slug}-og.jpg' if slug else 'og-cover.png')
 alternates='' if noindex else ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE_URL}{l}/{slug+"/" if slug else ""}">' for l in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}ru/{slug+"/" if slug else ""}">'
 org={'@type':'Organization','@id':BASE_URL+'#organization','name':'BEQSON Digital Studio','url':BASE_URL,'logo':BASE_URL+'assets/logo.svg','email':EMAIL,'telephone':'+'+PHONE,'sameAs':['https://t.me/digital_studio_beqson']}
 graph=[org,{'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'inLanguage':lang,'publisher':{'@id':BASE_URL+'#organization'}}]
 if slug:
  n=next(n for n in INDUSTRIES if n['slug']==slug)
  graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':c['home'],'item':BASE_URL+lang+'/'},{'@type':'ListItem','position':2,'name':n[lang]['name'],'item':canonical}]})
  graph.append({'@type':'Service','name':title,'description':description,'provider':{'@id':BASE_URL+'#organization'},'url':canonical,'serviceType':'Website design and development'})
 font='noto-sans-georgian' if lang=='ka' else 'manrope'
 return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title>
<meta name="description" content="{esc(description)}"><meta name="theme-color" content="#081529">{('<meta name="robots" content="noindex,follow">' if noindex else '')}
<link rel="canonical" href="{canonical}">{alternates}<link rel="icon" href="{base}assets/logo.svg" type="image/svg+xml"><link rel="icon" href="{base}assets/favicon.png" type="image/png"><link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png"><link rel="manifest" href="{base}site.webmanifest">
<meta property="og:type" content="website"><meta property="og:site_name" content="BEQSON Digital Studio"><meta property="og:locale" content="{c['locale']}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:type" content="{'image/jpeg' if slug else 'image/png'}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="{'800' if slug else '630'}"><meta property="og:image:alt" content="{esc(title)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{image}"><meta name="twitter:image:alt" content="{esc(title)}">
<link rel="preload" href="{base}assets/fonts/{font}-800.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{base}styles.css?v=9"><script src="{base}script.js?v=9" defer></script>
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)}</script></head>'''
HERO_SIZES='(max-width: 359px) calc((100vw - 28px) * .95), (max-width: 480px) calc((100vw - 36px) * .95), (max-width: 590px) calc((100vw - 48px) * .92), (max-width: 760px) 500px, (max-width: 1000px) calc((100vw - 73px) / 2), (max-width: 1180px) calc((100vw - 97px) / 2), (max-width: 1304px) calc((100vw - 106px) / 2.05), 600px'
INDUSTRY_HERO_SIZES='(max-width: 359px) calc((100vw - 28px) * .95), (max-width: 480px) calc((100vw - 36px) * .95), (max-width: 760px) calc((100vw - 48px) * .95), (max-width: 1000px) calc((100vw - 73px) / 2), (max-width: 1180px) calc((100vw - 104px) / 2), (max-width: 1304px) calc((100vw - 119px) * .5122), 608px'
MINI_SIZES='(max-width: 359px) calc((100vw - 28px) * .418), (max-width: 480px) calc((100vw - 36px) * .418), (max-width: 590px) calc((100vw - 48px) * .3956), (max-width: 760px) 215px, (max-width: 1000px) calc((100vw - 73px) * .255), (max-width: 1180px) calc((100vw - 97px) * .235), 285px'
CARD_SIZES='(max-width: 359px) calc(100vw - 28px), (max-width: 480px) calc(100vw - 36px), (max-width: 620px) calc(100vw - 48px), (max-width: 1000px) calc((100vw - 70px) / 2), (max-width: 1180px) calc((100vw - 109px) / 4), (max-width: 1304px) calc((100vw - 124px) / 4), 295px'
FULL_SIZES='(max-width: 480px) calc(100vw - 36px), (max-width: 1000px) calc(100vw - 48px), (max-width: 1304px) calc(100vw - 64px), 1240px'

def concept_picture(lang,base,slug,alt,sizes,eager=False):
 file=f'{base}assets/concepts/{lang}/{slug}'
 def srcset(ext):return f'{file}-320.{ext} 320w, {file}-480.{ext} 480w, {file}-768.{ext} 768w, {file}.{ext} 1536w'
 return f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}"><img src="{file}.webp" srcset="{srcset("webp")}" sizes="{sizes}" width="1536" height="1024" alt="{esc(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'></picture>'

def window_image(lang,base,slug,alt,small=False,eager=False,cls='',sizes=None):
 sizes=sizes or (MINI_SIZES if small else HERO_SIZES)
 return f'<div class="browser-window {cls}"><div class="browser-bar" aria-hidden="true"><span><i></i><i></i><i></i></span><b>BEQSON</b><em>{icon("arrow-up")}</em></div>{concept_picture(lang,base,slug,alt,sizes,eager)}</div>'
def industry_cards(lang,base,items=None):
 c=CONTENT[lang];cards=''
 for n in (items or INDUSTRIES):
  d=n[lang];slug=n['slug']
  cards+=f'''<a class="industry-card" href="{base}{lang}/{slug}/" style="--industry:{n['accent']}"><div class="card-image">{concept_picture(lang,base,slug,c['imageAlt']+d['name'],CARD_SIZES)}<span class="card-arrow">{icon('arrow-up')}</span></div><div class="card-body"><div class="card-heading">{tile(n['icon'],small=True)}<h3>{d['name']}</h3></div><p>{d['short']}</p><span class="card-link">{c['openConcept']} {icon('arrow')}</span></div></a>'''
 return cards

def pricing(lang):
 c=CONTENT[lang];cards=''
 for i,(name,price,ico) in enumerate(zip(('Start','Growth','Pro'),('250','490','890'),('rocket','trend','crown'))):
  subtitle,features=c['plans'][i]
  msg=c['waText']+' '+c['planMessage']+' '+name+'.'
  url='https://wa.me/'+PHONE+'?text='+quote(msg)
  cards+=f'''<article class="price-card {"featured" if i==1 else ""}"><div class="plan-top"><span class="plan-tag">{c['recommended'] if i==1 else ('01 / START' if i==0 else '03 / PRO')}</span>{tile(ico,'gold' if i==2 else '')}</div><h3>{name}</h3><p class="plan-subtitle">{subtitle}</p><p class="price-amount"><span>$</span>{price}<small>{c['oneTime']}</small></p><ul class="check-list">{''.join('<li>'+icon('check')+'<span>'+x+'</span></li>' for x in features)}</ul><a class="button {"primary" if i==1 else "outline"}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{c['choose']}{icon('arrow')}</a></article>'''
 return f'''<section class="pricing-section section" id="pricing"><div class="shell"><div class="section-heading centered"><p class="eyebrow">{c['pricingKicker']}</p><h2>{c['pricingTitle']}</h2><p>{c['pricingText']}</p></div><div class="pricing-grid">{cards}</div><div class="pricing-bottom"><p class="fine-print">{c['pricingNote']}</p><p class="maintenance">{c['maintenance']}<b>{c['perMonth']}</b></p></div></div></section>'''
def homepage(lang,base):
 c=CONTENT[lang]
 values=''.join(f'<div class="value-item">{tile(ico,small=True)}<div><p class="value-title">{title}</p><p>{desc}</p></div></div>' for ico,(title,desc) in zip(('globe','pin','layers','trend'),c['values']))
 steps=''.join(f'<article class="step-card"><span class="step-number">0{i+1}</span>{tile(ico)}<h3>{title}</h3><p>{desc}</p></article>' for i,(ico,(title,desc)) in enumerate(zip(('search','plan','pin','message','megaphone','chart'),c['steps'])))
 faqs=''.join(f'<details><summary>{esc(q)}{icon("plus")}</summary><p>{esc(a)}</p></details>' for q,a in c['faqs'])
 return head(lang,base,c['title'],c['description'])+f'''<body id="top">{header(lang,base)}<main id="main">
<section class="hero"><div class="hero-orbit" aria-hidden="true"></div><div class="shell hero-grid"><div class="hero-copy"><p class="eyebrow">{c['eyebrow']}</p><h1>{c['heroLead']} <span class="metal-text">{c['heroAccent']}</span> {c['heroEnd']}</h1><p class="hero-description">{c['heroText']}</p><div class="actions"><a class="button primary" href="#contact">{c['primary']}{icon('arrow-up')}</a><a class="text-link" href="#services">{c['secondary']}{icon('arrow')}</a></div><ul class="hero-notes">{''.join('<li>'+icon('check')+x+'</li>' for x in c['heroNotes'])}</ul></div>
<div class="hero-showcase"><span class="showcase-label">{c['conceptTag']} / 01—08</span><a class="hero-main-window" href="{base}{lang}/lawyers/">{window_image(lang,base,'lawyers',c['imageAlt']+INDUSTRIES[0][lang]['name'],eager=True)}</a><a class="hero-mini-window" href="{base}{lang}/dentists/">{window_image(lang,base,'dentists',c['imageAlt']+INDUSTRIES[1][lang]['name'],small=True)}</a><div class="hero-floating">{tile('sparkle',small=True)}<span><b>{c['heroFloat']}</b><small>{c['heroFloatSub']}</small></span></div><span class="showcase-index" aria-hidden="true">BEQSON / DESIGN SYSTEM</span></div></div></section>
<section class="value-section"><div class="shell value-grid">{values}</div></section>
<section class="section industries-section" id="services"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">{c['nicheKicker']}</p><h2>{lines(c['nicheTitle'])}</h2></div><p>{c['nicheText']}</p></div><div class="industry-grid">{industry_cards(lang,base)}</div><p class="concept-note">{icon('sparkle')}{c['conceptNote']}</p></div></section>
<section class="section growth-section" id="growth"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">{c['growthKicker']}</p><h2>{c['growthTitle']}</h2></div><p>{c['growthText']}</p></div><div class="steps-grid">{steps}</div><p class="fine-print growth-note">{c['growthNote']}</p></div></section>
{pricing(lang)}
<section class="section case-section" id="case"><div class="shell case-grid"><div><p class="eyebrow">{c['caseKicker']}</p><h2>{c['caseTitle']}</h2><p class="lead">{c['caseText']}</p><ul class="tags">{''.join('<li>'+x+'</li>' for x in c['caseTags'])}</ul><a class="button dark" href="https://levanilaw.ge/" target="_blank" rel="noopener noreferrer">{c['caseButton']}{icon('arrow-up')}</a></div><a class="case-visual" href="https://levanilaw.ge/" target="_blank" rel="noopener noreferrer"><span class="case-top">LEVANI KHELKHELAURI<span>LAWYER / TBILISI</span></span><div class="case-monogram" aria-hidden="true">LK</div><p>{lines(c['caseQuote'])}</p><span class="case-bottom">LEVANILAW.GE {icon('arrow-up')}</span></a></div></section>
<section class="section faq-section"><div class="shell faq-grid"><div><p class="eyebrow">FAQ</p><h2>{c['faqTitle']}</h2></div><div class="faq-list">{faqs}</div></div></section>
{contact_section(lang)}</main>{footer(lang,base)}</body></html>'''

def industry_page(lang,n):
 base='../../';c=CONTENT[lang];d=n[lang];slug=n['slug']
 title={'ru':'Сайт для бизнеса: ','en':'Website design for ','ka':'ვებსაიტი ბიზნესისთვის: '}[lang]+d['name']+' — BEQSON'
 features=''.join(f'<article class="feature-card"><span class="feature-number">0{i+1}</span>{tile(ico,small=True)}<h3>{t}</h3><p>{text}</p></article>' for i,(ico,(t,text)) in enumerate(zip(('layers','sparkle','message','check'),d['features'])))
 channels=''.join(f'<li><span>0{i+1}</span><p>{esc(text)}</p>{icon("arrow-up")}</li>' for i,text in enumerate(d['channels']))
 idx=INDUSTRIES.index(n);related=[INDUSTRIES[(idx+i)%8] for i in range(1,5)]
 image=f'{base}assets/concepts/{lang}/{slug}.webp'
 return head(lang,base,title,d['intro'],slug)+f'''<body id="top" class="industry-page" style="--industry:{n['accent']}">{header(lang,base,slug)}<main id="main">
<section class="industry-hero"><div class="shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../">{c['home']}</a><span>/</span><span>{d['name']}</span></nav><div class="industry-hero-grid"><div><p class="eyebrow">{c['nichePageKicker']}</p><div class="industry-label">{tile(n['icon'],small=True)}<span>{d['name']}</span></div><h1>{lines(d['headline'])}</h1><p class="lead">{d['intro']}</p><div class="actions"><a class="button primary" href="#contact">{c['nicheCta']}{icon('arrow-up')}</a><a class="text-link" href="#concept">{c['openConcept']}{icon('arrow')}</a></div></div><div class="industry-hero-visual"><a href="#concept">{window_image(lang,base,slug,c['imageAlt']+d['name'],eager=True,sizes=INDUSTRY_HERO_SIZES)}</a><div class="style-caption"><span>{n['brand']} / CONCEPT</span><b>{n['theme']}</b></div></div></div></div></section>
<section class="section concept-section" id="concept"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">{c['nichePreviewKicker']}</p><h2>{lines(c['nichePreviewTitle'])}</h2></div><p>{c['nichePreviewText']}</p></div><div class="concept-toolbar"><span>{icon('sparkle')}{c['demo']}</span><a class="text-link" href="{image}" target="_blank" rel="noopener" data-lightbox data-lightbox-title="{esc(d['name'])}">{c['zoom']}{icon('zoom')}</a></div><a class="full-concept" href="{image}" target="_blank" rel="noopener" data-lightbox data-lightbox-title="{esc(d['name'])}" aria-label="{esc(c['zoom'])}">{concept_picture(lang,base,slug,c['imageAlt']+d['name'],FULL_SIZES)}<span class="zoom-badge">{icon('zoom')}</span></a><div class="concept-meta"><ul class="style-list">{''.join('<li>'+x+'</li>' for x in d['style'])}</ul><p>{c['langNote']}</p></div><p class="concept-note">{icon('sparkle')}{c['conceptNote']}</p></div></section>
<section class="section industry-features"><div class="shell"><div class="section-heading split"><div><p class="eyebrow">BEQSON / DETAIL</p><h2>{lines(c['nicheFeaturesTitle'])}</h2></div><p>{c['nicheFeaturesText']}</p></div><div class="features-grid">{features}</div></div></section>
<section class="section industry-path"><div class="shell path-grid"><div><p class="eyebrow">SEO · LOCAL · ENQUIRIES</p><h2>{c['nichePathTitle']}</h2><p class="lead">{c['nichePathText']}</p><a class="text-link" href="../#pricing">{c['nav'][2]}{icon('arrow')}</a></div><ol class="channel-list">{channels}</ol></div></section>
{contact_section(lang,n)}
<section class="section related-section"><div class="shell"><div class="related-heading"><h2>{c['otherNiches']}</h2><a class="text-link" href="../#services">{c['allNiches']}{icon('arrow')}</a></div><div class="industry-grid">{industry_cards(lang,base,related)}</div></div></section>
</main>{footer(lang,base)}<dialog class="lightbox" aria-label="{esc(c['zoom'])}"><div class="lightbox-top"><span data-modal-title>{d['name']}</span><button class="lightbox-close" type="button" aria-label="{c['close']}">{icon('close')}</button></div><div class="lightbox-scroll"><img width="1536" height="1024" alt="{esc(c['imageAlt']+d['name'])}"></div></dialog></body></html>'''

def write(path,content):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8')
def main():
 write('assets/icons.svg','<svg xmlns="http://www.w3.org/2000/svg">'+''.join(f'<symbol id="{name}" viewBox="0 0 24 24">{paths}</symbol>' for name,paths in PATHS.items())+'</svg>\n')
 write('index.html',homepage('ru',''))
 for lang in LANGS:
  write(f'{lang}/index.html',homepage(lang,'../'))
  for n in INDUSTRIES:write(f'{lang}/{n["slug"]}/index.html',industry_page(lang,n))
 c=CONTENT['ru'];base=urlsplit(BASE_URL).path
 write('404.html',head('ru',base,'404 — BEQSON',c['notFoundText'],noindex=True)+f'<body id="top">{header("ru",base,force_home=True)}<main id="main"><div class="not-found"><p class="eyebrow">404 / BEQSON</p><h1>{c["notFound"]}</h1><p>{c["notFoundText"]}</p><a class="button primary" href="{BASE_URL}ru/">{c["returnHome"]}{icon("arrow")}</a></div>{contact_section("ru")}</main>{footer("ru",base)}</body></html>')
 urls=[]
 for slug in [None]+[n['slug'] for n in INDUSTRIES]:
  for lang in LANGS:
   path=lang+'/'+(slug+'/' if slug else '')
   alts=''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE_URL}{l}/{slug+"/" if slug else ""}" />' for l in LANGS)
   alts+=f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}ru/{slug+"/" if slug else ""}" />'
   urls.append('<url><loc>'+BASE_URL+path+'</loc>'+alts+'</url>')
 write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+'\n'.join(urls)+'\n</urlset>\n')
 write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+BASE_URL+'sitemap.xml\n')
 write('site.webmanifest',json.dumps({'name':'BEQSON Digital Studio','short_name':'BEQSON','lang':'ru','start_url':'./','scope':'./','display':'browser','background_color':'#f6f7fa','theme_color':'#081529','icons':[{'src':'assets/app-icon-192.png','sizes':'192x192','type':'image/png'},{'src':'assets/app-icon-512.png','sizes':'512x512','type':'image/png'}]},indent=2))
 write('.nojekyll','')
 print('Generated 28 content pages, 404, sitemap, robots and manifest.')
if __name__=='__main__':main()
