#%%  test connect to oven
import time

import OC

# usb_port = "/dev/ttyUSB0"
# oven = serial.Serial(port=usb_port)
#
#
# oven = OO.OvenController(oven, port=usb_port)
# oven.enable_oven()
#
# print("current T = ", oven.check_temperature(), " C")
# oven.close()
#
# usb_port = "COM7"
usb_port = "/dev/ttyUSB0"  # This is for use on linux, you can also use /dev/bus/usb/... maybe depending on your setup


oven = OC.OC(usb_port)  # OC3 Code from them

oven.enable()
oven.set_temperature(round(40))
print("Sleep for 10 seconds to see a different temperature")
time.sleep(10)
print(oven.temperature[0])
