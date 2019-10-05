from __future__ import division, absolute_import, print_function
from distutils.core import setup, Extension
import os
import sys

__all__ = ['Configuration']

EXTARGS = ['include_dirs', 'define_macros', 'undef_macros', 'library_dirs',
           'libraries', 'runtime_library_dirs', 'extra_objects', 
           'extra_comple_args', 'extra_link_args', 'export_symbols',
           'swig_opts', 'depends', 'language']


class Configuration(object):
    def __init__(self, package_name, sources, **kwargs):
        """
        Parameters
        ----------
        package_name : str
            Name of the package.
        """
        self.name = package_name
        self.sources = sources

        # convert this to a list to prevent modifying the original dict
        keys = list(kwargs.keys())

        setup_args = dict([(k, kwargs.pop(k)) for k in keys if k in EXTARGS])
        self.setup_args = setup_args
        self.misc_args = kwargs

    def get_extension_info(self):
        return Extension(self.name, self.sources, **self.setup_args)
