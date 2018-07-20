from __future__ import absolute_import, division

import os
import sys
import time
import numpy as np

# Definition in `timeit` module
if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time


__all__ = ['BenchmarkCase', 'BenchmarkSuite', 'BenchmarkLoader', 'BenchmarkRunner']


class BenchmarkCase(object):
    def __init__(self, func_name, enable_logging=True):
        self.func_name = func_name
        self.enable_logging = enable_logging

        # Default arguments for benchmark. User can modify them in `self.setup()`
        self.data = None
        self.args = ()
        self.kwargs = {}
        self.step = 100
        self.rd = 3

    def setup(self):
        pass

    def tear_down(self):
        pass

    def _check_bench_args(self):
        if self.data is None:
            raise ValueError('No data availabe.')
        if self.step < 1:
            raise ValueError('Step should not be less than 1.')
        if len(self.data) // self.step < 1:
            raise ValueError('Size of data is not large enough to be partitioned'
                'proportionally. It should at least equal to `step`.')

    def run(self):
        try:
            self._check_bench_args()
        except:
            raise

        func = getattr(self, self.func_name)
        # Note that first row should be zero (no data input)
        tlog = np.zeros((self.step + 1, self.rd))

        for i in range(1, self.step+1):
            rlen = len(self.data)*i//self.step
            for r in range(self.rd):
                st = default_timer()
                func(self.data[:rlen], *self.args, **self.kwargs)
                et = default_timer()
                tlog[i, r] = et - st
        return tlog

    def __call__(self):
        return self.run()


class BenchmarkSuite(object):
    def __init__(self, cases=()):
        self._cases = []
        self.add_cases(cases)

    def __iter__(self):
        return iter(self._cases)

    def add_case(self, case):
        if not hasattr(case, '__call__'):
            raise TypeError('Given case is not callable.')
        self._cases.append(case)

    def add_cases(self, cases):
        for case in cases:
            self.add_case(case)


class BenchmarkLoader(object):
    bench_prefix = 'time'
    suite_class = BenchmarkSuite

    def load_cases(self, case_class):
        if not issubclass(case_class, BenchmarkCase):
            raise TypeError('Given case is not a subclass of `BenchmarkCase`.')
        names = self.get_case_names(case_class)
        suite = self.suite_class(map(case_class, names))
        return suite

    def get_case_names(self, case_class):
        def is_bench_func(attrname, case_class=case_class, 
                            prefix=self.bench_prefix):
            return (attrname.startswith(prefix) and 
                hasattr(getattr(case_class, attrname), '__call__'))
        names = [v for v in dir(case_class) if is_bench_func(v)]
        return names


class BenchmarkRunner(object):
    logdir_name = 'bench_log'
    def _write_log(self, case, log):
        logdir = os.path.join(os.getcwd(), self.logdir_name)
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        logname = '{0}_{1}.{2}'.format(case.__class__.__name__, 
                                       case.func_name, 
                                       'csv')
        logpath = os.path.join(logdir, logname)
        np.savetxt(logpath, log, delimiter=',')

    def run_benchmark(self, case):
        try:
            case.setup()
            log = case.run()
            if case.enable_logging:
                self._write_log(case, log)
        except:
            raise
        finally:
            case.tear_down()

    def run_benchmark_suite(self, suite):
        for case in suite:
            self.run_benchmark(case)


class BenchLoop(BenchmarkCase):
    def setup(self):
        self.data = np.ones(500, dtype='float')
        self.args = ()
        self.kwargs = {}
        self.step = 10
        self.rd = 3
        self.enable_logging = True

    def tear_down(self):
        pass

    def time_foo(self, data, *args, **kwargs):
        foo(data, 10)

    def time_bar(self, data, *args, **kwargs):
        bar(10, data)


def foo(data, mask):
    return np.convolve(data, mask)

def bar(mask, data):
    return np.convolve(data, mask)
