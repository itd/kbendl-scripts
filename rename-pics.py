#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
This takes all the pics in the current
directory that are in the format:
    cam1-12-11-29_15-26-32-22.jpg
and renames them to:
    12112915263222.jpg
"""
import os

files = os.listdir('./')
files = [f for f in files if 'jpg' in f]
for fi in files:
    fout = fi.split('.jpg')
    fout = fout[0]
    fout = fout.split('-')[1:]
    fout = ''.join(fout)
    fout = fout.split('_')
    fout = ''.join(fout)
    fout = '%s.jpg' % fout
    os.rename(fi, fout)

