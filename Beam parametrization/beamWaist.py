from scipy.optimize import fsolve
import math

wavelength = 775e-9

z1 = 261e-3
w1 = 0.815309e-3

z2 = 888e-3
w2 = 0.952767e-3


def sys2(variables):
    w0, zwaist = variables
    eq1 = w1 - w(z1 - zwaist, w0, wavelength)
    eq2 = w2 - w(z2 - zwaist, w0, wavelength)
    return [eq1, eq2]


def w(z, w0, wavelength):
    return w0 * math.sqrt(1 + ((z * wavelength) / (math.pi * w0**2)) ** 2)


# Initial guess for the solution
initial_guess = [1e-3, 0]

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
