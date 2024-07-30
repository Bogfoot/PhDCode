import threading
import time
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter

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


def initialize_selected_channels():
    return {ch: tk.BooleanVar(value=True) for ch in channels}


# Function to format x-axis labels
def format_time(x, _):
    if x < 60:
        return f"{int(x)}"
    elif x < 3600:
        m, s = divmod(x, 60)
        return f"{int(m):02d}:{int(s):02d}"
    elif x < 86400:
        h, m = divmod(x // 60, 60)
        s = x % 60
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
    else:
        d, h = divmod(x // 3600, 24)
        m = (x % 3600) // 60
        s = x % 60
        return f"{int(d)}d {int(h):02d}:{int(m):02d}:{int(s):02d}"


# Plotting functions
time_label = "Time [dd hh:mm:ss]"


def plot_singles(ax):
    ax.cla()
    ax.set_title("Singles", fontsize=14, fontweight="bold")
    ax.set_xlabel(time_label, fontsize=12, fontweight="bold")
    ax.set_ylabel(f"Countrate [1/{expTime/1000}s]", fontsize=12, fontweight="bold")
    plotted = False
    for ch in channels:
        if selected_channels[ch].get():
            t_data = singles_data[ch]["t"]
            counts_data = singles_data[ch]["counts"]
            if counts_data:
                latest_count = counts_data[-1]
                ax.plot(t_data, counts_data, label=f"Ch{ch} ({latest_count})")
            plotted = True
    if plotted:
        ax.legend(loc="upper left")
    ax.xaxis.set_major_formatter(FuncFormatter(format_time))
    ax.grid(True)


def plot_coincidences(ax):
    ax.cla()
    ax.set_title("Coincidences", fontsize=14, fontweight="bold")
    ax.set_xlabel(time_label, fontsize=12, fontweight="bold")
    ax.set_ylabel(f"Countrate [1/{expTime/1000}s]", fontsize=12, fontweight="bold")
    plotted = False
    for coinc in coincidences:
        if (
            selected_channels[int(coinc[0])].get()
            and selected_channels[int(coinc[2])].get()
        ):
            t_data = coincidences_data[coinc]["t"]
            counts_data = coincidences_data[coinc]["counts"]
            if counts_data:
                # Calculate adjusted coincidences by subtracting noise
                noise = [
                    singles_data[int(coinc[0])]["counts"][i]
                    * singles_data[int(coinc[2])]["counts"][i]
                    * coincWin
                    / 1e12
                    for i in range(len(t_data))
                ]
                adjusted_counts = [
                    counts_data[i] - noise[i] for i in range(len(t_data))
                ]
                latest_count = counts_data[-1]
                latest_adjusted = adjusted_counts[-1]
                ax.plot(
                    t_data,
                    counts_data,
                    label=f"Coinc {coinc} ({latest_count}, {latest_adjusted:.2f})",
                )
            plotted = True
    if plotted:
        ax.legend(loc="upper left")
    ax.xaxis.set_major_formatter(FuncFormatter(format_time))
    ax.grid(True)


# Tkinter setup
root = tk.Tk()
root.title("QuTAG MC Data Plotter")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Initialize selected channels after Tk root is created
selected_channels = initialize_selected_channels()

# Create a figure for the plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

canvas = FigureCanvasTkAgg(fig, master=mainframe)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add buttons
button_frame = ttk.Frame(mainframe, padding="5 5 5 5")
button_frame.grid(column=0, row=1, sticky=(tk.W, tk.E))


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


singles_button = ttk.Button(button_frame, text="Show Singles", command=show_singles)
singles_button.grid(column=0, row=0, sticky=tk.W)

coincidences_button = ttk.Button(
    button_frame, text="Show Coincidences", command=show_coincidences
)
coincidences_button.grid(column=1, row=0, sticky=tk.W)

both_button = ttk.Button(button_frame, text="Show Both", command=show_both)
both_button.grid(column=2, row=0, sticky=tk.W)

# Key bindings
root.bind("1", lambda event: show_singles())
root.bind("2", lambda event: show_coincidences())
root.bind("3", lambda event: show_both())


# Update plot data function
def update_plot():
    global newdata
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
                root.after(0, plot_singles, ax1)
            elif current_plot == "coincidences":
                root.after(0, plot_coincidences, ax2)
            else:
                root.after(0, plot_singles, ax1)
                root.after(0, plot_coincidences, ax2)
            root.after(0, canvas.draw)


def on_close():
    global running
    running = False
    tt.deInitialize()
    print("Deinitializing TT and Closing")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)


# Example function to start the update loop in a separate thread
def start_update_thread():
    update_thread = threading.Thread(target=update_plot)
    update_thread.daemon = True
    update_thread.start()


start_update_thread()

# Run the Tkinter main loop
root.mainloop()
