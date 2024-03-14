from time import sleep

import numpy as np
from matplotlib import pyplot as plt

import Coinc_Counter as cc
import QuTAG_MC as qt

tt = qt.QuTAG()
tags, channels, valid = tt.getLastTimestamps(True)
sleep_dur = 1
print(f"Gathering data for {sleep_dur} seconds.")
sleep(sleep_dur)
tags, channels, valid = tt.getLastTimestamps(True)
print(f"Gathered data for {sleep_dur} seconds.")
tt.deInitialize()

ch1 = 0
ch2 = 1
dt = 10e-9
t = 0e-9
print("Running the scan")

maxT = 1e-6
coincidences = cc.CountCoincidences(
    tags, channels, int(valid), ch1, ch2, float(dt), float(t), float(maxT)
)
print(coincidences)
# n = 100
# coincidences = cc.CoincidancesWithBlocks(
#     tags, channels, int(valid), ch1, ch2, int(n), float(dt), float(t)
# )
# print(coincidences)

t1 = 0
t2 = 1e-8
histlen = 1000
coincidences = cc.getCoincidenceHistogram(
    tags, channels, int(valid), ch1, ch2, dt, t1, t2, histlen
)

plt.plot(np.linspace(t1, t2, np.size(coincidences)), coincidences)
plt.title("Coincidances vs ")
plt.xlabel("Time/s")
plt.ylabel("Coincidances/Hz")
plt.grid(True)
plt.show()
