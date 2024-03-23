import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
import QuTAG_MC
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Mockup function to simulate data acquisition
def get_coinc_counters():
    data = {i: random.randint(0, 100) for i in range(1, 9)}
    updates = 1  # You might replace this with your actual update logic
    return data, updates


class LivePlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Plot App")
        self.root.geometry("1000x800")
        self.root.config(bg="gray")
        self.frame = ttk.Frame(self.root)
        self.grid = ttk.Frame(self.frame, borderwidth=5, relief="ridge")

        self.tt = QuTAG_MC.QuTAG()

        # Variables to store selected channel numbers
        self.channel_1_var = tk.StringVar(value="1")
        self.channel_2_var = tk.StringVar(value="2")

        # Create widgets
        self.create_widgets()

        # Matplotlib setup
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(column=0, row=0, rowspan=10)
        self.animation()

    def create_widgets(self):
        # channelLabel = []
        # for channel in channels:
        #     channelLabel[channel] = ttk.Label(self.root, text=f"Channel {channel}: ")

        # Dropdown menus for channel selection
        channel1Label = ttk.Label(self.root, text="Channel 1:")
        channel1Label.grid(column=1, row=0, padx=5, sticky="NW")
        channel_1_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.channel_1_var,
            values=[str(i) for i in range(1, 9)],
        )
        channel_1_dropdown.grid(column=2, row=0, pady=0, sticky="N")

        channel2Label = ttk.Label(self.root, text="Channel 2:")
        channel2Label.grid(column=1, row=1, padx=5, sticky="NW")
        channel_2_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.channel_2_var,
            values=[str(i) for i in range(1, 9)],
        )
        channel_2_dropdown.grid(column=2, row=1, pady=0, sticky="N")

    def update_plot(self):
        # Get data from channels
        channel_1 = int(self.channel_1_var.get())
        channel_2 = int(self.channel_2_var.get())
        data, updates = self.tt.getCoincCounters()

        # Plot the data
        self.ax.clear()
        self.ax.plot(data[channel_1], marker="x")
        self.ax.plot(data[channel_2], marker="o")
        self.ax.set_xlabel("Channel")
        self.ax.set_ylabel("Counts")
        self.ax.set_title("Live Plot")

        # Redraw canvas
        self.canvas.draw()

    def animation(self):
        # Update the plot periodically (you might adjust the interval)
        self.update_plot()
        self.root.after(200, self.animation)  # 1000 milliseconds (1 second)


def on_q_pressed(event):
    confirm_exit = messagebox.askokcancel("Exit", "Do you want to exit the program?")
    if confirm_exit:
        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LivePlotApp(root)
    root.bind("<q>", on_q_pressed)
    root.mainloop()
