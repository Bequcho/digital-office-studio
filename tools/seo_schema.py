#!/usr/bin/env python3
"""Generate BEQSON JSON-LD and update only schema blocks in existing HTML.

python tools/seo_schema.py [--check]
No page rendering, metadata rewrites, or private CRM access occurs here.
"""
from pathlib import Path
from html.parser import HTMLParser
from copy import deepcopy
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://beqson.com/'
ORG = BASE + '#organization'
WEBSITE = BASE + '#website'
METADATA = json.loads((ROOT / 'tools/seo_metadata.json').read_text())
DESCRIPTIONS = {
    'en': 'BEQSON is an international digital studio based in Tbilisi and Batumi, Georgia, providing website design, web development, SEO and AI automation services to clients in Georgia and worldwide.',
    'ru': 'BEQSON — международная digital-студия, работающая из Тбилиси и Батуми. Создаём современные сайты, занимаемся SEO, цифровыми решениями и AI-автоматизацией для клиентов в Грузии и по всему миру.',
    'ka': 'BEQSON — საერთაშორისო ციფრული სტუდია, რომელიც მუშაობს თბილისიდან და ბათუმიდან. ვქმნით თანამედროვე ვებსაიტებს, ვთავაზობთ SEO-ს, AI ავტომატიზაციასა და ციფრულ გადაწყვეტილებებს კლიენტებს საქართველოში და მთელ მსოფლიოში.',
}
SERVICE_NAMES = {
    'lawyers': ['ვებსაიტების შექმნა ადვოკატებისთვის', 'Создание сайтов для адвокатов', 'Website Design for Lawyers'],
    'dentists': ['ვებსაიტების შექმნა სტომატოლოგებისთვის', 'Создание сайтов для стоматологов', 'Website Design for Dentists'],
    'clinics': ['ვებსაიტების შექმნა კლინიკებისთვის', 'Создание сайтов для клиник', 'Website Design for Clinics'],
    'realtors': ['ვებსაიტების შექმნა რეალტორებისთვის', 'Создание сайтов для риелторов', 'Website Design for Realtors'],
    'accountants': ['ვებსაიტების შექმნა ბუღალტრებისთვის', 'Создание сайтов для бухгалтеров', 'Website Design for Accountants'],
    'construction': ['ვებსაიტები სამშენებლო კომპანიებისთვის', 'Сайты для строительных компаний', 'Website Design for Construction Companies'],
    'autoservices': ['ვებსაიტების შექმნა ავტოსერვისებისთვის', 'Создание сайтов для автосервисов', 'Website Design for Auto Repair Businesses'],
    'hotels': ['ვებსაიტების შექმნა სასტუმროებისთვის', 'Создание сайтов для отелей', 'Website Design for Hotels'],
}
CONTENT = json.loads((ROOT / 'tools/content.json').read_text())
INDUSTRIES = {item['slug']: item for item in json.loads((ROOT / 'tools/industries.json').read_text())}
AREA = [{'@type': 'Country', 'name': 'Georgia'}, 'Worldwide']
SCHEMA_RE = re.compile(r'<script\b(?=[^>]*\btype=["\']application/ld\+json["\'])[^>]*>.*?</script\s*>', re.I | re.S)


