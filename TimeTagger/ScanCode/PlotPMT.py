import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            if fullPath.endswith(".data"):
                allFiles.append(fullPath)
    return allFiles


files = []
dirname = sys.argv[1]

listOfFiles = getListOfFiles(dirname)


# Read the data from the file, skipping rows starting with #
dts = [pd.read_csv(file, delim_whitespace=True, comment="#") for file in listOfFiles]

# Plot the dt
plt.figure(figsize=(10, 6))

for dt in dts:
    plt.plot(dt["Temperature"], dt["Clicks_1"], label="Clicks 1")
    plt.plot(dt["Temperature"], dt["Clicks_2"], label="Clicks 2")
    plt.plot(dt["Temperature"], dt["Correlations"] * 100, label="Correlations")

plt.title("Temperature vs. Clicks and Correlations")
plt.xlabel("Temperature (°C)")
plt.ylabel("Counts (Hz)")
plt.legend()
plt.grid(True)
plt.show()
