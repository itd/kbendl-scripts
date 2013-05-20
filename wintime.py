#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8

# Sourced from:
#   http://reliablybroken.com/b/2011/09/free-software-ftw-updated-filetimes-py/
# Then hacked a bit for my own nefarious desires. -kb
""" Converts between Microsoft / ACtive Directory times
    and Python datetime objects.
"""
import sys
from datetime import datetime, timedelta, tzinfo
from calendar import timegm
import argparse
from argparse import RawTextHelpFormatter

# http://support.microsoft.com/kb/167296
# How To Convert a UNIX time_t to a Win32 FILETIME or SYSTEMTIME
EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
HUNDREDS_OF_NANOSECONDS = 10000000

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

class UTC(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = UTC()

def dt_to_wintime(dt):
    """Converts a datetime to MS time format. If the object is
    time zone-naive, it is forced to UTC before conversion.

    >>> "%.0f" % dt_to_wintime(datetime(2009, 7, 25, 23, 0))
    '128930364000000000'

    >>> "%.0f" % dt_to_wintime(datetime(1970, 1, 1, 0, 0, tzinfo=utc))
    '116444736000000000'

    >>> "%.0f" % dt_to_wintime(datetime(1970, 1, 1, 0, 0))
    '116444736000000000'

    >>> dt_to_wintime(datetime(2009, 7, 25, 23, 0, 0, 100))
    128930364000001000
    """
    if (dt.tzinfo is None) or (dt.tzinfo.utcoffset(dt) is None):
        dt = dt.replace(tzinfo=utc)
    ft = EPOCH_AS_FILETIME + (timegm(dt.timetuple()) * HUNDREDS_OF_NANOSECONDS)
    return ft + (dt.microsecond * 10)


def wintime_to_dt(wintime):
    """Converts a Microsoft time number/string to a Python datetime. The new
    datetime object is time zone-naive but is equivalent to tzinfo=utc.
    Now accepts string or int for windows time.

    >>> wintime_to_dt(116444736000000000)
    datetime.datetime(1970, 1, 1, 0, 0)

    >>> wintime_to_dt(128930364000000000)
    datetime.datetime(2009, 7, 25, 23, 0)

    >>> wintime_to_dt(128930364000001000)
    datetime.datetime(2009, 7, 25, 23, 0, 0, 100)

    >>> wintime_to_dt('129806176114169067')
    datetime.datetime(2012, 5, 4, 15, 6, 51, 416906)
    """
    wintime = int(wintime)
    # Get seconds and remainder in terms of Unix epoch
    (s, ns100) = divmod(wintime - EPOCH_AS_FILETIME, HUNDREDS_OF_NANOSECONDS)
    # Convert to datetime object
    dt = datetime.utcfromtimestamp(s)
    # Add remainder in as microseconds. Python 3.2 requires an integer
    dt = dt.replace(microsecond=(ns100 // 10))
    return dt

def examples():
    content = """
    Decodes windows time to something human readable
    Minimal command usage:\n
    wintime.py 130236120000000000\n
     2013-09-14\n
\n
    ...and optionally a format option for long or medium (-fl, -fm):\n
    wintime.py -fl -t 130236120000000000\n
    Sep. 14 2013  06:00:00\n
\n
    wintime.py -fm 130236120000000000\n
    2013-09-14 06:00:00\n

    """
    return content


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=examples(),
                                formatter_class=RawTextHelpFormatter)
    p.add_argument('-e', action="store_true", default=False, dest='ex')
    p.add_argument('-f', action="store", default='s', dest='format',
        help="options are: s, m, l - short, medium, or long format",
        choices=('s', 'm', 'l')
        )
    p.add_argument('windows_time_stamp', action="store",
        help='The AD or Microsoft time stamp, e.g., "130236120000000000"')
    #print p.parse_args()
    results = p.parse_args()

    if results.ex:
        print examples()
        sys.exit()

    format = results.format
    wt = results.windows_time_stamp
    print wt
    # if len(wt) is not 18:
    #     print "The windows/AD time stamp entered should be 18 digits long."
    #     sys.exit()

    otime = wintime_to_dt(wt)
    out = otime.strftime('%Y-%m-%d')
    if format == 'm':
        out = otime.strftime('%Y-%m-%d %H:%M:%S')
    if format == 'l':
        out = otime.strftime('%b. %d %Y  %H:%M:%S')

    print out

