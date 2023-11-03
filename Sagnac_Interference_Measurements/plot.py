import csv
import plotly.graph_objects as go

# Read data from CSV file
with open("SIM.csv", "r") as csvfile:
    data = list(csv.reader(csvfile))

# Extract angles and powers from the CSV data
angles = [float(row[0]) for row in data]
powers = [float(row[1]) for row in data]

# Create a Plotly scatter plot with lines connecting the dots
fig = go.Figure()

# Add scatter plot trace
fig.add_trace(go.Scatter(x=angles, y=powers, mode="markers+lines", name="Data"))

# Set plot labels and title
fig.update_layout(
    title="Measurement of power vs angle of L/2 after Quantum Eraser in its H output",
    xaxis_title="Angle/°",
    yaxis_title="Power/mW",
)

# Show the interactive plot
fig.show()
