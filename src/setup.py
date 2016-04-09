from distutils.core import setup, Extension
import numpy.distutils.misc_util

cext = Extension('cext',
                   sources = ['main.c', 'dsp.c'])

setup (name = 'cext',
       version = '1.0',
       description = 'C extension',
       author = 'Nale Raphael',
       author_email = 'gmccntwxy@gmail.com',
       include_dirs = ['\"'+numpy.distutils.misc_util.get_numpy_include_dirs()[0]+'\"'],
       ext_modules = [cext])