import datetime
from time import localtime, perf_counter, sleep, strftime

import numpy as np

try:
    import QuTAG_MC as qt
except Exception as e:
    print("Can't find QuTAG_MC.")
    exit(1)


def deg_polar(deg: int, precision: int = 4):
    return round(np.cos(deg), precision) + 1j * round(np.sin(deg), precision)


# Initialize QuTAG device
tt = qt.QuTAG()
exposure_time = 0.1
tt.setExposureTime(int(exposure_time * 1000))
_, coincWin, expTime = tt.getDeviceParams()
print(f"Coincidence window: {coincWin}\nBins, exposure time: {expTime} ms")

# Initialize data structures
channels = [1, 2, 3, 4]
coincidences = {"1/2": 33, "1/3": 34, "2/3": 35, "1/4": 36, "2/4": 37, "3/4": 38}

exposure_time_timetagger = 60

angles = np.linspace(0, 358, 180, dtype=int)

tt.deInitialize()
print(angles)
exit(2)

data_for_tomography = f"Data/DataForTomography_{datetime.date.today()}_{strftime('%H_%M_%S', localtime())}.csv"
f = open(data_for_tomography, "w")
f.write("# Singles1,Singles2,Singles3,Singles4,1/2,1/3,2/3,1/4,2/4,3/4")

for angle in angles:
    sleep(exposure_time_timetagger)
    data, updates = tt.getCoincCounters()
    logdata = [deg_polar(angle, 4)]
    if updates == 0:
        print("Waiting for data...")
    else:
        # Singles
        for ch in channels:
            logdata.append(data[ch])
        # Coincidences
        for coinc in coincidences:
            coinc_idx = coincidences[coinc]
            logdata.append(data[coinc_idx])
    logdata_str = ",".join(map(str, logdata))
    f = open(data_for_tomography, "a")
    f.write(logdata_str + "\n")
    answer = input("Continue the scan or stop [y/n]")
    if answer == "y":
        continue
    else:
        break
tt.deInitialize()
