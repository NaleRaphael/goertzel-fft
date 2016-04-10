import os
import time
import traceback
import matplotlib.pylab as plt
import numpy
import fileio
from alg import dsp
from benchfunc import alglist

LOG_FOLDER = 'perflog'
DATA_FOLDER = 'data'


def benchmark(filename, fs, ft, width, method, step=100, rd=1):
    logname = str(method.__name__)+'_'+time.strftime('%y%m%d%H%M')+'.csv'
    logpath = os.path.join(os.getcwd(), LOG_FOLDER, logname)
    filepath = os.path.join(os.getcwd(), DATA_FOLDER, filename)
    
    data = fileio.csvtosig(filepath)
    try:
        logfile = open(logpath, mode='w')
    except:
        raise
    
    rps = range(rd)     # rounds per step
    tt = 0      # total time
    st = 0      # start time
    
    for i in range(1, step):
        rlen = len(data)*i/step
        for r in rps:
            st = time.time()        # start
##            mag50 = Common.goertzel(data[:rlen], fs, 50, rlen)
##            mag60 = Common.goertzel(data[:rlen], fs, 60, rlen)
##            mag50 = Common.goertzel_ext(data[:rlen], fs, 50, rlen)
##            mag60 = Common.goertzel_ext(data[:rlen], fs, 60, rlen)
##            result = FFTAnalysis.check_plf(data[:rlen], fs)
#            
#            # short-time version
##            mag50 = Common.shorttime_goertzel(data[:rlen], fs, 50, fs)
##            mag60 = Common.shorttime_goertzel(data[:rlen], fs, 60, fs)
#            mag = Common.shorttime_goertzel_m(data[:rlen], fs, ft, fs)
##            result = FFTAnalysis.check_plf_st(data[:rlen], fs, fs, method='stft')
            method(data[:rlen], fs, ft, width)
            tt += time.time()-st    # stop
        tt /= rd
        logfile.write('{0},{1}\n'.format(rlen, tt))
        tt = 0
    
    logfile.close()


def plt_perflog():
    logpath = os.getcwd()
    logpath = os.path.join(logpath, LOG_FOLDER)
    

if __name__ == '__main__':
    try:
        filename = 'sig_60Hz.csv'
#        method = alglist['goertzel']
#        method = alglist['goertzel_m']
#        method = alglist['goertzel_st']
#        method = alglist['goertzel_st_m']
#        method = alglist['fft']
        method = alglist['stft']
        fs = 1000
        ft = numpy.array([50, 60], dtype='float')
        width = 1*fs
        
        benchmark(filename, fs, ft, width, method, step=10, rd=1)
    except Exception as ex:
        print(ex.message)
        traceback.print_exc()
