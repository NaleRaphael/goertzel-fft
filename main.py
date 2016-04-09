import csv
import os
import time
import traceback

import numpy
import matplotlib.pylab as plt

import cbplot
from alg import dsp


def export_sig():
    ft = 60
    fs = 1000
    T = 10
    t = numpy.linspace(0, T, T*fs)
    sig = numpy.sin(2*numpy.pi*ft*t)
    
    data_dir = os.getcwd()
    outpath = os.path.join(data_dir, 'data', 'sig_60Hz.csv')
    outfile = open(outpath, mode='w')
    
    for d in iter(sig):
        outfile.write('{0}\n'.format(d))
    outfile.close()


def csvtosignal(filepath, lead=0):
    reader = csv.reader(open(filepath, 'r'), delimiter=',')
    x = list(reader)
    a = numpy.array(x)
    return a[:, lead].astype('float')


def main(pltfig):
    fs = 1000
    data_dir = os.getcwd()
    filepath = os.path.join(data_dir, 'data', 'sig_60Hz.csv')
    dname = filepath.split('\\')[-1]
    
    sig = csvtosignal(filepath)
    
    ft = numpy.array([50, 60], dtype='float')   # Target frequency
    filter_width = 1*fs     # 1 sec
    
    st = time.time()
    res_stgo = dsp.shorttime_goertzel_m(sig, fs, ft, filter_width)
    print('Goertzel-m: {0} secs'.format(time.time()-st))
    print('mag50: {0}'.format(res_stgo[0]))
    print('mag60: {0}'.format(res_stgo[1]))
    
    st = time.time()
    res_stft = dsp.fftalg(sig, fs, ft, filter_width, 
                          method='stft', cb_plt=cbplot.plt_spectrum)
    print('FFT_st: {0} secs'.format(time.time()-st))
    print('mag50: {0}'.format(res_stft[0]))
    print('mag60: {0}'.format(res_stft[1]))
    
    if pltfig:
        plt.plot(sig)
        plt.title('file:{0}'.format(dname))
        plt.show()


if __name__ == '__main__':
    try:
        main(pltfig=False)
#        export_sig()
    except Exception as ex:
        print(ex.message)
        traceback.print_exc()
