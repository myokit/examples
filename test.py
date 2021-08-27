#!/usr/bin/env python3
#
# Tests all notebooks
#
import os
import re
import subprocess
import sys

import nbconvert

# Natural sort regex
_natural_sort_regex = re.compile('([0-9]+)')


def test_notebooks():
    """
    Tests all example notebooks
    """
    # Known errors, or directories to avoid
    ignore = [
        'figures',
        'models',
        'venv',
    ]
    # Work in progress
    ignore.extend([
        #'real-data-2-capacitance-and-resistance.ipynb',
        #'real-data-3-xxx.ipynb',
    ])

    def scan(root, failed=None):
        """Scan directory, running notebooks as we find them."""
        if failed is None:
            failed = []

        for filename in sorted(os.listdir(root), key=natural_sort_key):
            if filename in ignore:
                continue
            path = os.path.join(root, filename)

            # Test notebooks
            if os.path.splitext(filename)[1] == '.ipynb':
                print('Testing ' + path + '.'*(max(0, 70 - len(path))), end='')
                sys.stdout.flush()
                res = test_notebook(root, filename)
                if res is None:
                    print('ok')
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
    print('Running all notebooks!')
    print('This is used for regular online testing.')
    print('If you are not interested in testing the notebooks,')
    print()
    print('  Press Ctrl+C to abort.')
    print()
    test_notebooks()
