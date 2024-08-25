import matplotlib.pyplot as plt
import numpy as np


def calcDensityMatrix(psi):
    return np.outer(psi, np.conj(psi))


def tensorProduct(psi, phi):
    return np.outer(psi, phi)


def purityOfState(psi):
    return np.trace(np.matmul(psi, psi))


H = 1 / np.sqrt(2) * np.array([1, 0])
V = 1 / np.sqrt(2) * np.array([0, 1])

# Testing with just H
HH = tensorProduct(H, H)
HHDensityMatrix = calcDensityMatrix(H)
print(f"HHDensityMatrix: {HHDensityMatrix}")
print(f"Purity of HHDensityMatrix: {purityOfState(HHDensityMatrix)}")


# Testing with D and A
D = H + V
A = H - V
DA = tensorProduct(D, A)
normDA = np.linalg.norm(DA)
DA = DA / np.linalg.norm(DA)
print(f" Norm of DA: {normDA}")
print(f"DA: {DA}")
AD = tensorProduct(A, D)
AD = DA / np.linalg.norm(AD)
normAD = np.linalg.norm(AD)
print(f" Norm of AD: {normAD}")
print(f"AD: {AD}")
Phi = DA + AD
normPhi = np.linalg.norm(Phi)
Phi = Phi / np.linalg.norm(Phi)
print(f" Norm of Phi: {normPhi}")
print(f"Phi: {Phi}")
PhiDensityMatrix = calcDensityMatrix(Phi)
print(f"PhiDensityMatrix =\n{PhiDensityMatrix}")
print(f"Purity of PhiDensityMatrix: {purityOfState(PhiDensityMatrix)}")

# Testing with bell states
print(f"HH: {HH}")
VV = tensorProduct(V, V)
print(f"VV: {VV}")

Psi = HH + VV
print(f"Psi: {Psi}")

PsiDensityMatrix = calcDensityMatrix(Psi)
print(f"PsiDensityMatrix =\n{PsiDensityMatrix}")

print(f"Purity of PsiDensityMatrix: {purityOfState(PsiDensityMatrix)}")

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
