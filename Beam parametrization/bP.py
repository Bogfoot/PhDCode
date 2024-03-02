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


# Define your function
def func(r, P0, r0, w, Poffset):
    return P0 / 2 * (1 - erfc((r - r0) / (w / np.sqrt(2)))) + Poffset


# Perform the curve fitting
popt, pcov = curve_fit(func, data2.T[0], data2.T[1])

# popt contains the optimized values for the parameters
P0_opt, r0_opt, w_opt, Poffset_opt = popt
print(P0_opt, w_opt, r0_opt, Poffset_opt)

# pcov contains the covariance matrix
# The diagonal elements of pcov are the variances for each parameter
# To get the standard deviation, take the square root of the diagonal elements
P0_std, r0_std, w_std, Poffset_std = np.sqrt(np.diag(pcov))
print(P0_std, w_std, r0_std, Poffset_std)
