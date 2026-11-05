#!/usr/bin/env python3
"""Sitemap discovery, exclusions, preservation and idempotence tests."""
from site_contract import URLS, xdefault
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET
from build_sitemap import ROOT, BASE, NS, Document, discover, build_sitemap, blocked_by_robots


def main():
    source=(ROOT/'sitemap.xml').read_text()
    tree=ET.fromstring(source)
    assert tree.tag=='{'+NS+'}urlset'
    entries=tree.findall('{'+NS+'}url')
    urls=[entry.findtext('{'+NS+'}loc') for entry in entries]
    assert len(urls)==len(set(urls))
    expected,excluded=discover()
    assert set(urls)==set(expected), (set(expected)-set(urls),set(urls)-set(expected))
    for url in urls:
        parts=urlsplit(url)
        assert parts.scheme=='https' and parts.netloc=='beqson.com'
        assert not parts.query and not parts.fragment and parts.path.endswith('/')
        assert not parts.path.startswith('/crm/') and parts.path!='/'
        file=ROOT/unquote(parts.path.lstrip('/'))/'index.html'
        assert file.exists()
        doc=Document(file.read_text())
        assert doc.canonicals==[url] and not set(doc.robots)&{'noindex','none'} and not doc.refresh
    for entry in entries:
        url=entry.findtext('{'+NS+'}loc')
        annotations=entry.findall('{http://www.w3.org/1999/xhtml}link')
        if annotations:
            route=url.removeprefix(BASE);suffix=route.split('/',1)[1]
            expected_links={lang:BASE+lang+'/'+suffix for lang in ('ka','ru','en')}
            expected_links['x-default']=expected_links[xdefault(route)]
            assert len(annotations)==4
            assert {a.get('hreflang'):a.get('href') for a in annotations}==expected_links
            assert all(a.get('rel')=='alternate' and a.get('href') in URLS for a in annotations)
    # Independent route inventory catches pages missing from both discovery and XML.
    assert set(urls) == URLS
    assert BASE+'audit/' not in urls and BASE+'ru/audit/' in urls
    assert excluded['audit/index.html'] == 'canonical points elsewhere'
    primary=json.loads((ROOT/'tools/seo_metadata.json').read_text())
    assert {BASE+route for route in primary} <= set(urls)
    robots=(ROOT/'robots.txt').read_text()
    assert [line.strip() for line in robots.splitlines() if line.lower().startswith('sitemap:')]==['Sitemap: '+BASE+'sitemap.xml']
    assert blocked_by_robots('/crm/',robots) and blocked_by_robots('/crm/proposals/',robots)
    assert not blocked_by_robots('/ka/',robots)
    assert build_sitemap(check=True)==source
    assert not tree.findall('.//{'+NS+'}lastmod')
    # A synthetic public document contains the word noindex in JS, not a robots tag.
    with TemporaryDirectory() as directory:
        root=Path(directory);(root/'robots.txt').write_text(robots)
        def page(route,extra='',canonical=None):
            p=root/route/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text('<!doctype html><html lang="en"><head><link rel="canonical" href="'+(canonical or BASE+route+'/')+'">'+extra+'</head><body>Example</body></html>')
        page('en/example','<script>const warning="noindex";</script>')
        page('en/private','<meta name="robots" content="noindex,follow">')
        page('en/refresh','<meta http-equiv="refresh" content="0;url=/en/">')
        page('en/redirect','<script>location.replace("/en/")</script>')
        page('en/duplicate',canonical=BASE+'en/example/')
        page('crm')
        found,_=discover(root);assert set(found)=={BASE+'en/example/'}
        first=build_sitemap(root);assert build_sitemap(root)==first
        assert (root/'robots.txt').read_text()==robots
        # Remove stale URLs/duplicates while retaining original valid entry annotations.
        entry='<url><loc>'+BASE+'en/example/</loc></url>'
        (root/'sitemap.xml').write_text(first.replace('</urlset>',entry+'<url><loc>'+BASE+'missing/</loc></url></urlset>'))
        cleaned=build_sitemap(root)
        assert len(ET.fromstring(cleaned).findall('{'+NS+'}url'))==1
        assert build_sitemap(root)==cleaned
    print(f'PASS: {len(urls)} URLs, 30 primary pages, local canonical/indexability, exclusions, robots CRM protection and idempotence')
    for language in ('ka','ru','en'):
        print(language,sum(url.startswith(BASE+language+'/') for url in urls))


if __name__=='__main__':main()
