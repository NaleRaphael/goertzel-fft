# Benchmark for Goertzel algorithm and scipy.fftpack.fft

## Overview

To evaluate the strength of specific frequency component in signal, 
`Goertzel algorithm` will be a better solution than 
`fast Fourier transform (FFT)`. Because `Goertzel algorithm` allows us to 
evaluate a single `DFT (Discrete Fourier Transform)` term at a time.

But the computational time is related to the size of data. If we need to analyze 
a huge volume of data, how can we improve the performance? In this project, 
`short-time technique` is introduced. It allows us to exchange some frequency 
resolution for a faster computational speed.


## Environments
### Machine
* OS: Windows 7
* CPU: Intel Core i5 5200U @ 2.20GHz
* RAM: 4.00 GB Single-Channel DDR3 @ 798MHz

### Version of Python and packages
* Python: 2.7.9
* Numpy: 1.9.1
* Scipy: 0.15.0


## Implemented algorithms

1. `dsp.goertzel`: Normal Goertzel algorithm.
2. `dsp.goertzel_m`: Same as 1., but it can take multiple values as `ft` (target 
  frequency). This implementation is used to inspect the decrement of overhead 
  resulting by calling `goertzel()` multiple times when we need to evaluate 
  several `ft`s.
3. `dsp.goertzel_st`: Short time version of Goertzel algorithm.
4. `dsp.goertzel_st_m`: Implemented with the same reason of `goertzel_m`.
5. `dsp.fft_eval`: Evaluate specific DFT terms by `scipy.fftpack.fft`.
6. `dsp.stfft_eval`: Short-time version of `fft_eval`.

**NOTE 01: In order to make the comparison as fair as possible, please note that the 
short-time techniques in `goertzel_st`, `goertzel_st_m` and `stfft_eval` are all 
implemented in python, not in C.**

**NOTE 02: In this project, `stfft_eval` (short-time version of `fft_eval`) is 
different to the widely-known [`STFT` (short-time Fourier transform)][STFT].**


## Algorithm verification

* To verify the correctness of implemented algorithms, you can run unit tests.
  All test cases are written in `gofft/alg/tests/test_dsp.py`.
```shell
$ python runtests.py
```

## Run benchmark

* Run all benchmark cases and plot result
```shell
$ python runbench.py
```

* Run all benchmark cases but don't plot result
```shell
$ python runbench.py --skip_plot
```

* Plot result only (please make sure that there are log files in folder `bench_log`)
```shell
$ python runbench.py --skip_bench
```

## Performance

* Data type: float64 (fig_02 is a partial view of fig_01)

![Fig 01. Result of benchmark][dtype_float64_o]

![Fig 02. Result of benchmark (zoomed in)][dtype_float64_z]


## Reference
[wikipedia - Goertzel](https://en.wikipedia.org/wiki/Goertzel_algorithm)  
[stackoverflow - Implementation of Goertzel algorithm in C](http://stackoverflow.com/questions/11579367)  

[dtype_float64_o]: https://i.imgur.com/vV9pjDE.png
[dtype_float64_z]: https://i.imgur.com/Bw3ohXI.png

[STFT]: https://en.wikipedia.org/wiki/Short-time_Fourier_transform
