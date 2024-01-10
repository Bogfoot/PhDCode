"""
Created on 2023-02-20

This file will run a temperature scan of a SPDC crystal. We vary the temperature of the crystal with a Covesion temperature
controler. The produced single photons are detected on Aurea SPDs, which sned TTL signals to a quTag timetagger. This script
interacts with these two maschines.

For timetagger, software/python wrapper was provided, so I am just referencing that.

For oven, we got a weird list of raw byte commands one sends over USB. hopefully the method is clear, but I tryed to
automize most of it. But it took some time to descipher what the techsupport said.

this file needs to be in the same folder as "QuTAGWindows.py" and the DLL_64 folder

you need to connect the
---------
connecting to oven uses "pyserial" pacakge.

@author: Žiga Pušavec
"""

import math
import os
# from scipy.optimize import curve_fit
import socket
import time
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import scipy
import serial.serialwin32
import serial.tools.list_ports as port_list

##################### setting correct working directory:


directorypath = "/home/bogfootlj/Documents/PhDCode/TimeTagger/TTCode/2023-09-15_1560nmtemperaturescan/"
# os.chdir(directorypath)
os.chdir(directorypath)  # change
###########################
# current relevant packages:

try:
    import QuTAGWindows as qt
except:
    print("Time Tagger wrapper QuTAG.py is not in the search path.")


######################################################## covesion, define functions
def covesion_enable_oven(
    oven,
    port="COM7",
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
):
    oven.port = port
    oven.baudrate = baudrate
    oven.parity = parity
    oven.stopbits = stopbits
    oven.bytesize = bytesize
    oven.timeout = 1

    oven.open()
    # define the right message string to eneable heating the oven
    send_message = "\x01j00CB"
    oven.write(send_message.encode())
    oven.close()

    return


def string_bit_converter(input_list):
    output_string = [""]
    j = 0
    for i in range(4, len(input_list)):
        if input_list[i] == ";":
            output_string.append("")
            j = j + 1
        elif input_list[i] != "\x01":
            output_string[j] = output_string[j] + input_list[i]
    return output_string


def covesion_check_temperature(oven):
    oven.open()
    # print("is the serial port open? ",oven.is_open)
    # print()

    # print("read line from controler over USB:")

    # define the right message string
    oven.flushOutput()
    send_message = "\x01j00CB"
    oven.write(send_message.encode())
    oven_output = oven.readline()
    # print(oven_output)
    oven_output_convert = list(oven_output)

    # this last if is there because sometimes the string we get back is not in the right format
    # who knows why. if this happens, i just reset the whole check
    if oven_output_convert[0] == 1:

        oven_output_ascii = list()
        for i in range(len(oven_output_convert)):
            oven_output_ascii.append(chr(oven_output_convert[i]))
        # print()
        oven.close()
        # print("is the serial port closed? ",oven.is_open * False == 0)

        return float(string_bit_converter(oven_output_ascii)[1])

    else:
        oven.close()
        return covesion_check_temperature(oven)


def command_packet_constructor(T):

    start = "\x01"
    command = "i"

    data = "1;" + str(T) + ";100;0;100;1;0;"

    data_lenght = str(len(data))
    check_sum = hex(sum(list((start + command + data_lenght + data).encode())))[3:]

    command_packet = start + command + data_lenght + data + check_sum
    return command_packet


def covesion_set_temperature(oven, T):
    oven.open()
    # print("is the serial port open? ",oven.is_open)
    # print()

    # define the right message string
    send_message = command_packet_constructor(T)
    # send_message = "\x01j00CB"
    oven.write(send_message.encode())
    oven.close()
    # print("is the serial port closed? ",oven.is_open * False == 0)

    return


def scan_plot_current_iteration(x, y):
    plt.close()
    plt.plot(x, y)
    plt.show()


#%%  test connecting to time tagger
channel_1 = 1
channel_2 = 2


# Initialize the quTAG device
tt = qt.QuTAG()

# Get the timebase (the resolution) from the quTAG. It is used as time unit by many other functions.
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")


# Set the exposure or integration time in milliseconds, range = 0..65535
tt.setExposureTime(1 * 1000)  # ms Counting

