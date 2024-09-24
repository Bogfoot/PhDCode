import numpy as np

data = {
    (0, 22.5): {"A+/B+": 10633, "A+/B-": 2018, "A-/B+": 1335, "A-/B-": 10377},
    (45, 22.5): {"A+/B+": 1726, "A+/B-": 13649, "A-/B+": 7075, "A-/B-": 2436},
    (45, 67.5): {"A+/B+": 1688, "A+/B-": 13940, "A-/B+": 8642, "A-/B-": 724},
    (0, 67.5): {"A+/B+": 2616, "A+/B-": 11373, "A-/B+": 7825, "A-/B-": 2528},
}


# Function to calculate E(A, B) for a given set of counts
def calculate_correlation(counts):
    N_pp = counts["A+/B+"]
    N_pm = counts["A+/B-"]
    N_mp = counts["A-/B+"]
    N_mm = counts["A-/B-"]

    numerator = (N_pp + N_mm) - (N_pm + N_mp)
    denominator = N_pp + N_mm + N_pm + N_mp

    return numerator / denominator if denominator != 0 else 0


# Calculate correlations for each angle pair
correlations = {
    angles: calculate_correlation(counts) for angles, counts in data.items()
}
print(correlations)

# Define sign based on the CHSH inequality formula
angle_pairs = [
    (0, 22.5),  # E(0, 22.5)
    (0, 67.5),  # E(0, 67.5)
    (45, 22.5),  # E(45, 22.5)
    (45, 67.5),  # E(45, 67.5)
]
# Corresponding to E(A,B) - E(A,B') + E(A',B) + E(A',B')
signs = [1, -1, -1, -1]

# Calculate S
S = 0
for i, pair in enumerate(angle_pairs):
    S += signs[i] * correlations[pair]
print(f"S = {S}")
