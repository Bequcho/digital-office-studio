#!/usr/bin/env python3
"""Manually validate sitemap URLs against production; dry-run by default."""
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, unquote
from urllib.request import Request, HTTPRedirectHandler, build_opener
import argparse
import json
import os
import re
import xml.etree.ElementTree as ET

from build_sitemap import BASE, NS, Document, discover, blocked_by_robots

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = 'https://api.indexnow.org/IndexNow'
LIMIT = 4 * 1024 * 1024
REDIRECT_JS = re.compile(r'(?:window\.)?location\s*(?:\.\s*(?:replace|assign)\s*\(|(?:\.\s*href)?\s*=)')


class Unavailable(RuntimeError):
    """Incomplete or untrustworthy production verification: never submit."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class Response:
    status: int
    url: str
    headers: dict
    body: str


def request(url, payload=None):
    """Bounded HTTP request with TLS verification and no redirect following."""
    headers = {'User-Agent': 'BEQSON-IndexNow-Validator/1.0', 'Accept-Encoding': 'identity'}
    if payload is not None:
        headers['Content-Type'] = 'application/json; charset=utf-8'
    req = Request(url, data=payload, headers=headers)
    opener = build_opener(NoRedirect())
    try:
        try:
            response = opener.open(req, timeout=10)
        except HTTPError as error:
            response = error  # Inspect 3xx/4xx; do not follow redirects.
        with response:
            data = response.read(LIMIT + 1)
            if len(data) > LIMIT:
                raise Unavailable(f'Response exceeds {LIMIT} bytes: {url}')
            charset = response.headers.get_content_charset() or 'utf-8'
            return Response(response.code, response.geturl(),
                            {k.lower(): ', '.join(response.headers.get_all(k)) for k in response.headers},
                            data.decode(charset, errors='replace'))
    except (URLError, OSError, LookupError, ValueError) as error:
        raise Unavailable(f'HTTP verification failed for {url}: {error}') from error


def sitemap_urls(source):
    try:
        tree = ET.fromstring(source)
    except ET.ParseError as error:
        raise Unavailable('Invalid sitemap XML') from error
    if tree.tag != '{'+NS+'}urlset':
        raise Unavailable('Expected sitemap urlset')
    result = []
    for entry in tree.findall('{'+NS+'}url'):
        locs = entry.findall('{'+NS+'}loc')
        if len(locs) != 1 or not locs[0].text:
            raise Unavailable('Sitemap entry must have exactly one nonempty loc')
        result.append(locs[0].text.strip())
    if not result:
        raise Unavailable('Empty sitemap')
    return result


def url_reason(url):
    parts = urlsplit(url)
    if parts.scheme != 'https' or parts.netloc != 'beqson.com':
        return 'not the canonical HTTPS domain beqson.com'
    if parts.query or parts.fragment:
        return 'query or fragment in URL'
    path = unquote(parts.path)
    segments = path.strip('/').split('/')
    if path == '/' or not path.endswith('/') or any(
            x in {'crm','scripts','tests','test','backend','assets'} or x.startswith('.') for x in segments):
        return 'private, technical or root redirect URL'
    return None


class LiveDocument(Document):
    def __init__(self, source):
        self.in_head = False
        self.canonical_outside_head = False
        super().__init__(source)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'head':
            self.in_head = True
        if tag == 'link' and 'canonical' in values.get('rel', '').lower().split() and not self.in_head:
            self.canonical_outside_head = True
        super().handle_starttag(tag, attrs)
        if tag == 'meta' and values.get('name', '').lower() in ('yandex', 'yandexbot'):
            self.robots.extend(re.split(r'[\s,]+', values.get('content', '').lower()))

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        if tag == 'head':
            self.in_head = False


def production_response(url, fetch):
    response = fetch(url)
    if response.status in (401, 403, 408, 429) or response.status >= 500:
        raise Unavailable(f'Production unavailable or access blocked: HTTP {response.status} at {url}')
    return response


def page_reason(url, response):
    if response.url != url or 300 <= response.status < 400 or 'location' in response.headers:
        return 'HTTP redirect'
    if response.status != 200:
        return f'HTTP {response.status}, expected 200'
    if response.headers.get('content-type', '').split(';')[0].strip().lower() not in ('text/html', 'application/xhtml+xml'):
        return 'response is not HTML'
    if re.search(r'\b(?:noindex|none)\b', response.headers.get('x-robots-tag', ''), re.I):
        return 'X-Robots-Tag prohibits indexing'
    doc = LiveDocument(response.body)
    if doc.html != 1:
        return 'not a complete HTML document'
    if {'noindex', 'none'} & set(doc.robots):
        return 'meta robots prohibits indexing'
    if doc.refresh or 'refresh' in response.headers or any(REDIRECT_JS.search(js) for js in doc.scripts):
        return 'HTML/JavaScript redirect'
    if doc.canonical_outside_head or doc.canonicals != [url]:
        return 'missing, duplicate or non-self canonical in head'
    return None


def required_file(url, fetch):
    response = production_response(url, fetch)
    if response.status != 200 or response.url != url or 'location' in response.headers:
        raise Unavailable(f'Required production file not available without redirect: {url} (HTTP {response.status})')
    return response.body


def run(root=ROOT, *, dry_run=True, manual=False, key='', fetch=request):
    report = {'dry_run': dry_run, 'accepted': [], 'skipped': [], 'blocked': None, 'submitted': 0}
    # Only a literal False opts into submission; unparsed strings must not do so.
    if type(dry_run) is not bool:
        raise ValueError('dry_run must be a boolean')
    if not dry_run and not manual:
        report['blocked'] = 'Submission requires an explicit manual workflow_dispatch on main'
        return report
    try:
        candidates = sitemap_urls((root/'sitemap.xml').read_text(encoding='utf-8'))
        indexable, _ = discover(root)
        live_sitemap = set(sitemap_urls(required_file(BASE+'sitemap.xml', fetch)))
        robots = required_file(BASE+'robots.txt', fetch)
        seen = set()
        for url in candidates:
            reason = 'duplicate sitemap URL' if url in seen else url_reason(url)
            seen.add(url)
            if not reason and url not in indexable:
                reason = 'not a local indexable self-canonical page (missing/noindex/redirect/robots/technical)'
            if not reason and url not in live_sitemap:
                reason = 'not present in the published sitemap'
            if not reason and blocked_by_robots(urlsplit(url).path, robots):
                reason = 'blocked by production robots.txt'
            if not reason:
                reason = page_reason(url, production_response(url, fetch))
            if reason:
                report['skipped'].append({'url': url, 'reason': reason})
            else:
                report['accepted'].append(url)
        if len(report['accepted']) > 10000:
            raise Unavailable('More than 10,000 validated URLs; refusing silent truncation')
        # Validate the existing key in both modes. Never treat key availability
        # as a deployment signal: every page and live sitemap were checked above.
        if not re.fullmatch(r'[a-zA-Z0-9-]{8,128}', key):
            raise Unavailable('Missing or invalid IndexNow key')
        if (root/(key+'.txt')).read_text().strip() != key:
            raise Unavailable('Local key file does not match the existing key')
        if required_file(BASE+key+'.txt', fetch).strip() != key:
            raise Unavailable('Published IndexNow key does not match')
        if not dry_run and report['accepted']:
            payload = json.dumps({'host': 'beqson.com', 'key': key, 'keyLocation': BASE+key+'.txt',
                                  'urlList': report['accepted']}).encode('utf-8')
            response = fetch(ENDPOINT, payload)
            if response.status not in (200, 202) or response.url != ENDPOINT:
                raise Unavailable(f'IndexNow rejected submission: HTTP {response.status}')
            report['submitted'] = len(report['accepted'])
    except (Unavailable, OSError, ValueError) as error:
        report['blocked'] = str(error)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', choices=('true', 'false'), default='true')
    args = parser.parse_args()
    manual = os.environ.get('GITHUB_EVENT_NAME') == 'workflow_dispatch' and os.environ.get('GITHUB_REF') == 'refs/heads/main'
    report = run(dry_run=args.dry_run == 'true', manual=manual, key=os.environ.get('INDEXNOW_KEY', ''))
    for item in report['skipped']:
        print(f'SKIP {item["url"]}: {item["reason"]}')
    for url in report['accepted']:
        print('VALID', url)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report['blocked']:
        raise SystemExit('BLOCKED: '+report['blocked'])
    print('DRY RUN: no URLs submitted' if report['dry_run'] else f'Submitted {report["submitted"]} URLs')


if __name__ == '__main__':
    main()