tt.enableChannels((1, 2))  # Enables channel 0,2,3

time.sleep(1)

data, updates = tt.getCoincCounters()

# wait a little to get the device started calibrating
time.sleep(2)

data, updates = tt.getCoincCounters()
print("Updates since last call: ", updates, "| Data: ", data)
print("channel: ", channel_1, ", counts: ", data[channel_1])
print("channel: ", channel_2, ", counts: ", data[channel_2])
print("channel: coincidences, counts: ", data[5])

print(tt.discover())

tt.deInitialize()

#%% Testing multiple TTs
tt = qt.QuTAG()

NoD = tt.discover()
print(f"Number of devices found: {NoD}")

if NoD > 1:
    # Connects to all devices
    for i in range(numberOfDevices):
        print("Connecting to device " + str(i))
        qutag.connect(i)


tt.deInitialize()

#%% find the right serial port for the oven


ports = list(port_list.comports())
for p in ports:
    print(p)

#%%  test connect to oven
import io  # needed for reading lines

oven = serial.serialwin32.Serial()

oven.baudrate = 19200
oven.port = usb_port
oven.parity = serial.PARITY_NONE
oven.stopbits = serial.STOPBITS_ONE
oven.bytesize = serial.EIGHTBITS
oven.timeout = 1

oven.open()
print("is the serial port open? ", oven.is_open)
print()

# oven.flushOutput()
# send_message = "(0x01)j00CB"
send_message = "\x01j00CB"
# send_message = "\x01i191;60;100;0;100;1;0;BB"
oven.write(send_message.encode())

print("read line from controler over USB:")
oven_output = oven.read(68)
oven_output_convert = list(oven_output)
a = list()
for i in range(len(oven_output_convert)):
    a.append(chr(oven_output_convert[i]))

print(a)
# print(oven.read(20))

print()
oven.close()
print("is the serial port closed? ", oven.is_open * False == 0)

#%% read oven temperature --- WORKS

oven = serial.serialwin32.Serial()
usb_port = "COM7"

covesion_enable_oven(oven, port=usb_port)

print("current T = ", covesion_check_temperature(oven), " C")

#%% scan temperature while recording the clicks

# timetagger:
channel_1 = 1
# oven:
# single photon detectors:
maxclickrate = 100e3  # Hz, single photon detect, so we dont fry them

# temperature scan:
temperature_start = 30
temperature_end = 50
temperature_step = 0.01

sleepy_sleepy_oven = 10  # s
exposure_time_timetagger = 60  # s max allow ed by the time tagger
sleepy_sleepy_timetagger = exposure_time_timetagger + 10  # s

# output arrays
n = int((temperature_end - temperature_start) / temperature_step)
temperature = np.linspace(temperature_start, temperature_end, n)
coincidences_measurment = np.zeros(n)

# do you want to see the current status of the measurment?
plot_current_iteration = False  # not working for some reason

print("Temperature scan will be performed.")
print("The scan will make ", n, " steps.")
print(
    "If everything goes according to plan, the scan will take approx. ",
    (sleepy_sleepy_timetagger * n + (2 * n * sleepy_sleepy_oven)) // (60 * 60),
    " h",
)
#
# Initialize the quTAG device
tt = qt.QuTAG()
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")
tt.setExposureTime(exposure_time_timetagger * 1000)  # ms Counting
tt.enableChannels((0, 1, 2, 3, 4))
time.sleep(10)

########################## oven
oven = serial.serialwin32.Serial()

covesion_enable_oven(oven, port=usb_port)

########################## temperature scan
for i in range(n):
    print("status: ", i, "/", int(n))
    stability_oven = False

    covesion_set_temperature(oven, round(temperature[i], 2))
    print("current set T: = ", round(temperature[i], 2), " C")
    while stability_oven == False:
        time.sleep(sleepy_sleepy_oven)
        print("current T = ", covesion_check_temperature(oven), " C")
        if abs(covesion_check_temperature(oven) - temperature[i]) < 0.015:
            stability_oven = True

    time.sleep(sleepy_sleepy_timetagger)
    data, updates = tt.getCoincCounters()
    #    coincidences_measurment[i] = tt.getCoincCounters()[0][channel1]
    coincidences_measurment[i] = data[channel_1]

    if (coincidences_measurment[i] / exposure_time_timetagger) > maxclickrate:
        covesion_set_temperature(oven, 22)
        break
    # check that the clicks are OK / that you are not rosting the single photon detectors

    if plot_current_iteration == True:
        scan_plot_current_iteration(temperature, coincidences_measurment)

