# %%  test connect to oven

import time

import OC

usb_port = "/dev/ttyUSB0"


print("OC.OC")
oven = OC.OC(usb_port)  # OC3 Code from them
print("Enable")
oven.enable()
print("Setting temp")
oven.set_temperature(45)
time.sleep(10)
print(oven.temperature[0])
oven.disable()
