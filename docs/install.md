# Install Foundvia Discovery

## Skills CLI

```bash
npx skills add curetcore/foundvia-discovery --skill foundvia-discovery
```

The [Vercel Labs CLI](https://github.com/vercel-labs/skills) lets you select the target agent and installation scope. Review those choices rather than silently enabling every module. Listing available skills does not require installing them:

```bash
npx skills add curetcore/foundvia-discovery --list
```

## Manual install

Clone the repository, then copy the **whole folder**, including scripts and references. Create the appropriate directory if needed:

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
