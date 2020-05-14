from .install import _install_packages
from .client import up

import paramiko
import inspect
import os
import time
import configparser
import requests


def kick_web(func):

    # grab context from calling jupyter notebook
    prev_frame = inspect.currentframe().f_back  # previous frame is the notebook
    callers_objects = inspect.getmembers(prev_frame)  # grab all objects from caller's global env
    env = callers_objects[27][1]  # this slice refers to global env from jupyter notebook
    cells =  env['_ih']  # all executed cells up to function call
    print(">> initialize")
    
    def modified_func(*args):

        # step 1: write cell entries into a single source file
        fname = "temp.py"
        _copy(fname, cells)
        
        # step 2: insert __main__ to so it can be called from command line
        _make_executable(cells, fname)
        
        # step 3: send source to server through socket
        port = 7725
        up(port, fname)

        # return res


    return modified_func


def _make_executable(cells, fname):
    """make python script executable by appending __main__.
    """
    caller = cells[-1]  # get the last cell, which is the caller
    f = open(fname, "a")  # a for append, w for overwrite
    scope = 'if __name__ == "__main__":\n' + '    print(' + caller + ")"
    f.write(scope)
    f.close()


def _copy(fname, cells):
    """copy code from jupyter notebook cells into a single python file.
    """
    f = open(fname, "w")

    # iterate through each cell...    
    for cell in cells[:-1]:  # the last one is the calling cell, to be ignored
        
        # inside each cell, iterate through each line...
        lines = cell.split("\n")
        for line in lines:
            if "@kick" in line:
                pass
            elif "Kick" in line:
                pass
            else:
                f.write(line + "\n")
        f.write("\n")
    f.close()