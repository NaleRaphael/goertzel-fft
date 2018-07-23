from __future__ import absolute_import, division
import unittest
import numpy as np

from gofft.bench import (BenchmarkCase, BenchmarkSuite, BenchmarkLoader,
                         BenchmarkRunner)


class FakeStream(object):
    def write(self, *args, **kwargs):
        """ Do nothing in unit test stage. """
        pass


class BenchArrayMultiplication(BenchmarkCase):
    def set_up(self):
        self.stream = FakeStream()
        self.enable_logging = False
        self.data = np.ones(100, dtype='float')
        self.args = ()
        self.kwargs = {}
        self.step = 10
        self.rd = 3

    def time_foo(self, data, *args, **kwargs):
        foo(data, np.array([2.0]))

    def time_bar(self, data, *args, **kwargs):
        bar(np.array([2.0]), data)


# ----- Functions with different order of input parameters -----
def foo(data, mask):
    return data*mask

def bar(mask, data):
    return data*mask


class TestBenchmarkSuite(unittest.TestCase):
    def test_create_suite(self):
        tests = ['time_foo', 'time_bar']
        suite = BenchmarkSuite(map(BenchArrayMultiplication, tests))
        for case in suite:
            self.assertTrue(case.func_name in tests)


class TestBenchmarkLoader(unittest.TestCase):
    def test_load_cases(self):
        tests = ['time_foo', 'time_bar']
        loader = BenchmarkLoader()
        suite = loader.load_cases(BenchArrayMultiplication)
        for case in suite:
            self.assertTrue(case.func_name in tests)


class TestBenchmarkRunner(unittest.TestCase):
    def test_run_suite(self):
        loader = BenchmarkLoader()
        suite = loader.load_cases(BenchArrayMultiplication)
        runner = BenchmarkRunner()
        runner.run_benchmark_suite(suite)
