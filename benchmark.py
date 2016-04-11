import os
import time
import traceback
import matplotlib.pylab as plt
import numpy
import fileio
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
            method(data[:rlen], fs, ft, width)
            tt += time.time()-st    # stop
        tt /= rd
        logfile.write('{0},{1}\n'.format(rlen, tt))
        tt = 0
    
    logfile.close()


def plt_perflog():
    logdir = os.path.join(os.getcwd(), LOG_FOLDER)
    fplist = fileio.getfiles(logdir)
    
    flegend = []
    
    fig = plt.figure().add_subplot(111)
    
    for f in fplist:
        x = fileio.csvtosig(f, column=0)
        y = fileio.csvtosig(f, column=1)
        x = numpy.append(numpy.array([0]), x)   # left padding
        y = numpy.append(numpy.array([0]), y)   # left padding
        
        fig.plot(x, y)
        alg_name = os.path.basename(f).split('.')[0]
        alg_name = '-'.join(alg_name.split('_')[:-1])
        flegend.append(alg_name)
    
    fig.legend(flegend, loc=2)
    plt.title('Comparision of running time')
    plt.xlabel('data length')
    plt.ylabel('time taken (s)')
    plt.show()
    

if __name__ == '__main__':
    try:
#        filename = 'rawecg.csv'
##        method = alglist['goertzel']
##        method = alglist['goertzel_m']
##        method = alglist['goertzel_st']
        method = alglist['goertzel_st_m']
##        method = alglist['fft']
##        method = alglist['stft']
#        fs = 1000
#        ft = numpy.array([50, 60], dtype='float')
#        width = 1*fs
#        
#        benchmark(filename, fs, ft, width, method, step=100, rd=5)
        
        plt_perflog()
    except Exception as ex:
        print(ex.message)
        traceback.print_exc()
