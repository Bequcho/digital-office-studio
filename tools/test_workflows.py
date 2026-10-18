#!/usr/bin/env python3
"""Validate workflows and simulate local Python generation, never publishing.

Requires PyYAML (tools/requirements-workflows.txt). GitHub runners/actions and
external services are not emulated. IndexNow is inspected, never executed.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
IGNORE = shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache', '.agents', '.codex')
HEREDOC = re.compile(r"python(?:3)? - <<'PY'\n(.*?)\nPY", re.S)


class UniqueLoader(yaml.BaseLoader):
    pass


def mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def load(path):
    return yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueLoader)


def validate(path, data):
    assert isinstance(data, dict) and data.get('name') and data.get('on') and data.get('jobs'), path
    assert set(data) <= {'name', 'run-name', 'on', 'permissions', 'env', 'defaults', 'concurrency', 'jobs'}, path
    # This repository uses only these expressions. Fail closed on additions so
    # unsupported expression syntax cannot silently pass this bounded validator.
    expressions = re.findall(r'\$\{\{(.*?)\}\}', path.read_text(), re.S)
    assert all(x.strip() in {'github.event.before', 'github.sha', 'inputs.dry_run'} for x in expressions), (path, expressions)
    for name, job in data['jobs'].items():
        assert job.get('runs-on') and job.get('steps'), (path, name)
        ids = [s['id'] for s in job['steps'] if 'id' in s]
        assert len(ids) == len(set(ids)), (path, 'duplicate step ids')
        for step in job['steps']:
            assert ('uses' in step) != ('run' in step), (path, step)
            if 'if' in step:
                match = re.fullmatch(r"steps\.([\w-]+)\.outputs\.([\w-]+) != '0'", step['if'])
                assert match and match[1] in ids, (path, step['if'])
                producer = next(s for s in job['steps'] if s.get('id') == match[1])
                assert 'GITHUB_OUTPUT' in producer.get('run', '') and match[2]+'=' in producer['run']
            run = step.get('run', '')
            for code in HEREDOC.findall(run):
                ast.parse(code, filename=str(path))
            shell = re.sub(r'\$\{\{.*?\}\}', 'VALIDATED_EXPRESSION', run)
            checked = subprocess.run(['bash', '-n'], input=shell, text=True, capture_output=True)
            assert checked.returncode == 0, (path, checked.stderr)
            if 'git push' in run:
                assert data.get('permissions', {}).get('contents') == 'write', path
                assert not re.search(r'git push.*(?:--force|\s-f\b)', run), path
                assert not any(key in s.get('with', {}) for s in job['steps'] for key in ('token', 'ssh-key')), path
    return data


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}


# Runs only local Python in a separate process. No git, shell, API or browser
# commands execute here. Deny network/process creation and writes outside copy.
SANDBOX = r'''
import sys, runpy, os
from pathlib import Path
def install_guard(directory):
    def guard(event, args):
        if event.startswith(('socket.', 'subprocess.')) or event in ('os.system', 'os.exec', 'os.posix_spawn'):
            raise RuntimeError('External action blocked: ' + event)
        if event == 'open' and isinstance(args[0], (str, bytes)):
            path = Path(os.fsdecode(args[0])).resolve()
            mode, flags = args[1:3]
            writes = (mode and any(x in mode for x in 'wax+')) or (flags and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
            if writes and not path.is_relative_to(directory):
                raise RuntimeError('Write outside simulation: ' + str(path))
    sys.addaudithook(guard)
install_guard(Path.cwd().resolve())
kind, *arguments = sys.argv[1:]
if kind == 'file':
    sys.argv = arguments
    sys.path.insert(0, str(Path(arguments[0]).resolve().parent))
    runpy.run_path(arguments[0], run_name='__main__')
else:
    exec(compile(sys.stdin.read(), '<workflow>', 'exec'), {'__name__': '__main__'})
'''


def simulate(path, data, root):
    calls = 0
    for job in data['jobs'].values():
        for step in job['steps']:
            run = step.get('run', '')
            blocks = HEREDOC.findall(run)
            remaining = HEREDOC.sub('', run)
            files = re.findall(r'^\s*python(?:3)? ([\w/.-]+\.py)([^\n]*)', remaining, re.M)
            operations = [('inline', code, []) for code in blocks]
            operations += [('file', script, args.split()) for script, args in files
                           if not script.startswith('tools/test_')]
            for kind, content, args in operations:
                cmd = [sys.executable, '-B', '-c', SANDBOX, kind]
                if kind == 'file':
                    cmd += [content, *args]
                result = subprocess.run(cmd, cwd=root, input=content if kind == 'inline' else '',
                                        text=True, capture_output=True, timeout=60)
                assert result.returncode == 0, f'{path.name} / {step.get("name")}:\n{result.stderr}'
                calls += 1
    return calls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--localization-only', action='store_true')
    args = parser.parse_args()
    workflows = {p: validate(p, load(p)) for p in sorted((ROOT/'.github/workflows').glob('*.yml'))}
    print(f'PASS: {len(workflows)} YAML workflows; duplicate keys, Python, shell, used expressions and write permissions')
    indexnow = next(d for p, d in workflows.items() if p.name == 'indexnow.yml')
    assert set(indexnow['on']) == {'workflow_dispatch'}, 'IndexNow must never run automatically'
    inputs = indexnow['on']['workflow_dispatch']['inputs']
    assert inputs['dry_run']['type'] == 'boolean' and inputs['dry_run']['default'] == 'true'
    submit = indexnow['jobs']['submit']['steps'][-1]
    assert submit['env']['DRY_RUN'] == '${{ inputs.dry_run }}'
    assert submit['env']['INDEXNOW_KEY'] == '9a97aa27a069ea0350203fe532357c06'
    assert submit['run'] == 'python tools/indexnow.py --dry-run "$DRY_RUN"'
    assert indexnow['permissions'] == {'contents': 'read'}
    calls = 0; count = 0
    with TemporaryDirectory(prefix='beqson-workflow-regression-') as directory:
        root = Path(directory)/'site'
        shutil.copytree(ROOT, root, ignore=IGNORE)
        baseline = snapshot(root)
        for path, data in workflows.items():
            if args.localization_only and path.name != 'localize-audit-pages.yml':
                continue
            # Read-only validation job is tested by running this script itself.
            # IndexNow is NEVER executed, including its detection/network steps.
            if data.get('permissions', {}).get('contents') != 'write':
                continue
            calls += simulate(path, data, root)
            after = snapshot(root)
            changes = sorted(n for n in baseline.keys() | after.keys() if baseline.get(n) != after.get(n))
            assert not changes, f'{path.name} changes approved files: {changes}'
            count += 1
            print('PASS:', path.name, '(no file changes)')
        # Explicitly check all localized audit graphs/locales, not just equality.
        for language, locale in [('ka','ka_GE'), ('ru','ru_RU'), ('en','en_US')]:
            source = (root/language/'audit/index.html').read_text()
            assert f'<html lang="{language}">' in source
            assert f'<meta property="og:locale" content="{locale}">' in source
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
            assert len(blocks) == 1
            graph = json.loads(blocks[0])['@graph']
            assert [e['@type'] for e in graph] == ['Organization','WebSite','WebPage','WebApplication']
            page = graph[2]
            assert page['inLanguage'] == language and page['url'] == f'https://beqson.com/{language}/audit/'
        # Explicit second pass for idempotence of audit localization and PDF v3.
        path = next(p for p in workflows if p.name == 'localize-audit-pages.yml')
        calls += simulate(path, workflows[path], root)
        assert snapshot(root) == baseline, 'Localization not idempotent'
    print(f'PASS: {count} local workflows, {calls} Python steps; all site files/SEO/CRM preserved; IndexNow not executed')


if __name__ == '__main__':
    main()
