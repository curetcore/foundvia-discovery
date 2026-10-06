"""Ensure missing documentation targets fail offline validation."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/check_repository.py'
spec = importlib.util.spec_from_file_location('repository_checks', SCRIPT)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class RepositoryTests(unittest.TestCase):
    def test_missing_image_and_link_are_reported_but_code_and_remote_links_are_not(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'README.md').write_text('[Missing](absent.md)\n<img src="missing.svg">\n'
                                          '[Remote](https://example.com)\n```md\n[Example](example.md)\n```')
            _, errors = checks.check(root)
            self.assertTrue(any('absent.md' in e for e in errors))
            self.assertTrue(any('missing.svg' in e for e in errors))
            self.assertFalse(any('example.md' in e or 'https://' in e for e in errors))
            self.assertTrue(any('Incomplete flagship' in e for e in errors))

    def test_repository_escape_fails_and_valid_encoded_local_path_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'my file.md').write_text('Useful documentation')
            (root / 'README.md').write_text('[Local](my%20file.md)\n[Escape](../outside.md)')
            _, errors = checks.check(root)
            self.assertTrue(any('escapes repository' in e for e in errors))
            self.assertFalse(any('my%20file.md' in e for e in errors))
