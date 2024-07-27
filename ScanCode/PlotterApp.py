import threading
import time
import tkinter as tk
from collections import deque
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

# Initialize data structures using deque
channels = [1, 2, 3, 4]
coincidences = {"1/2": 33, "1/3": 34, "2/3": 35, "1/4": 36, "2/4": 37, "3/4": 38}
singles_data = {
    ch: {"t": deque(maxlen=100), "counts": deque(maxlen=100)} for ch in channels
}
coincidences_data = {
    coinc: {"t": deque(maxlen=100), "counts": deque(maxlen=100)}
    for coinc in coincidences
}
newdata = 0
running = True
current_plot = "both"
legend_opacity = 0


# Function to get the last value from deque data
def get_last_value(deque_data):
    if len(deque_data["t"]) > 0:
        return deque_data["counts"][-1]
    return 0


# Define font properties
font_properties = {"weight": "bold", "size": 12}


# Plotting functions
def plot_singles(ax):
    ax.cla()
    ax.set_title("Singles", fontdict={"weight": "bold", "size": 13})
    ax.set_xlabel("Time [s]", fontdict={"weight": "bold", "size": 12})
    ax.set_ylabel(
        f"Countrate [1/{expTime/1000}s]", fontdict={"weight": "bold", "size": 12}
    )
    for ch in channels:
        last_value = get_last_value(singles_data[ch])
        ax.plot(
            list(singles_data[ch]["t"]),
            list(singles_data[ch]["counts"]),
            label=f"Ch {ch} (Last: {last_value})",
            linewidth=2,  # Makes the plot lines bold
        )
    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        fancybox=False,
        shadow=False,
        ncol=5,
        prop=font_properties,  # Apply font properties to legend
    )
    legend.get_frame().set_alpha(legend_opacity)


def plot_coincidences(ax):
    ax.cla()
    ax.set_title("Coincidences", fontdict={"weight": "bold", "size": 13})
    ax.set_xlabel("Time [s]", fontdict={"weight": "bold", "size": 12})
    ax.set_ylabel(
        f"Countrate [1/{expTime/1000}s]", fontdict={"weight": "bold", "size": 12}
    )
    for coinc in coincidences:
        last_value = get_last_value(coincidences_data[coinc])
        ax.plot(
            list(coincidences_data[coinc]["t"]),
            list(coincidences_data[coinc]["counts"]),
            label=f"Coinc {coinc} (Last: {last_value})",
            linewidth=2,  # Makes the plot lines bold
        )
    legend = ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        fancybox=False,
        shadow=False,
        ncol=5,
        prop=font_properties,  # Apply font properties to legend
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
root.title("Bogfoot's Corner")

# Create Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create frames for tabs
plotting_frame = ttk.Frame(notebook)
settings_frame = ttk.Frame(notebook)

# Add frames to notebook
notebook.add(plotting_frame, text="Plotting")
notebook.add(settings_frame, text="Settings")

# Create Matplotlib canvas
canvas = plt.Figure()
ax1 = canvas.add_subplot(211)
ax2 = canvas.add_subplot(212)
canvas_widget = FigureCanvasTkAgg(canvas, master=plotting_frame)
canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

button_frame = ttk.Frame(plotting_frame)
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
    root.focus_set()  # Move focus away from the entry widget


exposure_textbox.bind("<Return>", on_exposure_enter)


def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings Window")
    tk.Button(settings_window, text="Do Nothing").pack(pady=20)


# Add settings UI elements (placeholders)
tk.Button(settings_frame, text="Open Settings", command=open_settings_window).pack(
    pady=20
)


def on_close():
    global running
    running = False
    tt.deInitialize()
    print("Deinitializing TT and Closing")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)


# Keyboard event handling
def on_key_press(event):
    global current_plot
    if event.keysym == "1":
        show_singles()
    elif event.keysym == "2":
        show_coincidences()
    elif event.keysym == "3":
        show_both()
    elif event.keysym == "q":
        on_close()


root.bind("<KeyPress>", on_key_press)


# Function to update plot
def update_plot():
    global newdata
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
                singles_data[ch]["t"].popleft()
                singles_data[ch]["counts"].popleft()
            for coinc in coincidences:
                coincidences_data[coinc]["t"].popleft()
                coincidences_data[coinc]["counts"].popleft()

        if current_plot == "singles":
            plot_singles(ax1)
        elif current_plot == "coincidences":
            plot_coincidences(ax2)
        else:
            plot_singles(ax1)
            plot_coincidences(ax2)
        canvas_widget.draw()


# Function to run update in a separate thread
def run_update_thread():
    global running
    while running:
        update_plot()
        time.sleep(exposure_time)


# Start the update thread
update_thread = threading.Thread(target=run_update_thread)
update_thread.start()

# Start Tkinter main loop
root.mainloop()
