import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = './coincidences_output.txt'
data = pd.read_csv(file_path, header=None)

# Extract the values from the CSV file
x = np.array(data[0].values)
y = np.array(data[1].values)


# Plotting the data from the CSV file
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Values')

# Adding labels and title
plt.xlabel('Time Delay [ns]')
plt.ylabel('Coincidences')
plt.title(f'Time delay plot from {x[0]} to {x[-1]} ')

# Display grid and legend
plt.grid(True)
plt.legend()

# Show plot
plt.show()
