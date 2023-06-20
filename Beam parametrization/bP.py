import numpy as np
from scipy.special import erfc
from scipy.optimize import curve_fit, fsolve
import math
import matplotlib.pyplot as plt

#
# fileName = "./Beam_params.txt"
# Or use commandline arguments with fileName = sys.argv[1]...
# data1 = np.loadtxt(fileName)
# Load the data
data1 = np.array(
    [
        [0, 1.716],
        [1.35, 1.606],
        [1.55, 1.508],
        [1.68, 1.403],
        [1.75, 1.300],
        [1.86, 1.198],
        [1.98, 1.099],
        [1.99, 0.999],
        [2.05, 0.901],
        [2.11, 0.802],
        [2.17, 0.701],
        [2.23, 0.600],
        [2.30, 0.500],
        [2.355, 0.420],
        [2.375, 0.398],
        [2.46, 0.301],
        [2.59, 0.199],
        [2.81, 0.099],
        [2.94, 0.069],
        [3.975, 0.006],
    ]
)

data2 = np.array(
    [
        [0, 1.725],
        [2.68, 1.600],
        [2.85, 1.499],
        [2.95, 1.401],
        [3.06, 1.301],
        [3.14, 1.201],
        [3.22, 1.101],
        [3.30, 1.000],
        [3.37, 0.901],
        [3.44, 0.801],
        [3.51, 0.701],
        [3.58, 0.600],
        [3.65, 0.498],
        [3.74, 0.401],
        [3.84, 0.299],
        [3.96, 0.200],
        [4.15, 0.101],
        [4.39, 0.049],
        [5.07, 0.010],
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
z1 = 6.6 + 19.5
z2 = z1 + 62.7
z1 /= 100
z2 /= 100

# Print the optimized parameters
perr1 = np.sqrt(np.diag(pcov1))
np.set_printoptions(precision=3, suppress=False)
print(
    f"Optimized parameters for z2: P0={popt1[0]} +/- {perr1[0]}, r0={popt1[1]} +/- {perr1[1]}, w={popt1[2]} +/- {perr1[2]}, Poffset={popt1[3]} +/- {perr1[3]}"
)
perr2 = np.sqrt(np.diag(pcov2))
print(
    f"Optimized parameters for z2: P0={popt2[0]} +/- {perr2[0]}, r0={popt2[1]} +/- {perr2[1]}, w={popt2[2]} +/- {perr2[2]}, Poffset={popt2[3]} +/- {perr2[3]}"
)

# Plot the data and the fitted function
plt.plot(data1.T[0], data1.T[1], "r-", label="Knife edge profile at z1 = 0.261 m")
x = np.linspace(0, 5.5, 5500)
plt.plot(
    x,
    func(x, *popt1),
    "g:",
    label="Fit of z1 = 0.261 m data to erfc(x); x = (r - r0) / (w / np.sqrt(2))",
)

plt.plot(data2.T[0], data2.T[1], "b-", label="Knife edge profile at z2 = 0.888 m")
plt.plot(
    x,
    func(x, *popt2),
    "y:",
    label="Fit of z2 = 0.888 m data to erfc(x); x = (r - r0) / (w / np.sqrt(2))",
)
plt.xlabel("x [mm]")
plt.ylabel("P [mW]")
plt.legend()


wavelength = 775e-9

z1 = 261e-3
w1 = round(popt1[2], 5)

z2 = 888e-3
w2 = round(popt2[2], 5)


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
