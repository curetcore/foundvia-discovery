# Live agent checks — October 6, 2026

These checks exercise **actual skill reading and helper execution**, beyond the archived text-only benchmark. Three requests ran once each in separate temporary Codex projects containing the copied flagship skill. No target website code or settings were changed.

## Observed results

| Request | Agent behavior | Result |
|---|---|---|
| Explicit Foundvia audit of foundvia.dev | Read the installed skill and references, ran the helper, then inspected a same-origin child sitemap | Homepage HTTP 200; 8 PASS / 4 INFO; child sitemap contained 13 URLs including the homepage. Next action: owner-authorized Search Console inspection |
| Discovery audit of karrito.app without naming Foundvia | Selected the flagship by relevance, read it, and ran the helper | Homepage HTTP 200; 8 PASS / 4 INFO. Correctly disclosed that sitemap children and real indexing were not checked |
| Explicit audit of a deliberately inaccessible loopback URL | Read and ran the helper; explained connection refusal and the meaning of localhost | 5 UNKNOWN; did not invent metadata, ranking, or visibility failures; asked for the intended accessible URL |

All 15 authored behavioral assertions passed in same-author manual review. This is a small smoke check, not a statistical score or independent judgment. The script did not supply expected assertions to the agent.

## Environment and limitations

Codex CLI 0.157.0; default CLI model, with no model override. The subprocess used workspace-write sandboxing and network access for public fetches. Existing ChatGPT CLI authentication was used; no paid API key was configured or purchased. The skill's source commit and helper hash are recorded in the manifest.

The tests used isolated **project folders**, not a proven exclusive skill catalog. Other skills and tools could be available. The test set a 2,000-token skill-catalog budget. The inaccessible-URL run emitted a context-budget warning that removed skill descriptions; it still explicitly opened and executed Foundvia. That warning is preserved in the review record rather than hidden or treated as a clean catalog test.

The karrito.app run demonstrates selection for this one relevant request in this environment. It does not certify every wording, Claude Code/Cursor/other agents, or all model versions. A completed initial-response audit does not prove real crawler access, JavaScript rendering, indexing, citations, conversions, or growth. The local failure control is not a reproduction of a specific user's unknown setup.

## Evidence

[Manifest](../evals/results/live-agent-2026-10-06/manifest.json) · [Command receipts, warnings and assertion review](../evals/results/live-agent-2026-10-06/review.json) · [Run completion records](../evals/results/live-agent-2026-10-06/runs.json)

- Foundvia: [request](../evals/results/live-agent-2026-10-06/foundvia-explicit-request.txt), [response](../evals/results/live-agent-2026-10-06/foundvia-explicit-response.md), [helper JSON](../evals/results/live-agent-2026-10-06/foundvia-explicit-audit.json).
- Karrito: [request](../evals/results/live-agent-2026-10-06/karrito-trigger-request.txt), [response](../evals/results/live-agent-2026-10-06/karrito-trigger-response.md), [helper JSON](../evals/results/live-agent-2026-10-06/karrito-trigger-audit.json).
- Inaccessible control: [request](../evals/results/live-agent-2026-10-06/unreachable-request.txt), [response](../evals/results/live-agent-2026-10-06/unreachable-response.md), [helper JSON](../evals/results/live-agent-2026-10-06/unreachable-audit.json).

Full private event traces remain in the task workspace. Public records include the prompts, final responses, actual helper JSON and shell command receipts; they do not purport to contain every intermediate browser/web tool event. No personal runtime logs or global configuration paths are published.
