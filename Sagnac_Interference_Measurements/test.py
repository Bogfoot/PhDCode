import tkinter as tk
from tkinter import filedialog
import csv
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from PIL import Image, ImageTk

# Function to load data from a CSV file and update the plot
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'r') as csvfile:
            data = list(csv.reader(csvfile))
        # Process the data and update the plot
        update_plot(data)

# Function to update the plot and save it as an image
def update_plot(data):
    # Extract angles and powers from the loaded data (customize based on your CSV structure)
    angles = [float(row[0]) for row in data]
    powers = [float(row[1]) for row in data]

    # Create a subplot with a scatter plot for the data
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, shared_yaxes=True)
    fig.add_trace(go.Scatter(x=angles, y=powers, mode='markers', marker=dict(size=12), name='Data'))

    # Update subplot layout
    fig.update_layout(title='Angles vs Powers', xaxis_title='Angles', yaxis_title='Powers')

    # Save the plot as an image file
    pio.write_image(fig, "plot.png")

    # Load the saved image and display it in the Tkinter window
    image = Image.open("plot.png")
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

# Create the Tkinter GUI
root = tk.Tk()
root.title("Data Visualization App")

# Create a button to load data
load_button = tk.Button(root, text="Load Data", command=load_data)
load_button.pack(pady=20)

# Create a label to display the image
label = tk.Label(root)
label.pack()

# Start the Tkinter main loop
root.mainloop()
