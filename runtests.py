#!/usr/bin/env python
from __future__ import absolute_import, print_function
import unittest
import logging


def _check_extension_is_built():
    import os.path
    import sys

    if sys.version_info[0] >= 3:
        import builtins
    else:
        import __builtin__ as builtins
    builtins.__PKG_SETUP__ = True

    from gofft.distutils import get_extensions

    all_extensions_are_built = True
    exts = get_extensions('gofft')

    for ext in exts:
        fext = '.pyd' if sys.platform == 'win32' else '.so'
        fn = os.path.join(*ext.name.split('.'))
        fn = os.path.abspath('{}{}'.format(fn, fext))
        if not os.path.exists(fn):
            all_extensions_are_built = False
            break

    del builtins.__PKG_SETUP__
    return all_extensions_are_built


def _build_ext():
    from subprocess import Popen, PIPE, STDOUT
    cmd = 'python setup.py build_ext --inplace clean --all'
    proc = Popen(cmd.split(' '))
    out, _ = proc.communicate()


def run_test():
    if not _check_extension_is_built():
        logging.error('Some extensions are not built. Trying to build them...')
        _build_ext()

    loader = unittest.TestLoader()
    tests = loader.discover('.')
    unittest.TextTestRunner().run(tests)


if __name__ == '__main__':
    run_test()
