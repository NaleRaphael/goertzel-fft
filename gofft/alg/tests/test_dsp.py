from __future__ import absolute_import, division

import unittest
import numpy as np

from gofft.alg import (goertzel, goertzel_m, goertzel_st, goertzel_st_m)

__all__ = ['TestGoertzel']


class TestGoertzel(unittest.TestCase):
    def setUp(self):
        self.fs = 1000  # sampling frequency
        self.ft = 60    # target frequency
        dur = 2     # duration
        num = self.fs*dur
        t = np.linspace(0, dur, num)
        self.data = np.sin(2*np.pi*self.ft*t)

    def test_cmp_go_with_fft(self):
        mag_ft_fft = self._fft(self.data, self.fs, self.ft)
        mag_ft_go = goertzel(self.data, self.fs, self.ft, self.data.size)
        np.testing.assert_allclose(mag_ft_fft, mag_ft_go)

    def test_cmp_go_rng_with_fft(self):
        """ Add up all evaluated DFT terms in given range `[ft, ft + rng)` """
        width = self.data.size
        f_step = self.fs / width
        rng = 1.5
        ft = np.arange(self.ft, self.ft+rng, step=f_step)

        mag_ft_fft = self._fft(self.data, self.fs, ft)
        mag_ft_go_rng = goertzel(self.data, self.fs, self.ft, width, rng=rng)
        np.testing.assert_allclose(np.sum(mag_ft_fft), mag_ft_go_rng)

    def test_cmp_gom_with_fft(self):
        """ Evaluate multiple DFT terms at once """
        ft = np.array([50, 60, 70], dtype=float)
        mag_ft_fft = self._fft(self.data, self.fs, ft)
        mag_ft_gom = goertzel_m(self.data, self.fs, ft, self.data.size)
        np.testing.assert_allclose(mag_ft_fft, mag_ft_gom)

    def test_cmp_gost_with_fft(self):
        width = self.fs
        mag_ft_fftst = self._fft_st(self.data, self.fs, self.ft, width)
        mag_ft_gost = goertzel_st(self.data, self.fs, self.ft, width)
        np.testing.assert_allclose(mag_ft_fftst, mag_ft_gost)

    def test_cmp_gostm_with_fft(self):
        """ Evaluate multiple DFT terms at once """
        width = self.fs
        ft = np.array([50, 60, 70], dtype=float)
        mag_ft_fftstm = self._fft_st(self.data, self.fs, ft, width)
        mag_ft_gostm = goertzel_st_m(self.data, self.fs, ft, width)
        np.testing.assert_allclose(mag_ft_fftstm, mag_ft_gostm)

    def _fft(self, data, fs, ft):
        from scipy.fftpack import fft
        dlen = data.size
        ft = np.asfarray(ft)
        spec = fft(data) / dlen
        idx = (ft/fs*dlen).astype('int')
        mag = np.abs(spec[idx])
        return mag

    def _fft_st(self, data, fs, ft, width):
        from scipy.fftpack import fft
        ft = np.asfarray(ft)
        rem = data.size % width
        dlen = data.size - rem
        cnt = data.size // width
        mag = 0.0
        for i in range(0, dlen, width):
            spec = fft(data[i:i+width])/width
            idx = (ft/fs*width).astype('int')
            mag += np.abs(spec[idx])
        mag /= cnt
        return mag
