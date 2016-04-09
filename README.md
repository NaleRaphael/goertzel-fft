Benchmarking for Goertzel algorithm and scipy.fftpack.fft

---
# Package version
python: 2.7.9
numpy: 1.9.1
scipy: 0.15.0

---
# Implemented algorithms
1. dsp.goertzel: Normal Goertzel algorithm.
2. dsp.goertzel_m: Same as 1., but it can take multiple values as `ft`(target frequency). This implementation is used to inspect the decrement of overhead resulting by calling goertzel() multiple times when we need to evaluate several `ft`.
3. dsp.shorttime_goertzel: Short time version of Goertzel algorithm.
4. dsp.shorttime_goertzel_m: Implemented with the same reason of `goertzel_m`.
5. dsp.fftalg(method='fft'): Normal FFT algorithm.
6. dsp.fftalg(method='stft'): Short-time version of FFT.

In order to make the comparison as fair as possible, please note that the short-time techniques of `shorttime_goertzel`, `shorttime_goertzel_m` and `fftalg(method='stft')` are all implemented in python, not C.  

---
# Algorithm verification
To verify the correctness of implemented algorithms, you can execute `main.py`.
Download the file from the link below, and modify the path to choose the file you want to analyze.
[Dropbox | Test data](https://www.dropbox.com/sh/w02sfh10sqom8y5/AAC1E5IB7vnfHxn93PHdh9hLa?dl=0)

Ex:
```python
# main.py
def main(pltfig):
...
# filepath = os.path.join(data_dir, 'FOLDER', 'FILE_NAME.EXT')
filepath = os.path.join(data_dir, 'data', 'sig_60Hz.csv')
...
```

You can also generate a simple signal for analysis.
To do this, try to use the function `export_sig` in `main.py`.

EX:
```python
# main.py
def export_sig():
...
# outpath = os.path.join(data_dir, 'FOLDER', 'FILE_NAME.EXT')
outpath = os.path.join(data_dir, 'data', 'sig_60Hz.csv')
...
```
Path of output file was set to folder `data` by default.

---
# Benchmark
(NOT DONE YET)


---
# Reference
[wikipedia - Goertzel](https://en.wikipedia.org/wiki/Goertzel_algorithm)
[stackoverflow - Implementation of Goertzel algorithm in C](http://stackoverflow.com/questions/11579367)
