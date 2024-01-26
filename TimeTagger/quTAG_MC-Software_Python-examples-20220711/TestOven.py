# %%  test connect to oven

import OC

# import OvenLibV2

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


print("OC.OC")
oven = OC.OC(usb_port)  # OC3 Code from them
# oven = OvenLibV2.OvenController(usb_port)  # OC3 Code from them

print("Enable")
# oven.enable_oven()
oven.enable()
print("Setting temp")
oven.set_temperature(40)
# print("Sleep for 10 seconds to see a different temperature")
# time.sleep(10)
print(oven.temperature[0])
# print(oven.check_temperature())
