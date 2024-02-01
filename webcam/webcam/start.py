#!/usr/bin/python3
import os

location = "lab"  # set up also for home use
if location == "lab":
    os.chdir(r"/home/bogfootlj/Documents/PhDCode/webcam/webcam/")

import getopt
import sys

from PyQt5.QtWidgets import QApplication

from modelsvideo import Camera
from viewsvideo import StartWindow

USAGE = """usage: start.py 

options:

    -h          print this short info text
    -v          print version number
    -c <num>    use webcam number "num"
    -s          save a npz file containing an array of unix timestamps and an array of recorded frames
"""

VERSION = "2.0"
camnum = 0
save_frames = False


def parse_options():
    """
    parse the command line options
    """
    prog = sys.argv[0]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvc:s")
    except getopt.GetoptError:
        print("Error in the commandline options supplied")
        print(USAGE)
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            print(USAGE)
            sys.exit()
        elif o == "-v":
            print("Version ", VERSION)
            sys.exit()
        elif o == "-c":
            global camnum
            camnum = int(a)
            print("camera number parsed: ", camnum)
        elif o == "-s":
            global save_frames
            save_frames = True
            print("Frames will be saved in a npz file.")
        else:
            assert False, "unknown option"


parse_options()
print("data streamed from camera ", camnum)
camera = Camera(camnum)
camera.initialize()
app = QApplication([])
start_window = StartWindow(camera, save_frames)
start_window.show()
app.exit(app.exec_())
