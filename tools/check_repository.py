#!/usr/bin/env python3
"""Check local documentation links and the self-contained flagship package.

Offline structural validation, not a provider-guidance or agent-quality score.
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.git', 'node_modules', 'outputs-local', '.agents', '.codex'}


def check(root):
    errors = []
    files = [p for p in root.rglob('*.md') if not IGNORED.intersection(p.relative_to(root).parts)]
    for path in files:
        text = path.read_text(encoding='utf-8')
        # Commands/examples inside fenced code blocks aren't navigation links.
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        targets = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text)
        targets += re.findall(r'(?:src|srcset|href)="([^"]+)"', text)
        for target in targets:
            target = target.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            candidate = (path.parent / unquote(parsed.path)).resolve()
            if not candidate.is_relative_to(root.resolve()):
                errors.append(f'{path.relative_to(root)}: link escapes repository: {target}')
            elif not candidate.exists():
                errors.append(f'{path.relative_to(root)}: missing local target: {target}')
    skill = root / 'skills/foundvia-discovery'
    for item in ('SKILL.md', 'LICENSE', 'agents/openai.yaml', 'scripts/discovery_audit.py',
                 'references/discovery.md', 'references/measurement.md', 'references/report-template.md'):
        if not (skill / item).is_file():
            errors.append('Incomplete flagship skill: ' + item)
    return files, errors


def main():
    files, errors = check(ROOT)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Repository integrity passed: {len(files)} Markdown files; local targets and flagship files present.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
