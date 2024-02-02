import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit, fsolve
from scipy.special import erfc

#
# fileName = "./Beam_params.txt"
# Or use commandline arguments with fileName = sys.argv[1]...
# data1 = np.loadtxt(fileName)
# Load the data
z1 = 145
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
        [5, 0.00211],
        [5.05, 0.00206],
        [5.1, 0.00197],
        [5.15, 0.00191],
        [5.2, 0.00185],
        [5.25, 0.00178],
        [5.3, 0.00172],
        [5.35, 0.00166],
        [5.4, 0.00161],
        [5.45, 0.00157],
        [5.5, 0.00150],
        [5.55, 0.00145],
        [5.6, 0.00140],
        [5.65, 0.00137],
        [5.7, 0.00131],
        [5.75, 0.00127],
        [5.8, 0.00124],
        [5.85, 0.00120],
        [5.9, 0.00116],
        [5.95, 0.00112],
        [6, 0.00108],
        [6.05, 0.00104],
        [6.1, 0.00101],
        [6.15, 0.00097],
        [6.2, 0.00094],
        [6.25, 0.00091],
        [6.3, 0.00088],
        [6.35, 0.00084],
        [6.40, 0.00082],
        [6.45, 0.00079],
        [6.5, 0.00075],
        [6.55, 0.00072],
        [6.6, 0.00069],
        [6.65, 0.00067],
        [6.7, 0.00064],
        [6.75, 0.00061],
        [6.8, 0.00059],
        [6.85, 0.00057],
        [6.95, 0.00053],
        [7, 0.0005],
        [7.05, 0.00048],
        [7.1, 0.00047],
        [7.15, 0.00045],
        [7.2, 0.00043],
        [7.25, 0.00042],
        [9.0, 0.00018],
    ]
)
z2 = 345
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


# function to be fitted: P0/2*erfc(x) + Poffset; x = (r - r0) / (w / np.sqrt(2))
def func(r, P0, r0, w, Poffset):
    return P0 / 2 * erfc((r - r0) / (w / np.sqrt(2))) + Poffset


# Fit the data to the function
popt1, pcov1 = curve_fit(func, data1.T[0], data1.T[1])
# ,p0 = [estimates of ws], sigma= [uncertainties of Y - In this case we would need to redo the measurements at z1 for the same
# x position of the knife edge to see the uncertainties in power]
# ) # Same for the 2nd fit below.
popt2, pcov2 = curve_fit(func, data2.T[0], data2.T[1])

# Print the optimized parameters
perr1 = np.sqrt(np.diag(pcov1))
np.set_printoptions(precision=3, suppress=False)
print(
    f"Optimized parameters for z1: P0={popt1[0]} +/- {perr1[0]}, r0={popt1[1]} +/- {perr1[1]}, w={popt1[2]} +/- {perr1[2]}, Poffset={popt1[3]} +/- {perr1[3]}"
)
perr2 = np.sqrt(np.diag(pcov2))
print(
    f"Optimized parameters for z2: P0={popt2[0]} +/- {perr2[0]}, r0={popt2[1]} +/- {perr2[1]}, w={popt2[2]} +/- {perr2[2]}, Poffset={popt2[3]} +/- {perr2[3]}"
)

# Plot the data and the fitted function
plt.plot(data1.T[0], data1.T[1], "r-", label=f"Knife edge profile at z1 = 0.{z1} m")
x = np.linspace(0, 5.5, 5500)
plt.plot(
    x,
    func(x, *popt1),
    "g:",
    label=f"Fit of z1 = 0.{z1} m data to erfc(x); x = (r - r0) / (w / np.sqrt(2))",
)

plt.plot(data2.T[0], data2.T[1], "b-", label=f"Knife edge profile at z2 = 0.{z2} m")
plt.plot(
    x,
    func(x, *popt2),
    "y:",
    label=f"Fit of z2 = 0.z2 m data to erfc(x); x = (r - r0) / (w / np.sqrt(2))",
)
plt.xlabel("x [mm]")
plt.ylabel("P [mW]")
plt.legend()


wavelength = 780e-9

z1 = z1
w1 = round(popt1[2], 4)

z2 = z2
w2 = round(popt2[2], 4)


def sys2(variables):
    w0, zwaist = variables
    eq1 = w1 - w(z1 - zwaist, w0, wavelength)
    eq2 = w2 - w(z2 - zwaist, w0, wavelength)
    return [eq1, eq2]


def w(z, w0, wavelength):
    return w0 * math.sqrt(1 + ((z * wavelength) / (math.pi * w0**2)) ** 2)


# Initial guess for the solution
initial_guess = [1e-4, 0]

# Solve the equations
solutions, info, ier, mesg = fsolve(sys2, initial_guess, full_output=True)

# Check if the solver converged successfully
if ier == 1:
    w0_solution, zwaist_solution = solutions
    print("Solution found:")
    print(f"w0 = {w0_solution}")
    print(f"zwaist = {zwaist_solution}")
else:
    print("Solver did not converge. Error message:", mesg)

plt.show()
