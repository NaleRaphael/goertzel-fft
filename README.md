# Benchmark for Goertzel algorithm and scipy.fftpack.fft

**NOTICE: This branch is under maintenance. 
If you want to use the code, you can checkout the branch `legacy`.**

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

### Verions of Python and packages
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
5. `dsp.fftalg(method='fft')`: Normal FFT algorithm.
6. `dsp.fftalg(method='stfft')`: Short-time version of FFT.

**NOTE 01: In order to make the comparison as fair as possible, please note that the 
short-time techniques in `goertzel_st`, `goertzel_st_m` and `fftalg(method='stft')` 
are all implemented in python, not in C.**

**NOTE 02: In this project, `stfft` (short-time version of FFT) is different to the 
widely-known [`STFT` (short-time Fourier transform)][STFT].**


## Algorithm verification

* To verify the correctness of implemented algorithms, you can run unit tests.
  All test cases are in `gofft/alg/tests/test_dsp.py`.
```shell
$ python runtests.py
```

## Performance
Test data: [rawecg.csv](https://www.dropbox.com/s/bq4g8mx05xhu6ut/rawecg.csv?dl=0)  

* Data type: int32
![Fig 01. (data type: int32)][dtype_int32_o]  ![Fig 02. Zoomed Fig 01.][dtype_int32_z]

* Data type: float32
![Fig 03. (data type: float32)][dtype_float32_o]  ![Fig 04. Zoomed Fig 03][dtype_float32_z]


## Reference
[wikipedia - Goertzel](https://en.wikipedia.org/wiki/Goertzel_algorithm)  
[stackoverflow - Implementation of Goertzel algorithm in C](http://stackoverflow.com/questions/11579367)  

[dtype_int32_o]: http://i.imgur.com/afOVKyg.png
[dtype_int32_z]: http://i.imgur.com/HPSLw4W.png
[dtype_float32_o]: http://i.imgur.com/GP7Jq05.png
[dtype_float32_z]: http://i.imgur.com/VOIK9Dd.png

[STFT]: https://en.wikipedia.org/wiki/Short-time_Fourier_transform
