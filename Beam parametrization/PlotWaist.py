import numpy as np
import plotly.graph_objects as go


# Define the functions
def w(z, w0, wavelength):
    return w0 * np.sqrt(1 + ((z * wavelength) / (np.pi * w0**2)) ** 2)


# Define the parameters
lambda_val = 780e-9

w01 = 0.00021303563094762264
zwaist1 = 0.708728441598379

# Generate the data
zcm = np.linspace(-50, 200, 5000)
waist1 = [w(z - zwaist1, w01, lambda_val) * 10**3 for z in zcm]
# waist2 = [w(z - zwaist2, w02, lambda_val) * 10**3 for z in zcm]

# Create the plot
fig = go.Figure()

fig.add_trace(go.Scatter(x=zcm, y=waist1, mode="lines", name="solution 1"))

# fig.add_trace(go.Scatter(x=zcm, y=waist2, mode="lines", name="solution 2"))

# Add labels and annotations
fig.update_layout(
    title="780 nm beam after the IR filtering section",
    xaxis_title="z (cm)",
    yaxis_title="waist (mm)",
    showlegend=True,
    legend_title="Legend",
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor="black"),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor="black"),
    plot_bgcolor="white",
)

fig.update_xaxes(range=[-5, 5])
fig.update_yaxes(range=[0, 1.3])

# # Find the intersection point
# intersections = []
# for i in range(len(zcm) - 1):
#     if waist1[i] <= waist2[i] and waist1[i + 1] >= waist2[i + 1]:
#         # Linear interpolation to find the approximate x-coordinate of the intersection
#         x1 = zcm[i]
#         x2 = zcm[i + 1]
#         y1 = waist1[i]
#         y2 = waist1[i + 1]
#         slope = (y2 - y1) / (x2 - x1)
#         intersection = x1 + (waist2[i] - y1) / slope
#         intersections.append(intersection)
#
# if intersections is not None:
#     for intersect in intersections:
#         fig.add_annotation(
#             text="measured waist w₂",
#             x=intersect,
#             y=np.interp(intersect, zcm, waist2),
#             ax=34,
#             ay=0.74,
#             arrowhead=2,
#         )
#
fig.show()
