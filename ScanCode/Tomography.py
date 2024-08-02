import numpy as np
import QuantumTomography as qLib

# Coincidence counts for 9 measurements.
# Each row is the coincidence counts for detector pairs 1 H1H2 (1/4),2 H1V2 (1/3),3 V1H2 (2/4), and 4 V1V2 (2/3) respectfully
# coincidence_counts = np.array(
#     [
#         [21885.6, 177.2, 99.6, 9957],
#         [9586.8, 202.6, 84.4, 4141],
#         [12591.6, 190.2, 84.8, 5945],
#         [8620.2, 145.6, 111, 3882.2],
#         [850.8, 162.6, 93.6, 1080.2],
#         [16495.8, 169.8, 103.8, 11933],
#         [11715.8, 156.4, 112.8, 5440.6],
#         [16751.2, 178.6, 106, 11743],
#         [2144.2, 164.4, 99.6, 1356.6],
#     ]
# )
#

coincidence_counts = np.array(
    [
        [21885, 177, 99, 9957],
        [9586, 202, 84, 4141],
        [12591, 190, 84, 5945],
        [8620, 145, 111, 3882],
        [850, 162, 93, 1080],
        [16495, 169, 103, 11933],
        [11715, 156, 112, 5440],
        [16751, 178, 106, 11743],
        [2144, 164, 99, 1356],
    ]
)
# Measurement basis for 9 measurements
# In each row the first two (possible complex) numbers alpha and beta represent the state that the first qubit
# is projected onto when it ends up at detector 1.
# The next two numbers is the state the second qubit is projected onto when it ends up at detector 2.
measurements = np.array(
    [
        [1 + 0j, 0j, 1 + 0j, 0j],
        [1 + 0j, 0j, 0.70710678 + 0j, 0.7071067811865476 + 0j],
        [1 + 0j, 0j, 0.70710678 + 0j, 0.70710678j],
        [0.70710678 + 0j, 0.70710678 + 0j, 1 + 0j, 0j],
        [0.70710678 + 0j, 0.70710678 + 0j, 0.70710678 + 0j, 0.70710678 + 0j],
        [0.70710678 + 0j, 0.70710678 + 0j, 0.70710678 + 0j, 0.70710678j],
        [0.70710678 + 0j, 0.70710678j, 1 + 0j, 0j],
        [0.70710678 + 0j, 0.70710678j, 0.70710678 + 0j, 0.70710678 + 0j],
        [0.70710678 + 0j, 0.70710678j, 0.70710678 + 0j, 0.7071067811865476j],
    ]
)

# Initiate tomography object
tomo_obj = qLib.Tomography()

# Run tomography
[rho_approx, intensity, fval] = tomo_obj.StateTomography(
    measurements, coincidence_counts
)
# Print Results
tomo_obj.printLastOutput()
print("----------------")
bell_state = 1 / np.sqrt(2) * np.array([1, 0, 0, 1], dtype=complex)
print("Fidelity with actual : " + str(qLib.fidelity(bell_state, rho_approx)))
