#%%  test connect to oven
import OvenLib as OO
import serial

oven = serial.Serial()

usb_port = "COM7"


usb_port = "COM7"

covesion_enable_oven(oven, port=usb_port)

print("current T = ", OO.covesion_check_temperature(oven), " C")

OO.covesion_enable_oven(oven, port=usb_port)

print("current T = ", OO.covesion_check_temperature(oven), " C")
oven.close()
