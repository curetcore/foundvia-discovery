<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/discovery-cover-dark.svg">
  <img src="assets/discovery-cover-light.svg" alt="Foundvia Discovery. You shipped it. Now get found. Audit, fix, verify." width="1200">
</picture>

# Foundvia Discovery

**Find what blocks your public SaaS pages on Google and ChatGPT. Fix one verified problem. Measure the next step.**

An open-source toolkit from [Foundvia](https://foundvia.dev), built by [Ronaldo Paulino](https://x.com/ronaldships). A small Python auditor, a coding-agent skill, and a practical guide for your first 100 visits.

[Start auditing](#run-your-first-audit) · [First 100 visits](playbook/first-100-visits.md) · [Español](README.es.md)

**Python 3.10+ · No runtime dependencies · [MIT code and docs](LICENSE)**

## Run your first audit

From your terminal, with Git and Python installed:

```bash
git clone https://github.com/ronaldships/foundvia-discovery.git
cd foundvia-discovery
```

Audit **one intended public page**. Replace the URL with yours:

```bash
python3 skills/foundvia-discovery/scripts/discovery_audit.py \
  https://your-site.com > audit.md
```

Open `audit.md` in your editor. Each finding includes **evidence, a next action and a verification step**. No account or API key is needed.

The auditor reads the initial page response, robots rules and one sitemap. It does not render JavaScript, impersonate a crawler, or prove indexing, rankings or traffic. [Options and limits →](docs/auditor.md)

## See a blocker become a verified change

Try the controlled local example:

```bash
python3 examples/discovery-lab/run.py
```

Open `outputs-local/discovery-lab/before.md`, then `after.md`. The command starts a temporary server on your own computer and stops it afterward.

**Actual local finding:** the public guide contains a generic HTML `noindex` tag. The screenshot below shows an excerpt of the recorded Googlebot finding, presented in a readable report view. [Full generated report →](examples/discovery-lab/sample-results/before.md)

<img src="assets/report-example.png" alt="Recorded local audit excerpt. BLOCK noindex:Googlebot. Evidence: meta robots: noindex. Next: confirm whether exclusion is intentional; remove only on public search pages." width="640">

| Before | One change | After |
|---|---|---|
| Googlebot and OAI-SearchBot noindex blocks | Remove only the accidental noindex element | No observed blocks in the corrected page or clean re-audit |

GPTBot remains blocked in all three stages: training preferences are independent of search access. This example verifies a technical change; it demonstrates no organic growth. [Run and inspect the lab →](examples/discovery-lab/README.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/discovery-path-dark.svg">
  <img src="assets/discovery-path-light.svg" alt="Read the evidence, make one authorized change, rerun and compare. A clear report does not prove traffic." width="640">
</picture>

## Use the skill with your coding agent

Install **just the flagship skill** with the [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add ronaldships/foundvia-discovery \
  --skill foundvia-discovery
```

Then ask:

> Use foundvia-discovery to audit my public page. Show the evidence and propose one small fix in my repo. Keep training preferences and private areas intact. Verify the change; keep deployment separate.

The skill can help inspect, fix, plan a useful page and measure results when you provide the necessary tools, evidence and authorization. The Python auditor also works on its own.

Local copy-install and supplied-artifact evaluation were tested with Codex CLI. Other agents have installation instructions, not a blanket compatibility certification. In the 48-response evaluation, both the skill and model-only baseline passed the case rubric; no pass-rate improvement was demonstrated. [Installation →](docs/install.md) · [Evaluation evidence →](docs/quality-results.md)

## Work toward your first 100 visits

Start with one useful page and a real question from your audience.

1. Check access and fix one accidental blocker.
2. Answer the question with a tested example.
3. Share the answer where it is relevant and permitted.
4. Review measured sessions and product outcomes each week.

The milestone is **100 measured sessions from Google organic and observed ChatGPT referrals**, counted separately and then combined. Sessions are not unique people, signups or sales. There is no promised deadline or provider endorsement.

[Follow the beginner guide →](playbook/first-100-visits.md) · [Copy the weekly tracker →](templates/weekly-tracker.csv)

## Know what the evidence covers

| Component | What it can establish | What needs more evidence |
|---|---|---|
| Python auditor | Initial HTTP/HTML findings, common robots rules, one same-origin sitemap | JavaScript output, real crawler/CDN access, whole-site coverage |
| Agent-assisted work | Scoped proposals or code changes using the tools and evidence you provide | Deployment and live verification remain separate |
| Search Console | Google's reported inspection and search-performance data | A live test does not guarantee indexing or search appearance |
| Analytics | Sessions and outcomes under your documented attribution rules | Missing referrers, copied UTMs and tracking gaps limit attribution |

**Verified locally:** 32 Python tests, a fresh-copy lab run and a three-stage before/after example. The helper declares Python 3.10+; these local runs used Python 3.14.7. [O3 validation](docs/quality-results.md) · [O4 validation](docs/first-visits-validation.md)

## Find the next document

- [First 100 visits](playbook/first-100-visits.md): the main beginner path, with official sources beside each step.
- [Auditor reference](docs/auditor.md): commands, report fields and inspection limits.
- [Launch worksheet](templates/launch-worksheet.md): one question, one page and one next action.
- [Measurement dictionary](templates/measurement.md): how to count without mixing sessions, clicks and sales.
- [Advanced skill modules](skills/README.md): optional reference after the first audit.

## Build this with us

Found a wrong finding? Include a minimal public fixture, the command you ran, and expected versus actual behavior. Please remove credentials and customer data before sharing.

Run the Python checks locally:

```bash
python3 -m unittest discover -s tests -v
```

[Contributing](CONTRIBUTING.md) explains the workflow. If the toolkit helped you find a real issue, a star helps other builders discover it. Contributions with reproducible evidence make it more useful.

---

Code and documentation: [MIT](LICENSE). Identifying Foundvia assets: [brand provenance](docs/brand.md). Geist font: [SIL OFL 1.1](assets/fonts/OFL.txt). [Editable graphics and exports](assets/README.md).
