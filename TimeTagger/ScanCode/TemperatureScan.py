import datetime
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import QuTAG_MC as qt
from OC import OC
from scipy.optimize import curve_fit

# single photon detectors:
maxclickrate = 500e3  # Hz, single photon detect, so we dont fry them

# temperature scan:
temperature_start = 37.5
temperature_end = 38.8
temperature_step = 0.01  # Was 0.1 initially, maybe it will not be as stable

sleepy_sleepy_oven = 37  # s
exposure_time_timetagger = 39  # s max allowed by the time tagger
sleepy_sleepy_timetagger = exposure_time_timetagger + 15  # s


n = (
    int((temperature_end - temperature_start) / temperature_step) + 1
)  # +1 because of the initial temperature
temperature = np.linspace(temperature_start, temperature_end, n)

# do you want to see the current status of the measurement?
print(f"Temperature scan will be performed from {temperature_start}-{temperature_end}.")
print("The scan will make ", n, " steps.")
print(
    "If everything goes according to plan, the scan will take approx. ",
    (sleepy_sleepy_timetagger * n + (2 * n * sleepy_sleepy_oven)) // (60 * 60),
    " h",
)

# data files

data_file_name = (
    "Data/"
    + str(datetime.date.today())
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

tt.enableChannels(channels)
time.sleep(10)

f = open(data_file_name, "w")
f.write("# Temperature   Clicks_1   Clicks_2   Correlations\n")
f.write("# 28.01.2024 1560 SPDC measurement \n")
f.write(f"# Temperature scan between {temperature_start} and {temperature_start} °C\n")
f.write(
    "# This measurement DOES NOT include the coincidence stage where we separate single photons based on polarization per channel.\n"
)
f.write("# TEST MEASUREMENT")
f.write("# --------------------------------- \n")
f.write("# Input laser power: 90 mW  at 780 nm (262 mA) \n")
f.write("# Power at input: 65 mW  at 780 nm (262 mA) \n")
f.write("# Pump polarization: 'H' (21R) = 82.1 mW)")
f.write("# Periodic polling: 9.12 um\n")
f.write("# Initial setup alignment at 41.0 C\n")
f.write(f"# Integration time:  {sleepy_sleepy_timetagger} s \n")
f.write("# Single photon detector QE: 10% \n")
f.write("# Single photon detector dead time: 5 us \n")
delays = [tt.getChannelDelay(channel) for channel in channels]
f.write(f"# Time-delay of {delays} ns\n")
f.write("# ---------------------------------- \n")
f.write("# Temperature    Clicks_1    Clicks_2    Correlations \n")
f.write("# [C]    [/]    [/]    [/] \n")
f.close()


########################## oven

usb_port = "/dev/ttyUSB0"  # This is for use on linux, you can also use /dev/bus/usb/... maybe depending on your setup
oven = OC(usb_port)  # OC3 Code from them

oven.enable()
oven.set_temperature(round(temperature[0], 2))

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


##################################################
# Define the Gaussian function
def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-(((x - mean) / stddev) ** 2) / 2)


# Initial guess for the parameters
initial_guess = [1, np.mean(dt["Temperature"]), np.std(dt["Temperature"])]


# Fit the data to the Gaussian function
params, covariance = curve_fit(
    gaussian, dt["Temperature"], dt["Coincidances"] * 100, p0=initial_guess
)

# Extract the fitted parameters
amplitude, mean, stddev = params

# Plot the original data and the fitted Gaussian curve
# # Read the data from the file, skipping rows starting with #
column_names = ["Temperature", "ClicksH", "ClicksV", "Coincidances"]

dt = pd.read_csv(
    data_file_name,
    delim_whitespace=True,
    comment="#",
    names=column_names,
    encoding="latin-1",
)
plt.plot(
    dt["Temperature"],
    gaussian(dt["Temperature"], amplitude, mean, stddev),
    color="red",
    label="Gaussian Fit of Correlations",
)

# Print the parameters of the fitted Gaussian curve
print(f"Amplitude: {amplitude}")
print(f"Mean: {mean}")
print(f"Standard Deviation: {stddev}")
##################################################

oven.OC_close()
