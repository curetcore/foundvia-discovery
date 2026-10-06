**The audit could not retrieve the site. This does not prove the site is broken.** `127.0.0.1` refers to the machine running the audit, rather than a public website.

| Status | Resources | Evidence → consequence |
|---|---|---|
| Observed | `http://127.0.0.1:1/`, `/robots.txt`, `/sitemap.xml` | All returned “Connection refused”; no HTTP response or content was available. |
| Not checked | Those resources | Metadata, indexing directives, canonical URLs, schema, and crawler rules could not be evaluated. Google or ChatGPT visibility remains unverified. |

**Next action:** Confirm the intended address in your browser. For a public discovery audit, supply the public website URL. Then rerun the helper and verify that it retrieves the page and crawl resources before recommending changes.

No website code or settings were changed.
