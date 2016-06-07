import argparse
import os
import traceback

import fileio

DATA_FOLDER = 'data'

def export_sig(fs, ft):
    fileio.gensig()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fs', dest='fs', metavar='fs', type=int,
                           default=1000, help='sampling rate.')
    argparser.add_argument('--ft', dest='ft', metavar='ft', type=int,
                           default=60, help='target frequency.')
    argparser.add_argument('-T', dest='T', metavar='T', type=float,
                           default=100, help='duration of signal. signal length = T*fs.')
    argparser.add_argument('-f', dest='file', metavar='file', type=str,
                           default=None, help='file path.')

    try:
        args = argparser.parse_args()
    except Exception as ex:
        print(ex.message)
        exit()

    if args.file is None:
        dir_path = os.getcwd()
        filepath = os.path.join(dir_path, DATA_FOLDER, 'new_sig.csv')
    else:
        filepath = args.file

    try:
        newsig = fileio.gensig(args.T, args.fs, args.ft, filepath)
    except Exception as ex:
        print(ex.message)
        traceback.print_exc()
