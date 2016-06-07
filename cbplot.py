import matplotlib.pylab as plt
import numpy

__all__ = ['plt_spectrum']


def plt_spectrum(fs, n ,spec, dname=None):
    """
    Plot spectrum.
    """
    ax_f = numpy.linspace(0, fs/2, n/2)
    plt.plot(ax_f, numpy.abs(spec[0:n/2]))
    
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    
    str_title = 'Spectrum'
    if dname:
        str_title += ', data:'+dname
    
    plt.title(str_title)
    plt.show(block=False)
