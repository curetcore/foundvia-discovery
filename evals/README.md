# Behavioral evaluation

The eight cases in discovery-cases.json define assertions before execution. Give the model the request and raw artifacts only. Expected assertions belong in the review record, not in its prompt. Helper tests and source review are separate evidence.

## Controlled text-artifact A/B runs

The opt-in runner uses the existing Codex CLI login; check `codex login status` first. Do not use a paid API without authorized budget. ChatGPT account quota can be consumed. Pin an available model and record the CLI version:

```bash
python3 evals/scripts/list_skill_paths.py > /tmp/foundvia-disabled-skills.json
python3 evals/scripts/run_codex.py --output /absolute/new/evaluation-folder --model MODEL --workers 1 --disable-skills-file /tmp/foundvia-disabled-skills.json
```

Before the main run, use the same CLI flags with a no-tool prompt asking which skills appear in the developer catalog; verify NONE and inspect raw events. The runner disables supplied local skill paths only for its subprocesses, sets the catalog budget to one token, and uses strict config validation. It does not modify global configuration or remove installed skills. CLI behavior can change; stop on configuration warnings rather than claiming isolation.

There are 8 cases × 2 conditions × 3 repetitions = 48 responses. Each isolated run receives the same base instructions and artifacts; the skill condition additionally receives the flagship entrypoint and its three references. The order alternates by repetition. No expected assertions are sent. Candidate file hashes, exact prompts, raw events, responses, usage, timing, model, and return status are saved. An existing output folder is rejected to preserve prior results.

The common instruction forbids browsing/tools because this benchmark tests reasoning from supplied artifacts. Read-only sandboxing also constrains possible effects. Report unexpected tool attempts as protocol deviations; do not quietly discard or replace them. The test does not establish autonomous live crawling, real writes/deployments, or automatic skill selection.

## Review procedure

Read each full response and mark every case assertion pass, partial, or fail, with a reason or short supporting excerpt. A run meets all assertions only if every one passes. Record protocol deviations separately. Do not grade from keyword presence. Do not treat a missing detail as a wrong claim unless the assertion requires that detail.

Report per-case counts, failures, tradeoffs such as longer responses, and limits. A small authored benchmark with same-author review cannot establish superiority over other skills or general model uplift. A fixed correct answer may leave little room for improvement; that is a valid outcome. Do not change criteria after viewing results to manufacture a win.

## Candidate iteration record

The first exploratory round completed 48 responses on the existing local profile. One response reported skill-catalog truncation, so it is not used for a controlled uplift claim. The scope fixture also lacked code necessary for its concrete-patch assertion; the second round adds actual source and intended visibility before execution. Expected assertions remain unchanged. The flagship now explicitly rejects artificial publication staggering after that appeared as unnecessary advice in the exploratory responses. Preserve both rounds, identify their different candidates/fixtures, and report the clean round separately.

## Results — October 6, 2026

[Manual review](results/2026-10-06-review.json) · [manifest](results/2026-10-06-manifest.json) · [responses and runtime records](results/2026-10-06-responses.json) · [frozen candidate](results/2026-10-06-candidate.txt) · [retry manifest](results/2026-10-06-retries.json). Both conditions passed 24/24 case sets. This demonstrates no pass-rate improvement. Median response length was 111 words without the skill and 159 with it; median successful-call time was 13.971s versus 19.301s. These timing samples are operational observations, not stable model-speed benchmarks. Two 120-second timeouts were retained and retried with identical candidate hashes and configuration; 50 attempts yielded 48 reviewed responses. Catalog-removal warnings are preserved separately from tool calls (zero observed). No real credentials were supplied in injection fixtures.
