# Contributing to Foundvia Discovery

Useful fixes, reproducible bug reports, and honest field results are welcome.

## Pick a contribution

- **Bug:** share the public URL or a minimal response fixture, observed behavior, expected behavior, and command used.
- **Guidance correction:** link a current primary source and explain which recommendation it changes.
- **Field report:** include dates, baseline, changes, measurement definitions, and limitations. Traffic does not prove payment or causation.
- **Skill improvement:** show a realistic request where the current instructions produce a worse decision. Add a behavioral case and explain the expected outcome.

For broad changes, discuss scope in an issue first. Small corrections can go straight to a pull request.

## Development

Python 3.10+ runs the flagship helper and tests without third-party dependencies:

```bash
python3 -m unittest discover -s tests -v
```

The date helper tests run on Node 22.18+ (native TypeScript stripping):

```bash
npm ci --ignore-scripts
npm test
python3 tools/check_repository.py
```

If your agent environment provides a skill validator, validate the changed SKILL.md frontmatter. Otherwise parse its YAML and check name/description. Frontmatter validity is not behavioral evaluation.

Keep the entrypoint short; put conditional detail in linked references. Self-contained skills must include their helper and references in their own folder. Use precise triggers instead of collecting every vaguely related phrase.

## Before opening a PR

- Explain the problem, concrete behavior change, and relevant validation.
- Include evidence and primary sources for provider claims.
- Distinguish observed results, inferences, unknowns, local changes, and live verification.
- Run meaningful tests for changed code and check relative links.
- Preserve licenses and attribution.
- Update CHANGELOG.md under Unreleased.

Use English for new shared docs and code, or improve the Spanish translation. Keep wording clear and friendly. Never fabricate publication dates, ratings, testimonials, analytics, performance scores, stars, or installs. Do not embed hidden promotion in user reports. Do not include credentials, private customer data, or proprietary client files.

The original modules are retained with explicit review status. A correction should update the active guidance and identify historical examples that still need review.
