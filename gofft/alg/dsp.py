import numpy as np
from scipy.fftpack import fft as scipyfft
import dsp_ext as cext


__all__ = ['goertzel', 'goertzel_m', 'goertzel_st', 
           'goertzel_st_m', 'fft_eval', 'stfft_eval']

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

    if data.dtype != np.dtype('float'):
        data = data.astype('float')
    ft = np.asfarray(ft)

    try:
        if rng:
            val = cext.goertzel_rng(data, fs, ft, width, rng)
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

    if data.dtype != np.dtype('float'):
        data = np.asarray(data, dtype='float')
    ft = np.asfarray(ft)

    try:
        val = cext.goertzel_m(data, fs, ft, width)
    except:
        raise

    return val


def goertzel_st(data, fs, ft, width, rng=None, padding=False):
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

    if data.dtype != np.dtype('float'):
        data = np.asarray(data, dtype='float')
    ft = np.asfarray(ft)

    rem = len(data)%width
    dlen = len(data)-rem
    val = 0.0
    cnt = 0
    for i in range(0, dlen, width):
        cnt += 1
        val += cext.goertzel(data[i:i+width], fs, ft, width)

    if rem!=0 and padding:
        cnt += 1
        pdata = np.zeros(width-rem, dtype='float')
        pdata = np.append(data[i+width:], pdata)
        val += cext.goertzel(pdata, fs, ft, width)

    val /= cnt
    return val


def goertzel_st_m(data, fs, ft, width, padding=False):
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

    if data.dtype != np.dtype('float'):
        data = np.asarray(data, dtype='float')
    ft = np.asfarray(ft)

    rem = len(data)%width
    dlen = len(data)-rem
    val = 0.0
    cnt = 0
    for i in range(0, dlen, width):
        cnt += 1
        val += cext.goertzel_m(data[i:i+width], fs, ft, width)

    if rem!=0 and padding:
        cnt += 1
        pdata = np.zeros(width-rem, dtype='float')
        pdata = np.append(data[i+width:], pdata)
        val += cext.goertzel_m(pdata, fs, ft, width)

    val /= cnt
    return val


def fft_eval(sig, fs, ft):
    """
    Evaluate DFT terms of given tagert frequency.

    Parameters
    ----------
    sig : ndarray
        Input signal.
    fs : int
        Sampling frequency.
    ft : int, float or array-like
        Target frequency to be evaluated.

    Returns
    -------
    mag : ndarray
        Evaluated DFT terms.
    """
    ft = np.asfarray(ft)
    dlen = sig.size
    spec = scipyfft(sig) / dlen
    idx = (ft/fs*dlen).astype('int')
    mag = np.abs(spec[idx])
    return mag


def stfft_eval(sig, fs, ft, width):
    """
    Short-time version of `fft_eval()`.

    Parameters
    ----------
    sig : ndarray
        Input signal.
    fs : int
        Sampling frequency.
    ft : int, float or array-like
        Target frequency to be evaluated.
    width : int
        Window size for short-time technique.

    Returns
    -------
    mag : ndarray
        Evaluated DFT terms.
    """
    ft = np.asfarray(ft)
    rem = sig.size % width
    dlen = sig.size - rem
    cnt = sig.size // width
    mag = 0.0

    for i in range(0, dlen, width):
        spec = scipyfft(sig[i:i+width]) / width
        idx = (ft/fs*width).astype('int')
        mag += np.abs(spec[idx])
    mag /= cnt
    return mag
