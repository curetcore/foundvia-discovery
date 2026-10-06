# Read this before filling the weekly tracker

Copy [weekly-tracker.csv](weekly-tracker.csv) into your spreadsheet. It starts empty: no fabricated success figures. Save a copy of [launch-worksheet.md](launch-worksheet.md) beside it.

## Set the count once

Choose one start date, one analytics platform, one session definition and one timezone. Weeks use inclusive start/end dates with no overlap. The first row starts on your milestone start date; the next begins the day after the previous row ends. Use completed weeks, not partial exports. If your tool later revises a count, update that row and all following cumulative totals.

Use the analytics platform's **session-level acquisition** dimensions consistently. Define Google organic in that platform. For observed ChatGPT referrals, use `utm_source=chatgpt.com` on arrival; when absent, use an exact parsed referrer hostname of `chatgpt.com` or `chat.openai.com`. Record your rule and any conflicts in the worksheet. Apply one mutually exclusive channel assignment per session. If your tool only offers event-level counts, do not relabel them as sessions; configure a suitable session report before starting this milestone.

Test with a link you control using `?utm_source=chatgpt.com` (or `&utm_source=chatgpt.com` when a query already exists). Check its landing attribution in your tool's documented report, then exclude that test from your milestone. This tests collection only: a tag can be copied and does not prove ChatGPT generated the visit. Check that the parameter survives any redirects. Use the provider's published reporting delay before expecting to see it.

Do not override every later page view with a new source. If a UTM and a referrer disagree, follow and document your platform's session-attribution rules, then ensure the two exported counts cannot overlap. Do not add raw hostname pageviews to channel session totals. Missing referrers, consent choices, blocked analytics and copied tags limit the result; unknown/direct stays separate.

## Columns

| Column | Meaning / rule |
|---|---|
| `week_start`, `week_end` | Inclusive `YYYY-MM-DD` dates in `reporting_timezone` |
| `reporting_timezone` | Same named timezone each row |
| `google_organic_sessions` | Filtered session count for the configured Google organic channel |
| `chatgpt_sessions` | Filtered observed ChatGPT session count, excluding any session in the Google column |
| `combined_target_sessions` | Google + ChatGPT for this row only |
| `cumulative_target_sessions` | Sum of target sessions since the start date, including this row once |
| `other_sessions` | All other measured sessions, including direct/social/other search/AI; excluded from the target |
| `activated_users_all_channels` | Distinct users completing the worksheet's meaningful action during this week, across all channels |
| `signups_all_channels` | Successful new account creations this week, across all channels |
| `new_paying_customers_all_channels` | Distinct customers with their first confirmed payment this week, across all channels; not invoice creation or trial starts |
| `google_impressions`, `google_clicks` | Search Console Performance, Web search, same property/dates; diagnostic only |
| `top_landing_page` | Public landing page URL/path from your session report |
| `change_made` | One factual change; “none” is valid |
| `evidence_reference` | Export filename or redacted reference supporting the counts |
| `notes` | Missing data, rule changes, provider revisions or next question |

Product outcomes deliberately cover **all channels** here. They are not a Google/ChatGPT conversion funnel, and dividing them by target sessions would give a misleading conversion rate. Cohort/channel conversion analysis needs separate linked user/event records and definitions. Retention, revenue and refunds are also separate analyses.

A user may appear in activation counts in multiple weeks; do not sum weekly distinct users and call that lifetime unique users. Confirmed first payments need a stable customer identifier in your private payment system; the public tracker contains aggregates only.

## Arithmetic and missing data

Blank = not measured or unavailable. `0` = measured and zero. Never silently replace blank source counts with zero. Leave combined/cumulative blank while a required source count is missing; resume only when the missing measurement is resolved or you explicitly start a new, documented baseline.

Example arithmetic only: a week with 12 Google sessions and 3 observed ChatGPT sessions has 15 target sessions. If the previous cumulative count was 20, the new count is 35. Search Console's 18 clicks are **not** added. These figures are invented to explain arithmetic, not results from this project.

OpenAI's tagged referral guidance: [Publishers and Developers FAQ](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq). The exact-host fallback and tracker rules are this project's measurement convention. Search Console definitions: [Performance report](https://support.google.com/webmasters/answer/7576553). [Return to the guide](../playbook/first-100-visits.md).
