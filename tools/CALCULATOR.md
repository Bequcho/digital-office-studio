# Services calculator 3.0

This extends Calculator 2.0 on `/ru/calculator/`, `/ka/calculator/` and
`/en/calculator/`. It keeps one primary service per inquiry. Switching categories
keeps each category's selections in memory until the page is reloaded; it does
not silently combine draft categories into one quote.

## Sources

- `assets/website-calculator.js`: existing pricing, service selection, live summary,
  brief export and existing create-lead integration.
- `assets/calculator-config.js`: localized contextual questions and interface copy.
  Questions may apply to a category or selected subtypes. Hidden answers are kept
  for returning to a subtype but excluded from its current summary and payload.
- `assets/website-calculator.css`: standalone calculator styles, mobile estimate
  bar, keyboard focus, reduced motion and print-only brief.
- The three calculator HTML files load configuration before application code.
  Their WebPage metadata is normalized by the existing `tools/seo_schema.py`.
- `tools/home_sections.json` matches the already-approved Calculator 2.0 entry
  points; rebuilding must not revert these homepage teasers.

## Pricing and privacy

Website pricing, rounding, package selection, urgency surcharge and CRM budget
brackets remain unchanged in RUB, GEL and USD. New contextual answers do not
change prices. SEO, automation, design and maintenance have no rates: their
estimate requires a custom quote and their CRM budget stays null. Timelines for
these services express priority, not a guaranteed delivery date or surcharge.

Copy and Print / Save PDF use the same plain-text project brief as the CRM
message. Form contact fields are excluded from exports. Requirements are included
verbatim, with a visible reminder not to enter secrets or personal contacts.
No configuration or contact details are written into shareable URLs or storage.

The existing endpoint, authentication and database payload fields are preserved.
No migration, new secret or backend change is required. Do not test with live leads.

## Validation

With an existing Playwright installation and Chromium:

```sh
python tools/test_calculator.py
```

Set `CHROMIUM_PATH` if Chromium is not at `/usr/bin/chromium`. Optional
`CALCULATOR_SCREENSHOTS=/tmp/calculator-previews` saves visual previews outside
this repository. The browser tests block all external requests and intercept the
CRM endpoint with mock responses. Test-only pricing instrumentation is injected
into the served response, never into production assets.

Seven browser tests cover:

- All 24,576 website price combinations against Calculator 2.0 golden hashes
  (8,192 per currency), including CRM budget brackets.
- All service subtypes and localized contextual controls.
- Category drafts, subtype switching and exclusion of hidden answers.
- Copy, print, clipboard fallback, contact privacy and text escaping.
- Form validation and 15 intercepted CRM payloads across services and languages.
- Failed submission recovery without losing contact input.
- Keyboard focus, labels and overflow at 320, 390, 768 and 1440px in all languages.

Run the existing `tools/test_build.py` and `tools/test_workflows.py` with
`tools/requirements-workflows.txt` installed. Build tests rebuild twice in an
isolated copy, verify zero output drift and run metadata, schema, sitemap and
social regressions. Workflow simulation does not push, deploy or call IndexNow.
The historical RUB migration recognizes already-applied pricing; the calculator
link installer recognizes existing cards by class rather than obsolete copy.
