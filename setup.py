#!/usr/bin/env python
from __future__ import absolute_import, print_function
from setuptools import setup, find_packages

import sys
if sys.version_info[0] >= 3:
    import builtins
else:
    import __builtin__ as builtins
builtins.__PKG_SETUP__ = True


def get_requirements():
    with open('./requirements.txt', 'r') as f:
        reqs = f.read().splitlines()
    return reqs


def setup_package():
    import numpy.distutils.misc_util
    from gofft.distutils.misc_util import get_extensions
    NP_DEP = numpy.distutils.misc_util.get_numpy_include_dirs()

    # semantic versioning
    MAJOR = 1
    MINOR = 0
    MICRO = 0
    VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

    # package to be installed
    EXCLUDED = []
    PACKAGES = find_packages(exclude=EXCLUDED)

    REQUIREMENTS = get_requirements()

    EXTENSIONS = get_extensions('gofft')

    metadata = dict(
        name='gofft',
        version=VERSION,
        description='Benchmark for Goertzel algorithm and scipy.fftpack.fft',
        url='https://github.com/NaleRaphael/goertzel-fft',
        packages=PACKAGES,
        ext_modules=EXTENSIONS,
        include_dirs=NP_DEP,
        install_requires=REQUIREMENTS
    )

    setup(**metadata)


if __name__ == '__main__':
    try:
        setup_package()
    except Exception as ex:
        print(ex)

    del builtins.__PKG_SETUP__
