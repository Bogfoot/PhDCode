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
exposure_time = 1
tt.setExposureTime(int(exposure_time * 1000))
_, coincWin, expTime = tt.getDeviceParams()
print(f"Coincidence window: {coincWin} Bins, exposure time: {expTime} ms")

# Initialize data structures
channels = [1, 2, 3, 4]
coincidences = {"1/4": 36, "1/3": 34, "2/4": 37, "2/3": 35}

angles = [0, 22.5, 45]

data_for_tomography = f"Data/DataForTomography_{datetime.date.today()}_{strftime('%H_%M_%S', localtime())}.csv"
f = open(data_for_tomography, "w")
f.write("# S1,S2,S3,S4,1/4,1/3,2/4,2/3")
f.close()

for angle in angles:
    for other_angle in angles:
        for i in range(5):
            sleep(exposure_time)
            data, updates = tt.getCoincCounters()
            print(f"Iteration {i+1}, Angle left: {angle}, Angle right: {other_angle}")
            logdata = [i]
            logdata.append(angle)
            logdata.append(other_angle)

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
            print(logdata_str)
            f = open(data_for_tomography, "a")
            f.write(logdata_str + "\n")
            f.close()

        answer = input("Continue the scan or stop [y/n]")
        if answer == "":
            continue
        else:
            break
tt.deInitialize()
