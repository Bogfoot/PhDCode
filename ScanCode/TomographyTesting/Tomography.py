import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import QuantumTomography as qLib

# Coincidence counts for 9 measurements.
# Each row is the coincidence counts for detector pairs 1 H1H2 (1/4),2 H1V2 (1/3),3 V1H2 (2/4), and 4 V1V2 (2/3) respectfully
file_path = sys.argv[1]
data = pd.read_csv(file_path)

# Extract singles counts (columns 3-6) and coincidence counts (columns 7-10)
singles_counts = data[["1", "2", "3", "4"]].values[:9]  # Taking the first 9 rows
coincidence_counts = data[["1/4", "1/3", "2/4", "2/3"]].values[
    :9
]  # Taking the first 9 rows

# print(f"Singles counts:\n{singles_counts}\n coincidence_counts:\n{coincidence_counts}")


# Measurement basis for 9 measurements
# In each row the first two (possible complex) numbers alpha and beta represent the state that the first qubit
# is projected onto when it ends up at detector 1.
# The next two numbers is the state the second qubit is projected onto when it ends up at detector 2.
measurements = np.array(
    [
        [1 + 0j, 0j, 1 + 0j, 0j],
        [1 + 0j, 0j, 0.70710678 + 0j, 0.7071067811865476 + 0j],
        [1 + 0j, 0j, 0.70710678 + 0j, 0.70710678j],
        [0.70710678 + 0j, 0.70710678 + 0j, 1 + 0j, 0j],
        [0.70710678 + 0j, 0.70710678 + 0j, 0.70710678 + 0j, 0.70710678 + 0j],
        [0.70710678 + 0j, 0.70710678 + 0j, 0.70710678 + 0j, 0.70710678j],
        [0.70710678 + 0j, 0.70710678j, 1 + 0j, 0j],
        [0.70710678 + 0j, 0.70710678j, 0.70710678 + 0j, 0.70710678 + 0j],
        [0.70710678 + 0j, 0.70710678j, 0.70710678 + 0j, 0.7071067811865476j],
    ]
)

# Initiate tomography object
tomo_obj = qLib.Tomography()

# Run tomography
[rho_approx, intensity, fval] = tomo_obj.StateTomography(
    measurements,
    coincidence_counts,
    singles=singles_counts,
    window=np.array([0.4, 0.4, 0.4, 0.4]),
)
# Print Results
tomo_obj.printLastOutput()
print("----------------")
phi_plus = 1 / np.sqrt(2) * np.array([1, 0, 0, -1], dtype=complex)
phi_plus_I = 1 / np.sqrt(2) * np.array([1, 0, 0, 1j], dtype=complex)
psi_plus = 1 / np.sqrt(2) * np.array([1, 0, 0, 1], dtype=complex)
psi_minus = 1 / np.sqrt(2) * np.array([0, 1, 1, 0], dtype=complex)
phi_minus = 1 / np.sqrt(2) * np.array([0, 1, -1, 0], dtype=complex)

print("Fidelity with actual : " + str(qLib.fidelity(phi_plus_I, rho_approx)))
# Giveds the density matrix rho
print(rho_approx)
print(np.trace(np.matmul(rho_approx, rho_approx)))

bell_states = [phi_plus, phi_plus_I, psi_plus, psi_minus, phi_minus]

for state in bell_states:
    print()
    print(state)
    print("Fidelity with actual : " + str(qLib.fidelity(state, rho_approx)))
    

real_parts = rho_approx.real
imaginary_parts = rho_approx.imag

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
