import ctypes

import numpy as np

from timing import get_time

# Load the shared library
coincidence_counter = ctypes.CDLL(
    "./build/lib.linux-x86_64-3.10/Coinc_Counter.cpython-310-x86_64-linux-gnu.so"
)  # Adjust the filename/path as needed


# Define the Event structure
class Event(ctypes.Structure):
    _fields_ = [("channel", ctypes.c_int), ("timestamp", ctypes.c_longlong)]


# Define the countCoincidences function
# int64_t countCoincidences(Event events[], int size, long long threshold, char *unit);
# Mostly a joke - Do not run as it will give the wrong result
# coincidence_counter.countCoincidences.restype = ctypes.c_longlong
# coincidence_counter.countCoincidences.argtypes = [
#     ctypes.POINTER(Event),
#     ctypes.c_longlong,
#     ctypes.c_longlong,
#     ctypes.POINTER(ctypes.c_char),
# ]
# def count_coincidences(tags, ch, valid, threshold, unit):
#     events = Event * valid
#     events = events()
#     for i in range(valid):
#         events[i].timestamp = int(tags[i])
#         events[i].channel = int(ch[i])
#     return coincidence_counter.countCoincidences(
#         events, valid, threshold, unit.encode("utf-8")
#     )


# int64 determineCoincidences(Event events[], int64 valid, int64 ch1, int64 ch2, double dt, double T, double maxT); # count_coincidences
# Define the determineCoincidences function
# Define the function prototype
coincidence_counter.determineCoincidences.restype = ctypes.c_longlong
coincidence_counter.determineCoincidences.argtypes = [
    ctypes.POINTER(Event),
    ctypes.c_longlong,
    ctypes.c_longlong,
    ctypes.c_longlong,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
]


# tags, ch, size, int(valid), ch1, ch2, float(dt), float(t), float(maxT)
@get_time
def CountCoincidences(tags, ch, valid, ch1, ch2, dt, t, maxT):
    events = Event * valid
    events = events()
    for i in range(valid):
        events[i].timestamp = int(tags[i])
        events[i].channel = int(ch[i])
    return coincidence_counter.determineCoincidences(
        events, valid, ch1, ch2, dt, t, maxT
    )


# int64_t determineCoincidencesWithBlocks(Event events[], int64_t valid,
#                                        int64_t ch1, int64_t ch2, int64_t n,
#                                        double dt, double T)

coincidence_counter.determineCoincidencesWithBlocks.restype = ctypes.c_longlong
coincidence_counter.determineCoincidencesWithBlocks.argtypes = [
    ctypes.POINTER(Event),  # events
    ctypes.c_longlong,  # valid
    ctypes.c_longlong,  # ch1
    ctypes.c_longlong,  # ch2
    ctypes.c_longlong,  # n
    ctypes.c_double,  # dt
    ctypes.c_double,  # T
]


@get_time
def CoincidancesWithBlocks(tags, ch, valid, ch1, ch2, n, dt, t):
    events = Event * valid
    events = events()
    for i in range(valid):
        events[i].timestamp = int(tags[i])
        events[i].channel = int(ch[i])

    return coincidence_counter.determineCoincidencesWithBlocks(
        events, valid, int(ch1), int(ch2), int(n), float(dt), float(t)
    )


# Define the function prototype
coincidence_counter.determineCoincidenceHistogram.restype = None
coincidence_counter.determineCoincidenceHistogram.argtypes = [
    ctypes.POINTER(Event),
    ctypes.c_longlong,
    ctypes.c_longlong,
    ctypes.c_longlong,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_longlong),
    ctypes.c_longlong,
]


# int64_t determineCoincidenceHistogram(Event events[], int64_t valid, int64_t ch1, int64_t ch2, double dt, double T1, double T2, int64_t *hist, int64_t histlen);
# tags, ch, valid, ch1, ch2, dt, t1, t2, histlen
@get_time
def getCoincidenceHistogram(tags, ch, valid, ch1, ch2, dt, t1, t2, histlen):
    # Create a NumPy array to store the histogram
    hist = np.zeros(int(histlen), dtype=np.int64)
    # Convert the events to a pointer to Event structure

    events = Event * valid
    events = events()
    for i in range(valid):
        events[i].timestamp = int(tags[i])
        events[i].channel = int(ch[i])
    # Call the C function
    coincidence_counter.determineCoincidenceHistogram(
        events,
        valid,
        ch1,
        ch2,
        dt,
        t1,
        t2,
        hist.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
        histlen,
    )
    return hist
