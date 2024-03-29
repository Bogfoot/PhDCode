# %%  test connection to oven
import OC

usb_port = "/dev/ttyUSB0"


print("OC.OC")
oven = OC.OC(usb_port)  # OC3 Code from them
print("Enable")
oven.enable()
print(oven.temperature[0])
oven.disable()
