import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

dirname = sys.argv[1]


# # Read the data from the file, skipping rows starting with #
column_names = ["Temperature", "ClicksH", "ClicksV", "Coincidances"]
dt = pd.read_csv(
    dirname, delim_whitespace=True, comment="#", names=column_names, encoding="latin-1"
)

plt.figure(figsize=(10, 10))

label = dirname[:12]
dt["ClicksV"] = dt["ClicksV"] / 60
dt["ClicksH"] = dt["ClicksH"] / 60
dt["SumOfClicks"] = dt["ClicksV"] + dt["ClicksH"]
min_sum = dt["SumOfClicks"].min()
max_sum = dt["SumOfClicks"].max()
dt["NormallizedSumOfClicks"] = (dt["SumOfClicks"] - min_sum) / (max_sum - min_sum)
dt["Coincidances"] = dt["Coincidances"] / 60
min_value = dt["Coincidances"].min()
max_value = dt["Coincidances"].max()
dt["coincidance_normalized"] = (dt["Coincidances"] - min_value) / (
    max_value - min_value
)
plt.plot(dt["Temperature"], dt["Coincidances"]*100, label="Correlations")

plt.plot(dt["Temperature"], dt["SumOfClicks"], label="Sum of Clicks")
plt.plot(dt["Temperature"], dt["ClicksH"], label="Clicks H")
plt.plot(dt["Temperature"], dt["ClicksV"], label="Clicks V")


# Fitting gaussian


# Define the Gaussian function
def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-(((x - mean) / stddev) ** 2) / 2)


# Initial guess for the parameters
initial_guess = [1, np.mean(dt["Temperature"]), np.std(dt["Temperature"])]

# Fit the data to the Gaussian function
params, covariance = curve_fit(
    gaussian, dt["Temperature"], dt["Coincidances"]*100, p0=initial_guess
)

# Extract the fitted parameters
amplitude, mean, stddev = params

# Plot the original data and the fitted Gaussian curve
plt.plot(
    dt["Temperature"],
    gaussian(dt["Temperature"], amplitude, mean, stddev),
    color="red",
    label="Gaussian Fit of Correlations",
)

# Print the parameters of the fitted Gaussian curve
print(f"Amplitude: {amplitude}")
print(f"Mean: {mean}")
print(f"Standard Deviation: {stddev}")
plt.title("Clicks")
plt.xlabel("Temperature (°C)")
plt.ylabel("Normalized Counts (A.U.)")
plt.legend()
plt.grid(True)
plt.show()
