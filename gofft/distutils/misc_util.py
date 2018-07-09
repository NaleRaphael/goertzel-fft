from __future__ import division, absolute_import, print_function
from distutils.core import setup, Extension
import os
import sys
import logging

__all__ = ['get_extensions']


def get_extensions(top_path):
    setup_files = _find_setup_script_for_extension(top_path)
    extensions = []

    for f in setup_files:
        config = _get_configuration_from_setup(f)
        if config:
            extensions.append(config.get_extension_info())
    return extensions


def _find_setup_script_for_extension(top_path, 
                                     source_dir='src',
                                     setup_py='setup.py'):
    """
    Parameters
    ----------
    top_path : str
        An entry for `os.walk`.
    source_dir : str
        Name of directory where source files locate.
    setup_py : str
        File name of the setup file for C extension.
    """
    top_path = os.path.abspath(top_path)
    setup_files = []

    for root, dirs, files in os.walk(top_path):
        if len(files) == 0:
            continue
        if source_dir in dirs and setup_py in files:
            fp = os.path.abspath(os.path.join(root, setup_py))
            if fp == os.path.abspath(__file__):
                continue
            setup_files.append(fp)
    return setup_files


def _get_configuration_from_setup(setup_file, setup_py='setup.py'):
    """
    Parameters
    ----------
    setup_file : str
        Path of setup file.
    """
    # In case setup_py imports local modules
    cur_fp = os.path.abspath(os.path.dirname(setup_py))
    sys.path.insert(0, cur_fp)

    # Get filename without extension
    name = setup_py.split('.')[0]
    config = None
    try:
        des = ('.py', 'U', 1)  # (suffix, mode, type: PY_SOURCE)
        setup_module = _load_module(name, setup_file, des)

        if not hasattr(setup_module, 'configuration'):
            logging.warn('No configuration avalible in: {}'.format(setup_file))
        else:
            config = setup_module.configuration()
    except:
        raise
    finally:
        del sys.path[0]

    return config


def _load_module(name, fn, info=None):
    """
    Parameters
    ----------
    name : str
        Full module name.
    fn : str
        Path to module file.
    info : optional
        Information as returned by `imp.find_module` (suffix, mode, type)

    Returns
    -------
    mod : module
    """
    import imp

    if info is None:
        path = os.path.dirname(fn)
        fo, fn, info = imp.find_module(name, [path])
    else:
        fo = open(fn, info[1])

    try:
        mod = imp.load_module(name, fo, fn, info)
    finally:
        fo.close()
    return mod
