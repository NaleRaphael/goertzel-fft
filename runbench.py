from __future__ import absolute_import
from argparse import ArgumentParser
import traceback as tb


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--skip_bench', action='store_true', default=False, 
                        help='If this flag is true, benchmark will be skipped.')
    parser.add_argument('--skip_plot', action='store_true', default=False, 
                        help=('If this flag is true, no log will be plotted.'))

    try:
        args = parser.parse_args()
    except:
        raise
    return args


def run_bench():
    from gofft.bench import BenchmarkLoader, BenchmarkRunner
    loader = BenchmarkLoader()
    suite = loader.discover('gofft')
    BenchmarkRunner().run_benchmark_suite(suite)


def plot_log():
    from gofft.plotter import LogPlotter
    plotter = LogPlotter('bench_log', 'BenchDSP_*.csv')
    plotter.plot(scatter_plot=True)


def main():
    args = parse_args()
    if not args.skip_bench:
        run_bench()
    if not args.skip_plot:
        plot_log()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex)
        tb.print_exc()
