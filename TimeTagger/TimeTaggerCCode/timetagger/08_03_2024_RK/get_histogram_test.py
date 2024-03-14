#!/usr/bin/python3

import sys, getopt, ctypes, readline, csv
import numpy as np
import ctypes
import QuTAGlinux as qt
import readline
from matplotlib import pyplot as plt


USAGE='''usage: get_histogram.py 

options:

    -h           print this short info text
    -d filename  load time-tagger data from file "filename"
''' 

def parse_options():
    '''
    parse the command line options
    '''
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

with open(filename, 'r') as f:
    valid = f.readline().strip()
    csv_reader = csv.reader(f)
    ch = []
    tags = []
    for row in csv_reader:
        ch.append(int(row[0]))
        tags.append(int(row[1]))

print("loaded %ld tags from %s" % (tags.size, filename))

if ( tags.size<=0 ):
    print("something went wrong, exiting")
    sys.exit()
    
print("everything is good - leaving for now")
sys.exit()
quit()

print("exited but still being a zombi")

