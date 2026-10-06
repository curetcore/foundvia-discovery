# Search and training bot policies

| Bot | Purpose | Policy |
|---|---|---|
| OAI-SearchBot | OpenAI search discovery | Review rules for pages intended for search |
| GPTBot | Potential model training | Independent publisher choice |
| ChatGPT-User | Certain user-initiated actions | Not the search eligibility control |

Use [OpenAI documentation](https://developers.openai.com/api/docs/bots) for current behavior and IP ranges. Do not classify training access as search access. For other vendors, look up their current official documentation before recommending a policy; this repository does not certify a universal list.

Specific user-agent groups do not inherit wildcard restrictions. Repeat appropriate private-path restrictions in each relevant group, and use authentication for private data. An allowed rule does not prove CDN bot access, indexing, or citations.
