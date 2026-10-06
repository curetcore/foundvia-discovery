"""The teaching example must demonstrate one real change, not fabricated growth."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lab', ROOT / 'examples/discovery-lab/run.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class LabTests(unittest.TestCase):
    def test_before_after_clean_and_training_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            summary = lab.run(folder)
            self.assertEqual(summary['stages']['before']['exit_code'], 1)
            self.assertEqual(set(summary['stages']['before']['blocks']), {'noindex:Googlebot', 'noindex:OAI-SearchBot'})
            self.assertEqual((folder / 'before.html').read_text().replace(lab.NOINDEX, ''), (folder / 'after.html').read_text())
            self.assertEqual((folder / 'after.html').read_bytes(), (folder / 'clean.html').read_bytes())
            for stage in ('after', 'clean'):
                self.assertEqual(summary['stages'][stage], {'exit_code': 0, 'blocks': []})
            for stage in ('before', 'after', 'clean'):
                report = json.loads((folder / (stage + '.json')).read_text())
                training = next(f for f in report['findings'] if f['check'] == 'robots:GPTBot')
                self.assertEqual(training['status'], 'info')
                self.assertIn('Disallowed', training['evidence'])
                self.assertTrue((folder / (stage + '.md')).read_text().startswith('# Discovery audit'))
            self.assertGreater(summary['first_json_report_seconds'], 0)
