import ctypes

import numpy as np

# Load the shared library
coincidence_counter = ctypes.CDLL(
    "./build/lib.linux-x86_64-3.10/Coinc_Counter.cpython-310-x86_64-linux-gnu.so"
)  # Adjust the filename/path as needed


# Define the Event structure
class Event(ctypes.Structure):
    _fields_ = [("channel", ctypes.c_int), ("timestamp", ctypes.c_longlong)]


# Define the countCoincidences function


# int64_t countCoincidences(Event events[], int size, long long threshold, char *unit);
def count_coincidences(events, size, threshold, unit):
    return coincidence_counter.countCoincidences(
        events, size, threshold, unit.encode("utf-8")
    )


# int64 determineCoincidences(Event events[], int64 valid, int64 ch1, int64 ch2, double dt, double T, double maxT); # count_coincidences
# Define the determineCoincidences function
def CountCoincidences(events, valid, ch1, ch2, dt, t, maxT):
    return coincidence_counter.determineCoincidences(
        events, valid, ch1, ch2, dt, t, maxT
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
def getCoincidenceHistogram(events, valid, ch1, ch2, dt, t1, t2, histlen):
    # Create a NumPy array to store the histogram
    hist = np.zeros(int(histlen), dtype=np.int64)
    # Convert the events to a pointer to Event structure

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
