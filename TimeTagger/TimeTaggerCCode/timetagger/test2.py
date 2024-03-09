import Coinc_Counter as cc

events = (cc.Event * 10)()  # Assuming a maximum of 10 events
events[0].tag = 100
events[0].channel = 1
events[1].tag = 202
events[1].channel = 2
events[2].tag = 102
events[2].channel = 1
events[3].tag = 203
events[3].channel = 2
events[4].tag = 105
events[4].channel = 1
events[5].tag = 205
events[5].channel = 2
valid = 2
ch1 = 1
ch2 = 2
dt = 0.1
T1 = 0.0
T2 = 1.0
histlen = 10
hist = cc.getCoincidenceHistogram(events, valid, ch1, ch2, dt, T1, T2, histlen)
print("Histogram:", hist)
