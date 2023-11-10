import csv
import plotly.graph_objects as go, numpy as np


# Change function to account for last measurement being a max, compare the angles to do so.
def visibility(extrema, maxs, mins):
    vis = []
    for i in range(len(extrema)):
        vis.append((maxs[i][1] - mins[i][1]) / (maxs[i][1] + mins[i][1]))
    return vis


# Read data from CSV file
with open("SIM3.csv", "r") as csvfile:
    data = list(csv.reader(csvfile))

# Extract angles and powers from the CSV data
angles = [float(row[0]) for row in data]
powers = [float(row[1]) for row in data]

# Sort data points based on angles
sorted_indices = sorted(range(len(angles)), key=lambda k: angles[k])
sorted_angles = [angles[i] for i in sorted_indices]
sorted_powers = [powers[i] for i in sorted_indices]

# Find minima and maxima
minima_indices = [
    i
    for i in range(1, len(sorted_angles) - 1)
    if sorted_powers[i - 1] > sorted_powers[i] < sorted_powers[i + 1]
]
maxima_indices = [
    i
    for i in range(1, len(sorted_angles) - 1)
    if sorted_powers[i - 1] < sorted_powers[i] > sorted_powers[i + 1]
]

# Create lists of points for minima and maxima
minima_points = [(sorted_angles[i], sorted_powers[i]) for i in minima_indices]
maxima_points = [(sorted_angles[i], sorted_powers[i]) for i in maxima_indices]

# formula for visibility
# \ni = (I_max - I_min)/(I_max + I_min)
vis = []
if len(maxima_points) >= len(minima_points):
    vis = visibility(maxima_points, maxima_points, minima_points)
else:
    vis = visibility(minima_points, maxima_points, minima_points)

mean_vis = np.mean(vis)
std_vis = np.std(vis)
print(f"Max visibility: {np.max(vis)*100:4f}")
print(f"The mean visibility is: {mean_vis*100:4f} +/- {std_vis*100:4f}")

# Create a Plotly scatter plot with lines connecting minima and maxima
fig = go.Figure()

# Define color scale for data points
# color_scale = [powers[i] for i in sorted_indices]
# color_scale = [
#     (x - min(color_scale)) / (max(color_scale) - min(color_scale)) for x in color_scale
# ]  # Normalize to [0, 1] range

# Add scatter plot trace for data points with color scale
fig.add_trace(
    go.Scatter(
        x=angles,
        y=powers,
        mode="markers",
        # marker=dict(
        #     color=color_scale,
        #     colorscale="Viridis",
        #     size=12,
        #     colorbar=dict(title="Power", xanchor="right"),
        #     colorbar_x=0.98,
        # ),
        name="Power on power meter",
    )
)

# Add lines connecting minima
fig.add_trace(
    go.Scatter(
        x=[point[0] for point in minima_points],
        y=[point[1] for point in minima_points],
        mode="lines",
        line=dict(color="blue", width=2),
        name="Minima Lines",
    )
)

# Add lines connecting maxima
fig.add_trace(
    go.Scatter(
        x=[point[0] for point in maxima_points],
        y=[point[1] for point in maxima_points],
        mode="lines",
        line=dict(color="red", width=2),
        name="Maxima Lines",
    )
)

if visibility is not None:
    for i in range(len(vis)):
        fig.add_annotation(
            x=maxima_points[i][0],
            y=maxima_points[i][1],
            text=f"Visibility: {vis[i]*100:.4f}%",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="black",
            ax=40,
            ay=-40,
            bgcolor="white",
        )

# Add legend point for ratios
fig.add_trace(
    go.Scatter(
        x=[maxima_points[-1][0]],
        y=[maxima_points[-1][1]],
        mode="markers",
        marker=dict(color="white", size=15, symbol="circle"),
        name=f"Visibility, {mean_vis*100:4f} +/- {std_vis*100:4f}",
    )
)

# Set plot labels and title
fig.update_layout(
    title="Power vs Angle by variying the L/2 WP of the Pump, measuring after Quantum Eraser H output.\nSet diode current is 82 mA. Max diode current is 262 mA.",
    xaxis_title="Angle/°",
    yaxis_title="Power/mW",
    legend=dict(x=0.01, y=0.10),
)

# Show the interactive plot
fig.show()
