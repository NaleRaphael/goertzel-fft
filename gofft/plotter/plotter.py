from __future__ import absolute_import
import os
import re
import numpy as np
import matplotlib.pylab as plt
from gofft.bench import LogReader


__all__ = ['LogPlotter']


COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

REGRESSION_LINE_TYPE = {
    'max': lambda x, axis: np.max(x, axis=axis),
    'min': lambda x, axis: np.min(x, axis=axis),
    'mean': lambda x, axis: np.mean(x, axis=axis),
    'median': lambda x, axis: np.median(x, axis=axis)
}

class LogPlotter(object):
    log_reader_class = LogReader

    def __init__(self, log_dir_name, file_pattern='Bench*.csv', log_reader_class=None,
                 alg_pat=r'time_(\w+)'):
        self.log_dir_name = log_dir_name
        self.file_pat = file_pattern
        self.alg_pat = alg_pat
        self.alg_regex = re.compile(self.alg_pat)
        if log_reader_class is None:
            return
        if issubclass(log_reader_class, self.log_reader_class):
            self.log_reader_class = log_reader_class
        else:
            raise TypeError('`log_reader_class` should be a subclass of '
                            '{}'.format(self.log_reader_class))

    def _get_log_files(self):
        from fnmatch import fnmatch

        log_dir = os.path.join(os.getcwd(), self.log_dir_name)
        if not os.path.exists(log_dir):
            raise IOError('No such directory: {}'.format(log_dir))

        files = os.listdir(log_dir)
        log_files = [os.path.join(log_dir ,f) for f in files if fnmatch(f, self.file_pat)]
        return log_files

    def _get_alg_name(self, fn):
        # Get file name without extension
        fn_wo_ext = os.path.basename(fn).split('.')[0]
        res = self.alg_regex.search(fn_wo_ext)
        if len(res.groups()) != 1:
            raise Exception('Filename does not match to the pattern.')
        return res.group(1)

    def plot(self, reg_line_type='median', line_plot=True, scatter_plot=False):
        """
        Plot all log files. (currently, only .csv file is supported)

        Parameters
        ----------
        reg_line : str, optional.
            Type of regression line to be found from log.
            Available mode: ['max', 'min', 'mean', 'median']
        line_plot : bool, optional
            If true, regression line will be plotted.
        sactter_plot : bool, optional.
            If true, all data points in a log will be plotted.
        """
        if reg_line_type not in REGRESSION_LINE_TYPE:
            raise ValueError('Invalid `reg_line_type`.')
        if not line_plot and not scatter_plot:
            raise ValueError('At least one plot should be selected.')

        log_files = self._get_log_files()
        if len(log_files) == 0:
            raise Exception('No log file can be plotted.')

        log_reader = self.log_reader_class()

        fig = plt.figure().add_subplot(1, 1, 1)
        handles = []
        labels = []

        for i, f in enumerate(log_files):     # test
            x, y = log_reader.read(f)
            if scatter_plot:
                fig.plot(x, y, marker='+', linestyle='None', 
                         color=COLORS[i%len(COLORS)])
            if line_plot:
                reg_line = REGRESSION_LINE_TYPE[reg_line_type](y, axis=1)
                handle, = fig.plot(x, reg_line, linestyle='-', 
                                   color=COLORS[i%len(COLORS)])

            handles.append(handle)
            alg_name = self._get_alg_name(f)
            labels.append(alg_name)

        fig.legend(handles, labels, loc=2)
        plt.xlim(xmax=x[-1])
        plt.title('Comparision of running time')
        plt.xlabel('Data length')
        plt.ylabel('Time (ms)')
        plt.grid()
        plt.show()
