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


selected_channels = None


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
            if t_data and counts_data:
                last_value = counts_data[-1]
                label = f"Ch {ch}: {last_value}"  # Show the last value
                ax.plot(t_data, counts_data, label=label, linewidth=2)
                plotted = True
    if plotted:
        legend = ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, 1.15),
            fancybox=False,
            shadow=False,
            ncol=5,
            fontsize=legend_font_size,
        )
        legend.get_frame().set_alpha(legend_opacity)
    ax.xaxis.set_major_formatter(FuncFormatter(format_time))
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=10)


def plot_coincidences(ax):
    ax.cla()
    ax.set_title("Coincidences", fontsize=14, fontweight="bold")
    ax.set_xlabel(time_label, fontsize=12, fontweight="bold")
    ax.set_ylabel(f"Countrate [1/{expTime/1000}s]", fontsize=12, fontweight="bold")
    plotted = False
    active_channels = [ch for ch in channels if selected_channels[ch].get()]
    for coinc in coincidences:
        ch1, ch2 = map(int, coinc.split("/"))
        if ch1 in active_channels and ch2 in active_channels:
            t_data = coincidences_data[coinc]["t"]
            counts_data = coincidences_data[coinc]["counts"]
            if t_data and counts_data:
                last_value = counts_data[-1]
                label = f"Coinc {coinc}: {last_value}"  # Show the last value
                ax.plot(t_data, counts_data, label=label, linewidth=2)
                plotted = True
    if plotted:
        legend = ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, 1.15),
            fancybox=False,
            shadow=False,
            ncol=5,
            fontsize=legend_font_size,
        )
        legend.get_frame().set_alpha(legend_opacity)
    ax.xaxis.set_major_formatter(FuncFormatter(format_time))
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=10)


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
# root.state('zoomed')  # Start the application maximized

# Initialize selected_channels after creating the root window
selected_channels = initialize_selected_channels()

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create frames for each tab
plotting_tab = ttk.Frame(notebook)
settings_tab = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(plotting_tab, text="Plotting")
notebook.add(settings_tab, text="Settings")

# Plotting tab
main_frame = ttk.Frame(plotting_tab)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create Matplotlib canvas
canvas = plt.Figure()
ax1 = canvas.add_subplot(211)
ax2 = canvas.add_subplot(212)
canvas_widget = FigureCanvasTkAgg(canvas, master=main_frame)
canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

button_frame = ttk.Frame(plotting_tab)
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
    root.focus_set()


exposure_textbox.bind("<Return>", on_exposure_enter)

# Settings tab
settings_frame = ttk.Frame(settings_tab)
settings_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(settings_frame, text="Channel Settings", font=("Arial", 14)).pack(pady=10)

for ch in channels:
    ttk.Checkbutton(
        settings_frame, text=f"Channel {ch}", variable=selected_channels[ch]
    ).pack(anchor="w")


def open_channel_settings():
    channel_settings_window = tk.Toplevel()
    channel_settings_window.title("Channel Settings")
    ttk.Label(
        channel_settings_window, text="Channel settings can be configured here."
    ).pack(pady=10)
    ttk.Button(
        channel_settings_window, text="Close", command=channel_settings_window.destroy
    ).pack(pady=5)


ttk.Button(
    settings_frame, text="Open Channel Settings", command=open_channel_settings
).pack(pady=20)


def on_key_press(event):
    global legend_font_size
    if event.char == "1":
        legend_font_size = 20
        show_singles()
    elif event.char == "2":
        legend_font_size = 20
        show_coincidences()
    elif event.char == "3":
        legend_font_size = 12
        show_both()
    elif event.char == "q":
        on_close()


root.bind("<KeyPress>", on_key_press)


def update_plot():
    global running, newdata
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
