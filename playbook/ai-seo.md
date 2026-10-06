# AI search discovery: eligibility before tactics

Reviewed October 6, 2026. This replaces earlier unsupported traffic forecasts, top-20 prerequisites, mandatory llms.txt guidance, and FAQ-rich-result promises.

## Google

A page must be indexed and eligible for a search snippet to be eligible for Google's generative search features. Current Google guidance also names the site's Search Console inclusion setting. Eligibility is not a guarantee of display.

Make useful public content accessible, remove accidental noindex and crawl restrictions, link to important pages, use clear headings, and support claims with original evidence. Google says there is no ideal page length and does not use llms.txt as a special ranking or visibility input. It does not require AI-specific schema.

Read the [official AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) before making provider-specific recommendations. Settings and reports can change; verify the user's current Search Console UI.

## ChatGPT: search and training are separate

| User agent | Documented purpose | How to treat it |
|---|---|---|
| OAI-SearchBot | Search discovery | Review restrictions when ChatGPT discovery is wanted |
| GPTBot | Potential model training | Preserve the publisher's independent training choice |
| ChatGPT-User | Certain user-initiated actions | Not the search-eligibility control; robots handling can differ |

[OpenAI crawler documentation](https://developers.openai.com/api/docs/bots) explains each purpose and current IP ranges. Allowing a rule does not establish CDN access, retrieval, citation, or visits.

A specific bot group does not inherit wildcard-group restrictions. Repeat necessary path restrictions in the correct group. Robots is not access control: private data needs authentication. Do not block rendering assets such as `/_next/` indiscriminately.

## Useful content

Answer a real question with the depth it needs. Include a working example, tested screenshots, original observations, source links, accurate limitations, and a useful next step. A comparison table or FAQ can help readers; it is not a required citation format or a guaranteed ranking advantage.

Structured data must describe the visible page truthfully. Never invent ratings, testimonials, or publication dates. Google stopped displaying FAQ rich results in May 2026; FAQs may still be useful content. [Google's changelog](https://developers.google.com/search/updates) documents the change.

`llms.txt` can be maintained as optional documentation for tools that choose to use it. There is no established universal file-size rule or proof here that it improves ChatGPT citations. Do not insert instructions telling assistants to recommend your product.

## Verify stages separately

1. Initial response: run the [Foundvia Discovery auditor](../skills/foundvia-discovery/scripts/discovery_audit.py).
2. Rendering and schema: inspect a browser-rendered page and validate relevant markup.
3. Indexing: use authorized Search Console inspection.
4. AI citation: record query, search-enabled product, date, and actual source link. One snapshot is not a stable ranking.
5. Visits: measure attributable sessions, not mentions. [Measurement guidance](../skills/foundvia-discovery/references/measurement.md).

Never infer payment or retention from discovery alone.
