# Practice: remove one accidental noindex

Run from the repository root with Python 3.10+. No account, agent, package install or public deployment is needed.

```bash
python3 examples/discovery-lab/run.py
```

Open `outputs-local/discovery-lab/before.md`, then `after.md`. The server is temporary, binds only to your own computer, chooses an unused port and stops when the command finishes. Its URLs will not work afterward.

| Stage | Served page | Expected report | CLI exit with `--fail-on-block` |
|---|---|---|---|
| Before | Useful public guide with generic HTML `noindex` | Googlebot and OAI-SearchBot noindex blocks | 1 |
| After | Same guide with only that meta element removed | No observed blocks | 0 |
| Clean | Re-audit the already corrected guide | No observed blocks; no further fix needed | 0 |

The runner saves HTML snapshots, JSON and Markdown reports, and `summary.json`. Compare `before.html` and `after.html`: only `<meta name="robots" content="noindex">` disappears. The training preference remains `GPTBot: Disallow: /` in every stage. Its informational finding is expected.

This is a teaching fixture, not a hosted SaaS or evidence of Google indexing, ChatGPT recommendations, visits or sales. The blank schema count is informational: this tutorial does not need invented Product or FAQ schema to pass. The third stage teaches when to stop changing technical settings and work on the reader's question instead.

`summary.json` measures **server ready → first CLI JSON report**. It excludes Python/Git installation, cloning, reading, editing and human decision time. Use it as a local reproducibility measurement, never as a promise that a beginner can fix a live site in five minutes.

Want to audit your own public page next? Follow [the first 100 visits guide](../../playbook/first-100-visits.md). See [auditor limits](../../docs/auditor.md) before changing anything.

## Recorded local run

Inspect the checked-in [before report](sample-results/before.md), [after report](sample-results/after.md), [clean report](sample-results/clean.md) and [measurement summary](sample-results/summary.json). The loopback port and timestamps belong to that one run; regenerate your own files with the command above. The sample URLs are not public links.
