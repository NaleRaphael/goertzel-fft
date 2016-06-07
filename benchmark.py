import argparse
import os
import time
import traceback
import matplotlib.pylab as plt
import numpy
import fileio
from benchfunc import alglist

LOG_FOLDER = 'perflog'
DATA_FOLDER = 'data'
DEMO_FILE = 'rawecg.csv'


def benchmark(filename, fs, ft, width, method, step=100, rd=1):
    logname = str(method.__name__)+'_'+time.strftime('%y%m%d%H%M%S')+'.csv'
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

    logfile.write('{0},{1}\n'.format(0, 0))
    for i in range(1, step+1):
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
#        alg_name = os.path.basename(f)
        flegend.append(alg_name)

    fig.legend(flegend, loc=2)
    plt.title('Comparision of running time')
    plt.xlabel('data length')
    plt.ylabel('time taken (s)')
    plt.show()


def parse_str2ary(string):
    if string:
        raw = string.split(',')
        ft = numpy.zeros(len(raw))
        try:
            for i, f in enumerate(raw):
                ft[i] = numpy.float(f)
        except:
            raise
        return ft


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-m', dest='method', metavar='method',
                           default=None, help='method name.')
    argparser.add_argument('-f', dest='file', metavar='file',
                           default=None, help='test file (data).')
    argparser.add_argument('--fs', dest='fs', metavar='fs', type=int,
                           default=1000, help='sampling rate.')
    argparser.add_argument('--ft', dest='ft', metavar='ft', type=str,
                           default='50,60', help='target frequency, please use comma(\',\') as a delimiter.')
    argparser.add_argument('--width', dest='width', metavar='width', type=int,
                           default=1000, help='width of window for short time algorithm.')
    argparser.add_argument('--step', dest='step', metavar='step', type=int,
                           default=100, help='rounds for computation starting from 0 to len(data).')
    argparser.add_argument('--rd', dest='rd', metavar='rd', type=int,
                           default=5, help='repeated execution times per step.')

    try:
        args = argparser.parse_args()
    except Exception as ex:
        print(ex.message)
        exit()

    single_run = True  # no selected method
    if args.method is None:
        single_run = False
    elif not alglist.get(args.method):
        print('Invalid method name.')
        exit()

    if args.file:
        if not os.path.exists(args.file):
            print(args.file)
            print('File does not exist.')
            exit()
    else:
        data_dir = os.getcwd()
        args.file = os.path.join(data_dir, DATA_FOLDER, DEMO_FILE)
        if not os.path.exists(args.file):
            print('Please check \'data\' folder.')
            exit()
    
    ft = parse_str2ary(args.ft)
    if ft is None:
        print('No target frequency is given.')
        exit()

    try:
        if single_run:
            method = alglist[args.method]
            print method
            benchmark(args.file, args.fs, ft, args.width, method,
                      step=args.step, rd=args.rd)
        else:
            for k in alglist.keys():
                print('Currently running: {0}'.format(k))
                method = alglist[k]
                print method
                benchmark(args.file, args.fs, ft, args.width, method,
                      step=args.step, rd=args.rd)
        # plot result
        plt_perflog()
    except Exception as ex:
        print(ex.message)
        traceback.print_exc()
