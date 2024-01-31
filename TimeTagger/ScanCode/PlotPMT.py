import sys

import matplotlib.pyplot as plt
import pandas as pd

file_name = sys.argv[1]
# Read the data from the file, skipping rows starting with #
data = pd.read_csv(file_name, delim_whitespace=True, comment="#")

# Plot the data
plt.figure(figsize=(10, 6))

plt.plot(data["Temperature"], data["Clicks_1"], label="Clicks_1")
plt.plot(data["Temperature"], data["Clicks_2"], label="Clicks_2")
plt.plot(data["Temperature"], data["Correlations"]*100, label="Correlations")

plt.title("Temperature vs. Clicks and Correlations")
plt.xlabel("Temperature (°C)")
plt.ylabel("Counts")
plt.legend()
plt.grid(True)
plt.show()
