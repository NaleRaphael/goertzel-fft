import numpy
import scipy.fftpack as fft
import cext

__all__ = ['goertzel', 'goertzel_m', 'shorttime_goertzel', 
           'shorttime_goertzel_m', 'fftalg']

def goertzel(data, fs, ft, n, rng=None):
    """
    Goertzel algorithm, an efficiency method to evaluate specific terms of a
    discrecte Fourier transform.
    
    Parameters
    ----------
    sig : ndarray
        Input signal.
    fs : int
        Sampling frequency.
    ft : int
        Target frequency.
    N : int
        Block size. (related to frequency resolution)

    Returns
    -------
    mag : float
        Magnitude of a single DFT term corresponding to target frequency.

    Note
    ----
    1. To get a better result, target frequency should not be too low.
    2. The higher `N` is, the better freqency resolution we can get, however, 
       with longer computation time will be taken.
    ref : https://en.wikipedia.org/wiki/Goertzel_algorithm
    """
    if fs > len(data):
        raise ValueError(
            'Data length is too short:{0}'.format(len(data)))
    
    if n > len(data):
        raise ValueError(
            'Size of Goertzel block(N) should be less than data length.')
    
    if data.dtype != numpy.dtype('float'):
        data = data.astype('float')
    
    try:
        if rng:
            val = cext.goertzel_rng(data, fs, ft, rng, n)
        else:
            val = cext.goertzel(data, fs, ft, n)
    except:
        raise
    
    return val


def goertzel_m(data, fs, ft, width):
    if fs > len(data):
        raise ValueError(
            'Data length is too short:{0}'.format(len(data)))
    
    if width > len(data):
        raise ValueError(
            'Size of Goertzel block(N) should be less than data length.')
    
    if data.dtype != numpy.dtype('float'):
        data = numpy.asarray(data, dtype='float')
    
    try:
        val = cext.goertzel_m(data, fs, ft, width)
    except:
        raise
    
    return val


def shorttime_goertzel(data, fs, ft, width, rng=None, padding=False):
    if fs > len(data):
        raise ValueError(
            'Data length is too short:{0}'.format(len(data)))
    
    if width > len(data):
        raise ValueError(
            'Size of Goertzel block(N) should be less than data length.')
    
    if data.dtype != numpy.dtype('float'):
        data = numpy.asarray(data, dtype='float')
    
    rem = len(data)%width
    dlen = len(data)-rem
    val = 0.0
    cnt = 0
    for i in range(0, dlen, width):
        cnt += 1
        val += cext.goertzel(data[i:i+width], fs, ft, width)
    
    if rem!=0 and padding:
        cnt += 1
        pdata = numpy.zeros(width-rem, dtype='float')
        pdata = numpy.append(data[i+width:], pdata)
        val += cext.goertzel(pdata, fs, ft, width)
    
    val /= cnt
    return val


def shorttime_goertzel_m(data, fs, ft, width, rng=None, padding=False):
    if fs > len(data):
        raise ValueError(
            'Data length is too short:{0}'.format(len(data)))
    
    if width > len(data):
        raise ValueError(
            'Size of Goertzel block(N) should be less than data length.')
    
    if data.dtype != numpy.dtype('float'):
        data = numpy.asarray(data, dtype='float')
    
    rem = len(data)%width
    dlen = len(data)-rem
    val = 0.0
    cnt = 0
    for i in range(0, dlen, width):
        cnt += 1
        val += cext.goertzel_m(data[i:i+width], fs, ft, width)
    
    if rem!=0 and padding:
        cnt += 1
        pdata = numpy.zeros(width-rem, dtype='float')
        pdata = numpy.append(data[i+width:], pdata)
        val += cext.goertzel_m(pdata, fs, ft, width)
    
    val /= cnt
    return val


def _fft(sig, fs, ft, width, rng=False, padding=False):
    spec = fft.fft(sig)
    unit = float(len(spec))/(fs)
    
    val = numpy.zeros(len(ft))
    for i, f in enumerate(ft):
        val[i] += numpy.abs(spec[int(f*unit)])/len(sig)
        
    return val


def _stft(sig, fs, ft, width, padding=False, cb_plt=None):
    rem = len(sig)%width
    dlen = len(sig)-rem
    unit = float(width)/float(fs)
    val = numpy.zeros(len(ft))
    cnt = 0
    
    if cb_plt:
        output = numpy.zeros(width, dtype='float')
    
    for i in range(0, dlen, width):
        cnt += 1
        spec = fft.fft(sig[i:i+width])
        for i, f in enumerate(ft):
            val[i] += numpy.abs(spec[int(f*unit)])/(width/2)
        if cb_plt:
            output += numpy.abs(spec)/(width/2)
    
    if rem!=0 and padding:
        cnt += 1
        pdata = numpy.zeros(width-rem, dtype='float')
        pdata = numpy.append(sig[i+width:], pdata)
        spec = fft.fft(pdata)
        for i, f in enumerate(ft):
            val[i] += numpy.abs(spec[int(f*unit)])/(width/2)
        if cb_plt:
            output += numpy.abs(spec)/(width/2)
    
    val /= cnt
    
    if cb_plt:
        output /= cnt
        cb_plt(fs, width, output)

    return val


check_plf_methods = {
    'fft': _fft,
    'stft': _stft,
}
def fftalg(sig, fs, ft, width, rng=None, method=None, padding=False, cb_plt=None):
    if method in check_plf_methods:
        return check_plf_methods[method](sig, fs, ft, width, padding=padding, cb_plt=cb_plt)
    else:
        raise ValueError(
            'Invalid method: {0}'.format(str(method)))
