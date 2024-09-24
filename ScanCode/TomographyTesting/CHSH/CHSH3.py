from uncertainties import ufloat

# Updated data with uncertainties (errors are the square roots of the counts)
data = {
    (0, 22.5): {
        "A+/B+": ufloat(10633, 10633**0.5),
        "A+/B-": ufloat(2018, 2018**0.5),
        "A-/B+": ufloat(1335, 1335**0.5),
        "A-/B-": ufloat(10377, 10377**0.5),
    },
    (45, 22.5): {
        "A+/B+": ufloat(1726, 1726**0.5),
        "A+/B-": ufloat(13649, 13649**0.5),
        "A-/B+": ufloat(7075, 7075**0.5),
        "A-/B-": ufloat(2436, 2436**0.5),
    },
    (45, 67.5): {
        "A+/B+": ufloat(1688, 1688**0.5),
        "A+/B-": ufloat(13940, 13940**0.5),
        "A-/B+": ufloat(8642, 8642**0.5),
        "A-/B-": ufloat(724, 724**0.5),
    },
    (0, 67.5): {
        "A+/B+": ufloat(2616, 2616**0.5),
        "A+/B-": ufloat(11373, 11373**0.5),
        "A-/B+": ufloat(7825, 7825**0.5),
        "A-/B-": ufloat(2528, 2528**0.5),
    },
}


# Function to calculate E(A, B) for a given set of counts with uncertainties
def calculate_correlation_with_uncertainties(counts):
    N_pp = counts["A+/B+"]
    N_pm = counts["A+/B-"]
    N_mp = counts["A-/B+"]
    N_mm = counts["A-/B-"]

    numerator = (N_pp + N_mm) - (N_pm + N_mp)
    denominator = N_pp + N_mm + N_pm + N_mp

    return numerator / denominator if denominator != 0 else ufloat(0, 0)


# Calculate correlations with uncertainties for each angle pair
correlations_with_uncertainties = {
    angles: calculate_correlation_with_uncertainties(counts)
    for angles, counts in data.items()
}

# List of correlation signs for the CHSH formula
signs = [1, -1, -1, -1]

# List of the relevant angle pairs for the calculation
angle_pairs = [(0, 22.5), (0, 67.5), (45, 22.5), (45, 67.5)]

# Initialize S (CHSH parameter) as a ufloat for uncertainty propagation
S = ufloat(0, 0)

# Loop to calculate the CHSH parameter S, including uncertainties
for i, pair in enumerate(angle_pairs):
    S += signs[i] * correlations_with_uncertainties[pair]

# The resulting CHSH parameter S with propagated uncertainty
print(f"{S:1.6f}")
