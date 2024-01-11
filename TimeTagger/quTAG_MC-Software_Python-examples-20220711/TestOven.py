#%%  test connect to oven
import OvenLibV2 as OO
import serial
usb_port = "/dev/ttyUSB0"
oven = serial.Serial(port=usb_port)


oven = OO.OvenController(oven, port=usb_port)
oven.enable_oven()

print("current T = ", oven.check_temperature(), " C")
oven.close()
