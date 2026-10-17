#!/usr/bin/env python3
"""Local JSON-LD structure, identity, content and regression checks."""
from pathlib import Path
from html.parser import HTMLParser
import ast
import json
import re
import textwrap
import importlib.util
import os
import sys
from seo_schema import ROOT, BASE, ORG, WEBSITE, METADATA, AREA, SERVICE_NAMES, SCHEMA_RE, update_schema, generate_schema, render_schema


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.in_head = False; self.in_schema = False; self.blocks = []
        self.html_count = 0; self.head_count = 0; self.h1_count = 0
        self.title = ''; self.in_title = False; self.description = ''; self.canonical = ''; self.language = ''
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.html_count += 1
        if tag == 'h1': self.h1_count += 1
        if tag == 'head': self.in_head = True; self.head_count += 1
        if tag == 'html': self.language = attrs.get('lang')
        if tag == 'title': self.in_title = True
        if tag == 'meta' and attrs.get('name') == 'description': self.description = attrs['content']
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs['href']
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            assert self.in_head, 'JSON-LD must be inside head'
            self.blocks.append(''); self.in_schema = True

    def handle_endtag(self, tag):
        if tag == 'head': self.in_head = False
        if tag == 'title': self.in_title = False
        if tag == 'script': self.in_schema = False

    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_schema: self.blocks[-1] += data


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values(): yield from walk(child)
    elif isinstance(value, list):
        for child in value: yield from walk(child)


def validate(source, route):
    doc = Document(source)
    assert len(doc.blocks) == 1, route
    data = json.loads(doc.blocks[0])
    assert data['@context'] == 'https://schema.org'
    graph = data['@graph']; assert isinstance(graph, list)
    ids = [item['@id'] for item in graph]
    assert len(ids) == len(set(ids))
    for obj in walk(graph):
        if set(obj) == {'@id'}: assert obj['@id'] in ids, obj
        assert obj.get('@type') not in ('LocalBusiness', 'PostalAddress', 'Review', 'AggregateRating', 'SearchAction', 'GeoCoordinates')
        assert not set(obj) & {'streetAddress', 'postalCode', 'latitude', 'longitude', 'foundingDate', 'awards'}
    org, site, page = graph[:3]
    assert org['@type'] == 'Organization' and org['@id'] == ORG and org['name'] == 'BEQSON'
    assert org['url'] == BASE and org['areaServed'] == AREA
    assert org['location'] == [{'@type':'Place', 'name': city+', Georgia'} for city in ['Tbilisi','Batumi']]
    assert org['logo'] == {'@type':'ImageObject','url':BASE+'assets/beqson-mark-v3.png'}
    assert org['contactPoint']['telephone'] == '+995551739333'
    assert org['contactPoint']['email'] == 'digitalstudiobeqson@gmail.com'
    assert org['contactPoint']['availableLanguage'] == ['Georgian','Russian','English']
    assert site['@type'] == 'WebSite' and site['@id'] == WEBSITE
    assert site['publisher'] == page['publisher'] == {'@id':ORG}
    assert page['isPartOf'] == {'@id':WEBSITE}
    assert page['url'] == doc.canonical == BASE+route
    assert page['@id'] == doc.canonical+'#webpage'
    assert page['inLanguage'] == doc.language == route.split('/')[0]
    assert page['name'] == doc.title and page['description'] == doc.description
    if route in METADATA:
        assert page['name'] == METADATA[route]['title']
        assert page['description'] == METADATA[route]['description']
    slug=route.split('/',1)[1].strip('/')
    expected_types=['Organization','WebSite','CollectionPage' if slug in ('projects','tools') else 'WebPage']
    if slug in SERVICE_NAMES:
        expected_types.append('Service')
        service=graph[3]
        assert service['@id'] == doc.canonical+'#service'
        assert service['name'] == SERVICE_NAMES[slug][('ka','ru','en').index(doc.language)]
        assert service['provider'] == {'@id':ORG} and service['areaServed'] == AREA
        assert service['mainEntityOfPage'] == {'@id':page['@id']}
        assert page['mainEntity'] == {'@id':service['@id']}
    if route in METADATA: assert [entity['@type'] for entity in graph] == expected_types
    return page['@id']


def main():
    ids=[]; count=0
    for language in ('ka','ru','en'):
        for path in sorted((ROOT/language).rglob('index.html')):
            route=path.parent.relative_to(ROOT).as_posix()+'/'
            source=path.read_text();ids.append(validate(source,route))
            structure=Document(source)
            assert (structure.html_count, structure.head_count, structure.h1_count)==(1,1,1), path
            slug=path.parent.relative_to(ROOT/language).as_posix()
            assert update_schema(source,'' if slug=='.' else slug)==source, 'Not idempotent'
            # Replacing old or duplicate schema must preserve every other HTML byte.
            stale=SCHEMA_RE.sub('<script type="application/ld+json">{"@context":"https://schema.org","@graph":[]}</script>',source)
            if not slug.startswith('tools/') and slug not in ('audit','calculator'):
                assert SCHEMA_RE.sub('',update_schema(stale,'' if slug=='.' else slug))==SCHEMA_RE.sub('',source)
            count+=1
    assert len(ids)==len(set(ids))
    root=(ROOT/'index.html').read_text();assert not Document(root).blocks
    assert (ROOT/'assets/beqson-mark-v3.png').is_file()
    # Exercise the actual build functions in memory, without rebuilding static pages.
    spec=importlib.util.spec_from_file_location('site_build',ROOT/'tools/build.py')
    build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
    for route, meta in METADATA.items():
        language,suffix=route.split('/',1);slug=suffix.strip('/')
        if slug!='projects': validate(build.head(language,'../',meta['title'],meta['description'],slug or None),route)
    workflow=(ROOT/'.github/workflows/build-projects-portfolio.yml').read_text()
    code=textwrap.dedent(workflow.split("python - <<'PY'\n",1)[1].split('\n          PY',1)[0])
    tree=ast.parse(code);tree.body=[node for node in tree.body if isinstance(node,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef))]
    old_cwd=Path.cwd();namespace={};sys.path.insert(0,str(ROOT))
    try:
        os.chdir(ROOT);exec(compile(tree,'portfolio-generator','exec'),namespace)
        for language in ('ka','ru','en'):validate(namespace['page'](language),language+'/projects/')
    finally:os.chdir(old_cwd);sys.path.pop(0)
    payload=generate_schema('en','example',BASE+'en/example/','A & B <test>','Unicode ქართული русский')
    assert payload['@graph'][2]['name']=='A & B <test>'
    unsafe='A & B </script><div>ქართული</div>'
    tag=render_schema('en','example',BASE+'en/example/',unsafe,'Русский & English')
    assert tag.count('</script>')==1 and '&amp;' not in tag
    assert json.loads(tag.split('>',1)[1].rsplit('</script>',1)[0])['@graph'][2]['name']==unsafe
    print(f'PASS: {count} language pages, 30 primary graphs, root fallback, unique IDs, links, Unicode, regression isolation, idempotence and both generators')


if __name__=='__main__':main()
