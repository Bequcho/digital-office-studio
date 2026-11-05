# Static build sources and regression checks

`python tools/build.py` owns the root fallback, three homepages, 24 profession
pages, 404, SVG sprite and manifest. It discovers sitemap entries from all
indexable HTML, preserving the other generators' pages, robots rules and CRM.
It does not run historical installation workflows or publish anything.

## Source ownership

- `build.py`: page composition, shared header/footer, core profession layout,
  sprite paths, manifest and asset versions.
- `content.json`: shared localized copy and the original core sections.
- `industries.json`: profession identities, visible hero headlines/intros,
  concept image data and core features.
- `home_sections.json`: current prices/currencies and localized audit,
  calculator/GEO promo variants, industry cards, hero stylesheet versions and Clutch content.
  `industries.additionalCards` belongs only to the three public homepages; the
  root fallback keeps its historic card inventory.
- `industry_sections.json`: localized editorial data for profession details,
  pricing and FAQ; each profession declares section placement and whether its
  details replace or supplement the original generic sections.
- `build_components.py`: shared rendering for these sections (not page copies).
- `templates/home-hero-*.html`: existing hero text/layout components.
- `templates/home-media-*.html`: approved hero illustrations and orbit markup,
  composed only into public homepages, not the historic root fallback.
- `templates/home-work-*.html`: approved localized project galleries. These
  section sources replace the obsolete case + portfolio-teaser composition on
  public homepages. They are read directly; builds never extract from output HTML.
- `templates/home-audit-style.html`: the existing inline audit-strip stylesheet,
  moved into a shared source without changing its rendered bytes.
- `seo_metadata.json`, `seo_hreflang.py`, `seo_schema.py`, `seo_social.py`:
  existing centralized SEO generation; visible content does not override them.

The root is a redirect with its established Georgian fallback. Its historic
fallback pricing and social tags are deliberately preserved separately from
`/ka/`; changing those is outside this build-repair task. The 404 metadata and
all asset cache versions are also preserved. The optional hreflang render order
preserves existing HTML serialization without changing any language targets.

The initial synchronization baseline is commit `f2841a62`. Later approved
content changes should update the source and generated HTML together. Do not
use one-off scripts that patch output HTML as the permanent source of content.

## Verification

Run `python tools/test_build.py` and `git diff --check` before accepting a build.
The regression suite:

1. Copies the current checkout into a temporary directory, without `.git`.
2. Deletes all HTML/assets owned by the generator, so skipping generation or
   copying existing output cannot pass.
3. Rebuilds and compares every file byte-for-byte with the approved checkout,
   including non-generated pages, styles, images, robots, sitemap and CRM.
4. Builds again and checks idempotence.
5. Checks prices/currencies, lead scripts/styles, section inventory, home tools,
   portfolio, lawyer sections and root redirect explicitly.
6. Runs the existing metadata/language/hreflang, schema, sitemap and social tests
   against the rebuilt copy.

No network access, git writes, publishing, CRM operations or form submissions
are part of the test. Tests use Python's standard library and do not modify
application files in the working checkout. For an intentional content change,
review and update generated output rather than weakening the comparison.

This repair does not change the separate audit-localization, audit-entry or
IndexNow workflows. Their previously identified issues remain separate work.

## Homepage reproducibility repair

The initial P0 repair preserved the approved homepage markup at `f0f7cce` byte-for-byte, including
motion assets, cache versions, ten industry cards and the current project gallery.
The GEO promo keeps `geo-home-strip`; it must not render as a second plain
`audit-home-strip`. Audit, calculator and GEO intentionally share the base class.
The root fallback, profession pages, SEO and public assets remain unchanged.

On Windows use the installed Python 3.12 executable with `PYTHONUTF8=1` and
`PYTHONDONTWRITEBYTECODE=1`. No extra packages are needed for the build itself.

## Offline validation contract

`site_contract.py` lists the 24 current route families independently of discovery
and sitemap. Tests require each family in all three languages (72 URLs), exact
technical routes, reciprocal head hreflang and English x-default. Source fragments
under `tools/templates` are validated through generated pages, not as URLs.

The central schema/social updater owns the original pages and tools. Dedicated
AI, GEO, Shopify, Meta Ads and showcase pages retain their own representations:
Service/CreativeWork objects, graphs with optional IDs, SVG or external Shopify
images, and Twitter Open Graph fallbacks. Showcase pages currently have no JSON-LD;
this is intentional and does not excuse malformed or missing schema elsewhere.
Core pages retain all original strict schema, image dimensions, metadata and
updater-isolation checks. Technical redirects and the private CRM have explicit
structure/noindex rules. Audit JavaScript HTML strings are not document doctypes.

Run `test_build.py`, `test_site.py`, `test_indexnow.py` and `test_project_covers.py`.
The build suite also runs all four SEO suites, site validation and the negative
controls in `test_validation.py` in its rebuilt copy. Negative controls corrupt
canonical, hreflang, schema, social metadata, resources, anchors and SVG symbols,
and remove a public route. They must fail validation; fixtures remain temporary.

Two source defects were repaired: the autoservice `map` symbol now uses the existing
location artwork, and Motion Lab declares English x-default in its owning generator.
No browser, CRM request, deployment or IndexNow submission is involved.

## Shared lead dialog

