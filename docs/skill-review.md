# Public skill review

Reviewed October 6, 2026. This is a source-level design review of four relevant public skills, not a claim to have audited every skill or proven superior model performance. Popularity is not a correctness test. We reviewed the instructions; we did not execute third-party agents or installers.

## Sources and reproducibility

| Skill | Pinned source | What it does well | Limitation relevant to this project | Our design response |
|---|---|---|---|---|
| Corey Haines: seo-audit 2.0.1 | [SKILL.md](https://github.com/coreyhaines31/marketingskills/blob/dda3841f0b294e01e93b1541486beefbfab0915e/skills/seo-audit/SKILL.md) | Prioritizes access/indexing, reuses product context, requires evidence/fix/priority, warns about static-vs-rendered schema | Broad audit scope and some rigid title/description targets; mentions the retired Mobile-Friendly Test | A bounded preflight with explicit observation limits; no fixed-length ranking failures |
| Corey Haines: ai-seo 2.7.2 | [SKILL.md](https://github.com/coreyhaines31/marketingskills/blob/dda3841f0b294e01e93b1541486beefbfab0915e/skills/ai-seo/SKILL.md) | Separates search, training, and user retrieval; encourages query/citation baselines and original evidence | Some platform claims and fixed answer lengths are stronger than official sources establish; reporting claims can drift | Primary-source references, independent bot policy, measured sessions, and no guaranteed citation format |
| Vercel: web-design-guidelines 1.0.0 | [SKILL.md](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines/SKILL.md) | Narrow entrypoint, latest source rules, concise file:line findings | Needs an external rules fetch; it is a UI reviewer, not a discovery auditor | Short entrypoint with local references and executable fallback; URL/file evidence |
| Anthropic: skill-creator | [SKILL.md](https://github.com/anthropics/skills/blob/683bc88e56f3e09ba94f7055977f3d3aa499f202/skills/skill-creator/SKILL.md) | Realistic prompts, assertions, iteration, and with/without-skill evaluation | Describes an evaluation process; it does not establish that this new skill works | Publish runnable helper tests and honest behavioral cases; evaluate supplied-artifact reasoning and preserve limits |

These are independent projects. There is no endorsement or affiliation. The new instructions are written for Foundvia Discovery; the comparison is attribution, not a copied skill pack.

Provider claims should be checked against [Google's AI search guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Google's updates](https://developers.google.com/search/updates), and [OpenAI's bots documentation](https://developers.openai.com/api/docs/bots). For example, Google's updates document the 2023 retirement of the Mobile-Friendly Test and the 2026 removal of FAQ rich results.

## Problems in our own original pack

| Finding | Why it matters | Change |
|---|---|---|
| Hash-generated publication/update dates | Stable output does not establish real editorial history | Removed generators; explicit record validation and migration notes |
| GPTBot classified as search traffic | Search and training preferences are independent | Corrected AI skill and guide |
| Mandatory llms.txt / FAQ-rich-result claims | Not supported by current Google guidance | Corrected all focused references in O3 |
| Traffic forecasts without attributable evidence | Acquisition is not guaranteed and does not establish payment | Removed from the landing page; blank measurement templates |
| No first-step standalone helper | User could get a long plan without verifying basic access | Bundled Python preflight, JSON output, controlled HTTP tests |

## What has actually been tested

Run `python3 -m unittest discover -s tests -v` for rule parsing, bot separation, scoped noindex directives, redirects, response failures, truncation, sitemap selection, and CLI exit behavior. The dates helper has a separate executable test. These establish helper behavior for controlled cases, not rankings or agent judgment.

Behavioral cases in [evals/discovery-cases.json](../evals/discovery-cases.json) cover launch, existing traffic losses, training-policy preservation, frontend rendering, attribution, injection, and permission boundaries. [48 controlled responses](../evals/results/2026-10-06-review.json) were manually reviewed with three repetitions per condition. Both conditions passed all case assertions (24/24 each); this small authored benchmark does not demonstrate uplift or a global ranking. Two operational timeouts and their successful retries are retained separately. See [evaluation procedure](../evals/README.md) and [module review](module-review.md) for boundaries.

To evaluate: give a capable agent a case and only its raw artifacts; run with and without the skill in isolated copies; score evidence, correction accuracy, scope, and usefulness. Record model/version, prompt, artifacts, output, duration, and the reasons for every assertion. Repeated runs are needed before interpreting differences.
