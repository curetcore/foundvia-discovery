#!/usr/bin/env python3
"""Print SKILL.md paths for an explicit local evaluation override; writes no config."""
import json
import os
from pathlib import Path

paths = set()
for root in (Path.home() / '.codex/skills', Path.home() / '.agents/skills'):
    visited = set()
    for directory, children, files in os.walk(root, followlinks=True):
        real = Path(directory).resolve()
        if real in visited:
            children[:] = []
            continue
        visited.add(real)
        if 'SKILL.md' in files:
            entry = Path(directory) / 'SKILL.md'
            paths.update((str(entry), str(entry.resolve())))
print(json.dumps(sorted(paths), indent=2))
