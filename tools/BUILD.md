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
  calculator, industry cards, portfolio teaser and Clutch content.
- `industry_sections.json`: localized editorial data for profession details,
  pricing and FAQ; each profession declares section placement and whether its
  details replace or supplement the original generic sections.
- `build_components.py`: shared rendering for these sections (not page copies).
- `templates/home-hero-*.html`: existing hero components.
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
