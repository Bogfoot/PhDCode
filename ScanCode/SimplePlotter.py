import time
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    import QuTAG_MC
except ImportError:
    print("TT wrapper not found.")
    exit(1)

# Initialize QuTAG device
tt = QuTAG_MC.QuTAG()
exposure_time = 0.1
tt.setExposureTime(int(exposure_time * 1000))
_, coincWin, expTime = tt.getDeviceParams()
print(f"Coincidence window: {coincWin}\nBins, exposure time: {expTime} ms")

# Initialize data structures
channels = [1, 2, 3, 4]
coincidences = {"1/2": 33, "1/3": 34, "2/3": 35, "1/4": 36, "2/4": 37, "3/4": 38}
singles_data = {ch: {"t": [], "counts": []} for ch in channels}
coincidences_data = {coinc: {"t": [], "counts": []} for coinc in coincidences}
newdata = 0
running = True
current_plot = "both"
legend_opacity = 0


# Plotting functions
def plot_singles(ax):
    ax.cla()
    ax.set_title("Singles")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(f"Countrate [1/{expTime/1000}s]")
    for ch in channels:
        ax.plot(singles_data[ch]["t"], singles_data[ch]["counts"], label=f"Ch {ch}")
    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        fancybox=False,
        shadow=False,
        ncol=5,
    )
    legend.get_frame().set_alpha(legend_opacity)


def plot_coincidences(ax):
    ax.cla()
    ax.set_title("Coincidences")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(f"Countrate [1/{expTime/1000}s]")
    for coinc in coincidences:
        ax.plot(
            coincidences_data[coinc]["t"],
            coincidences_data[coinc]["counts"],
            label=f"Coinc {coinc}",
        )
    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        fancybox=False,
        shadow=False,
        ncol=5,
    )
    legend.get_frame().set_alpha(legend_opacity)


def show_singles():
    global current_plot, ax1, ax2
    current_plot = "singles"
    ax1.set_visible(True)
    ax2.set_visible(False)
    ax1.set_position([0.1, 0.15, 0.85, 0.65])
    canvas_widget.draw()


def show_coincidences():
    global current_plot, ax1, ax2
    current_plot = "coincidences"
    ax1.set_visible(False)
    ax2.set_visible(True)
    ax2.set_position([0.1, 0.15, 0.85, 0.65])
    canvas_widget.draw()


def show_both():
    global current_plot, ax1, ax2
    current_plot = "both"
    ax1.set_visible(True)
    ax2.set_visible(True)
    ax1.set_position([0.1, 0.6, 0.85, 0.35])
    ax2.set_position([0.1, 0.1, 0.85, 0.35])
    canvas_widget.draw()


def submit_exposure_time(text):
    global exposure_time, expTime, newdata
    try:
        new_exposure_time = int(text)
        if 1 <= new_exposure_time <= 10000:
            exposure_time = new_exposure_time / 1000
            tt.setExposureTime(new_exposure_time)
            _, _, expTime = tt.getDeviceParams()
            print(f"Updated exposure time: {expTime} ms")

            # Clear the plot data
            for ch in channels:
                singles_data[ch]["t"].clear()
                singles_data[ch]["counts"].clear()

            for coinc in coincidences:
                coincidences_data[coinc]["t"].clear()
                coincidences_data[coinc]["counts"].clear()

            newdata = 0
        else:
            print("Exposure time must be between 1 and 10000 ms.")
    except ValueError:
        print("Invalid input. Please enter an integer between 1 and 10000.")


# Initialize Tkinter
root = tk.Tk()
root.title("QuTAG Plotter App")

main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create Matplotlib canvas
canvas = plt.Figure()
ax1 = canvas.add_subplot(211)
ax2 = canvas.add_subplot(212)
canvas_widget = FigureCanvasTkAgg(canvas, master=main_frame)
canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

button_frame = ttk.Frame(root)
button_frame.pack()

h, w = 2, 10
tk.Button(button_frame, text="Singles", command=show_singles, height=h, width=w).pack(
    side=tk.LEFT
)
tk.Button(
    button_frame, text="Coincidences", command=show_coincidences, height=h, width=w
).pack(side=tk.LEFT)
tk.Button(button_frame, text="Both", command=show_both, height=h, width=w).pack(
    side=tk.LEFT
)
tk.Label(button_frame, text="Exposure time (ms):").pack(side=tk.LEFT)

exposure_textbox = ttk.Entry(button_frame, width=5)
exposure_textbox.insert(0, str(int(exposure_time * 1000)))
exposure_textbox.pack(side=tk.LEFT)


def on_exposure_enter(event):
    submit_exposure_time(exposure_textbox.get())


exposure_textbox.bind("<Return>", on_exposure_enter)


def on_close():
    global running
    running = False
    tt.deInitialize()
    print("Deinitializing TT and Closing")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)

try:
    while running:
        root.update_idletasks()
        root.update()
        time.sleep(exposure_time)
        data, updates = tt.getCoincCounters()
        if updates == 0:
            print("Waiting for data...")
        else:
            newdata += 1
            time_val = newdata * expTime / 1000
            # Singles
            for ch in channels:
                singles_data[ch]["t"].append(time_val)
                singles_data[ch]["counts"].append(data[ch])
            # Coincidences
            for coinc in coincidences:
                coinc_idx = coincidences[coinc]
                coincidences_data[coinc]["t"].append(time_val)
                coincidences_data[coinc]["counts"].append(data[coinc_idx])

            if len(singles_data[channels[0]]["t"]) > 100:
                for ch in channels:
                    singles_data[ch]["t"].pop(0)
                    singles_data[ch]["counts"].pop(0)
                for coinc in coincidences:
                    coincidences_data[coinc]["t"].pop(0)
                    coincidences_data[coinc]["counts"].pop(0)
            if current_plot == "singles":
                plot_singles(ax1)
            elif current_plot == "coincidences":
                plot_coincidences(ax2)
            else:
                plot_singles(ax1)
                plot_coincidences(ax2)
            canvas_widget.draw()
except Exception as e:
    print(f"Caught an exception: {e}")
    tt.deInitialize()
    root.destroy()
finally:
    if running:
        tt.deInitialize()
        print("Deinitializing TT and Closing")
    root.destroy()
    exit(2)
