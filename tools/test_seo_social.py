#!/usr/bin/env python3
"""Validate social metadata, image files, generator output and update isolation."""
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from pathlib import Path
import ast
import importlib.util
import json
import os
import sys
import textwrap
from PIL import Image
from seo_social import ROOT, LOCALES, META_RE, is_social, update_social
from seo_schema import PageMetadata, METADATA
from build_sitemap import discover


class Social(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True);self.head=False;self.values={};self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='head':self.head=True
        key=attrs.get('property',attrs.get('name',''))
        if tag=='meta' and key.startswith(('og:','twitter:')):
            assert self.head and key not in self.values, key
            assert attrs.get('content','').strip(),key
            self.values[key]=attrs['content']
    def handle_endtag(self,tag):
        if tag=='head':self.head=False


def validate(source):
    page=PageMetadata(source);tags=Social(source).values
    for prefix in ['og','twitter']:
        assert tags[prefix+':title']==page.title
        assert tags[prefix+':description']==page.description
    assert tags['og:url']==page.canonical and tags['og:type']=='website'
    assert tags['og:site_name']=='BEQSON' and tags['og:locale']==LOCALES[page.language]
    assert tags['twitter:card']=='summary_large_image'
    assert tags['twitter:image']==tags['og:image']
    assert tags['twitter:image:alt']==tags['og:image:alt']
    url=urlsplit(tags['og:image']);assert url.scheme=='https' and url.netloc=='beqson.com'
    path=ROOT/unquote(url.path.lstrip('/'));assert path.is_file()
    with Image.open(path) as image:
        assert image.size==(int(tags['og:image:width']),int(tags['og:image:height']))
        assert image.width>=1200 and image.width>image.height
        assert tags['og:image:type']==Image.MIME[image.format]
    assert update_social(source)==source
    return tags


def main():
    pages,_=discover()
    for url,path in pages.items():
        source=path.read_text();validate(source)
        # Social updater must preserve all non-social bytes, even with duplicate input.
        clean=lambda s:META_RE.sub(lambda m:'' if is_social(m[0]) else m[0],s)
        duplicate=source.replace('</head>','<meta property="og:title" content="old"></head>')
        updated=update_social(duplicate);validate(updated);assert clean(source)==clean(updated)
    spec=importlib.util.spec_from_file_location('site_build',ROOT/'tools/build.py')
    build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
    for route,meta in METADATA.items():
        lang,suffix=route.split('/',1);slug=suffix.strip('/')
        if slug!='projects':validate(build.head(lang,'../',meta['title'],meta['description'],slug or None))
    workflow=(ROOT/'.github/workflows/build-projects-portfolio.yml').read_text()
    code=textwrap.dedent(workflow.split("python - <<'PY'\n",1)[1].split('\n          PY',1)[0])
    tree=ast.parse(code);tree.body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef))]
    namespace={};before=Path.cwd();sys.path.insert(0,str(ROOT))
    try:
        os.chdir(ROOT);exec(compile(tree,'portfolio-generator','exec'),namespace)
        for lang in ['ka','ru','en']:validate(namespace['page'](lang))
    finally:os.chdir(before);sys.path.pop(0)
    print(f'PASS: {len(pages)} pages, metadata/locale/canonical, actual image dimensions, duplicates, idempotence and both generators')


if __name__=='__main__':main()