tt.deInitialize()

np.save(file_name_8, np.array([temperature, coincidences_measurment]))

#%%
data1 = np.load(file_name_7)
data2 = np.load(file_name_8)

plt.close()

plt.plot(data1[0], data1[1])
plt.plot(data2[0], data2[1])
# plt.plot(temperature,coincidences_measurment)

plt.show()
import matplotlib.pyplot as plt
#%%
import numpy as np

data = np.loadtxt("C:\\Users\\Admin\\Coincidences_44.txt", skiprows=5, delimiter=";").T

# print(data.shape)
plt.plot(data[1])
# plt.xlim(0, 25000)
# plt.show()
#%% Correlation measurments---------------------------------------------

oven = serial.serialwin32.Serial()

covesion_enable_oven(oven, port=usb_port)


print("current T = ", covesion_check_temperature(oven), " C")

#%% scan temperature while recording the clicks ---------- 1560 source ------- !!1!1!1!1!1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! USE THIS


# timetagger:
channel_1 = 1
channel_2 = 2

# oven:

# single photon detectors:
maxclickrate = 100e3  # Hz, single photon detect, so we dont fry them

# temperature scan:
temperature_start = 35
temperature_end = 39
temperature_step = 0.2  # Was 0.1 initially, maybe it will not be as stable

sleepy_sleepy_oven = 10  # s
exposure_time_timetagger = 1  # s max allowed by the time tagger
sleepy_sleepy_timetagger = exposure_time_timetagger + 15  # s

# output arrays<*+

n = (
    int((temperature_end - temperature_start) / temperature_step) + 1
)  # +1 because of the initial temperature
temperature = np.linspace(temperature_start, temperature_end, n)

# do you want to see the current status of the measurement?
plot_current_iteration = False  # not working for some reason

print("Temperature scan will be performed.")
print("The scan will make ", n, " steps.")
print(
    "If everything goes according to plan, the scan will take approx. ",
    (sleepy_sleepy_timetagger * n + (2 * n * sleepy_sleepy_oven)) // (60 * 60),
    " h",
)

# data files

data_file_name = (
    str(date.today())
    + "_SPDC_1560_phase_matching_fine_tsweep_"
    + str(temperature_start)
    + "-"
    + str(temperature_end)
    + "degC.txt"
)
file_name = data_file_name

#%% Actually runs the measurement - for the 1560 source
#
#
#
# Wait for X hours before  starting the measurement
# sleeptime = 6 #h
# seconds = 3600 #s
# print(f"Sleeping for {sleeptime} hours!")
# time.sleep(sleeptime*seconds)


t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print("Waking up! Please make me coffee!")
print(f"Starting the finer measurement at {current_time}!")

# Initialize the quTAG device
tt = qt.QuTAG()
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")
tt.setExposureTime(exposure_time_timetagger * 1000)  # ms Counting
tt.enableChannels((0, 1, 2, 3, 4))
time.sleep(sleepy_sleepy_timetagger)
data, updates = tt.getCoincCounters()


