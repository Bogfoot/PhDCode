import time

import OC

try:
    import QuTAG_MC as qt
except:
    print(f"Didn't find QuTAG or something went wrong.")

# %%  test connecting to time tagger
channel_1 = 1
channel_2 = 2
coincidances12 = 33


# Initialize the quTAG device
tt = qt.QuTAG()
oven = OC.OC("/dev/ttyUSB0")
oven.enable()
oven.set_temperature(41.10)
print(oven.get_temperature())
# Get the timebase (the resolution) from the quTAG. It is used as time unit by many other functions.
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")


# Set the exposure or integration time in milliseconds, range = 0..65535
exposure_time_seconds = 1
tt.setExposureTime(int(1000 * exposure_time_seconds))  # ms Counting

time.sleep(1)

data, updates = tt.getCoincCounters()

# wait a little to get the device started calibrating
time.sleep(1)

data, updates = tt.getCoincCounters()
print("Updates since last call: ", updates, "| Data: ", data)
print("channel: ", channel_1, ", counts: ", data[channel_1])
print("channel: ", channel_2, ", counts: ", data[channel_2])
print("channel: ", 3, ", counts: ", data[3])
print("channel: coincidences, counts: ", data[coincidances12])

print(tt.discover())

tt.deInitialize()
tt.getDeviceParams()
oven.OC_close()
