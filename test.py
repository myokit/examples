#!/usr/bin/env python3
#
# Tests all notebooks
#
import os
import re
import subprocess
import sys

import nbconvert
import requests

# Natural sort regex
_natural_sort_regex = re.compile(r'([0-9]+)')

# Markdown link regex
_markdown_link_regex = re.compile(r'\[([^]]+)\]\(([^\s]+)\)')

# Don't check links twice
_checked_links = {}


def test_notebooks(links=False):
    """
    Tests all example notebooks.

    If ``links==True`` the notebook code will not be tested, but the notebook
    links will be tested instead.
    """
    # Known errors, or directories to avoid
    ignore = [
        'data',
        'figures',
        'models',
        'venv',
    ]

    # Work in progress
    ignore.extend([
        # 'real-data-2-capacitance-and-resistance.ipynb',
        # 'real-data-3-xxx.ipynb',
        '0-1-before-you-begin.ipynb',
    ])

    # Extensions to check
    allowed_extensions = ['.ipynb']
    if links:
        allowed_extensions.append('.md')

    # Scan directory, running notebooks as we find them.
    def scan(root, failed=None):
        if failed is None:
            failed = []

        for filename in sorted(os.listdir(root), key=natural_sort_key):
            if filename in ignore:
                continue
            path = os.path.join(root, filename)

            # Test notebooks
            if os.path.splitext(filename)[1] in allowed_extensions:
                print('Testing ' + path + '.'*(max(0, 70 - len(path))), end='')
                sys.stdout.flush()

                if links:
                    res = check_links(root, filename)
                else:
                    res = test_notebook(root, filename)
                if res is None:
                    print('ok')
                else:
                    if links:
                        failed.append((path, res))
                    else:
                        failed.append((path, *res))
                    print('FAIL')

            # Recurse into subdirectories
            elif os.path.isdir(path):
                # Ignore hidden directories
                if filename[:1] == '.':
                    continue
                scan(path, failed)

        return failed

    failed = scan('.')
    if failed:
        if links:
            for path, msg in failed:
                print('-' * 79)
                print('Link issues in: ' + path)
                print(msg.strip())
                print()
        else:
            for path, stdout, stderr in failed:
                print('-' * 79)
                print('Error output for: ' + path)
                print((stdout + stderr).replace('\\n', '\n').strip())
                print()

        print('-' * 79)
        print('Test failed (' + str(len(failed)) + ') error(s).')
    else:
        print('Test passed.')


def test_notebook(root, path):
    """
    Tests a notebook in a subprocess; returns ``None`` if it passes or a tuple
    (stdout, stderr) if it fails.
    """
    # Load notebook, convert to python
    e = nbconvert.exporters.PythonExporter()
    code, _ = e.from_filename(os.path.join(root, path))

    # Remove coding statement, if present
    code = '\n'.join([x for x in code.splitlines() if x[:9] != '# coding'])

    # Tell matplotlib not to produce any figures
    env = os.environ.copy()
    env['MPLBACKEND'] = 'Template'

    # Run in subprocess
    cmd = [sys.executable, '-c', code]
    curdir = os.getcwd()
    try:
        os.chdir(root)
        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
        )
        stdout, stderr = p.communicate()
        # TODO: Use p.communicate(timeout=3600) if Python3 only
        if p.returncode != 0:
            # Show failing code, output and errors before returning
            return (stdout.decode('utf-8'), stderr.decode('utf-8'))
    except KeyboardInterrupt:
        p.terminate()
        return ('', 'Keyboard Interrupt')
    finally:
        os.chdir(curdir)
    return None


def check_links(root, path):
    """
    Checks all (Markdown) links in a given notebook, and checks that they
    resolve. Returns ``None`` if succesfull, or an error message if one or more
    links are broken.
    """
    # Non-local link roots to convert to local root
    convert = [
        'https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/'
        'blob/main/',
    ]

    # Load contents
    if os.path.splitext(path)[1] == '.ipynb':
        # Convert notebook
        e = nbconvert.exporters.MarkdownExporter()
        code, _ = e.from_filename(os.path.join(root, path))
    else:
        # Load as plain text
        with open(os.path.join(root, path), 'r') as f:
            code = f.read()

    # Method to check a local link
    def check_local(href):
        if href[:1] == '/':
            href = href[1:]
        else:
            href = os.path.join(root, href)
        if not os.path.exists(href):
            return f'Unknown path: {href}'

    # Method to check a remote link
    def check_remote(href):
        try:
            response = _checked_links[href]
        except Exception:
            response = _checked_links[href] = requests.head(href).status_code

        if response not in [200, 301, 302]:
            return f'HTTP {response}: {href}'

    # Scan over links, create error message
    errors = []
    for m in _markdown_link_regex.finditer(code):
        name, href = m.groups()

        # Ignore figures inside notebook
        if name == 'png' and href[:7] == 'output_' and href[-4:] == '.png':
            continue
        if name == 'svg' and href[:7] == 'output_' and href[-4:] == '.svg':
            continue

        # Convert selected http/https links to local root
        for pre in convert:
            if href.startswith(pre):
                href = href[len(pre):]
                if href[:1] != '/':
                    href = '/' + href

        # Check link
        if href[:7].lower() in ['http://', 'https:/']:
            ok = check_remote(href)
        else:
            ok = check_local(href)
        if ok is not None:
            errors.append(ok)

    # Join error messages and return
    if errors:
        return '\n'.join(errors)
    return None


def natural_sort_key(s):
    """
    Function to use as ``key`` in a sort, to get natural sorting of strings
    (e.g. "2" before "10").

    Example::

        names.sort(key=natural_sort_key)

    """
    # Code adapted from: http://stackoverflow.com/questions/4836710/
    return [
        int(text) if text.isdigit() else text.lower()
        for text in _natural_sort_regex.split(s)]


if __name__ == '__main__':
    links = 'links' in sys.argv
    if links:
        print('Checking links in all notebooks')
    else:
        print('Running all notebooks!')
    print('This is used for regular online testing.')
    print('If you are not interested in testing the notebooks,')
    print()
    print('  Press Ctrl+C to abort.')
    print()
    test_notebooks(links)