f = open(file_name, "w")
f.write("# 2023-10-10 1560 SPDC measurment \n")
# f.write("# Both crystals are (again) oriented in the same direction\n")
f.write("# Temperature scan betwen 36 and 38.5 °C \n")
f.write("# Swapped the oven to one from IJS \n")
f.write(
    "# This measurement DOES NOT inculde the coincidence stage where we seperate single photons based on polarization per channel. \n"
)
f.write("# A narrowband filter is implemented in C21 (1560.61 nm) bandwidth of 100 GHz")
f.write("# Each single-photon detector is connected to the coincidence stage")
f.write(
    "# A SPD is connected to one branch of the coincidence stage, while the other SPD is connected directly to the V photon branch on the temp scan\n"
)
f.write("# TEST MEASUREMENT")
f.write("# --------------------------------- \n")
f.write("# input laser power: 83 mW  at 780 nm (262 mA) \n")
f.write("# pump polarization: 'H' (Ch1, C21R)(uW)  = 82.1 mW)")
f.write("# periodic polling: 9.12 um")
f.write("# initial setup alignment at 22.0 C")
f.write("# integration time: 60 s \n")
f.write("# single photon detector darkcounts: 0.3 and 0.27 kHz \n")
f.write("# single photon detector QE: 10% \n")
f.write("# single photon detector dead time: 20 us \n")
f.write("# Time-delay of 86.2 ns")
f.write("# ---------------------------------- \n")
f.write("# Temperature    Clicks_1    Clicks_2    Correlations \n")
f.write("# [C]    [/]    [/]    [/] \n")
f.close()

########################## oven
oven = serial.serialwin32.Serial()
# usb_port = "COM5"

covesion_enable_oven(oven, port=usb_port)
covesion_set_temperature(oven, round(temperature[0], 2))

########################## temperature scan
for i in range(n):
    print("status: ", i, "/", int(n))
    stability_oven = False

    covesion_set_temperature(oven, round(temperature[i], 2))
    print("current set T: = ", round(temperature[i], 2), " C")
    while stability_oven == False:
        time.sleep(sleepy_sleepy_oven)
        print("current T = ", covesion_check_temperature(oven), " C")
        if abs(covesion_check_temperature(oven) - temperature[i]) < 0.015:
            stability_oven = True
            print("Temperature stable, starting a measurement.")

    time.sleep(sleepy_sleepy_timetagger)
    data, updates = tt.getCoincCounters()
    f = open(file_name, "a")
    f.write(
        str(round(temperature[i], 2))
        + "    "
        + str(data[1])
        + "    "
        + str(data[2])
        + "    "
        + str(data[5])
        + "\n"
    )
    f.close()

    if (data[1] / exposure_time_timetagger) > maxclickrate:
        covesion_set_temperature(oven, 24)
        break
    if (data[2] / exposure_time_timetagger) > maxclickrate:
        covesion_set_temperature(oven, 24)
        break
    # check that the clicks are OK / that you are not rosting the single photon detectors

    # if plot_current_iteration == True:
    #     scan_plot_current_iteration(temperature,coincidences_measurment)

tt.deInitialize()

covesion_set_temperature(oven, 37.9)


#%%

file_name = data_file_name


data1 = np.loadtxt(file_name, comments="#", delimiter="    ").transpose()

plt.close()
# plt.plot(data1[0], data1[1])
# plt.plot(data1[0], data1[2])
plt.plot(data1[0], data1[1] / 10000, label="H polarization [xe4]")
plt.plot(data1[0], data1[2] / 10000, label="V polarization [xe4]")
plt.plot(data1[0], (data1[1] + data1[2]) / 10000, label="H + V polarization [xe4]")
plt.plot(data1[0], data1[3] / 100, label="coincidences [x100]")

plt.show()

plt.xlabel("Temperature [C]")
plt.ylabel("Counts []")
plt.title(
    "Phase matching measurment, pump polarization: H, 1560 nm, coinc_window = 1 ns, T_int = 60 s, alligned at 37,39 °C"
)
plt.legend()
# plt.plot(data2[0],data2[1])
# plt.plot(temperature,coincidences_measurment)

plt.show()
# Save figure if
plot_filename = (
    str(os.getcwd()) + "\\Pictures\\" + "tempscan-SPDC-" + str(date.today()) + ".png"
)
if os.path.isfile(plot_filename) == False:
    plt.savefig(plot_filename)
else:
    print("File already exists, please change the name.")

#%%
file_name_1 = file_name_48
file_name_2 = file_name_49


data1 = np.loadtxt(file_name_1, comments="#", delimiter="    ").transpose()
data2 = np.loadtxt(file_name_2, comments="#", delimiter="    ").transpose()

