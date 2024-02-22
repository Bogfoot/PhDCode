from time import sleep

from OC import OC

oven = OC("/dev/ttyUSB0")
temp = 41.0
ramp = 0.5

oven.enable()
sleep(1)

oven.set_ramp_rate(ramp)
oven.set_temperature(temp)
sleep(60)
oven.OC_close()
