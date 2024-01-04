"""
Created on 2023-02-20

This file will run a temperature scan of a SPDC crystal. We vary the temperature of the crystal with a Covesion temperature
controller. The produced single photons are detected on Aurea SPDs, which sned TTL signals to a quTag timetagger. This script
interacts with these two maschines.

For timetagger, software/python wrapper was provided, so I am just referencing that.

For oven, we got a weird list of raw byte commands one sends over USB. hopefully the method is clear, but I tried to
automize most of it. But it took some time to descipher what the techsupport said.

this file needs to be in the same folder as "QuTAGWindows.py" and the DLL_64 folder

you need to connect the
---------
connecting to oven uses "pyserial" package.

@author: Žiga Pušavec
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import serial.serialwin32

##################### setting correct working directory:


directorypath = "/home/bogfootlj/Documents/PhDCode/TimeTagger/TTCode/2023-09-15_1560nmtemperaturescan/"
# os.chdir(directorypath)
os.chdir(directorypath)  # change
###########################
# current relevant packages:


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
    # define the right message string to enable heating the oven
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
    # print("read line from controller over USB:")

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
