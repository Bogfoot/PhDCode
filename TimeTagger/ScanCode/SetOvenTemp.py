from OC import OC

oven = OC("/dev/ttyUSB0")
temp = 41.7
oven.set_temperature(temp)
oven.OC_close()
