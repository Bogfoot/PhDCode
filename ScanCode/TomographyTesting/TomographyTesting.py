import matplotlib.pyplot as plt
import numpy as np

H = 1 / np.sqrt(2) * np.array([1, 0])
V = 1 / np.sqrt(2) * np.array([0, 1])

HH = np.outer(H, H)
print(f"HH: {HH}")
VV = np.outer(V, V)
print(f"VV: {VV}")

Psi = HH + VV
print(f"Psi: {Psi}")

PsiDensityMatrix = np.outer(Psi, Psi)
print(f"PsiDensityMatrix =\n{PsiDensityMatrix}")

print(f"Trace of Psi^2: {np.trace(np.matmul(Psi,Psi))}")

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

    print(x, y, z, dx, dy, dz)

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
ax1 = fig.add_subplot(111, projection="3d")
plot_3d_bars(ax1, PsiDensityMatrix, "Real Parts")

plt.show()
