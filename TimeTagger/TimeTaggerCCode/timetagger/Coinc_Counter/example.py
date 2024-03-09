import csv

import Coinc_Counter as cc

# import QuTAG_MC as qt


valid = 0
ch = []
tags = []
size = 0
with open("time_tags_08-03-2024.csv", "r") as f:
    valid = f.readline().strip()
    header = f.readline().strip()
    csv_reader = csv.reader(f)
    for row in csv_reader:
        ch.append(int(row[0]))
        tags.append(int(row[1]))
        size += 1
threshold = 5
unit = "ns"

events = cc.Event * size  # Assuming a maximum of 1000 events
events = events()
for i in range(size):
    events[i].channel = ch[i]
    events[i].timestamp = tags[i]
ch1 = 1
ch2 = 2
dt = 0.000000001
t = 0
maxT = 1e-7

coincidences = cc.CountCoincidences(
    events, int(valid), ch1, ch2, float(dt), float(t), float(maxT)
)
print(coincidences)
#
# t1 = 0
# t2 = 1e-8
# histlen = 1000
# coincidences = cc.getCoincidenceHistogram(
#     events, int(valid), ch1, ch2, dt, t1, t2, histlen
# )
# from matplotlib import pyplot as plt
#
# plt.hist(coincidences, bins=10)
# plt.title("Histogram of Sample Data")
# plt.xlabel("Value")
# plt.ylabel("Frequency")
# plt.grid(True)
# plt.show()
