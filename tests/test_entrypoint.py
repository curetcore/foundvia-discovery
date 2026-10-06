"""Verify the README's short commands forward to the existing tools."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'discovery.py'


class EntrypointTests(unittest.TestCase):
    def test_audit_arguments_and_error_exit_are_forwarded(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), 'audit', '--help'], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn('--fail-on-block', proc.stdout)
        proc = subprocess.run([sys.executable, str(SCRIPT), 'audit', 'invalid', '--format', 'json'], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn('http', proc.stderr.lower())

    def test_practice_works_outside_repo_and_forwards_output(self):
        with tempfile.TemporaryDirectory() as folder:
            proc = subprocess.run([sys.executable, str(SCRIPT), 'practice', '--output', 'practice-output'], cwd=folder, capture_output=True, text=True, timeout=30)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            summary=json.loads(proc.stdout)
            self.assertEqual(summary['stages']['before']['exit_code'], 1)
            self.assertEqual(summary['stages']['after'], {'exit_code':0,'blocks':[]})
            self.assertTrue((Path(folder)/'practice-output/clean.md').is_file())

    def test_unknown_command_is_an_error(self):
        proc=subprocess.run([sys.executable,str(SCRIPT),'publish'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2)
        self.assertIn('Unknown command',proc.stderr)
