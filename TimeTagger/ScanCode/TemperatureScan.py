# %% Testing multiple TTs
tt = qt.QuTAG()

NoD = tt.discover()
print(f"Number of devices found: {NoD}")

if NoD > 1:
    # Connects to all devices
    for i in range(numberOfDevices):
        print("Connecting to device " + str(i))
        qutag.connect(i)


tt.deInitialize()

# %% scan temperature while recording the clicks ---------- 1560 source ------- !!1!1!1!1!1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! USE THIS


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

tt.deInitialize()

covesion_set_temperature(oven, 37.9)
