import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = sys.argv[1]
data = pd.read_csv(file_path, header=None)

# Extract the values from the CSV file
x = np.array(data[0].values - (data[0].values)[0])
y = np.array(data[1].values)


# Plotting the data from the CSV file
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Values')

# Adding labels and title
plt.xlabel('Time [s]')
plt.ylabel('Singles')
plt.title(f'Singles plot, Total singles = {np.sum(y)}')

# Display grid and legend
plt.grid(True)
plt.legend()

# Show plot
plt.show()
