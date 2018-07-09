from __future__ import absolute_import, division, print_function

import os
import sys
import time
#import gc

# Definition in `timeit` module
if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time


__all__ = ['benchmark']

LOG_FOLDER = os.path.join(os.getcwd(), 'bench_log')

def benchmark(data, method, *args, **kwargs):
    """
    Benchmark execution time of given method.

    Parameters
    ----------
    data : array_like
        Data for benchmarking.
    method :
        Method for benchmarking.
    step : int, optional
        Steps (loops) should be run. Default is 100.
        Notice that length of data for each step is controlled by this argument.
        ```
        length_of_data_for_a_single_run = loop_count*len(data)//steps
        ```
    rd : int, optional
        Times should be run in each step (loops). Default is 3.
    *args
        Argument for given method.
    **kwargs
        Keyword argument for given method.
    """
    step = 100 if kwargs['step'] is None else kwargs.pop('step')
    rd = 3 if kwargs['rd'] is None else kwargs.pop('rd')

    if 'logpath' in kwargs:
        logpath = kwargs.pop('logpath')
    else:
        if not os.path.exists(LOG_FOLDER):
            os.mkdir(LOG_FOLDER)
        mname = (str(method.__name__) if kwargs['mname'] is None 
                 else kwargs.pop('mname'))
        logname = '{0}_{1}.{2}'.format(mname, 
                                       time.strftime('%y%m%d%H%M%S'), 'csv')
        logpath = os.path.join(LOG_FOLDER, logname)

    try:
        logfile = open(logpath, mode='w')
    except:
        raise

    rps = range(rd)     # rounds per step
    st = 0      # start time
    tlog = [0]*rd       # log of time

    logfile.write('{0},{1}\n'.format(0, ','.join(map(str, [0]*rd))))
    for i in range(1, step+1):
        rlen = len(data)*i//step
        for r in rps:
            st = default_timer()       # start
            method(data[:rlen], *args, **kwargs)
            tt = default_timer()-st    # stop
            tlog[r] = tt
#        gc.collect()
        tlog_str = ','.join(map(str, tlog))
        logfile.write('{0},{1}\n'.format(rlen, tlog_str))
    logfile.close()
    return logpath
