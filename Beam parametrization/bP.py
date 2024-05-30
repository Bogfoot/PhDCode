import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import erfc
from sympy import Eq, pi, solve, sqrt, symbols

#
# fileName = "./Beam_params.txt"
# Or use commandline arguments with fileName = sys.argv[1]...
# data1 = np.loadtxt(fileName)
# Load the data

z1 = 300e-3
z2 = 1021e-3

data1 = np.array(
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

data2 = np.array(
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
    ]
)


# Define your function
def func(r, P0, r0, w, Poffset):
    return P0 / 2 * (1 - erfc((r - r0) / (w / np.sqrt(2)))) + Poffset


# This part needs to be calculated in mm and mW, because otherwise it doesn't converge. It can also be
# scaled up, but not down
# Perform the curve fitting
popt1, pcov1 = curve_fit(func, data1.T[0], data1.T[1], maxfev=10000)
popt2, pcov2 = curve_fit(func, data2.T[0], data2.T[1], maxfev=10000)

# errP1 = data1.T[2]
# errP2 = data2.T[2]

# Get the optimized parameters
P0_opt1, r0_opt1, w_opt1, Poffset_opt1 = popt1
P0_opt2, r0_opt2, w_opt2, Poffset_opt2 = popt2
# Get the errors
P0_std1, r0_std1, w_std1, Poffset_std1 = np.sqrt(np.diag(pcov1))

P0_std2, r0_std2, w_std2, Poffset_std2 = np.sqrt(np.diag(pcov2))
print("The results for w1 and w2 will be in mm due to optimization reasons.")

# Comment above 'curve_fit' lines is why this is in mm, not in m
print(f"w1 = {abs(w_opt1)} +/- {w_std1} mm")
print(f"w2 = {abs(w_opt2)} +/- {w_std2} mm")

# Define symbols
w0, zwaist = symbols("w0 zwaist")

# Given values
lambda780 = 1550e-9

# Saling this back to meters gives pretty much the same result.
w1 = abs(round(w_opt1 / 1000, 10))
w2 = abs(round(w_opt2 / 1000, 10))


# Define function for beam waist width
def w(z, w0, _lambda):
    return w0 * sqrt(1 + ((z * _lambda) / (np.pi * w0**2)) ** 2)


# Define equations
eq1 = Eq(w1, w(z1 - zwaist, w0, lambda780))
eq2 = Eq(w2, w(z2 - zwaist, w0, lambda780))

# Solve the system of equations
solutions = solve((eq1, eq2), (w0, zwaist))
# Extract and format solutions
beam_waist_width = solutions[0][0]
beam_waist_position = solutions[0][1]
# Print formatted solutions
print("Beam waist (radius) is in um for readability.")
print(f"Beam Waist (w0): {beam_waist_width*10**6} um")
print(f"Beam Waist Position (z_waist): {beam_waist_position} m")

z_range = np.linspace(-0.3, 0.3, 1000)  # Range of z values for plotting

z, w0 = symbols("z w0")


# Define function for beam waist width
def w(z, w0):
    return w0 * sqrt(1 + ((lambda780 * z) / (pi * w0**2)) ** 2)


# Calculate beam waist width for the given range of z values
w_values = [w(z_value, beam_waist_width) for z_value in z_range]

# Plot the waist function
plt.plot(z_range, w_values, color="blue")
plt.xlabel("z (meters)")
plt.ylabel("Beam Waist Width (meters)")
plt.title("Beam Waist Width as a function of z")
plt.grid(True)

min_w = min(w_values)
min_index = w_values.index(min_w)
min_z = z_range[min_index]

plt.annotate(
    f"Minimum: {min_w*10**6:.2f} um at z = {min_z*1000:.2f} mm",
    xy=(min_z, min_w),
    xytext=(min_z, min_w),
    arrowprops=dict(facecolor="black", shrink=0.05),
)
plt.show()
