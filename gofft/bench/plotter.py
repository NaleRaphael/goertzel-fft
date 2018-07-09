from __future__ import absolute_import, division, print_function

import os

import matplotlib.pylab as plt
import numpy as np

from . import fileio

__all__ = ['plotlog']


COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

PERFLOG_MODE = {
'max': lambda x, axis: np.max(x, axis=axis),
'min': lambda x, axis: np.min(x, axis=axis),
'mean': lambda x, axis: np.mean(x, axis=axis),
'median': lambda x, axis: np.median(x, axis=axis)
}

def plotlog(logdir, mode='median', scatter_plot=True):
    """
    Plot all log files from a given directory.
    Currently, only .csv file is supported.

    Parameters
    ----------
    logdir : str
        Directory of log files.
    mode : ['max', 'min', 'mean', 'median'], optional. Default is 'median'.
        Mode for finding the regression line of scatter plot. Notice that the 
        line of 'line_plot' (when `scatter_plot` is `False`) is also determined 
        by this argument.
    sactter_plot : bool, optional. Default is True.
        Generate a scatter plot. Otherwise, generate a line plot.
    """
    if mode not in PERFLOG_MODE:
        raise ValueError('Invalid `mode`.')

    fplist = fileio.getfiles(logdir)
    if len(fplist) == 0:
        return

    fig = plt.figure().add_subplot(111)
    handles = []
    labels = []

    for i, f in enumerate(fplist):
        x = fileio.csvtosig(f, column=0)
        y = fileio.csvtosig(f, column=1, rng='end')

        if scatter_plot:
            fig.plot(x, y, marker='+', linestyle='None', 
                               color=COLORS[i%len(COLORS)])
            # Plot regression line
            reg_line = PERFLOG_MODE[mode](y, axis=1)
            handle, = fig.plot(x, reg_line, color=COLORS[i%len(COLORS)])
        else:
            # Show regression lint only if we don't want to see scatter plot
            reg_line = PERFLOG_MODE[mode](y, axis=1)
            handle, = fig.plot(x, reg_line, linestyle='-', 
                               color=COLORS[i%len(COLORS)])

        handles.append(handle)
        alg_name = os.path.basename(f).split('.')[0]
        alg_name = '-'.join(alg_name.split('_')[:-1])
        labels.append(alg_name)

    fig.legend(handles, labels, loc=2)
    plt.xlim(xmax=x[-1])
    plt.title('Comparision of running time')
    plt.xlabel('data length')
    plt.ylabel('time taken (s)')
    plt.show()
