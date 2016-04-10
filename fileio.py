import csv
import os
import numpy


__all__ = ['gensig', 'csvtosig']

DATA_FOLDER = 'data'

def gensig(T, fs, ft, fname=None):
    """
    Generate a signal series according to given parameters.
    
    Parameters 
    ----------
    T : int or float
        Duration of signal. signal length: T*fs
    fs : int
        Sampling rate.
    ft : int
        Target frequency.
    fname : string
        If fname is given, generated signal will be saved as a file.
    
    Returns
    -------
    sig : ndarray
        Generated signal.
    
    Example
    -------
    To generate a 60Hz signal
    
    >>> sig = gensig(10, 1000, 60, 'sig_60Hz.csv')
    
    and the file will be saved at "..\data\sig_60Hz.csv"
    """
    t = numpy.linspace(0, T, T*fs)
    sig = numpy.sin(2*numpy.pi*ft*t)
    
    if fname:
        data_dir = os.getcwd()
        outpath = os.path.join(data_dir, DATA_FOLDER, fname)
        try:
            outfile = open(outpath, mode='w')
        except:
            raise
    
    for d in iter(sig):
        outfile.write('{0}\n'.format(d))
    outfile.close()
    
    return sig


def csvtosig(filepath, column=0):
    """
    Convert .csv file (no header) to singal.
    
    Parameters
    ----------
    filepath : string
        Path of .csv file.
    
    column : int
        If the dimension of data is more than 1, user should specify which 
        column to return.
    
    Returns
    -------
    sig : ndarray
        Converted signal.
    """
    reader = csv.reader(open(filepath, 'r'), delimiter=',')
    x = list(reader)
    a = numpy.array(x)
    return a[:, column].astype('float')
