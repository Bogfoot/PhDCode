import datetime
import sys
from time import perf_counter, sleep, strftime, localtime

# QuTAG import and initialization
try:
    import QuTAG_MC as qt
except Exception as e:
    print("Can't find QuTAG_MC.")
    exit(1)

# Initialize QuTAG device
tt = qt.QuTAG()


# Function to convert human-readable time formats to seconds
def parse_time(duration: str) -> int:
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    unit = duration[-1].lower()
    if unit not in units:
        raise ValueError("Invalid time format. Use 's', 'm', 'h', or 'd'.")
    time_value = int(duration[:-1])
    return time_value * units[unit]


# Function for long measurement
def perform_measurement(total_duration: str):
    exposure_time = 1  # Integration time per measurement in seconds
    total_seconds = parse_time(total_duration)  # Total time in seconds
    start_time = perf_counter()

    # Set the exposure time in the device
    tt.setExposureTime(int(exposure_time * 1000))
    _, coincWin, expTime = tt.getDeviceParams()
    print(f"Coincidence window: {coincWin} Bins, exposure time: {expTime} ms")

    # Initialize data structures
    channels = [1, 2, 3, 4]
    coincidences = {"1/4": 36, "1/3": 34, "2/4": 37, "2/3": 35}

    # File to store results
    data_file = f"Data/DataForMeasurement_{datetime.date.today()}_{strftime('%H_%M_%S', localtime())}.csv"
    with open(data_file, "w") as f:
        f.write("# Time,S1,S2,S3,S4,1/4,1/3,2/4,2/3\n")

    while perf_counter() - start_time < total_seconds:
        sleep(exposure_time)  # Wait for exposure time

        # Get data from the QuTAG device
        data, updates = tt.getCoincCounters()

        # Get current time in yyyy_mm_dd_HH_ss format
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        logdata = [timestamp]

        if updates == 0:
            print("Waiting for data...")
        else:
            # Gather singles
            for ch in channels:
                logdata.append(data[ch])
            # Gather coincidences
            for coinc in coincidences:
                coinc_idx = coincidences[coinc]
                logdata.append(data[coinc_idx])

        # Convert log data to a comma-separated string
        logdata_str = ",".join(map(str, logdata))
        print(logdata_str)

        # Write data to file
        with open(data_file, "a") as f:
            f.write(logdata_str + "\n")

    print("Measurement complete!")

time_duration = sys.argv[1]

# Example of calling the function for a 1-hour measurement
perform_measurement(time_duration)
