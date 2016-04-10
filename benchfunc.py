"""
Standard interface for benchmarking.
"""
from alg import dsp

__all__ = ['goertzel', 'goertzel_m', 'goertzel_st', 'goertzel_st_m',
           'fft', 'stft']

def goertzel(data, fs, ft, width):
    for f in ft:
        print dsp.goertzel(data, fs, f, width)


def goertzel_m(data, fs, ft, width):
    print dsp.goertzel_m(data, fs, ft, width)


def goertzel_st(data, fs, ft, width):
    for f in ft:
        print dsp.shorttime_goertzel(data, fs ,f, width)


def goertzel_st_m(data, fs, ft, width):
    print dsp.shorttime_goertzel_m(data, fs, ft, width)


def fft(data, fs, ft, width):
    # NOTE: For FFT, width is set as the length of input data.
    for f in ft:
        print dsp.fftalg(data, fs, ft, len(data), method='fft')


def stft(data, fs, ft, width):
    print dsp.fftalg(data, fs, ft, width, method='stft')


# function list
alglist = {
    'goertzel': goertzel,
    'goertzel_m': goertzel_m,
    'goertzel_st': goertzel_st,
    'goertzel_st_m': goertzel_st_m,
    'fft': fft,
    'stft': stft
}