plt.close()
# plt.plot(data1[0], data1[1])
# plt.plot(data1[0], data1[2])
plt.plot(
    data1[0], (data1[1] + data1[2]) / 10000, label="H pump, H + V polarization [xe4]"
)
plt.plot(
    data1[0], (data2[1] + data2[2]) / 10000, label="V pump, H + V polarization [xe4]"
)
plt.plot(data1[0], data1[3] / 100, label="H pump, coincidences [x100]")
plt.plot(data2[0], data2[3] / 100, label="V, pump coincidences [x100]")

plt.show()

plt.xlabel("Temperature [C]")
plt.ylabel("Counts []")
plt.title("Phase matching measurment, 1550 nm, coinc_window = 10 ns, T_int = 60 s")
plt.legend()
# plt.plot(data2[0],data2[1])
# plt.plot(temperature,coincidences_measurment)

plt.show()

#%%
file_name = file_name_37


data1 = np.loadtxt(file_name, comments="#", delimiter="    ").transpose()

plt.close()
# plt.plot(data1[0], data1[1])
# plt.plot(data1[0], data1[2])
plt.plot(data1[0], data1[3], label="coincidences")


plt.show()

plt.xlabel("Temperature [C]")
plt.ylabel("Coincidences []")
plt.title(
    "Phase matching measurment, 1550 nm,coinc_window = 1 ns ,T_int = 60 s, alligned at 22 C"
)
plt.legend()
# plt.plot(data2[0],data2[1])
# plt.plot(temperature,coincidences_measurment)

plt.show()

#%%

file_name1 = file_name_31
file_name2 = file_name_38


data1 = np.loadtxt(file_name1, comments="#", delimiter="    ").transpose()
data2 = np.loadtxt(file_name2, comments="#", delimiter="    ").transpose()

plt.close()
plt.plot(data1[0], data1[2] / 10000, label="SFG, first crystal [xe4]")
plt.plot(data2[0], (data2[1]) / 100000, label="SFG, second crystal [xe5]")
plt.plot(data2[0], data2[3] / 100, label="coincidences [x100]")
# plt.plot(data2[0], (data2[1] + data2[2])/100000, label = "crystal 1 + crystal 2")

plt.xlabel("Temperature [C]")
plt.ylabel("Counts per channel []")
plt.title(
    "Coincidence measurment, T_int = 60 s, coinc_window = 10 ns, alligned at 22 C"
)
# plt.plot(data2[0],data2[1])
# plt.plot(temperature,coincidences_measurment)
plt.legend()
plt.show()


#%% scan temperature while recording the clicks ---------- 1310 source -------

file_name = file_name_43

# timetagger:
channel_1 = 1
channel_2 = 2

# oven:

# single photon detectors:
maxclickrate = 500e3  # Hz, single photon detect, so we dont fry them

# temperature scan:
temperature_start = 30
temperature_end = 100
temperature_step = 0.1

sleepy_sleepy_oven = 10  # s
exposure_time_timetagger = 60  # s max allow ed by the time tagger
sleepy_sleepy_timetagger = exposure_time_timetagger + 10  # s

# output arrays
n = (
    int((temperature_end - temperature_start) / temperature_step) + 1
)  # +1 because of the inital temperature
temperature = np.linspace(temperature_start, temperature_end, n)

# do you want to see the current status of the measurment?
plot_current_iteration = False  # not working for some reason

print("Temperature scan will be performed.")
print("The scan will make ", n, " steps.")
print(
    "If everything goes according to plan, the scan will take approx. ",
    (sleepy_sleepy_timetagger * n + (2 * n * sleepy_sleepy_oven)) // (60 * 60),
    " h",
)
#
# Initialize the quTAG device
tt = qt.QuTAG()
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")
tt.setExposureTime(exposure_time_timetagger * 1000)  # ms Counting
tt.enableChannels((0, 1, 2, 3, 4))
time.sleep(sleepy_sleepy_timetagger)
data, updates = tt.getCoincCounters()


