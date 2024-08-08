import matplotlib.pyplot as plt
import numpy as np

# Define the data
data = np.array(
    [
        [0.628, 0.0181 - 0.0789j, -1.49e-03 - 0.0681j, 0.0585 - 0.467j],
        [0.0181 + 0.0789j, 0.0104, 8.51e-03 - 2.15e-03j, 0.0604 - 6.13e-03j],
        [-1.49e-03 + 0.0681j, 8.51e-03 + 2.15e-03j, 7.38e-03, 0.0505 + 7.46e-03j],
        [0.0585 + 0.467j, 0.0604 + 6.13e-03j, 0.0505 - 7.46e-03j, 0.354],
    ]
)

# Extract real and imaginary parts
real_parts = data.real
imaginary_parts = data.imag

# Define the labels with Bra-Ket notation
labels = ["|HH⟩", "|HV⟩", "|VH⟩", "|VV⟩"]


# Function to plot 3D bar chart
def plot_3d_bars(ax, values, title):
    # Define the coordinates for the bars
    _x = np.arange(values.shape[0])
    _y = np.arange(values.shape[1])
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()

    # Define the heights of the bars
    z = np.zeros_like(x)
    dx = dy = 0.5
    dz = values.ravel()

    # Plot the bars
    ax.bar3d(x, y, z, dx, dy, dz, shade=True)

    # Set labels and title
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Value")
    ax.set_title(title)

    # Set tick labels with Bra-Ket notation
    ax.set_xticks(_x)
    ax.set_xticklabels(labels)
    ax.set_yticks(_y)
    ax.set_yticklabels(labels[::-1])


# Create a figure with two subplots
fig = plt.figure(figsize=(12, 6))

# Plot the real parts
ax1 = fig.add_subplot(121, projection="3d")
plot_3d_bars(ax1, real_parts, "Real Parts")

# Plot the imaginary parts
ax2 = fig.add_subplot(122, projection="3d")
plot_3d_bars(ax2, imaginary_parts, "Imaginary Parts")

plt.show()
