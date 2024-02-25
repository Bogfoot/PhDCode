from time import sleep

from OC import OC

oven = OC("/dev/ttyUSB0")
temp = 39.0

oven.enable()
sleep(1)

# oven.set_ramp_rate(ramp)
oven.set_temperature(temp)
oven.OC_close()