f = open(file_name, "w")
f.write("# 2023-05-17 1310 SFG measurment\n")
f.write(
    "# full measurement of the phasematching condition, now for controler 2 and oven 2 \n"
)
f.write("# temperature scan betwen 30 and 90 C \n")
f.write("# now for a different pooling \n")
f.write("# --------------------------------- \n")
f.write("# input laser power: __ mW at 1310 nm (70 mA) \n")
f.write("# pump polarization: H + V ")
f.write(
    "# periodic pooling: 6.57 um (same as the first measurement for the first controler"
)
f.write("# initial setup alignment at 23.0 C")
f.write("# integration time: 60 s \n")
f.write("# single photon detector darkcounts: 150 Hz \n")
f.write("# single photon detector QE: __% \n")
f.write("# single photon detector dead time: __ us \n")
f.write("# ---------------------------------- \n")
f.write("# Temperature    Clicks_1    Clicks_2    Correlations \n")
f.write("# [C]    [/]    [/]    [/] \n")
f.close()

########################## oven
oven = serial.serialwin32.Serial()
# usb_port = "COM5"

covesion_enable_oven(oven, port=usb_port)
covesion_set_temperature(oven, round(temperature[0], 2))

########################## temperature scan
for i in range(n):
    print("status: ", i, "/", int(n))
    stability_oven = False

    covesion_set_temperature(oven, round(temperature[i], 2))
    print("current set T: = ", round(temperature[i], 2), " C")
    while stability_oven == False:
        time.sleep(sleepy_sleepy_oven)
        print("current T = ", covesion_check_temperature(oven), " C")
        if abs(covesion_check_temperature(oven) - temperature[i]) < 0.015:
            stability_oven = True

    time.sleep(sleepy_sleepy_timetagger)
    data, updates = tt.getCoincCounters()
    f = open(file_name, "a")
    f.write(
        str(round(temperature[i], 2))
        + "    "
        + str(data[1])
        + "    "
        + str(data[2])
        + "    "
        + str(data[5])
        + "\n"
    )
    f.close()

    if (data[1] / exposure_time_timetagger) > maxclickrate:
        covesion_set_temperature(oven, 22)
        break
    if (data[2] / exposure_time_timetagger) > maxclickrate:
        covesion_set_temperature(oven, 22)
        break
    # check that the clicks are OK / that you are not rosting the single photon detectors

    # if plot_current_iteration == True:
    #     scan_plot_current_iteration(temperature,coincidences_measurment)

tt.deInitialize()

covesion_set_temperature(oven, 30)

#%%
file_name1 = file_name_24
file_name2 = file_name_44


data1 = np.loadtxt(file_name1, comments="#", delimiter="    ").transpose()
data2 = np.loadtxt(file_name2, comments="#", delimiter="    ").transpose()

plt.close()
plt.plot(data1[0], data1[1] / 100000, label="first temperature controler")
plt.plot(data2[0], data2[1] / 100000, label="second temperature cotnroler")
# plt.plot(data2[0], (data2[1] + data2[2])/100000, label = "crystal 1 + crystal 2")

plt.xlabel("Temperature [C]")
plt.ylabel("Counts per channel [100k]")
plt.title("1310_655 SFG measurment, T_int = 60 s, alligned at 22 C")
# plt.plot(data2[0],data2[1])
# plt.plot(temperature,coincidences_measurment)
plt.legend()
plt.show()

#%% scan temperature while recording the clicks ---------- 655 SHG source -------

file_name = file_name_43

# timetagger:
channel_1 = 1
channel_2 = 2

# oven:

# single photon detectors:
maxclickrate = 800e3  # Hz, single photon detect, so we dont fry them

# temperature scan:
temperature_start = 30
temperature_end = 100
temperature_step = 0.1

sleepy_sleepy_oven = 10  # s
exposure_time_timetagger = 60  # s max allow ed by the time tagger
sleepy_sleepy_timetagger = exposure_time_timetagger + 15  # s

# output arrays
n = (
    int((temperature_end - temperature_start) / temperature_step) + 1
)  # +1 because of the inital temperature
temperature = np.linspace(temperature_start, temperature_end, n)

# do you want to see the current status of the measurment?
plot_current_iteration = False  # not working for some reason

