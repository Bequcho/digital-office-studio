#!/usr/bin/env python3
"""Offline IndexNow tests. All HTTP is fake; sockets are blocked as a backstop."""
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import URLError
import json
import unittest
import xml.etree.ElementTree as ET

from indexnow import BASE, NS, ROOT, ENDPOINT, Response, Unavailable, NoRedirect, request, run, sitemap_urls, url_reason
from build_sitemap import discover

KEY = '9a97aa27a069ea0350203fe532357c06'


def html(url, extra='', canonical=None):
    return f'<!doctype html><html lang="en"><head><title>Test</title><link rel="canonical" href="{canonical or url}">{extra}</head><body><h1>Test</h1></body></html>'


def xml(urls):
    root = ET.Element('urlset', xmlns=NS)
    for url in urls:
        ET.SubElement(ET.SubElement(root, 'url'), 'loc').text = url
    return ET.tostring(root, encoding='unicode')


class FakeHTTP:
    def __init__(self, responses):
        self.responses = responses
        self.gets = []
        self.posts = []

    def __call__(self, url, payload=None):
        if payload is not None:
            self.posts.append((url, json.loads(payload)))
            return Response(202, url, {}, '')
        self.gets.append(url)
        response = self.responses[url]
        if isinstance(response, Exception):
            raise response
        return response


class IndexNowTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory(prefix='beqson-indexnow-test-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /crm/\n')
        (self.root/(KEY+'.txt')).write_text(KEY)
        self.url = BASE+'en/'
        self.other = BASE+'ru/'
        for url in (self.url, self.other):
            path = self.root/url.removeprefix(BASE)/'index.html'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html(url))
        self.responses = {
            BASE+'sitemap.xml': Response(200, BASE+'sitemap.xml', {}, xml([self.url, self.other])),
            BASE+'robots.txt': Response(200, BASE+'robots.txt', {}, (self.root/'robots.txt').read_text()),
            BASE+KEY+'.txt': Response(200, BASE+KEY+'.txt', {}, KEY),
            self.url: Response(200, self.url, {'content-type':'text/html; charset=utf-8'}, html(self.url)),
            self.other: Response(200, self.other, {'content-type':'text/html'}, html(self.other)),
        }
        self.set_urls([self.url, self.other])
        self.http = FakeHTTP(self.responses)
        sockets = patch('socket.socket', side_effect=AssertionError('Real network forbidden in tests'))
        sockets.start(); self.addCleanup(sockets.stop)

    def set_urls(self, urls):
        (self.root/'sitemap.xml').write_text(xml(urls))

    def check(self, **kwargs):
        return run(self.root, key=KEY, fetch=self.http, **kwargs)

    def test_default_dry_run_never_posts(self):
        report = self.check()
        self.assertTrue(report['dry_run'])
        self.assertEqual(report['accepted'], [self.url, self.other])
        self.assertIsNone(report['blocked'])
        self.assertEqual(self.http.posts, [])

    def test_manual_false_submits_only_validated_urls(self):
        self.responses[self.other] = replace(self.responses[self.other], status=404)
        report = self.check(dry_run=False, manual=True)
        self.assertEqual(report['submitted'], 1)
        self.assertEqual(self.http.posts, [(ENDPOINT, {'host':'beqson.com','key':KEY,
            'keyLocation':BASE+KEY+'.txt','urlList':[self.url]})])
        self.assertIn('HTTP 404', report['skipped'][0]['reason'])

    def test_automatic_or_untyped_submission_forbidden(self):
        report = self.check(dry_run=False)
        self.assertTrue(report['blocked'])
        self.assertFalse(self.http.gets or self.http.posts)
        with self.assertRaises(ValueError):
            self.check(dry_run='false', manual=True)

    def test_sitemap_domain_duplicates_private_and_missing(self):
        bad = [BASE+'crm/', BASE+'scripts/', BASE+'en/missing/', BASE,
               'https://www.beqson.com/en/', 'https://beqson.com.evil/en/',
               'http://beqson.com/en/', BASE+'en/?utm_source=test', BASE+'en/#anchor']
        self.set_urls([self.url, self.url, *bad])
        report = self.check(dry_run=False, manual=True)
        self.assertEqual(report['accepted'], [self.url])
        self.assertEqual(len(report['skipped']), len(bad)+1)
        self.assertEqual(report['skipped'][0]['reason'], 'duplicate sitemap URL')
        self.assertTrue(all(url not in self.http.gets for url in bad))

    def test_local_noindex_redirect_and_other_canonical(self):
        for extra, canonical in [('<meta name="robots" content="noindex">', None),
                                  ('<meta http-equiv="refresh" content="0;url=/ka/">', None),
                                  ('', BASE+'ka/')]:
            with self.subTest(extra=extra, canonical=canonical):
                (self.root/'en/index.html').write_text(html(self.url, extra, canonical))
                report = self.check()
                self.assertNotIn(self.url, report['accepted'])
                self.assertIn('local indexable', report['skipped'][0]['reason'])

    def test_live_sitemap_required(self):
        self.responses[BASE+'sitemap.xml'] = replace(self.responses[BASE+'sitemap.xml'], body=xml([self.other]))
        report = self.check()
        self.assertEqual(report['accepted'], [self.other])
        self.assertIn('published sitemap', report['skipped'][0]['reason'])
        self.assertNotIn(self.url, self.http.gets)

    def test_live_robots_blocks_page(self):
        self.responses[BASE+'robots.txt'] = replace(self.responses[BASE+'robots.txt'], body='User-agent: *\nDisallow: /en/\n')
        report = self.check()
        self.assertEqual(report['accepted'], [self.other])
        self.assertIn('robots.txt', report['skipped'][0]['reason'])

    def test_live_rejections_are_explained(self):
        original = self.responses[self.url]
        cases = [
            (replace(original, status=301, headers={'location':self.other}), 'redirect'),
            (replace(original, url=self.other), 'redirect'),
            (replace(original, status=404), 'HTTP 404'),
            (replace(original, body=html(self.url, '<meta name="robots" content="noindex,follow">')), 'prohibits indexing'),
            (replace(original, body=html(self.url, '<meta name="yandex" content="none">')), 'prohibits indexing'),
            (replace(original, headers={**original.headers,'x-robots-tag':'googlebot: noindex'}), 'prohibits indexing'),
            (replace(original, body=html(self.url, '<meta http-equiv="refresh" content="1;url=/ka/">')), 'redirect'),
            (replace(original, body=html(self.url, '<script>location.replace("/ka/")</script>')), 'redirect'),
            (replace(original, headers={**original.headers,'refresh':'0;url=/ka/'}), 'redirect'),
            (replace(original, body=html(self.url, canonical=self.other)), 'canonical'),
            (replace(original, body=html(self.url, f'<link rel="canonical" href="{self.url}">')), 'canonical'),
            (replace(original, body=html(self.url).replace(f'<link rel="canonical" href="{self.url}">','')), 'canonical'),
            (replace(original, body=html(self.url).replace(f'<link rel="canonical" href="{self.url}">','').replace('<body>', f'<body><link rel="canonical" href="{self.url}">')), 'canonical'),
            (replace(original, headers={'content-type':'application/json'}), 'not HTML'),
        ]
        for response, reason in cases:
            with self.subTest(reason=reason):
                self.responses[self.url] = response
                report = self.check()
                self.assertEqual(report['accepted'], [self.other])
                self.assertIn(reason, report['skipped'][0]['reason'])
        self.assertFalse(self.http.posts)

    def test_unavailable_page_blocks_entire_batch_after_valid_page(self):
        for status in (401,403,408,429,500,503):
            with self.subTest(status=status):
                self.responses[self.other] = replace(self.responses[self.other], status=status)
                report = self.check(dry_run=False, manual=True)
                self.assertTrue(report['blocked'])
                self.assertEqual(report['submitted'], 0)
        self.assertFalse(self.http.posts)

    def test_connection_failure_blocks_batch(self):
        self.responses[self.other] = Unavailable('connection timeout')
        report = self.check(dry_run=False, manual=True)
        self.assertIn('timeout', report['blocked'])
        self.assertFalse(self.http.posts)

    def test_required_files_unavailable_or_invalid_block_submission(self):
        for url in (BASE+'sitemap.xml', BASE+'robots.txt', BASE+KEY+'.txt'):
            with self.subTest(url=url):
                original = self.responses[url]
                self.responses[url] = replace(original, status=302)
                self.assertTrue(self.check(dry_run=False, manual=True)['blocked'])
                self.responses[url] = original
        self.responses[BASE+'sitemap.xml'] = replace(self.responses[BASE+'sitemap.xml'], body='not XML')
        self.assertTrue(self.check(dry_run=False, manual=True)['blocked'])
        self.assertFalse(self.http.posts)

    def test_key_mismatch_blocks_submission(self):
        self.responses[BASE+KEY+'.txt'] = replace(self.responses[BASE+KEY+'.txt'], body='wrong key')
        self.assertTrue(self.check(dry_run=False, manual=True)['blocked'])
        self.assertFalse(self.http.posts)

    def test_transport_disables_redirects_and_reports_unavailability(self):
        self.assertIsNone(NoRedirect().redirect_request(None,None,302,'',{},BASE))
        with patch('indexnow.build_opener') as opener:
            opener.return_value.open.side_effect = URLError('unreachable')
            with self.assertRaises(Unavailable):
                request(BASE)
            self.assertIsInstance(opener.call_args.args[0], NoRedirect)

    def test_real_sitemap_dry_run_with_mocked_production(self):
        urls = sitemap_urls((ROOT/'sitemap.xml').read_text())
        pages, _ = discover(ROOT)
        self.assertEqual(len(urls), 52)
        self.assertEqual(set(urls), set(pages))
        replies = {url:Response(200,url,{'content-type':'text/html'},p.read_text()) for url,p in pages.items()}
        replies.update({BASE+'sitemap.xml':Response(200,BASE+'sitemap.xml',{},(ROOT/'sitemap.xml').read_text()),
                        BASE+'robots.txt':Response(200,BASE+'robots.txt',{},(ROOT/'robots.txt').read_text()),
                        BASE+KEY+'.txt':Response(200,BASE+KEY+'.txt',{},KEY)})
        fake = FakeHTTP(replies)
        report = run(ROOT, key=KEY, fetch=fake)
        self.assertIsNone(report['blocked'])
        self.assertEqual(len(report['accepted']), 52)
        self.assertFalse(report['skipped'] or fake.posts)


if __name__ == '__main__':
    unittest.main(verbosity=2)
