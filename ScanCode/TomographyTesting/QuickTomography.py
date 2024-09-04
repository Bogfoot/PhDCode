# Quick tomography, 9 measurements
import datetime
from time import localtime, sleep, strftime

try:
    import QuTAG_MC as qt
except Exception as e:
    print("Can't find QuTAG_MC.")
    exit(1)

channels = [1, 2, 3, 4]
coincidences = {"1/4": 36, "1/3": 34, "2/4": 37, "2/3": 35}
angles = [0, 22.5, 45]
exposure_time_timetagger = 1

# Initialize QuTAG device
tt = qt.QuTAG()
tt.setExposureTime(exposure_time_timetagger * 1000)
_, coincWin, expTime = tt.getDeviceParams()
print(f"Coincidence window: {coincWin}\nBins, exposure time: {expTime} ms")


data_for_tomography = f"Data/DataForTomography_{datetime.date.today()}_{strftime('%H_%M_%S', localtime())}.csv"
f = open(data_for_tomography, "w")
f.write("# angle,other_angle,1,2,3,4,1/4,1/3,2/4,2/3\n")
f.close()

for angle in angles:
    print(f"Now doing left side @ {angle}.")
    for other_angle in angles:
        print(f"Now doing right side @ {other_angle}.")
        print(angle, other_angle)
        sleep(exposure_time_timetagger)
        data, updates = tt.getCoincCounters()
        logdata = []
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
        answer = input("Continue the scan or stop [y/n]: ")
        if answer == "n":
            tt.deInitialize()
            exit()
tt.deInitialize()
