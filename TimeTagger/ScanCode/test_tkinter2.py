from tkinter import *
from tkinter import ttk

import QuTAG_MC as QT
import serial
from OC import OC


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass


def check_serial_device(port):
    try:
        # Try to open the serial port
        with serial.Serial(port) as ser:
            print(f"Serial device found at {port}")
            print(f"Device information: {ser}")
    except serial.SerialException:
        print(f"No serial device found at {port}")


# Oven
usb_port = "/dev/ttyUSB0"
try:
    check_serial_device(usb_port)
    oven = OC(usb_port)
except:
    pass

# TimeTagger initialization
tt = QT.QuTAG()
data, updates = tt.getCoincCounters()
na, coincWin, expTime = tt.getDeviceParams()

# Tkinter initialization
root = Tk()
root.title("Singles and Coincidances")

mainframe = ttk.Frame(root, padding="9 9 20 20")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(
    column=3, row=3, sticky=W
)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()
