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
z1 = 145e-3
data1 = np.array(
    [
        [0, 1.86],
        [2.43, 1.85],
        [2.54, 1.84],
        [2.58, 1.83],
        [2.62, 1.82],
        [2.65, 1.81],
        [2.68, 1.80],
        [2.71, 1.79],
        [2.735, 1.77],
        [2.755, 1.75],
        [2.8, 1.73],
        [2.85, 1.7],
        [2.9, 1.65],
        [2.95, 1.6],
        [3.0, 1.53],
        [3.05, 1.46],
        [3.1, 1.38],
        [3.15, 1.28],
        [3.2, 1.19],
        [3.25, 1.08],
        [3.3, 0.97],
        [3.35, 0.87],
        [3.4, 0.76],
        [3.45, 0.66],
        [3.5, 0.55],
        [3.55, 0.46],
        [3.6, 0.38],
        [3.65, 0.314],
        [3.7, 0.252],
        [3.75, 0.201],
        [3.8, 0.159],
        [3.85, 0.128],
        [3.9, 0.0998],
        [3.95, 0.077],
        [4.0, 0.0573],
        [4.05, 0.0419],
        [4.1, 0.0307],
        [4.15, 0.0215],
        [4.2, 0.015],
        [4.25, 0.0109],
        [4.3, 0.0076],
        [4.35, 0.0057],
        [4.4, 0.00470],
        [4.45, 0.00396],
        [4.5, 0.00336],
        [4.55, 0.00309],
        [4.6, 0.00288],
        [4.65, 0.00273],
        [4.7, 0.00260],
        [4.75, 0.00251],
        [4.8, 0.00243],
        [4.85, 0.00235],
        [4.9, 0.00226],
        [4.95, 0.00220],
    ]
)
z2 = 345e-3
data2 = np.array(
    [
        [0.0, 1.866],
        [0.05, 1.865],
        [0.10, 1.864],
        [4.11, 1.882],
        [4.5, 1.778],
        [5.0, 1.276],
        [5.05, 1.045],
        [5.1, 0.880],
        [5.15, 0.730],
        [5.2, 0.590],
        [5.25, 0.473],
        [5.3, 0.365],
        [5.35, 0.273],
        [5.4, 0.193],
        [5.45, 0.136],
        [5.5, 0.096],
        [5.55, 0.060],
        [5.6, 0.038],
        [5.65, 0.025],
        [5.7, 0.0018],
        [5.85, 0.00052],
        [6.05, 0.000314],
        [8.3, 0.0001],
        [10.50, 0.00024],
    ]
)


# Define your function
def func(r, P0, r0, w, Poffset):
    return P0 / 2 * (1 - erfc((r - r0) / (w / np.sqrt(2)))) + Poffset


# This part needs to be calculated in mm and mW, because otherwise it doesn't converge. It can also be
# scaled up, but not down
# Perform the curve fitting
popt1, pcov1 = curve_fit(func, data1.T[0], data1.T[1])
popt2, pcov2 = curve_fit(func, data2.T[0], data2.T[1])

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
lambda780 = 780e-9

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
