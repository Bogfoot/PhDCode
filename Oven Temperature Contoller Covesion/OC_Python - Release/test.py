import time

import OC

usb = "/dev/ttyUSB0"
oc = OC.OC(usb)
# Turn off the OC
oc.disable()
time.sleep(2)
oc.enable()
time.sleep(2)
oc.disable()
time.sleep(2)
oc.enable()
time.sleep(2)
oc.disable()


# Close the serial port
oc.OC_close()
