#!/usr/bin/python3

import ctypes
import sys
import time

import numpy as np
import QuTAGlinux as qt
from matplotlib import pyplot as plt

USAGE = """usage: get_histogram.py

options:

    -h           print this short info text
    -d filename  load time-tagger data from file "filename"
"""


import getopt


def parse_options():
    """
    parse the command line options
    """
    prog = sys.argv[0]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:")
    except getopt.GetoptError:
        print("Error in the commandline options supplied")
        print(USAGE)
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            print(USAGE)
            sys.exit()
        elif o == "-d":
            global filename
            filename = a
            print("filename parsed: ", filename)
        else:
            assert False, "unknown option"


print("parsing now")
parse_options()
print("done parsing")

import pandas as pd

df = pd.read_csv(filename, skiprows=1)
chsraw = np.array(df["ch"], dtype=np.int8)
tagsraw = np.array(df["tags"], dtype=np.longlong)
tags = tagsraw[chsraw > 0]
chs = chsraw[chsraw > 0]
tags = tags[chs < 20]
chs = chs[chs < 20]

print("loaded %ld correct tags from %s" % (tags.size, filename))
valids = tags.size

if tags.size <= 0:
    print("something went wrong, exiting")
    sys.exit()


tt = qt.QuTAG()
# tags, chs, valids = tt.getLastTimestamps(True)
# time.sleep(10)
# tags, chs, valids = tt.getLastTimestamps(True)

coinc = tt.coincLib.determineCoincidences(
    tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
    chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
    valids,
    1,
    2,
    1e-8,
    5e-8,
    1e-5,
)
print("%d coincidences" % (coinc))


# (delaysNew,coincNew) = tt.getCoincidenceHistogram(tags,chs,valids,1,2,1e-8,0,9e-6,100)

# (delaysNew,coincNew) = tt.getSimpleHistogram(tags,chs,valids,1,2,1e-5,1e-8,100)
dt = 10e-9
maxT = 1e-6
bins = 100
tstep = maxT / bins
print("tstep (microseconds): %f" % (tstep * 1e6))
delaysNew = np.arange(bins, dtype=np.double) * tstep
print(delaysNew)
coincNew = np.zeros(bins, dtype=np.double)
i = 0
tt.coincLib.determineCoincidencesSimpleHz(
    tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
    chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
    valids,
    1,
    2,
    dt,
    7.0e-6,
)
tt.coincLib.countSinglesHz(
    tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
    chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
    valids,
    1,
)
tt.coincLib.countSinglesHz(
    tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
    chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
    valids,
    2,
)
for delay in delaysNew:
    coincNew[i] = tt.coincLib.determineCoincidencesSimpleHz(
        tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
        chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
        valids,
        2,
        1,
        dt,
        delay,
    )
    print("%ld: %f (ns), %ld Hz: " % (i, delay * 1e9, coincNew[i]))
    i = i + 1
plt.plot(delaysNew, coincNew)
plt.xlabel("delay (s)")
plt.ylabel("coincidences (Hz)")
plt.show()

print("everything is good - leaving for now")
sys.exit()
