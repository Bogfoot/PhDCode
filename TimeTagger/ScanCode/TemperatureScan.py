# TODO: Change OvenLib to be a class that can be easily used
# %% scan temperature while recording the clicks ---------- 1560 source ------- !!1!1!1!1!1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! USE THIS
import datetime
import time

import numpy as np
import QuTAG_MC as qt
from OC import OC

# oven:

# single photon detectors:
maxclickrate = 500e3  # Hz, single photon detect, so we dont fry them

# temperature scan:
temperature_start = 35
temperature_end = 45
temperature_step = 0.1  # Was 0.1 initially, maybe it will not be as stable

sleepy_sleepy_oven = 10  # s
exposure_time_timetagger = 1  # s max allowed by the time tagger
sleepy_sleepy_timetagger = exposure_time_timetagger + 15  # s


n = (
    int((temperature_end - temperature_start) / temperature_step) + 1
)  # +1 because of the initial temperature
temperature = np.linspace(temperature_start, temperature_end, n)

# do you want to see the current status of the measurement?

print("Temperature scan will be performed.")
print("The scan will make ", n, " steps.")
print(
    "If everything goes according to plan, the scan will take approx. ",
    (sleepy_sleepy_timetagger * n + (2 * n * sleepy_sleepy_oven)) // (60 * 60),
    " h",
)

# data files

data_file_name = (
    str(datetime.date.today())
    + "_SPDC_1560_phase_matching_fine_tsweep_"
    + str(temperature_start)
    + "-"
    + str(temperature_end)
    + "degC.data"
)

print("Do you wish to proceed with the scan or do you want to exit now?")
confirmation = input("Enter 'y' to continue, or 'n' to quit: ")
if confirmation.lower() == "y":
    pass
else:
    exit()


current_time = time.strftime("%H:%M:%S", time.localtime())
print("Waking up! Please make me coffee!")
print(f"Starting the finer measurement at {current_time}!")

# Initialize the quTAG device
tt = qt.QuTAG()
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")
tt.setExposureTime(exposure_time_timetagger * 1000)  # ms Counting

channel_1 = 1
channel_2 = 2
channels = [channel_1, channel_2]
coincidances_12 = 33

tt.enableChannels((channel_1, channel_2))
time.sleep(sleepy_sleepy_timetagger)

f = open(data_file_name, "w")
f.write("Temperature   Clicks_1   Clicks_2   Correlations")
f.write("# 28.01.2024 1560 SPDC measurement \n")
f.write(f"# Temperature scan between {temperature_start} and {temperature_start} °C \n")
f.write(
    "# This measurement DOES NOT include the coincidence stage where we separate single photons based on polarization per channel. \n"
)
f.write("# TEST MEASUREMENT")
f.write("# --------------------------------- \n")
f.write("# Input laser power: 90 mW  at 780 nm (262 mA) \n")
f.write("# Power at input: 90 mW  at 780 nm (262 mA) \n")
f.write("# Pump polarization: 'D' (Ch1, C21R)(uW)  = 82.1 mW)")
f.write("# Periodic polling: 9.12 um")
f.write("# Initial setup alignment at 22.0 C")
f.write("# Integration time: 60 s \n")
f.write("# Single photon detector darkcounts: 0.3 and 0.27 kHz \n")
f.write("# Single photon detector QE: 10% \n")
f.write("# Single photon detector dead time: 20 us \n")
delays = [tt.getChannelDelay(channel) for channel in channels]
f.write(f"# Time-delay of {delays} ns")
f.write("# ---------------------------------- \n")
f.write("# Temperature    Clicks_1    Clicks_2    Correlations \n")
f.write("# [C]    [/]    [/]    [/] \n")
f.close()


########################## oven

usb_port = "/dev/ttyUSB0"  # This is for use on linux, you can also use /dev/bus/usb/... maybe depending on your setup
oven = OC(usb_port)  # OC3 Code from them

oven.enable()
oven.set_temperature(round(temperature[0], 2))
print("Sleep for 10 seconds to see a different temperature")
time.sleep(10)
print(oven.get_temperature())

# timetagger:

########################## temperature scan
coincidances = []
for i in range(n):
    print("status: ", i, "/", int(n))
    stability_oven = False

    oven.set_temperature(round(temperature[i], 2))
    print("current set T: = ", round(temperature[i], 2), " C")
    while stability_oven == False:
        time.sleep(sleepy_sleepy_oven)
        print("current T = ", oven.get_temperature(), " C")
        if abs(oven.get_temperature() - temperature[i]) < 0.015:
            stability_oven = True
            print("Temperature stable, starting a measurement.")

    time.sleep(sleepy_sleepy_timetagger)
    data, _ = tt.getCoincCounters()
    f = open(data_file_name, "a")
    f.write(
        str(round(temperature[i], 2))
        + "    "
        + str(data[channel_1])
        + "    "
        + str(data[channel_2])
        + "    "
        + str(data[coincidances_12])
        + "\n"
    )
    f.close()
    coincidances.append(data[coincidances_12])
    if (data[1] / exposure_time_timetagger) > maxclickrate:
        oven.set_temperature(24)
        break
    if (data[2] / exposure_time_timetagger) > maxclickrate:
        oven.set_temperature(24)
        break
    # check that the clicks are OK / that you are not rosting the single photon detectors

tt.deInitialize()
max_coinc_index = coincidances.index(np.max(coincidances))

print(
    f"Setting temperature to highest coincidence temperature: {temperature[max_coinc_index]}."
)
oven.set_temperature(temperature[max_coinc_index])
oven.OC_close()
