from time import sleep

import matplotlib.pyplot as plt
import numpy as np


def calcDensityMatrix(psi):
    return np.outer(psi, np.conj(psi))


def tensorProduct(psi, phi):
    return np.outer(psi, phi)


def purityOfState(psi):
    return np.trace(np.matmul(psi, psi))


H = np.array([1, 0])
V = np.array([0, 1])

# Testing with just H
HH = tensorProduct(H, H)
VV = tensorProduct(V, V)
print(f"HH: {HH}")
print(f"VV: {VV}")
HV = tensorProduct(H, V)
VH = tensorProduct(V, H)

# Testing with bell states
Phiplus = 1 / np.sqrt(2) * (HH + VV)
print(f"Phiplus: {Phiplus}")
PhiplusDensityMatrix = calcDensityMatrix(Phiplus)

Phiminus = 1 / np.sqrt(2) * (HH - VV)
print(f"Phiminus: {Phiminus}")
PhiminusDensityMatrix = calcDensityMatrix(Phiminus)

Psiplus = 1 / np.sqrt(2) * (HV + VH)
print(f"Psiplus: {Psiplus}")
PsiplusDensityMatrix = calcDensityMatrix(Psiplus)

Psiminus = 1 / np.sqrt(2) * (HV - VH)
print(f"Psiminus: {Psiminus}")
PsiminusDensityMatrix = calcDensityMatrix(Psiminus)

PhiIMinus = 1 / np.sqrt(2) * (HV - VH * 1j)
PhiIminusDensityMatrix = calcDensityMatrix(PhiIMinus)

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
rhos = [
    PsiplusDensityMatrix,
    PsiminusDensityMatrix,
    PhiplusDensityMatrix,
    PhiminusDensityMatrix,
    PhiIminusDensityMatrix,
]

# ax1 = fig.add_subplot(331, projection="3d")  # Create a new subplot
# plot_3d_bars(ax1, rhos[0], "Psi Plus")  # Replace with your 3D plotting function
# ax2 = fig.add_subplot(332, projection="3d")  # Create a new subplot
# plot_3d_bars(ax2, rhos[2], "Psi Minus")  # Replace with your 3D plotting function
# ax3 = fig.add_subplot(333, projection="3d")  # Create a new subplot
# plot_3d_bars(ax3, rhos[1], "Phi Plus")  # Replace with your 3D plotting function
# ax4 = fig.add_subplot(334, projection="3d")  # Create a new subplot
# plot_3d_bars(ax4, rhos[3], "Phi Minus")  # Replace with your 3D plotting function
ax5 = fig.add_subplot(335, projection="3d")  # Create a new subplot
rhos[4] = rhos[4].real + rhos[4].imag
plot_3d_bars(ax5, rhos[4], "Phi I Minus")  # Replace with your 3D plotting function
plt.show()
