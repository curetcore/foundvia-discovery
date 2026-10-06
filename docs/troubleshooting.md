# Get a useful audit result

## Every finding is UNKNOWN

Read **Access problem — audit incomplete** first. UNKNOWN means the tool could not check something; it does not mean your website failed every SEO check.

1. Check the public URL opens while signed out.
2. Run `python3 discovery.py audit https://YOUR-PUBLIC-SITE.com --format json` from the repo folder.
3. Look at `resources[].error` and `resources[].status`. A DNS failure, timeout, certificate error, HTTP rate limit, or blocked environment needs a different remedy. Increasing timeout will not fix every error.
4. If the site opens in a browser but fails in your agent, use the browser or another available fetch tool to inspect the page, `/robots.txt`, and the intended sitemap. Keep the failed attempt in the report.

Keep TLS verification enabled. Do not make private pages public or change firewall/training preferences simply to get a passing report.

## The skill gives generic advice or cannot find its helper

Confirm the whole skill folder was installed, including `scripts/` and `references/`. Use your agent's documented reload mechanism if the new skill is not discovered. Start with an explicit request containing your public URL:

> Use foundvia-discovery to audit https://YOUR-PUBLIC-SITE.com. Run its helper if available, explain the evidence and limitations, and propose one useful next action. If access fails, explain why rather than guessing.

The skill instructs your existing agent; it does not supply internet access, an analytics account, or an autonomous background service. Automatic selection and compatibility with every agent have not been certified.

## PASS, INFO and an incomplete summary appear together

Individual resources are independent. A page may load while robots or the sitemap fail. PASS applies to that check only. INFO can mean an index was read but its children were not fetched. Even a completed summary covers only this helper's declared scope; indexing and rendered JavaScript still require separate evidence.

## How to report a bug

Use the repository's **Incorrect or incomplete audit** issue form. Include the public URL or a minimal fixture, exact command/prompt, tool and Python versions, expected behavior, and redacted output. Never include private tokens or customer data.

[Auditor options](auditor.md) · [Back to the quickstart](../README.md)
