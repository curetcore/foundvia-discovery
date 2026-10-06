#!/usr/bin/env python3
"""Short entry point for the existing auditor and local practice lab."""
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    'audit': ROOT / 'skills/foundvia-discovery/scripts/discovery_audit.py',
    'practice': ROOT / 'examples/discovery-lab/run.py',
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print('Usage: python3 discovery.py {audit|practice} [arguments]\n'
              'audit: inspect one public URL; add --help for auditor options.\n'
              'practice: run the controlled local before/after lab.')
        return 0
    command = sys.argv.pop(1)
    if command not in COMMANDS:
        print('Unknown command: ' + command, file=sys.stderr)
        return 2
    sys.argv[0] = str(COMMANDS[command])
    runpy.run_path(sys.argv[0], run_name='__main__')
    return 0


if __name__ == '__main__':
    sys.exit(main())
