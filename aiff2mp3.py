#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
aiff2mp3.py

Created by kurt on 2010-07-12.

Uses ffmpeg to convert all the .aiff files in a dir to mp3.
Drops them into the ./converted directory.

aiff2mp3.py -s /some/src/dir -t Author-TitleOfDisk -d 03

"""

import sys
import os
import logging
import subprocess
import datetime
import fnmatch
import shutil
import optparse


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


LOG_FILENAME = 'aiff2mp3-conversion.log'
if not os.path.isfile(LOG_FILENAME):
    fpath = os.getcwd() + '/' + LOG_FILENAME
    LOG_FILENAME = fpath
    f = open(fpath, 'a')
    f.close()

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


def tstamp():
    """Fri, 2009-03-20 13:46:55"""
    return datetime.datetime.now().strftime("%a, %Y-%m-%d %H:%M:%S")


def getFiles(source_dir):
    """gets a list of aiff files"""
    files = [file for file in os.listdir(source_dir) if fnmatch.fnmatch(file, '*.aiff')]
    return files

def ripFiles(source_dir, files, title, disk, output_dir):
    """   """
    for f in files:
        fn = f[:-5]
        infile ='%s/%s.aiff' % (source_dir, fn)

        if len(fn[:2].strip()) == 1:
            fn = '0' + fn
        ofile = fn + '.aiff'
        #if len(f[5:-4].strip()) == 1:
        #    ofile = '0' + f[5:-4].strip()

        #Make sure there's a place to write the files once they are done.
        #os.path.expanduser('~')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        outfile = '%s/%s-%s-%s.mp3' % (output_dir,
                                       title, disk, fn)

        #prog = [ffmpeg, '-i', infile, '-acodec', 'libmp3lame', '-ab', '128k', outfile,]
        prog = [which('ffmpeg'), '-i', infile,
            '-f', 'mp3',
            '-ab', '128k', outfile,]
        convert = subprocess.Popen(prog, stdout=subprocess.PIPE)
        ripout = convert.communicate()[0]
        logging.debug(ripout)
        old_dir = source_dir + '/old'
        if os.path.exists(old_dir):
            #os.makedirs(old_dir)
            shutil.move(infile, '%s/%s.aiff' % (old_dir, fn))


def usage():
    content = """
    You must include at least --title and --disk...
      ./aiff2mp3.py --title TitleOfAlbum --disk 02

    and optionally a source:
      ./aiff2mp3.py --source /some/directory --title TitleOfAlbum --disk 02

    You may also use -s, -d, and -t for source, disk, and title:
      ./aiff2mp3.py -s /some/directory -t TitleOfAlbum -d 02

"""
    return content


# ffmpeg -i ky20091127.wmv -acodec libmp3lame -qscale 22 -ab 48k -ar 22050 -y -f flv ky20091127.flv
def main():
    #fprefix = 'Paolini-Eldest-Disk-04-track-'
    p = optparse.OptionParser()
    p.add_option('--title', '-t',
        help='The disk title, e.g., "Princess_Bride"')
    p.add_option('--disk', '-d',
        help='Use something like: 01')
    p.add_option('--source', '-s',
        default='/web/music',
        help='Defaults to /web/music for source files.')
    p.add_option('--usage', '-?', action='store_true',
        help="Get usage examples.")
    p.add_option('--output', '-o',
        default='/web/music/converted',
        help="Where to write the output.")
    #    p.add_option('--details', '-?', action='store_true',
#        help="Get usage examples.")

    options, arguments = p.parse_args()
    source_dir = options.source

    if options.usage:
        print usage()
        sys.exit()

    if options.disk and options.title:
        fprefix = '%s-%s-' % (options.title, options.disk)

        # does the directory exist?
        if not os.path.isdir(source_dir):
            print '\nWARNING: There is no source directory at: %s' % (source_dir)
            sys.exit()

        #do any aiff files exist?
        files = getFiles(source_dir)
        if not len(files):
            print '\nWARNING: There are no files in %s' % (source_dir)
            sys.exit()

        # is there an ffmpeg?
        if not which('ffmpeg'):
            print '\ALERT: There is no "ffmpeg" in the working $PATH.'
            sys.exit()

        logging.debug('##### Starting batch convert @ %s #####' % (tstamp()))
        ripFiles(source_dir=source_dir, files=files,
            title=options.title, disk=options.disk,
            output_dir=options.output)
        logging.debug('##### Completed batch @ %s #####\n\n' % (tstamp()))
    else:
        print usage()

if __name__ == '__main__':
    main()