`assets/lead-system.js` owns the localized dialog markup, validation, network
payloads and modal lifecycle for all three languages. `assets/lead-system.css`
owns its layout and stacking. No page HTML needs regeneration for these changes.
The close button must remain above the positioned heading for pointer hit testing.
The dialog temporarily preserves/restores background inert states, traps keyboard
focus only while open, and clears open/close timers before reopening. Required
name/contact/message fields trim edges, retain internal text and use localized
custom validity messages. Contact formats and CRM payload fields are unchanged.

Run `tools/test_lead_modal.py` with the isolated Playwright Python environment
and `CHROMIUM_PATH` pointing to an existing browser when needed. It checks all
RU/KA/EN × 320/375/390/430/768/1024/1440 widths with mouse, touch, keyboard and
mock CRM/email responses. Its virtual local origin is served from repository
files via Playwright; all other requests are mocked or aborted. It requires no
production access, local server or additional application dependencies.

The dialog touch-close test opens with the keyboard to isolate its own control;
the separate touch-launcher integration matrix exercises real touch open and
close. The previous KA/320 failure is repaired by the responsive source changes
below; keep the integration gate without force clicks or skips.

## Responsive regression repair

The mobile audit/GEO promo layout belongs to `templates/home-audit-style.html`.
It uses a shrinkable single grid track and wrapping CTA text. After editing this
source, run `build.py` to update the inline stylesheet in the three homepages.
The responsive repair deliberately changes those stylesheet bytes; homepage body
content, head metadata, prices and asset versions are preserved.

`styles.css` owns profession hero column/label shrinking. `assets/tools-hub.css`,
`search-preview.css`, `kakheti-showcase.css`, `motion-lab.css` and
`ai-business-service.css` are directly maintained shared stylesheets for their
respective dedicated pages. Their page generators reference these files and do
not own replacement CSS strings. Fix widths/min-content and word wrapping there;
never mask page overflow on html/body. Narrow RU profession headings and the KA
AI heading adapt in size only at the smallest breakpoints to avoid fragmenting
words. Desktop hero/logo animation sources are unchanged.

Run `tools/test_responsive.py` with the same isolated Playwright environment.
It checks the independent 72-route inventory at all seven widths, local images,
actual heading text rectangles, clipping ancestors, control bounds, reduced
motion, mobile menu and AI panel. Intentional overflow:auto/scroll carousels are
checked by scrolling each offscreen control into view and testing its hit target;
a hidden or unreachable control still fails. Negative controls recreate the old
GEO overflow, clipped AI heading and an inaccessible carousel. Optional
`BEQSON_RESPONSIVE_OUTPUT` stores JSON/screenshots outside the repository.

## Audit and FORME HOME language navigation

`audit/index.html` is the maintained Russian source and the legacy `/audit/`
alias (canonical `/ru/audit/`). Its compact header language navigation is
localized by `scripts/localize_audit.py`; each link keeps the audit route family.
To regenerate the three localized audit pages without reverting the existing
translation/PDF corrections, run the complete existing pipeline in order:

```
python scripts/localize_audit.py
python scripts/fix_audit_i18n.py
python scripts/install_audit_pdf_v3.py
```

`ru/forme-home/index.html`, `ka/forme-home/index.html` and
`en/forme-home/index.html` are directly maintained localized showcase sources,
not outputs of `build.py` or the separate WordPress theme/blueprint. Edit their
small header language component directly; do not regenerate the showcase from
the demo theme. `assets/page-languages.css` scopes the shared language styles
and responsive header arrangement to these two interfaces. Content, demo links,
canonical/hreflang/x-default and the main site's header remain independent.

Run `tools/test_language_navigation.py` with the existing Playwright Python
environment. It verifies reciprocal same-family links against the independent
public route inventory and SEO metadata, recreates audit outputs from sources,
and repeats the full localization pipeline byte-for-byte. The browser matrix
checks all six pages at seven widths with mouse, native Tab/Shift+Tab/Enter and
touch, including visible focus, current-language styling, hit targets and page
overflow. Negative controls remove or misroute links and hide, clip or cover
the navigation. `BEQSON_LANGUAGE_OUTPUT` optionally stores screenshots and the
completed input/transition matrix outside the repository. All external traffic
is blocked; no audit, CRM, email or WordPress Playground request is submitted.

## BEQSON Signature Motion

`assets/home-motion.css` and `assets/home-motion.js` own the homepage signature.
The original RGBA `beqson-mark-v3.png` remains the visible image, unchanged;
its alpha channel masks only temporary light overlays. Do not substitute the
different geometry in `logo.svg`. The 2.6-second signature reveals the mark,
then the existing shaped wordmark (without splitting glyphs), then a brief glow.
The enhancement removes its class on completion and has a bounded cleanup timer.
Decode/font preparation reserves layout and falls back to the visible static
logo after at most 1.2 seconds; asset failure cannot leave the wordmark hidden.
Session storage prevents replay between homepage languages within the same tab.
Unavailable storage, JavaScript or reduced motion all retain the static logo.
The existing compact wordmark-only layout at 320 px is preserved.

The homepage generator owns cache versions for these two assets. Regenerate
the three homepages after changing those versions. Hero animations and client
projects are independent and must remain intact.

Run `tools/test_signature_motion.py` with the existing Playwright environment.
It checks all three languages at seven widths, static fallbacks, stable header
geometry and session navigation. Set `BEQSON_SIGNATURE_OUTPUT` to a directory
outside the repository to record real-time desktop/mobile WebM videos and
deterministic keyframes. Video capture uses Playwright's official FFmpeg helper.
