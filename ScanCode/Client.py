import datetime
import socket
import time

import numpy as np
from OC import OC

# temperature scan:
temperature_start = 35
temperature_end = 45
temperature_step = 0.1  # Was 0.1 initially, maybe it will not be as stable

data_file_name = (
    "Data/"
    + str(datetime.date.today())
    + "_SPDC_1560_phase_matching_fine_tsweep_"
    + str(temperature_start)
    + "-"
    + str(temperature_end)
    + "degC.data"
)


def client():
    host = "141.255.216.191"  # The server's hostname or IP address
    port = 65432  # The port used by the server

    n = (
        int((temperature_end - temperature_start) / temperature_step) + 1
    )  # +1 because of the initial temperature

    temperatures = np.linspace(temperature_start, temperature_end, n)
    usb_port = "/dev/ttyUSB0"
    oven = OC(usb_port)
    sleepy_sleepy_oven = 10

    file = open(data_file_name, "w")
    file.write("# Temperature ClicksH ClicksV Coincidances\n")
    file.close()

    for temp in temperatures:
        oven.set_temperature(temp)

        stability_oven = False

        oven.set_temperature(round(temp, 2))
        print("current set T: = ", round(temp, 2), " C")
        while stability_oven == False:
            time.sleep(sleepy_sleepy_oven)
            print("current T = ", oven.get_temperature(), " C")
            if abs(oven.get_temperature() - temp) < 0.015:
                stability_oven = True
                print("Temperature stable, starting a measurement.")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(b"GATHER DATA")
            data = s.recv(1024).decode("utf-8")
            print(f"Temperature: {temp}, Received: {data}")

            # Check if the received data is an error message or a close oven message
            if "Error" in data:
                print(f"Error received from server: {data}")
                file.write(f"{temp} Error: {data}\n")
                s.sendall(b"CLOSE OVEN")
                break

            # Parse the received data
            parts = data.split(", ")
            clicksH = parts[0].split(": ")[1]
            clicksV = parts[1].split(": ")[1]
            coincidences = parts[2].split(": ")[1]

            # Write data to file
            file = open(data_file_name, "a")
            file.write(f"{temp},{clicksH},{clicksV},{coincidences}\n")
            file.close()

    oven.OC_close()


if __name__ == "__main__":
    client()
