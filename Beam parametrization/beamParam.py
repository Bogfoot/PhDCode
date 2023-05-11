import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, integrate

z1 = 6.6 + 19.5
z2 = z1 + 62.7

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

x1 = data1.T[0]
y1 = data1.T[1]


# Fitting to model
# define a function that integrates or evaluates f depending on the Boolean flag func_integr
def cerf(x, a, b, c, func_integr=True):
    # type(x)
    # <class 'numpy.ndarray'>
    # type(a)
    # <class 'numpy.float64'>
    # type(b)
    # <class 'numpy.float64'>
    # type(c)
    # <class 'numpy.float64'>
    f = lambda x: a * np.exp(((-1) * (x - b) ** 2) / (2 * (c**2)))
    # flag is preset to True, so will return the integrated values
    if func_integr:
        return np.asarray([integrate.quad(f, i, np.inf)[0] for i in x])
    # unless the flag func_integr is set to False, then it will return the function values
    else:
        return f(x)


# provide reasonable start values...
index_ = int(len(x1) / 2)
start_p = [y1[0], x1[index_], y1[-1]]
# pars, pcov = optimize.curve_fit(cerf, x1, y1, y1[0], x1[9], False)
pars, cov = optimize.curve_fit(cerf, x1, y1, start_p)
print(pars)
# [1.61259825 2.08418308 0.41858526] data1
# [1.42648098 3.3929937  0.48120944] data2


# plot our results
plt.plot(x1, y1, "x", label="Data")
plt.plot(x1, cerf(x1, *pars), "-", label="fit")
plt.xlabel("x [m]")
plt.ylabel("P [W]")
plt.legend(loc="best")
plt.show()
