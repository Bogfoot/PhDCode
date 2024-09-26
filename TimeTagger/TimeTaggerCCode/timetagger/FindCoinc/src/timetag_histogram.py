import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to read the timestamps from a file for channel 1
def read_channel_1_timestamps(filename):
    timestamps = []
    with open(filename, 'r') as file:
        for line in file:
            timestamp, channel = line.strip().split(',')
            channel = int(channel)
            timestamp = int(timestamp)
            if channel == 1:
                timestamps.append(timestamp)
    return np.array(timestamps)

# Read timestamps for channel 1 from both files
timestamps_11_03 = read_channel_1_timestamps('qkd_timestamps_11_03.txt')
timestamps_11_07 = read_channel_1_timestamps('qkd_timestamps_11_07.txt')

# Define 1-second bins (10^12 picoseconds)
bin_width = 1e12  # 1 second in picoseconds
min_timestamp = min(timestamps_11_03.min(), timestamps_11_07.min())
max_timestamp = max(timestamps_11_03.max(), timestamps_11_07.max())

# Create bins based on the range of timestamps and bin width
bins = np.arange(min_timestamp, max_timestamp + bin_width, bin_width)

# Plot histograms for both files
plt.figure(figsize=(12, 6))

# Histogram for qkd_timestamps_11_03
plt.hist(timestamps_11_03, bins=bins, alpha=0.5, label='Channel 1 - 11_03')

# Histogram for qkd_timestamps_11_07
plt.hist(timestamps_11_07, bins=bins, alpha=0.5, label='Channel 1 - 11_07')

# Labels and title
plt.xlabel('Timestamps (ps)')
plt.ylabel('Counts')
plt.title('Histogram of Channel 1 Timestamps')
plt.legend(loc='upper right')

# Display the plot
plt.tight_layout()
plt.show()
