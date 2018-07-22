from __future__ import absolute_import
import sys

try:
	__PKG_SETUP__
except NameError:
	__PKG_SETUP__ = False

if __PKG_SETUP__:
	sys.stderr.write('Running from source directory.\n')
else:
	from . import alg
	from . import bench
	from . import distutils
	from . import plotter

	__all__ = []
	__all__.extend(['alg'])
	__all__.extend(['bench'])
	__all__.extend(['distutils'])
	__all__.extend(['plotter'])
