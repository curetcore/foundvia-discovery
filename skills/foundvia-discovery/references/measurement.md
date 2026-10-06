# Measurement

Default: cumulative analytics sessions attributed to Google organic or ChatGPT from a recorded start date. A returning visitor may create multiple sessions. Keep the analytics tool's definition unchanged and assign each session to one channel.

Track channels separately. Exclude your own testing and known bots where supported. Do not add Search Console clicks to analytics sessions. Keep social, paid, other search, and other AI channels outside the default combined total.

OpenAI documents `utm_source=chatgpt.com` on ChatGPT referral links. Check it alongside recognized referrer hosts and analytics classification. Parse URLs and compare exact hostnames rather than substrings. A UTM is attribution evidence, not authenticated proof; it can be copied or spoofed. Missing referrers mean attribution can be incomplete. Do not infer all direct traffic is AI or all Bing traffic is Copilot.

Preserve first-arrival channel within the session; do not count an AI event on each page view as a new visit. If several signals disagree, use a documented precedence rule and show ambiguous cases separately.

Use non-overlapping date ranges for weekly totals. Combined target sessions = Google organic sessions + ChatGPT sessions. Cumulative target sessions = prior cumulative total + current combined sessions. Use blank for unavailable data, not zero.

Record one product-specific useful action, then signups and payments separately. Traffic does not establish activation, retention, or payment. Manual unbranded ChatGPT questions with search enabled can record citation snapshots; they do not measure visits or stable rankings.

Sources:

- https://help.openai.com/en/articles/12627856
- https://support.google.com/webmasters/answer/7576553

Guidance checked October 6, 2026.
