import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import erfc


# Define the error function model for the knife-edge measurement
def knife_edge_model(x, P0, r0, w, Poffset):
    return (P0 / 2) * erfc((x - r0) / (w / np.sqrt(2))) + Poffset


z1 = 310e-3
dataz1 = np.array(
    [
        [0, 2.555],
        [3.5, 2.540],
        [3.75, 2.420],
        [4, 2.261],
        [4.25, 2.085],
        [4.5, 1.855],
        [4.75, 1.614],
        [5, 1.361],
        [5.25, 1.099],
        [5.5, 0.865],
        [5.75, 0.647],
        [6, 0.437],
        [6.25, 0.266],
        [6.5, 0.159],
        [6.75, 0.0961],
        [7, 0.0617],
        [7.25, 0.0433],
        [7.5, 0.0323],
        [7.75, 0.0223],
        [8, 0.0162],
        [8.25, 0.0111],
        [8.5, 0.0081],
        [8.76, 0.00623],
        [9, 0.00495],
        [9.25, 0.00424],
        [9.5, 0.00361],
        [10, 0.00269],
        [10.5, 0.00179],
        [11, 0.0006],
        [11.5, 0.00015],
        [12, 0.00004],
        [12.5, 0.00001],
    ]
)

z2 = 485e-3
dataz2 = np.array(
    [
        [0, 2.567],
        [4.9, 2.545],
        [5, 2.515],
        [5.25, 2.393],
        [5.5, 2.230],
        [5.75, 2.036],
        [6, 1.806],
        [6.25, 1.555],
        [6.5, 1.313],
        [6.75, 1.070],
        [7, 0.85],
        [7.25, 0.652],
        [7.5, 0.444],
        [7.75, 0.275],
        [8, 0.159],
        [8.25, 0.0933],
        [8.5, 0.0598],
        [8.75, 0.0424],
        [9, 0.0317],
        [9.25, 0.0241],
        [9.5, 0.0175],
        [9.75, 0.0125],
        [10, 0.0088],
        [10.25, 0.0068],
        [10.5, 0.0055],
        [10.75, 0.0045],
        [11, 0.0039],
        [11.25, 0.0034],
        [11.5, 0.0028],
        [11.75, 0.0025],
        [12, 0.0022],
        [12.25, 0.0016],
        [12.5, 0.0009],
        [13, 0.0002],
        [13.5, 0.00005],
    ]
)

z3 = 1040e-3
dataz3 = np.array(
    [
        [0, 2.566],
        [0.95, 2.550],
        [1, 2.540],
        [1.25, 2.448],
        [1.5, 2.303],
        [1.75, 2.111],
        [2, 1.908],
        [2.25, 1.675],
        [2.5, 1.447],
        [2.75, 1.211],
        [3, 1.008],
        [3.25, 0.810],
        [3.5, 0.622],
        [3.75, 0.446],
        [4, 0.303],
        [4.25, 0.172],
        [4.5, 0.091],
        [4.75, 0.0494],
        [5, 0.0343],
        [5.25, 0.027],
        [5.5, 0.0223],
        [5.75, 0.019],
        [6, 0.015],
        [6.25, 0.011],
        [6.5, 0.0085],
        [6.75, 0.0069],
        [7, 0.0061],
        [7.25, 0.0056],
        [7.5, 0.0052],
        [7.75, 0.0047],
        [8, 0.0043],
        [8.25, 0.0038],
        [8.5, 0.0034],
        [9, 0.0027],
        [9.5, 0.0015],
        [10, 0.0009],
        [10.5, 0.0008],
        [11, 0.0007],
        [12, 0.0002],
    ]
)

z_positions = [z1, z2, z3]
knife_edge_data = [
    dataz1,
    dataz2,
    dataz3,
]  # Each datazi is a tuple (positions, power_measurements)

waists = []


def fit_knife_edge(data, z):
    x_data = data[:, 0]
    p_data = data[:, 1]

    # Initial guess for the parameters
    initial_guess = [np.max(p_data), np.mean(x_data), 1.0, np.min(p_data)]

    # Perform the curve fit
    popt, _ = curve_fit(knife_edge_model, x_data, p_data, p0=initial_guess)

    # Extract the beam waist
    waist = popt[2]

    return x_data, p_data, knife_edge_model(x_data, *popt), z, waist, popt


# Fit the knife-edge data for each z position
fit_results1 = fit_knife_edge(dataz1, z1)
fit_results2 = fit_knife_edge(dataz2, z2)
fit_results3 = fit_knife_edge(dataz3, z3)

# Extract the z positions and corresponding waists
z_positions = np.array([fit_results1[3], fit_results2[3], fit_results3[3]])
waists = np.array([fit_results1[4], fit_results2[4], fit_results3[4]])
print(f"The waists are { fit_results1[4] }, { fit_results2[4] } , { fit_results3[4] }.")

# Plot the knife-edge fits on the same plot
plt.figure()
plt.plot(fit_results1[0], fit_results1[1], "ro", label=f"Measured Data at z = {z1}")
plt.plot(fit_results1[0], fit_results1[2], "r-", label=f"Fit at z = {z1}")
plt.plot(fit_results2[0], fit_results2[1], "go", label=f"Measured Data at z = {z2}")
plt.plot(fit_results2[0], fit_results2[2], "g-", label=f"Fit at z = {z2}")
plt.plot(fit_results3[0], fit_results3[1], "bo", label=f"Measured Data at z = {z3}")
plt.plot(fit_results3[0], fit_results3[2], "b-", label=f"Fit at z = {z3}")
plt.xlabel("Knife edge position [mm]")
plt.ylabel("Power [mW]")
plt.title("Knife-edge Measurements and Fits")
plt.legend()
plt.show()


# Define the theoretical beam waist model
def beam_waist(z, w0, z0, zr):
    return w0 * np.sqrt(1 + ((z - z0) / zr) ** 2)


# Convert z_positions and waists to numpy arrays
waists = np.array(waists)

# Check if we have at least as many data points as parameters
print(f"z positions are: { z_positions }")
if len(z_positions) < 3:
    raise ValueError(
        "Not enough data points to fit the model. Need at least 3 data points."
    )

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
plt.xlabel("z [m]")
plt.ylabel("Beam waist [mm]")
plt.legend()
plt.title("Beam Waist Fitting")
plt.show()
