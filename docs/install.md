# Install Foundvia Discovery

## Skills CLI

```bash
npx skills add ronaldships/foundvia-discovery --skill foundvia-discovery
```

The [Vercel Labs CLI](https://github.com/vercel-labs/skills) lets you select the target agent and installation scope. Review those choices rather than silently enabling every module. Listing available skills does not require installing them:

```bash
npx skills add ronaldships/foundvia-discovery --list
```

## Manual install

Clone the repository, then copy the **whole folder**, including scripts, references and assets. Create the appropriate directory if needed:

```bash
# Codex
mkdir -p ~/.codex/skills
cp -R skills/foundvia-discovery ~/.codex/skills/

# Claude Code
mkdir -p ~/.claude/skills
cp -R skills/foundvia-discovery ~/.claude/skills/
```

Choose one command for the agent you use. Restart or reload the agent if it does not discover the new skill. Other agents may use different paths; consult their own documentation.

The skill does not include a background service, analytics account, paid API, or automatic deployment. Python 3.10+ is needed for the bundled helper; without it, an agent can inspect resources manually and state what it could not verify.

## Verified candidate environment

O3 tested a local project copy using Skills CLI 1.7.0 targeting Codex, including the whole flagship folder and its helper. Codex CLI 0.157.0 with gpt-6-astra was evaluated on supplied artifacts. A later [live Codex smoke check](live-agent-validation.md) observed selection for one relevant request and actual helper execution on two public projects plus an inaccessible control. Other agents and universal automatic selection remain unverified. Manual paths above are installation examples, not a compatibility certification. The Python helper ran on Python 3.14.7; the copyable TypeScript helper checks ran with React 19.2.0 and Node 22.18.0/24.20.0. A full Next.js app build was not tested. The public install command installs the published branch, not an unpublished local candidate.

The HTML renderer requires `assets/report.html` and the bundled font files. Keep the whole skill folder when installing. Code and documentation use MIT; Geist uses the [SIL Open Font License](../skills/foundvia-discovery/assets/fonts/OFL.txt).
