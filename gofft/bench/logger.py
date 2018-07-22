from __future__ import absolute_import
import numpy as np

__all__ = ['LogWriter', 'LogReader']


class LogWriter(object):
    """
    Default log writer. 
    User can create a custom writer by inheriting this class.
    """
    def write(self, fn, content, delimiter=','):
        np.savetxt(fn, content, delimiter=delimiter)


class LogReader(object):
    """
    Default log reader. 
    User can create a custom reader by inheriting this class.
    """
    def read(self, fn, delimiter=','):
        """
        Parameters
        ----------
        fn : str
            Path of log file.
        """
        content = np.loadtxt(fn, delimiter=delimiter)
        x = content[:, 0]
        y = content[:, 1:]
        return x, y
