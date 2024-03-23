import sys

from OC import OC

temp = float(sys.argv[1])
ramp = float(sys.argv[2])
oven = OC("/dev/ttyUSB0")
oven.set_temperature(temp)
oven.set_ramp_rate(ramp)
print(oven.ramp_rate)
oven.OC_close()
