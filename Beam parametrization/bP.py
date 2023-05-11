import numpy as np
from scipy.special import erfc
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


# Define the function to be fitted
def func(r, P0, r0, w, Poffset):
    return P0 / 2 * erfc((r - r0) / (w / np.sqrt(2))) + Poffset


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
x = data1.T[0]
y = data1.T[1]

# Fit the data to the function
popt1, pcov1 = curve_fit(func, data1.T[0], data1.T[1])
popt2, pcov2 = curve_fit(func, data2.T[0], data2.T[1])

# Print the optimized parameters
print("Optimized parameters: P0=%g, r0=%g, w=%g, Poffset=%g" % tuple(popt1))
print("Optimized parameters: P0=%g, r0=%g, w=%g, Poffset=%g" % tuple(popt2))

# Plot the data and the fitted function
plt.plot(x, y, "b-", label="data1")
plt.plot(x, func(x, *popt1), "r-", label="fit1")

plt.plot(data2.T[0], data2.T[1], "b:", label="data2")
plt.plot(x, func(x, *popt2), "r:", label="fit2")
plt.xlabel("x [mm]")
plt.ylabel("P [mW]")
plt.legend()
plt.show()
