"""Negative controls: corrupt temporary fixtures and exercise production validators."""
import contextlib
import io
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import test_site
from test_seo_metadata import check
from test_seo_schema import validate
from test_seo_social import validate as social
from site_contract import URLS

ROOT=Path(__file__).resolve().parents[1]

class ValidationTests(unittest.TestCase):
    def test_metadata_rejects_corruption(self):
        source=(ROOT/'en/index.html').read_text()
        check(source,canonical='https://beqson.com/en/',hreflang=True)
        mutations=[source.replace('rel="canonical"','rel="broken"',1),
                   source.replace('hreflang="x-default"','hreflang="unknown"',1),
                   source.replace('hreflang="ru"','hreflang="en"',1),
                   source.replace('<title>','<title></title><title>',1)]
        for changed in mutations:
            with self.subTest(change=changed[:70]), self.assertRaises(AssertionError):
                check(changed,canonical='https://beqson.com/en/',hreflang=True)

    def test_schema_rejects_missing_malformed_duplicate_and_wrong_identity(self):
        from seo_schema import SCHEMA_RE
        for route in ('en/','en/ai-consultant/','en/meta-static-ads/','en/shopify/','en/geo/'):
            source=(ROOT/route/'index.html').read_text();validate(source,route)
            raw=SCHEMA_RE.search(source).group()
            for changed in (source.replace(raw,''),source.replace(raw,raw+raw),
                            source.replace(raw,'<script type="application/ld+json">{</script>'),
                            source.replace('https://beqson.com/'+route,'https://beqson.com/wrong/')):
                with self.subTest(route=route), self.assertRaises((AssertionError,ValueError,KeyError)):
                    validate(changed,route)

    def test_social_rejects_missing_duplicate_and_wrong_image(self):
        for route in ('en/','en/ai-consultant/','en/geo/','en/shopify/'):
            source=(ROOT/route/'index.html').read_text();social(source)
            for changed in (source.replace('property="og:image"','property="broken"'),
                            source.replace('</head>','<meta property="og:title" content="duplicate"></head>'),
                            source.replace('property="og:image" content="https://','property="og:image" content="http://')):
                with self.subTest(route=route), self.assertRaises((AssertionError,KeyError,ValueError)):
                    social(changed)

    def test_inventory_resources_links_and_svg_negative_controls(self):
        with TemporaryDirectory(prefix='beqson-negative-') as directory:
            root=Path(directory)/'site'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__','.agents','.codex'))
            def run(method):
                with patch.object(test_site,'ROOT',root), contextlib.redirect_stdout(io.StringIO()):
                    test_site.SiteTests.setUpClass()
                    result=unittest.TestResult()
                    test_site.SiteTests(method).run(result)
                    return result.wasSuccessful()
            for method in ('test_routes_and_language','test_local_references_and_anchors','test_icon_sprite_references'):
                self.assertTrue(run(method),method)
            page=root/'en/index.html';original=page.read_bytes()
            for fragment,method in [('<img src="/missing-image.png">','test_local_references_and_anchors'),
                                    ('<script src="/missing.js"></script>','test_local_references_and_anchors'),
                                    ('<link rel="stylesheet" href="/missing.css">','test_local_references_and_anchors'),
                                    ('<a href="/en/#missing-anchor">broken</a>','test_local_references_and_anchors'),
                                    ('<a href="/en/missing/">broken</a>','test_local_references_and_anchors'),
                                    ('<img srcset="/missing.webp 320w">','test_local_references_and_anchors'),
                                    ('<svg><use href="/assets/icons.svg#missing-symbol"></use></svg>','test_icon_sprite_references')]:
                page.write_text(original.decode().replace('</body>',fragment+'</body>'),encoding='utf-8')
                with self.subTest(fragment=fragment):self.assertFalse(run(method))
                page.write_bytes(original)
            missing=root/'en/ai-consultant/index.html';missing.unlink()
            self.assertFalse(run('test_routes_and_language'))
            from build_sitemap import discover
            self.assertNotEqual(set(discover(root)[0]),URLS)

if __name__=='__main__':unittest.main(verbosity=2)
