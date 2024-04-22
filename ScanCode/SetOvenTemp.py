import sys
from time import sleep

from OC import OC

oven = OC("/dev/ttyUSB0")
temp = float(sys.argv[1])

oven.enable()
sleep(1)

oven.set_temperature(temp)
oven.OC_close()
