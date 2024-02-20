import os
import sys

import matplotlib.pyplot as plt
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
print(listOfFiles)
print(len( listOfFiles ))

# Read the data from the file, skipping rows starting with #
dts = [pd.read_csv(file, delim_whitespace=True, comment="#") for file in listOfFiles]
print(dts)

# Plot the dt
plt.figure(figsize=(10, 10))

for dt in dts:
    plt.plot(dt["Temperature"], dt["Clicks_1"] + dt["Clicks_2"], label="Sum of Clicks")
    # plt.plot(dt["Temperature"], dt["Clicks_2"], label="Clicks 2")
    plt.plot(dt["Temperature"], dt["Correlations"] * 100, label="Correlations")

plt.title("Temperature vs. Clicks and Correlations")
plt.xlabel("Temperature (°C)")
plt.ylabel("Counts (Hz)")
plt.legend()
plt.grid(True)
plt.show()
