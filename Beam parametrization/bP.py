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

z1 = 310e-3
data1 = np.array(
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
data2 = np.array(
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
        [8, 0.85],
        [8.25, 0.652],
        [8.5, 0.444],
        [8.75, 0.275],
        [9, 0.159],
        [9.25, 0.0933],
        [9.5, 0.0598],
        [9.75, 0.0424],
        [10, 0.0317],
        [10.25, 0.0241],
        [10.5, 0.0175],
        [10.75, 0.0125],
        [11, 0.0088],
        [11.25, 0.0068],
        [11.5, 0.0055],
        [11.75, 0.0045],
        [12, 0.0039],
        [12.25, 0.0034],
        [12.5, 0.0028],
        [12.75, 0.0025],
        [13, 0.0022],
        [13.25, 0.0016],
        [13.5, 0.0009],
        [14, 0.0002],
        [14.5, 0.00005],
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
