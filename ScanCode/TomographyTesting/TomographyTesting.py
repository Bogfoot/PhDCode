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
print(f"PhiplusDensityMatrix =\n{PhiplusDensityMatrix}")
Phiminus = 1 / np.sqrt(2) * (HH - VV)
print(f"Phiminus: {Phiminus}")
PhiminusDensityMatrix = calcDensityMatrix(Phiminus)
print(f"PhiminusDensityMatrix =\n{PhiminusDensityMatrix}")

Psiplus = 1 / np.sqrt(2) * (HV + VH)
print(f"Psiplus: {Psiplus}")
PsiplusDensityMatrix = calcDensityMatrix(Psiplus)
print(f"PsiplusDensityMatrix =\n{PsiplusDensityMatrix}")

Psiminus = 1 / np.sqrt(2) * (HV - VH)
print(f"Psiminus: {Psiminus}")
PsiminusDensityMatrix = calcDensityMatrix(Psiminus)
print(f"PsiminusDensityMatrix =\n{PsiminusDensityMatrix}")

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
]

for rho in rhos:
    ax1 = fig.add_subplot(111, projection="3d")  # Create a new subplot
    plot_3d_bars(ax1, rho, "Real Parts")  # Replace with your 3D plotting function
    plt.show()  # Show the current plot
    sleep(5)  # Pause for 5 seconds
    plt.clf()  # Clear the figure for the next plot
