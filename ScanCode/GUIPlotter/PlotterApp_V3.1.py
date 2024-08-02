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
legend_font_size = 20

def initialize_selected_channels():
    return {ch: tk.BooleanVar(value=True) for ch in channels}

selected_channels = initialize_selected_channels()

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
            if t_data:
                ax.plot(t_data, counts_data, label=f"CH{ch}")
                plotted = True
    if plotted:
        ax.legend(loc="upper right", fontsize=legend_font_size, fancybox=True, framealpha=legend_opacity)
    ax.xaxis.set_major_formatter(FuncFormatter(format_time))
    ax.grid(True)

    # Handle auto-scaling and manual limits
    if not autoscale_x.get():
        ax.set_xlim(float(x_min.get()), float(x_max.get()))
    if not autoscale_y.get():
        ax.set_ylim(float(y_min.get()), float(y_max.get()))

def plot_coincidences(ax):
    ax.cla()
    ax.set_title("Coincidences", fontsize=14, fontweight="bold")
    ax.set_xlabel(time_label, fontsize=12, fontweight="bold")
    ax.set_ylabel(f"Countrate [1/{expTime/1000}s]", fontsize=12, fontweight="bold")
    plotted = False
    for coinc in coincidences:
        t_data = coincidences_data[coinc]["t"]
        counts_data = coincidences_data[coinc]["counts"]
        if t_data:
            ax.plot(t_data, counts_data, label=coinc)
            plotted = True
    if plotted:
        ax.legend(loc="upper right", fontsize=legend_font_size, fancybox=True, framealpha=legend_opacity)
    ax.xaxis.set_major_formatter(FuncFormatter(format_time))
    ax.grid(True)

    # Handle auto-scaling and manual limits
    if not autoscale_x.get():
        ax.set_xlim(float(x_min.get()), float(x_max.get()))
    if not autoscale_y.get():
        ax.set_ylim(float(y_min.get()), float(y_max.get()))

# Tkinter GUI setup
root = tk.Tk()
root.title("QuTAG Plotter")

main_frame = ttk.Frame(root, padding="5")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, columnspan=4)

# Add control panel
control_frame = ttk.Frame(main_frame, padding="5")
control_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

# Auto-scaling controls
autoscale_x = tk.BooleanVar(value=True)
autoscale_y = tk.BooleanVar(value=True)
ttk.Checkbutton(control_frame, text="Auto-scale X", variable=autoscale_x).grid(row=0, column=0)
ttk.Checkbutton(control_frame, text="Auto-scale Y", variable=autoscale_y).grid(row=0, column=1)

# Manual range controls
ttk.Label(control_frame, text="X min:").grid(row=1, column=0)
x_min = ttk.Entry(control_frame)
x_min.grid(row=1, column=1)
ttk.Label(control_frame, text="X max:").grid(row=1, column=2)
x_max = ttk.Entry(control_frame)
x_max.grid(row=1, column=3)

ttk.Label(control_frame, text="Y min:").grid(row=2, column=0)
y_min = ttk.Entry(control_frame)
y_min.grid(row=2, column=1)
ttk.Label(control_frame, text="Y max:").grid(row=2, column=2)
y_max = ttk.Entry(control_frame)
y_max.grid(row=2, column=3)

# Add channel selection checkbuttons
selected_channels = initialize_selected_channels()
for idx, ch in enumerate(channels):
    ttk.Checkbutton(control_frame, text=f"Channel {ch}", variable=selected_channels[ch]).grid(row=3, column=idx)

# Example function to update plots
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
            # print(f"Time: {time_val}s, Data: {data}")
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
            root.after(0, canvas_widget.draw)

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
