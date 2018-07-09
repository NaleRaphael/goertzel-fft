from __future__ import absolute_import


def configuration():
	import numpy.distutils.misc_util
	import os.path as op
	from gofft.distutils import Configuration

	absjoin = lambda *x: op.abspath(op.join(*x))

	NP_DEP = numpy.distutils.misc_util.get_numpy_include_dirs()
	name = 'gofft.alg.dsp_ext'
	files = ['main.c', 'dsp.c']
	this_dir = op.dirname(op.abspath(__file__))
	sources = [absjoin(this_dir, 'src', f) for f in files]
	deps = [NP_DEP]

	setup_args = dict(
		include_dirs=NP_DEP, 
	)

	config = Configuration(name, sources, **setup_args)
	return config
