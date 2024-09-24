import numpy as np

# Provided data
data = {
    (0, 22.5): {"A+/B+": 10633, "A+/B-": 2018, "A-/B+": 1335, "A-/B-": 10377},
    (45, 22.5): {"A+/B+": 1726, "A+/B-": 13649, "A-/B+": 7075, "A-/B-": 2436},
    (45, 67.5): {"A+/B+": 1688, "A+/B-": 13940, "A-/B+": 8642, "A-/B-": 724},
    (0, 67.5): {"A+/B+": 2616, "A+/B-": 11373, "A-/B+": 7825, "A-/B-": 2528}
}

# Convert data into a matrix of counts
counts = np.array([
    [data[(0, 22.5)]["A+/B+"], data[(0, 22.5)]["A+/B-"], data[(0, 22.5)]["A-/B+"], data[(0, 22.5)]["A-/B-"]],
    [data[(45, 22.5)]["A+/B+"], data[(45, 22.5)]["A+/B-"], data[(45, 22.5)]["A-/B+"], data[(45, 22.5)]["A-/B-"]],
    [data[(45, 67.5)]["A+/B+"], data[(45, 67.5)]["A+/B-"], data[(45, 67.5)]["A-/B+"], data[(45, 67.5)]["A-/B-"]],
    [data[(0, 67.5)]["A+/B+"], data[(0, 67.5)]["A+/B-"], data[(0, 67.5)]["A-/B+"], data[(0, 67.5)]["A-/B-"]]
])

# Function to calculate the binary trace
def binary_trace(n):
    return sum(int(digit) for digit in bin(n)[2:])

# Pre-exp values calculation
preexpvals = np.zeros((4, 4))
for row in range(4):
    for column in range(4):
        column_bin_trace = binary_trace(column)  # Equivalent to Tr[IntegerDigits[column - 1, 2]] in Mathematica
        numerator = (-1)**column_bin_trace * counts[row, column]
        denominator = sum(counts[row, :])
        preexpvals[row, column] = numerator / denominator

# Exp values calculation
expvals = np.sum(preexpvals, axis=1)

# S calculation
S = expvals[0] - expvals[1] - expvals[2] - expvals[3]

# Final result
result = S / (2 * np.sqrt(2))

print("Preexpvals:", preexpvals)
print("Expvals:", expvals)
print("S:", S)
print("Result:", result)
