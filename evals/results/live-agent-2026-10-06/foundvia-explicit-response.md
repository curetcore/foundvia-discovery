**No obvious discovery blocker was found on the homepage.** I ran the skill’s helper and checked the child sitemap.

| Evidence — observed | Meaning |
|---|---|
| [Homepage](https://foundvia.dev/) returns HTTP 200, with no applicable `noindex` detected in initial HTML or headers. | No initial-response indexing exclusion found. |
| Homepage canonical points to itself; title, description, and H1 are present. | Basic page signals are in place. |
| [robots.txt](https://foundvia.dev/robots.txt) allows Googlebot and OAI-SearchBot for `/`. | Published rules permit homepage crawling. |
| [Child sitemap](https://foundvia.dev/sitemap-0.xml) returns HTTP 200 and includes the homepage among 13 URLs. | The homepage is listed for discovery. |

**One next action:** Have the site owner inspect `https://foundvia.dev/` in Google Search Console’s URL Inspection. Check whether it is indexed and whether Google selected the same canonical. That provides the missing evidence before proposing a fix.

Actual indexing, ChatGPT citations, rendered HTML, and real crawler access were **not checked**. No website code or settings were changed.
