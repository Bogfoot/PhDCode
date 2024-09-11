import numpy as np
from scipy.linalg import kron


# Define the matrices for the quarter-waveplate and half-waveplate
def quarter_waveplate(phi):
    return np.array([[1, 0], [0, np.exp(1j * phi)]])


def half_waveplate(theta):
    return np.array([[np.cos(theta), np.sin(theta)], [np.sin(theta), -np.cos(theta)]])


# Define the states
def horiz(theta):
    return np.dot(
        np.dot(quarter_waveplate(np.pi / 4), half_waveplate(theta)),
        quarter_waveplate(np.pi / 4),
    ).dot(np.array([[1], [0]]))


def vert(theta):
    return np.dot(
        np.dot(quarter_waveplate(np.pi / 4), half_waveplate(theta)),
        quarter_waveplate(np.pi / 4),
    ).dot(np.array([[0], [1]]))


# Define the projector
def projector(state):
    return np.dot(state, state.T.conj())


# Generate results for different values of theta
thetas = np.linspace(0, 2 * np.pi, 32)  # 32 values of theta between 0 and 2*pi
results = []
print(horiz(0))
for theta in thetas:
    state = (
        kron(horiz(theta), horiz(theta)) + kron(vert(theta), vert(theta))
    ) / np.sqrt(2)
    proj = projector(state)
    real_part = np.real(proj)
    imag_part = np.imag(proj)
    results.append((real_part, imag_part))

# Print or output results (show first pair as example)
for i, (real, imag) in enumerate(results[:2]):  # show the first two
    print(f"Theta {thetas[i]}:")
    print("Real part:")
    print(real)
    print("Imaginary part:")
    print(imag)
    print("\n")
