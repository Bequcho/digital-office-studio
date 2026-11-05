"""Recreate approved portfolio output from sources, offline and without git writes."""
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import unittest
import subprocess
import sys
import test_workflows as workflows


class ProjectsBuildTests(unittest.TestCase):
    def test_schema_cli_ownership(self):
        with TemporaryDirectory(prefix='beqson-schema-ownership-') as directory:
            root = Path(directory) / 'site'
            shutil.copytree(workflows.ROOT, root, ignore=workflows.IGNORE)
            before = workflows.snapshot(root)
            for arguments in ([], [], ['--check']):
                result = subprocess.run([sys.executable, '-B', 'tools/seo_schema.py', *arguments],
                                        cwd=root, capture_output=True, text=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(before, workflows.snapshot(root))

    def test_recreate_and_repeat(self):
        with TemporaryDirectory(prefix='beqson-projects-regression-') as directory:
            root = Path(directory) / 'site'
            shutil.copytree(workflows.ROOT, root, ignore=workflows.IGNORE)
            before = workflows.snapshot(root)
            path = root / '.github/workflows/build-projects-portfolio.yml'
            data = workflows.load(path)
            for lang in ('ru', 'ka', 'en'):
                (root / lang / 'projects/index.html').unlink()
            (root / 'projects/index.html').unlink()
            for iteration in (1, 2):
                workflows.simulate(path, data, root)
                self.assertEqual(before, workflows.snapshot(root), f'Generation {iteration}')
            # Missing source components and maintained runtime must fail closed.
            for source in ('tools/templates/projects-cards-ru.html', 'assets/projects.js'):
                target = root / source
                saved = target.read_bytes()
                target.unlink()
                try:
                    with self.subTest(source=source):
                        with self.assertRaises(AssertionError):
                            workflows.simulate(path, data, root)
                finally:
                    target.write_bytes(saved)


if __name__ == '__main__':
    unittest.main(verbosity=2)
