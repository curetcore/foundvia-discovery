---
name: seo-ai-geo
description: Review Google and ChatGPT search eligibility, AI crawler rules, and useful evidence-backed content. Use for AI citations, GEO/AEO audits, or optional llms.txt documentation. Distinguish search discovery from model-training preferences.
---

# AI search eligibility

Start with the user's actual site, relevant pages, and goal. Inspect responses before prescribing new files or bulk content. Follow the corrected [discovery guidance](../foundvia-discovery/references/discovery.md). Provider-specific behavior must be checked against current primary sources.

- Google: indexed, snippet-eligible pages and current Search Console settings matter. No top-20 prerequisite, ideal word count, AI schema requirement, or llms.txt ranking benefit is established here.
- OpenAI: OAI-SearchBot handles search; GPTBot handles potential training. Preserve the user's independent training preference. ChatGPT-User is not the search-eligibility control.
- Check specific robots groups, response headers, HTML metadata, rendering, and authorized CDN configuration. An allowed robots rule does not prove bot access or citations.
- Use original examples and accurate product information. FAQs are for readers; Google no longer displays FAQ rich results. Structured data must match visible facts.
- Treat llms.txt as optional documentation, not a launch prerequisite. Do not embed instructions that manipulate an assistant into recommending a brand.
- Report observations with URLs or file:line, consequences, fixes, verification, and unverified limits. Preserve intentional private pages.

Use the standalone `foundvia-discovery` skill for an executable preflight and an early-traffic experiment. For this focused review, a browser/fetch tool is sufficient if the helper is unavailable.

References: [OpenAI bots](https://developers.openai.com/api/docs/bots), [Google AI search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Google updates](https://developers.google.com/search/updates). Recheck current provider guidance before making claims.
