import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import erfc


# Define the error function model for the knife-edge measurement
def knife_edge_model(x, P0, r0, w, Poffset):
    return (P0 / 2) * erfc((x - r0) / (w / np.sqrt(2))) + Poffset


# Synthetic data: Replace these with your actual measurements
z1 = 300e-3
z2 = 303e-3
z3 = 1010e-3
dataz1 = np.array(
    [
        [0, 0.1187],
        [3.19, 0.1181],
        [4.45, 0.1176],
        [4.5, 0.1164],
        [4.75, 0.1087],
        [5, 0.0979],
        [5.25, 0.0849],
        [5.5, 0.0714],
        [5.75, 0.0548],
        [6, 0.0379],
        [6.25, 0.02384],
        [6.5, 0.01445],
        [6.75, 0.00841],
        [7, 0.00516],
        [7.25, 0.00335],
        [7.5, 0.00241],
        [7.75, 0.00171],
        [8, 0.00127],
        [8.25, 0.00104],
        [8.5, 0.00085],
        [8.75, 0.00078],
        [9, 0.00065],
        [9.25, 0.00064],
        [9.5, 0.00057],
        [9.75, 0.00048],
        [10.5, 0.00035],
        [10.75, 0.00021],
        [11, 0.00011],
        [11.25, 0.00004],
        [11.5, 0.00001],
        [11.6, 0.000005],
    ]
)
dataz2 = np.array(
    [
        [3.88, 0.126],
        [4.38, 0.122],
        [4.63, 0.115],
        [4.88, 0.104],
        [5.18, 0.088],
        [5.38, 0.077],
        [5.63, 0.055],
        [5.83, 0.041],
        [6.13, 0.024],
        [6.38, 0.016],
        [6.63, 0.0093],
        [6.88, 0.0055],
        [7.13, 0.0035],
        [7.38, 0.0025],
        [7.63, 0.0018],
        [7.88, 0.0013],
        [8.13, 0.0009],
        [8.38, 0.0008],
        [8.63, 0.0006],
        [8.88, 0.0006],
        [9.38, 0.00045],
        [9.88, 0.00045],
        [10.38, 0.00015],
        [10.88, 0.00005],
    ]
)
dataz3 = np.array(
    [
        [0, 0.136],
        [0.25, 0.134],
        [0.5, 0.128],
        [0.55, 0.126],
        [0.6, 0.124],
        [0.65, 0.12],
        [0.7, 0.118],
        [0.75, 0.116],
        [0.8, 0.113],
        [0.85, 0.111],
        [0.9, 0.109],
        [0.95, 0.105],
        [1, 0.103],
        [1.05, 0.1],
        [1.1, 0.097],
        [1.15, 0.0988],
        [1.2, 0.0954],
        [1.25, 0.0924],
        [1.3, 0.0892],
        [1.35, 0.0865],
        [1.4, 0.0832],
        [1.45, 0.0801],
        [1.5, 0.0768],
        [1.55, 0.0732],
        [1.6, 0.0698],
        [1.65, 0.664],
        [1.7, 0.0632],
        [1.75, 0.0605],
        [1.8, 0.0569],
        [1.85, 0.054],
        [1.9, 0.0508],
        [1.95, 0.0476],
        [2, 0.0445],
        [2.05, 0.0413],
        [2.1, 0.038],
        [2.15, 0.0347],
        [2.2, 0.0313],
        [2.25, 0.0283],
        [2.3, 0.0254],
        [2.35, 0.0229],
        [2.4, 0.02],
        [2.45, 0.0175],
        [2.5, 0.015],
        [2.55, 0.013],
        [2.6, 0.01113],
        [2.65, 0.00953],
        [2.7, 0.00824],
        [2.75, 0.00717],
        [2.8, 0.00629],
        [2.85, 0.00555],
        [2.9, 0.00490],
        [2.95, 0.00436],
        [3, 0.00393],
        [3.05, 0.00354],
        [3.1, 0.00323],
        [3.15, 0.00297],
        [3.2, 0.00277],
        [3.25, 0.00259],
        [3.3, 0.00244],
        [3.35, 0.00231],
        [3.4, 0.00219],
        [3.45, 0.00205],
        [3.5, 0.00196],
        [3.55, 0.00187],
        [3.6, 0.00177],
        [3.65, 0.00169],
        [3.7, 0.00163],
        [3.75, 0.00157],
        [3.8, 0.00151],
        [3.85, 0.00147],
        [3.9, 0.00141],
        [3.95, 0.00137],
        [4, 0.00132],
        [4.05, 0.00126],
        [4.1, 0.00120],
        [4.15, 0.00116],
        [4.2, 0.00111],
        [4.25, 0.00106],
        [4.5, 0.00088],
        [4.75, 0.00076],
        [5, 0.00069],
        [5.5, 0.00061],
        [6, 0.00052],
        [7, 0.00031],
        [8, 0.000],
    ]
)

z_positions = [z1, z2, z3]
knife_edge_data = [
    dataz1,
    dataz2,
    dataz3
]  # Each datazi is a tuple (positions, power_measurements)

waists = []

for z, data in zip(z_positions, knife_edge_data):
    positions = data[:, 0]
    power_measurements = data[:, 1]

    # Initial guess for the fit parameters: [P0, r0, w, Poffset]
    initial_guess = [
        max(power_measurements),
        np.median(positions),
        1.0,
        min(power_measurements),
    ]

    # Fit the knife-edge data to the model
    popt, _ = curve_fit(
        knife_edge_model, positions, power_measurements, p0=initial_guess
    )

    # Extract the beam waist (w) at this z position
    P0, r0, w, Poffset = popt
    waists.append(w)

    # Optionally, plot the fit for each z position
    plt.figure()
    plt.scatter(positions, power_measurements, label="Measured data")
    fit_x = np.linspace(min(positions), max(positions), 1000)
    fit_y = knife_edge_model(fit_x, *popt)
    plt.plot(fit_x, fit_y, label=f"Fitted curve at z = {z}", color="red")
    plt.xlabel("Knife edge position")
    plt.ylabel("Power")
    plt.legend()
    plt.title(f"Knife-edge Measurement at z = {z}")
    plt.show()

print(f"Waist measurements at positions {z_positions}: {waists}")


# Define the theoretical beam waist model
def beam_waist(z, w0, z0, zr):
    return w0 * np.sqrt(1 + ((z - z0) / zr) ** 2)


# Convert z_positions and waists to numpy arrays
z_positions = np.array(z_positions)
waists = np.array(waists)

# Initial guess for the beam waist fit parameters: [w0, z0, zr]
initial_guess = [min(waists), np.mean(z_positions), max(z_positions) - min(z_positions)]

# Fit the waist data to the theoretical model
popt, pcov = curve_fit(beam_waist, z_positions, waists, p0=initial_guess)

# Extract the fitted parameters
w0, z0, zr = popt
print(f"Fitted parameters:\n w0: {w0}\n z0: {z0}\n zr: {zr}")

# Plot the waist data and the fitted curve
plt.scatter(z_positions, waists, label="Measured waists")
z_fit = np.linspace(min(z_positions), max(z_positions), 1000)
waist_fit = beam_waist(z_fit, w0, z0, zr)
plt.plot(z_fit, waist_fit, label="Fitted curve", color="red")
plt.xlabel("z")
plt.ylabel("Beam waist")
plt.legend()
plt.title("Beam Waist Fitting")
plt.show()