def generate_schema(language, slug, canonical, title, description, page_type='WebPage', extra_entities=()):
    if language not in DESCRIPTIONS:
        raise ValueError('Unsupported language')
    slug = slug or ''
    expected = BASE + language + '/' + (slug + '/' if slug else '')
    if language == 'ru' and slug == 'audit' and canonical == BASE + 'audit/':
        expected = canonical
    if canonical != expected or page_type not in ('WebPage', 'CollectionPage'):
        raise ValueError('Schema URL/type must match the localized page')
    # The primary 30 pages always use the SEO Step 2 source of truth.
    metadata = METADATA.get(language + '/' + (slug + '/' if slug else ''))
    if metadata:
        title, description = metadata['title'], metadata['description']
    organization = {
        '@type': 'Organization', '@id': ORG, 'name': 'BEQSON', 'url': BASE,
        'description': DESCRIPTIONS[language],
        'logo': {'@type': 'ImageObject', 'url': BASE + 'assets/beqson-mark-v3.png'},
        'location': [{'@type': 'Place', 'name': city + ', Georgia'} for city in ('Tbilisi', 'Batumi')],
        'areaServed': deepcopy(AREA),
        'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer support',
                         'telephone': '+995551739333', 'email': 'digitalstudiobeqson@gmail.com',
                         'availableLanguage': ['Georgian', 'Russian', 'English']},
        # Both profiles are linked from the published site as BEQSON profiles.
        'sameAs': ['https://clutch.co/profile/beqson-digital-studio', 'https://t.me/digital_studio_beqson'],
    }
    website = {'@type': 'WebSite', '@id': WEBSITE, 'url': BASE, 'name': 'BEQSON',
               'publisher': {'@id': ORG}, 'inLanguage': ['ka', 'ru', 'en']}
    page = {'@type': page_type, '@id': canonical + '#webpage', 'url': canonical,
            'name': title, 'description': description, 'inLanguage': language,
            'isPartOf': {'@id': WEBSITE}, 'publisher': {'@id': ORG}, 'about': {'@id': ORG}}
    graph = [organization, website, page]
    if slug in SERVICE_NAMES:
        service_id = canonical + '#service'
        page['mainEntity'] = {'@id': service_id}
        graph.append({'@type': 'Service', '@id': service_id, 'url': canonical,
                      'name': SERVICE_NAMES[slug][('ka', 'ru', 'en').index(language)],
                      'description': description, 'provider': {'@id': ORG},
                      'areaServed': deepcopy(AREA), 'mainEntityOfPage': {'@id': page['@id']}})
        breadcrumb_id = canonical + '#breadcrumb'
        page['breadcrumb'] = {'@id': breadcrumb_id}
        graph.append({'@type': 'BreadcrumbList', '@id': breadcrumb_id,
                      'itemListElement': [
                          {'@type': 'ListItem', 'position': 1, 'name': CONTENT[language]['home'],
                           'item': BASE + language + '/'},
                          {'@type': 'ListItem', 'position': 2, 'name': INDUSTRIES[slug][language]['name'],
                           'item': canonical}]})
    # The standalone audit implements the same real audit tool as localized pages.
    if canonical == BASE + 'audit/' and not extra_entities:
        extra_entities = [{'@type': 'WebApplication', '@id': canonical + '#app',
                           'name': title, 'url': canonical, 'inLanguage': language,
                           'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Any',
                           'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'RUB'}}]
    # Keep the actual existing tool application; never fabricate a new application.
    for entity in extra_entities:
        if entity.get('@type') not in ('WebApplication', 'SoftwareApplication'):
            raise ValueError('Unsupported supplemental entity')
        entity = deepcopy(entity)
        entity['publisher'] = {'@id': ORG}
        entity['isPartOf'] = {'@id': WEBSITE}
        entity['mainEntityOfPage'] = {'@id': page['@id']}
        graph.append(entity)
        page['mainEntity'] = {'@id': entity['@id']}
    return {'@context': 'https://schema.org', '@graph': graph}


def render_schema(*args, **kwargs):
    payload = json.dumps(generate_schema(*args, **kwargs), ensure_ascii=False, separators=(',', ':'))
    # JSON escaping, not HTML entities: preserve Unicode and prevent closing a script.
    return '<script type="application/ld+json">' + payload.replace('<', '\\u003c') + '</script>'


class PageMetadata(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.title = ''; self.description = ''; self.canonical = ''; self.language = ''
        self.robots = ''; self.in_title = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.language = attrs.get('lang', '')
        if tag == 'title': self.in_title = True
        if tag == 'meta' and attrs.get('name') == 'description': self.description = attrs.get('content', '')
        if tag == 'meta' and attrs.get('name') == 'robots': self.robots = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs.get('href', '')

    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False

    def handle_data(self, data):
        if self.in_title: self.title += data


def update_schema(source, slug):
    meta = PageMetadata(source)
    old_entities = []
    for block in SCHEMA_RE.findall(source):
        payload = json.loads(re.sub(r'^<script[^>]*>|</script\s*>$', '', block, flags=re.I))
        old_entities.extend(payload.get('@graph', [payload]))
    applications = [item for item in old_entities if item.get('@type') in ('WebApplication', 'SoftwareApplication')]
    page_type = 'CollectionPage' if slug in ('projects', 'tools') else 'WebPage'
    tag = render_schema(meta.language, slug, meta.canonical, meta.title, meta.description, page_type, applications)
    # Normalize to exactly one head script; all other HTML stays byte-for-byte intact.
    matches = list(SCHEMA_RE.finditer(source))
    head_end = source.index('</head>')
    if len(matches) == 1 and matches[0].end() < head_end:
        return source[:matches[0].start()] + tag + source[matches[0].end():]
    clean = SCHEMA_RE.sub('', source)
    return clean.replace('</head>', tag + '</head>', 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    count = 0
    for language in ('ka', 'ru', 'en'):
        for path in sorted((ROOT / language).rglob('index.html')):
            source = path.read_text()
            if 'noindex' in PageMetadata(source).robots:
                continue
            slug = path.parent.relative_to(ROOT / language).as_posix()
            result = update_schema(source, '' if slug == '.' else slug)
            if args.check:
                if result != source: raise SystemExit(f'Stale schema: {path.relative_to(ROOT)}')
            elif result != source:
                path.write_text(result)
            count += 1
    path = ROOT / 'audit/index.html'
    source = path.read_text(); result = update_schema(source, 'audit')
    if args.check:
        if result != source: raise SystemExit('Stale schema: audit/index.html')
    elif result != source:
        path.write_text(result)
    count += 1
    # Root remains a redirect fallback, with no independent structured-data entity.
    path = ROOT / 'index.html'; source = path.read_text(); result = SCHEMA_RE.sub('', source)
    if args.check:
        if source != result: raise SystemExit('Root redirect must not carry independent JSON-LD')
    elif source != result:
        path.write_text(result)
    print(f'Schema {"verified" if args.check else "updated"}: {count} indexable pages and root fallback')


if __name__ == '__main__':
    main()
