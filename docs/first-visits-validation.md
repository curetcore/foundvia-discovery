# First 100 visits guide: validation

October 6, 2026 · O4 local candidate · Python 3.14.7 on macOS.

## Delivered

- [English beginner path](../playbook/first-100-visits.md) with six ordered steps; each has Action, Expected and Check.
- [Spanish summary](../playbook/first-100-visits.es.md).
- [One-page launch worksheet](../templates/launch-worksheet.md), [empty weekly CSV](../templates/weekly-tracker.csv) and [measurement dictionary](../templates/measurement.md).
- [Runnable local lab](../examples/discovery-lab/README.md) and recorded HTML / JSON / Markdown for before, after and a clean re-audit.

## Checked behavior

`python3 -m unittest discover -s tests -v` passed **32 tests**: the 31 existing auditor tests and one new integration test covering all three lab stages. The new test verifies actual CLI exit codes, Google/OpenAI noindex findings, the one-element HTML difference, unchanged training policy and generated reports. No helper or Next.js implementation changed in O4; their unrelated suites were not rerun.

A fresh source-file copy with no installed project packages ran the documented lab command successfully. Git and Python were already installed on the host. The lab performs loopback HTTP requests only and shuts down its temporary server.

| Stage | Observed noindex blocks | Exit with `--fail-on-block` |
|---|---|---|
| Before | Googlebot and OAI-SearchBot | 1 |
| After | None | 0 |
| Clean re-audit | None | 0 |

The corrected page is byte-identical to the before page after removal of its noindex element. GPTBot stays disallowed and informational. “No observed blocks” remains a bounded preflight result, not search eligibility certification.

In that clean-copy run, server-ready to first JSON report took **0.0874 seconds**; the full three-stage lab process took **0.9776 seconds**. This excludes prerequisite installation, clone/download, reading and human actions. It does not establish that a beginner reaches a useful report or fixes a live site in five minutes. No five-minute marketing claim is published.

Nine changed Markdown entry/guide files had their local links checked. The CSV has 17 columns and eight empty rows with consistent widths. Missing data is distinct from zero; outcomes cover all channels and are not mislabeled as a channel conversion funnel. `git diff --check` passed.

## Beginner walkthrough review

This is an author walkthrough, **not an independent beginner usability study**.

| Decision a beginner faces | Guide answer / verification |
|---|---|
| Which skill do I install? | None needed for the guide; one terminal command runs the bundled auditor |
| Which URL do I inspect? | One intended public page, with an explicit replacement placeholder |
| Where is the output? | A named Markdown file opened in the editor |
| What do I fix first? | One observed accidental block, using its evidence; unknown requires investigation |
| What if nothing is blocked? | Stop technical edits and move to one real customer question |
| What does Search Console success mean? | Property verification, live inspection and indexed status remain distinct |
| How do I share? | One useful answer, venue rules, ownership disclosure and approval when acting for someone |
| What counts toward 100? | Non-overlapping Google organic and observed ChatGPT sessions, never clicks or sales |

## Current primary sources

The guide links claims next to the relevant steps. Checked live October 6, 2026:

- [Search Console property setup](https://support.google.com/webmasters/answer/34592).
- [URL Inspection](https://support.google.com/webmasters/answer/9012289).
- [Sitemaps report](https://support.google.com/webmasters/answer/7451001).
- [Google recrawl guidance](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).
- [Search Console Performance](https://support.google.com/webmasters/answer/7576553).
- [OpenAI crawler overview](https://developers.openai.com/api/docs/bots).
- [OpenAI publisher referral FAQ](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq).
- [Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content).

## Remaining boundaries

No live production change, Google property setup, real analytics integration, publishing, outreach or organic growth experiment was executed. Windows instructions and the declared Python 3.10 minimum were not locally tested in O4. GitHub-hosted CI has not run for this unpublished branch. Remote install/clone instructions will receive release verification when the candidate is published; clean-copy validation here uses local candidate files.

O5 owns the complete README and visual redesign. O6 owns release/publication. Historical publisher snapshot bytes remain unchanged; their index now identifies their age and unverified status. The private Foundvia application was not modified or copied.
