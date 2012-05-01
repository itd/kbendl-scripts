#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
An example pythonish 'which' implementation. I used it to check
for the existence of, and get the path for, a specific executable.
"""

import os

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
