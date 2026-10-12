# BEQSON Lead CRM v1

BEQSON is evolving from a static multilingual studio website into a lead-management platform.

## Current live layer

- Multilingual lead form injected across public site pages (RU / KA / EN)
- Captures name, contact, industry, website, goal and budget
- Captures attribution: referrer, UTM source / medium / campaign, page URL and language
- Tracks WhatsApp, Telegram and email clicks through a common analytics event layer
- Temporary submission transport: FormSubmit AJAX -> `digitalstudiobeqson@gmail.com`
- Responsive modal UI with basic validation and honeypot spam field

## Planned production backend

1. Supabase PostgreSQL database using `supabase-schema.sql`
2. Supabase Edge Function for validated public lead intake
3. Authenticated `/crm/` dashboard
4. Pipeline: New -> Contacted -> Proposal -> Won -> In progress -> Done / Lost
5. Telegram/email notification on new lead
6. AI lead summary, lead score and recommended package
7. Proposal generator and client onboarding
8. Analytics dashboard and payment status integration

## Security rule

GitHub Pages is a public frontend. Service-role keys, payment secrets and private CRM credentials must never be committed to this repository or exposed in browser JavaScript. Public submissions should go through a server-side function.