#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
wav2mp3.py

Created by kurt on 2010-07-12.

Uses ffmpeg to convert all the .wav files in a dir to mp3.

wav2mp3.py -s /some/src/dir -t Author-TitleOfDisk -d 03 

"""

import sys
import os
import logging
import subprocess
import datetime
import fnmatch
import shutil
import optparse



#source_dir = '/web/music'
#ffmpeg = '/usr/bin/ffmpeg'
#ffmpeg = '/usr/local/bin/ffmpeg'
ffmpeg = '/usr/bin/env ffmpeg'


LOG_FILENAME = '/web/log/mp3-conversion.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


def tstamp():
    """Fri, 2009-03-20 13:46:55"""
    return datetime.datetime.now().strftime("%a, %Y-%m-%d %H:%M:%S")


def getFiles(source_dir):
    """gets a list of wmv files"""
    files = [file for file in os.listdir(source_dir) \
            if fnmatch.fnmatch(file, '*.wav')]
    return files


def ripFiles(source_dir, files, title, disk):
    """   """
    for f in files:
        fn = f[:-4]
        infile ='%s/%s.wav' % (source_dir, fn)

        ofile = f[5:-4].strip()
        if len(f[5:-4].strip()) == 1:
            ofile = '0' + f[5:-4].strip()

        outfile = '%s/converted/%s-%s-%s.mp3' % (source_dir,
                                                title, disk, ofile)

        prog = [ffmpeg,
            '-i', infile,
            '-acodec', 'libmp3lame',
            '-ab', '128k',
            outfile,
            ]
        convert = subprocess.Popen(prog, stdout=subprocess.PIPE)
        ripout = convert.communicate()[0]
        logging.debug(ripout)
        shutil.move(infile, '%s/old/%s.wav' % (source_dir, fn))


def usage():
    content = """
    You must include at least --title and --disk...
      ./wav2mp3.py --title TitleOfAlbum --disk 02

    and optionally a source:
      ./wav2mp3.py --source /some/directory --title TitleOfAlbum --disk 02

    You may also use -s, -d, and -t for source, disk, and title:
      ./wav2mp3.py -s /some/directory -t TitleOfAlbum -d 02

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
#    p.add_option('--details', '-?', action='store_true',
#        help="Get usage examples.")

    options, arguments = p.parse_args()
    source_dir = options.source

    #import pdb; pdb.set_trace()
    if options.usage:
        print usage()
        sys.exit()

    if options.disk and options.title:
        fprefix = '%s-%s-' % (options.title, options.disk)

        # does the directory exist?
        if not os.path.isdir(source_dir):
            print '\nWARNING: There is no source directory at: %s' % (source_dir)
            sys.exit()

        #do any flv files exist?
        files = [file for file in os.listdir(source_dir)
            if fnmatch.fnmatch(file, '*.wav')]
        if not len(getFiles(source_dir)):
            print '\nWARNING: There are no files in %s' % (source_dir)
            sys.exit()

        logging.debug('##### Starting batch convert @ %s #####' % (tstamp()))
        ripFiles(source_dir=source_dir, files=files,
            title=options.title, disk=options.disk)
        logging.debug('##### Completed batch @ %s #####\n\n' % (tstamp()))
    else:
        print usage()

if __name__ == '__main__':
    main()


