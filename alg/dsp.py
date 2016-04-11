import numpy
import scipy.fftpack as fft
import cext


__all__ = ['goertzel', 'goertzel_m', 'shorttime_goertzel', 
           'shorttime_goertzel_m', 'fftalg']

def goertzel(data, fs, ft, width, rng=None):
    """
    Goertzel algorithm, an efficiency method to evaluate specific terms of a
    discrecte Fourier transform.
    
    Parameters
    ----------
    data : ndarray
        Input signal.
    fs : int
        Sampling frequency.
    ft : int
        Target frequency.
    width : int
        Width of filter. (related to frequency resolution)
    rng : ndarray
        Frequency range for evaluation.

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
    
    if width > len(data):
        raise ValueError(
            'Size of Goertzel block(N) should be less than data length.')
    
    if data.dtype != numpy.dtype('float'):
        data = data.astype('float')
    ft = numpy.asfarray(ft)
    
    try:
        if rng:
            val = cext.goertzel_rng(data, fs, ft, rng, width)
        else:
            val = cext.goertzel(data, fs, ft, width)
    except:
        raise
    
    return val


def goertzel_m(data, fs, ft, width):
    """
    Modified Goertzel algorithm. This method evaluate all `ft` at once.
    
    Parameters
    ----------
    data : ndarray
        Input signal.
    fs : int
        Sampling frequency.
    ft : ndarray
        Target frequency.
    width : int
        Width of filter. (related to frequency resolution)
    
    Returns
    -------
    mag : ndarray
        Magnitude of a single DFT term corresponding to target frequency.
    """
    if fs > len(data):
        raise ValueError(
            'Data length is too short:{0}'.format(len(data)))
    
    if width > len(data):
        raise ValueError(
            'Size of Goertzel block(N) should be less than data length.')
    
    if data.dtype != numpy.dtype('float'):
        data = numpy.asarray(data, dtype='float')
    ft = numpy.asfarray(ft)
    
    try:
        val = cext.goertzel_m(data, fs, ft, width)
    except:
        raise
    
    return val


def shorttime_goertzel(data, fs, ft, width, rng=None, padding=False):
    """
    Short-time Goertzel algorithm.
    
    Parameters
    ----------
    data : ndarray
        Input signal.
    fs : int
        Sampling frequency.
    ft : ndarray
        Target frequency.
    width : int
        Width of filter. (related to frequency resolution)
    rng : ndarray
        Frequency range for evaluation.
    padding : bool
        Apply padding for this algorithm.
    
    Returns
    -------
    val : ndarray
        Magnitude of a single DFT term corresponding to target frequency.
    """
    
    if fs > len(data):
        raise ValueError(
            'Data length is too short:{0}'.format(len(data)))
    
    if width > len(data):
        raise ValueError(
            'Size of Goertzel block(N) should be less than data length.')
    
    if data.dtype != numpy.dtype('float'):
        data = numpy.asarray(data, dtype='float')
    ft = numpy.asfarray(ft)
    
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


def shorttime_goertzel_m(data, fs, ft, width, padding=False):
    """
    Modified short-time Goertzel algorithm. This method evaluates all `ft` 
    at once.
    
    Parameters
    ----------
    data : ndarray
        Input signal.
    fs : int
        Sampling frequency.
    ft : ndarray
        Target frequency.
    width : int
        Width of filter. (related to frequency resolution)
    padding : bool
        Apply padding for this algorithm.
    
    Returns
    -------
    val : ndarray
        Magnitude of a single DFT term corresponding to target frequency.
    """
    if fs > len(data):
        raise ValueError(
            'Data length is too short:{0}'.format(len(data)))
    
    if width > len(data):
        raise ValueError(
            'Size of Goertzel block(N) should be less than data length.')
    
    if data.dtype != numpy.dtype('float'):
        data = numpy.asarray(data, dtype='float')
    ft = numpy.asfarray(ft)
    
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


def _fft(sig, fs, ft, width, padding=False, cb_plt=None):
    # TODO: Revise parameter `width`
    spec = fft.fft(sig)
    unit = float(len(spec))/fs
    
    val = numpy.zeros(len(ft))
    for i, f in enumerate(ft):
        val[i] += numpy.abs(spec[int(f*unit)])/(width/2)
    
    if cb_plt:
        cb_plt(fs, width, numpy.abs(spec)/(width/2))
    
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


fftalglist = {
    'fft': _fft,
    'stft': _stft,
}
def fftalg(sig, fs, ft, width, method=None, padding=False, cb_plt=None):
    """
    FFT algorithm.
    
    Parameters
    ----------
    sig : ndarray
        Input signal.
    fs : int
        Sampling rate.
    ft : ndarray
        Target frequency for evaluation.
    width : int
        Signal length for FFT analysis.
    method : string
        'fft': normal FFT.
        'stft': short-time FFT.
    padding : bool
        Apply padding for stft.
    cb_plt : function
        Callback function for plotting spectrum.
    """
    if method in fftalglist:
        return fftalglist[method](sig, fs, ft, width, padding=padding, cb_plt=cb_plt)
    else:
        raise ValueError(
            'Invalid method: {0}'.format(str(method)))
