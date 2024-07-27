import os
import datetime
import numpy as np

# Configurable parameters
start, stop, steps = -50000, 50000, 201
time_delay = np.linspace(start, stop, steps, dtype=int)
channels = [1, 2, 3, 4]

# Coincidence channels
pairs = ['1/2', '1/3', '1/4', '2/3', '2/4', '3/4']
coincidences_dict = {
    '1/2': 33,
    '1/3': 34,
    '1/4': 35,
    '2/3': 36,
    '2/4': 37,
    '3/4': 38
}

# Simulated data retrieval function
def get_simulated_data():
    return {33: 100, 34: 101, 35: 102, 36: 103, 37: 104, 38: 105}

# Create data directory if it doesn't exist
if not os.path.exists("Data"):
    os.mkdir("Data")

# Loop over each channel
for i, channel in enumerate(channels):
    remaining_channels = channels[i+1:]
    if not remaining_channels:
        break

    # Create file name
    file_name = f"Data/coincidences_{channel}{''.join(map(str, remaining_channels))}.csv"
    
    # Open data file for appending
    with open(file_name, "a") as f:
        # Main loop for time delay scanning
        for times in time_delay:
            try:
                print(f"Currently on iteration {times} for channel {channel}.")

                # Simulate setting the delay for the current channel
                # Simulate integrating time
                
                # Get simulated coincidence counters
                data = get_simulated_data()
                
                # Log data for each coincidence pair involving the current channel
                log_data = [times]
                for other_channel in remaining_channels:
                    pair = f"{channel}/{other_channel}"
                    coinc_value = data[coincidences_dict[pair]]
                    log_data.append(coinc_value)
                
                # Print and write the log data
                log_data_str = ','.join(map(str, log_data))
                print(f"Now it's: {datetime.date.today()}\n{log_data_str}\n")
                f.write(log_data_str + "\n")

            except Exception as e:
                print(f"Error during iteration {times} for channel {channel}: {e}")
                raise
