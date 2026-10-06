---
name: seo-analytics
description: Interpret authorized Search Console and analytics data for organic acquisition, AI referrals, or traffic changes. Use for reporting and attribution; keep clicks, sessions, activation, and payment distinct and investigate established-site drops before proposing launch content.
---

# Organic and AI referral measurement

Identify the metric, date range, timezone, property, filters, and comparison period before calculating anything. Read authorized exports or connected analytics; if data is unavailable, provide a blank plan instead of invented totals.

## Interpret correctly

- Search Console clicks and analytics sessions measure different events. Do not add them together or assume they should match.
- Use parsed referrer hostnames, not substring matching: chatgpt.com.evil.example is not chatgpt.com. Check exact approved hosts and, where appropriate, their true subdomains.
- Keep ChatGPT UTM attribution (utm_source=chatgpt.com) separate from referrer attribution. Session-level deduplication is needed when both are present.
- Bing traffic alone does not prove Copilot; direct traffic is unknown without other evidence. State consent, redirects, referrer loss, and sampling limits.
- Separate visits, registrations, activation, returning users, and payments. Only compare consistent definitions and filters. No universal CTR, organic-share, or indexed-page target is meaningful for every site.

## Investigate a decline

For an established site's drop, compare affected pages, queries, countries, devices, search types, and equivalent dates. Align the change with migrations, redirects, canonicals, noindex, index coverage, and release history. Prioritize evidence that distinguishes hypotheses; do not announce a cause from correlation alone.

## Instrument carefully

Reuse the project's analytics and consent conventions. Send the minimum needed event fields; avoid raw full URLs, query tokens, personal data, and duplicate subscriptions. Check real events with a controlled visit and cleanup during component unmount. Do not copy an untested tracking hook into production.

Deliver source → calculation → result → limits → next investigation. For early acquisition, use [measurement guidance](../foundvia-discovery/references/measurement.md). Source: [OpenAI publisher referral guidance](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq).
