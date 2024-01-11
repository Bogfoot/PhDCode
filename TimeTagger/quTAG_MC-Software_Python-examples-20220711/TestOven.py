#%%  test connect to oven
import OvenLibV2 as OO
import pyserial

usb_port = "/dev/ttyUSB0"
oven = pyserial.Serial(usb_port)


oven = OO.OvenController(oven, port=usb_port)
oven.enable_oven()

print("current T = ", oven.check_temperature(), " C")
oven.close()
