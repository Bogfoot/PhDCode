#%%  test connect to oven
import serial

oven = serial.Serial()

usb_port = "COM7"


oven.baudrate = 19200
oven.port = usb_port
oven.parity = serial.PARITY_NONE
oven.stopbits = serial.STOPBITS_ONE
oven.bytesize = serial.EIGHTBITS
oven.timeout = 1

oven.open()
print("is the serial port open? ", oven.is_open)
print()

# oven.flushOutput()
# send_message = "(0x01)j00CB"
send_message = "\x01j00CB"
# send_message = "\x01i191;60;100;0;100;1;0;BB"
oven.write(send_message.encode())

print("read line from controler over USB:")
oven_output = oven.read(68)
oven_output_convert = list(oven_output)
a = list()
for i in range(len(oven_output_convert)):
    a.append(chr(oven_output_convert[i]))

print(a)
# print(oven.read(20))

print()
print("is the serial port closed? ", oven.is_open * False == 0)


covesion_enable_oven(oven, port=usb_port)

print("current T = ", covesion_check_temperature(oven), " C")
oven.close()
