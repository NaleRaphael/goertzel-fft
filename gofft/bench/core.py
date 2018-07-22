from __future__ import absolute_import, division

import os
import sys
import time
import numpy as np
from .logger import LogWriter

# Definition in `timeit` module
if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time


__all__ = ['BenchmarkCase', 'BenchmarkSuite', 'BenchmarkLoader', 'BenchmarkRunner']


class BenchmarkCase(object):
    def __init__(self, func_name, enable_logging=True, stream=sys.stderr):
        self.func_name = func_name
        self.enable_logging = enable_logging
        self.stream = stream

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
        self.stream.write('Current running: {}\n'.format(self.func_name))
        try:
            self._check_bench_args()
        except:
            raise
        msg_progress = 'progress: {}/{}\r'

        func = getattr(self, self.func_name)
        # NOTE:
        # 1. First row should be zero (no data input) -> self.step + 1
        # 2. Data length in each step should be written in log too -> self.rd + 1
        tlog = np.zeros((self.step + 1, self.rd + 1))

        for i in range(1, self.step+1):
            rlen = len(self.data)*i//self.step
            tlog[i, 0] = rlen
            for r in range(self.rd):
                st = default_timer()
                func(self.data[:rlen], *self.args, **self.kwargs)
                et = default_timer()
                tlog[i, r+1] = et - st
            self.stream.write(msg_progress.format(i, self.step))
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

    def add_suite(self, suite):
        if not isinstance(suite, BenchmarkSuite):
            raise TypeError('Given suite is not a isinstance of `BenchmarkSuite`.')
        for case in suite:
            self.add_case(case)


class BenchmarkLoader(object):
    bench_prefix = 'time'
    suite_class = BenchmarkSuite
    case_class = BenchmarkCase

    def _find_benchmark_case_files(self, start_dir, pattern_dir, pattern_file):
        from fnmatch import fnmatch
        entry = os.path.abspath(start_dir)
        result = []
        for root, dirs, files in os.walk(entry):
            if len(files) == 0:
                continue
            if not fnmatch(os.path.basename(root), pattern_dir):
                continue
            result.extend([os.path.join(root, f) for f in files if fnmatch(f, pattern_file)])
        return result

    def discover(self, start_dir='.', pattern_dir='benchmarks', 
                 pattern_file='bench_*.py'):
        case_files = self._find_benchmark_case_files(start_dir, pattern_dir, pattern_file)
        suite = BenchmarkSuite()
        for f in case_files:
            name = os.path.basename(f).split('.')[0]
            des = ('.py', 'U', 1)   # (suffix, mode, type: PY_SOURCE)
            mod = _load_module(name, f, info=des)
            su = self.load_cases_from_module(mod)
            suite.add_suite(su)
        return suite

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

    def load_cases_from_module(self, mod):
        suite = self.suite_class()
        for v in dir(mod):
            attr = getattr(mod, v)
            if not isinstance(attr, type) or not issubclass(attr, self.case_class):
                continue
            # In case that user imports case_class by `from XXX import case_class`
            if attr is self.case_class:
                continue
            su = self.load_cases(attr)
            suite.add_cases([case for case in su])
        return suite


class BenchmarkRunner(object):
    logdir_name = 'bench_log'
    log_writer_class = LogWriter

    def __init__(self, log_writer_class=None):
        if log_writer_class is None:
            return
        if issubclass(log_writer_class, self.log_writer_class):
            self.log_writer_class = log_writer_class
        else:
            raise TypeError('`log_writer_class` should be a subclass of '
                            '{}'.format(self.log_writer_class))

    def _write_log(self, case, log):
        logdir = os.path.join(os.getcwd(), self.logdir_name)
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        logname = '{0}_{1}.{2}'.format(case.__class__.__name__, 
                                       case.func_name, 
                                       'csv')
        logpath = os.path.join(logdir, logname)
        writer = self.log_writer_class()
        writer.write(logpath, log)

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


def _load_module(name, fn, info=None):
    import imp

    if info is None:
        path = os.path.dirname(fn)
        fo, fn, info = imp.find_module(name, [path])
    else:
        fo = open(fn, info[1])

    try:
        mod = imp.load_module(name, fo, fn, info)
    except:
        raise
    finally:
        fo.close()
    return mod
