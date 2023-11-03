import csv
import plotly.graph_objects as go

# Read data from CSV file
with open('SIM.csv', 'r') as csvfile:
    data = list(csv.reader(csvfile))

# Extract angles and powers from the CSV data
angles = [float(row[0]) for row in data]
powers = [float(row[1]) for row in data]

# Sort data points based on angles
sorted_indices = sorted(range(len(angles)), key=lambda k: angles[k])
sorted_angles = [angles[i] for i in sorted_indices]
sorted_powers = [powers[i] for i in sorted_indices]

# Find minima and maxima
minima_indices = [i for i in range(1, len(sorted_angles) - 1) if sorted_powers[i - 1] > sorted_powers[i] < sorted_powers[i + 1]]
maxima_indices = [i for i in range(1, len(sorted_angles) - 1) if sorted_powers[i - 1] < sorted_powers[i] > sorted_powers[i + 1]]

# Create lists of points for minima and maxima
minima_points = [(sorted_angles[i], sorted_powers[i]) for i in minima_indices]
maxima_points = [(sorted_angles[i], sorted_powers[i]) for i in maxima_indices]

# Create a Plotly scatter plot with lines connecting minima and maxima
fig = go.Figure()

# Add scatter plot trace for data points
fig.add_trace(go.Scatter(x=sorted_angles, y=sorted_powers, mode='markers', name='Data'))

# Add lines connecting minima
fig.add_trace(go.Scatter(x=[point[0] for point in minima_points], y=[point[1] for point in minima_points], mode='lines', name='Minima Lines'))

# Add lines connecting maxima
fig.add_trace(go.Scatter(x=[point[0] for point in maxima_points], y=[point[1] for point in maxima_points], mode='lines', name='Maxima Lines'))

# Set plot labels and title
fig.update_layout(title='Angles vs Powers with Lines Connecting Minima and Maxima', xaxis_title='Angles', yaxis_title='Powers')

# Show the interactive plot
fig.show()
