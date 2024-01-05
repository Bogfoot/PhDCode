import time

try:
    import QuTAG as qt
except:
    print(f"Didn't find QuTAG or something went wrong.")

#%%  test connecting to time tagger
channel_1 = 1
channel_2 = 2


# Initialize the quTAG device
tt = qt.QuTAG()

# Get the timebase (the resolution) from the quTAG. It is used as time unit by many other functions.
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")


# Set the exposure or integration time in milliseconds, range = 0..65535
tt.setExposureTime(1 * 1000)  # ms Counting

tt.enableChannels((1, 2))  # Enables channel 0,2,3

time.sleep(1)

data, updates = tt.getCoincCounters()

# wait a little to get the device started calibrating
time.sleep(2)

data, updates = tt.getCoincCounters()
print("Updates since last call: ", updates, "| Data: ", data)
print("channel: ", channel_1, ", counts: ", data[channel_1])
print("channel: ", channel_2, ", counts: ", data[channel_2])
print("channel: coincidences, counts: ", data[5])

print(tt.discover())

tt.deInitialize()