print("Temperature scan will be performed.")
print("The scan will make ", n, " steps.")
print(
    "If everything goes according to plan, the scan will take approx. ",
    (sleepy_sleepy_timetagger * n + (2 * n * sleepy_sleepy_oven)) // (60 * 60),
    " h",
)
#
# Initialize the quTAG device
tt = qt.QuTAG()
timebase = tt.getTimebase()
print("Device timebase:", timebase, "s")
tt.setExposureTime(exposure_time_timetagger * 1000)  # ms Counting
tt.enableChannels((0, 1, 2, 3, 4))
time.sleep(sleepy_sleepy_timetagger)
data, updates = tt.getCoincCounters()


f = open(file_name, "w")
f.write("# 2023-05-15 655 SHG measurment\n")
f.write("# doing the SHG scan again, this time to do it properly \n")
f.write("# temperature scan betwen 30 and 75 C \n")
f.write(
    "# this measurement now includes the coincidence stage where we seperate single photons based on polarization per channel \n"
)
f.write(
    "# i am now repeating this measurment to see if the measurment is reproducable or the controler introduces an offset \n"
)
f.write("# --------------------------------- \n")
f.write("# input laser power: ___ mW at 1310 nm (70 mA) \n")
f.write("# pump polarization: _")
f.write("# periodic pooling: _ um")
f.write("# initial setup alignment at 22.0 C")
f.write("# integration time: 60 s \n")
f.write("# single photon detector darkcounts: 500 Hz \n")
f.write("# single photon detector QE: _% \n")
f.write("# single photon detector dead time: __ us \n")
f.write("# ---------------------------------- \n")
f.write("# Temperature    Clicks_1    Clicks_2    Correlations \n")
f.write("# [C]    [/]    [/]    [/] \n")
f.close()

########################## oven
oven = serial.serialwin32.Serial()
# usb_port = "COM5"

covesion_enable_oven(oven, port=usb_port)
covesion_set_temperature(oven, round(temperature[0], 2))

########################## temperature scan
for i in range(n):
    print("status: ", i, "/", int(n))
    stability_oven = False

    covesion_set_temperature(oven, round(temperature[i], 2))
    print("current set T: = ", round(temperature[i], 2), " C")
    while stability_oven == False:
        time.sleep(sleepy_sleepy_oven)
        print("current T = ", covesion_check_temperature(oven), " C")
        if abs(covesion_check_temperature(oven) - temperature[i]) < 0.015:
            stability_oven = True

    time.sleep(sleepy_sleepy_timetagger)
    data, updates = tt.getCoincCounters()
    f = open(file_name, "a")
    f.write(
        str(round(temperature[i], 2))
        + "    "
        + str(data[1])
        + "    "
        + str(data[2])
        + "    "
        + str(data[5])
        + "\n"
    )
    f.close()

    if (data[1] / exposure_time_timetagger) > maxclickrate:
        covesion_set_temperature(oven, 22)
        break
    if (data[2] / exposure_time_timetagger) > maxclickrate:
        covesion_set_temperature(oven, 22)
        break
    # check that the clicks are OK / that you are not rosting the single photon detectors

    # if plot_current_iteration == True:
    #     scan_plot_current_iteration(temperature,coincidences_measurment)

tt.deInitialize()

covesion_set_temperature(oven, 30)

#%%
file_name1 = file_name_40
file_name2 = file_name_42


data1 = np.loadtxt(file_name1, comments="#", delimiter="    ").transpose()
data2 = np.loadtxt(file_name2, comments="#", delimiter="    ").transpose()

plt.close()
plt.plot(data1[0], data1[1] / 100000, label="yesterdays scan")
plt.plot(data2[0], data2[1] / 100000, label="todays scan")
# plt.plot(data2[0], (data2[1] + data2[2])/100000, label = "crystal 1 + crystal 2")

plt.xlabel("Temperature [C]")
plt.ylabel("Counts per channel [100k]")
plt.title("SHG temperature scan, T_int = 60 s")
# plt.plot(data2[0],data2[1])
# plt.plot(temperature,coincidences_measurment)
plt.legend()
plt.show()
