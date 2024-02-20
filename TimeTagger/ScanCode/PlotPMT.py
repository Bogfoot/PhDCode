import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            if fullPath.endswith(".data"):
                allFiles.append(fullPath)
    return allFiles


dirname = sys.argv[1]

listOfFiles = getListOfFiles(dirname)

# Read the data from the file, skipping rows starting with #
column_names = ["Temperature", "ClicksH", "ClicksV", "Coincidances"]
dts = [
    pd.read_csv(
        file, delim_whitespace=True, comment="#", names=column_names, encoding="latin-1"
    )
    for file in listOfFiles
]

# Plot the dt
plt.figure(figsize=(10, 10))

for dt in dts:
    # sum = dt["ClicksV"] + dt["ClicksH"]
    min_value = dt["Coincidances"].min()
    max_value = dt["Coincidances"].max()
    dt["coincidance_normalized"] = (dt["Coincidances"] - min_value) / (
        max_value - min_value
    )
    plt.plot(dt["Temperature"], dt["coincidance_normalized"], label="Sum of Clicks")
    # plt.plot(dt["Temperature"], dt["Coincidances"] * 100, label="Correlations")

plt.title("Phase Matching Curve")
plt.xlabel("Temperature (°C)")
plt.ylabel("Counts (Hz)")
plt.legend()
plt.grid(True)
plt.show()
