import datetime
import os
import time

import numpy as np
import QuTAG_MC as qt

# Configurable parameters
exp_time = 60  # Exposure time in seconds
start, stop, steps = -50000, 50000, 201
time_delay = np.linspace(start, stop, steps, dtype=int)
channels = [1, 2, 3, 4]

# Coincidence channels
coincidences_dict = {"1/2": 33, "1/3": 34, "1/4": 35, "2/3": 36, "2/4": 37, "3/4": 38}

# Initialize QuTAG device
try:
    tt = qt.QuTAG()
except Exception as e:
    print(f"Failed to initialize QuTAG: {e}")
    raise

# Get and print the device timebase
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")

# Set exposure time
tt.setExposureTime(exp_time * 1000)  # ms Counting

# Enable channels
tt.enableChannels(tuple(channels))
time.sleep(2)

# Create data directory if it doesn't exist
if not os.path.exists("Data"):
    os.mkdir("Data")

# Loop over each channel
for i, channel in enumerate(channels):
    remaining_channels = channels[i + 1 :]
    if not remaining_channels:
        break

    # Create file name
    file_name = (
        f"Data/coincidences_{channel}{'-'.join(map(str, remaining_channels))}.csv"
    )
    print(file_name)

    # Open data file for appending
    with open(file_name, "a") as f:
        # Main loop for time delay scanning
        for times in time_delay:
            try:
                print(f"Currently on iteration {times} for channel {channel}.")

                # Setting the delay for the current channel
                tt.setChannelDelay(channel, times)
                time.sleep(exp_time)  # integrating

                # Get coincidence counters
                data, _ = tt.getCoincCounters()

                # Log data for each coincidence pair involving the current channel
                log_data = [times]
                for other_channel in remaining_channels:
                    pair = f"{channel}/{other_channel}"
                    coinc_value = data[coincidences_dict[pair]]
                    log_data.append(coinc_value)

                # Print and write the log data
                log_data_str = ",".join(map(str, log_data))
                print(f"Now it's: {datetime.date.today()}\n{log_data_str}\n")
                f.write(log_data_str + "\n")

                # Clearing the buffer
                time.sleep(1)
            except Exception as e:
                print(f"Error during iteration {times} for channel {channel}: {e}")
                tt.deInitialize()
                raise

# Deinitialize the QuTAG device
tt.deInitialize()
