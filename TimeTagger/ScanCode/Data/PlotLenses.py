import matplotlib.pyplot as plt
import numpy as np

# Data
lens = [175, 200, 250, 300]
S1 = [60, 45, 50, 41]
S2 = [50, 36, 36, 36]
Coinc = [250, 200, 130, 150]
Coinc_sqrt = [4.564355, 4.96904, 3.064129, 3.904344]

# Set the bar width
bar_width = 0.2

# Set position of bar on X axis
r1 = np.arange(len(lens))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

# Plotting
plt.bar(r1, S1, color="b", width=bar_width, edgecolor="grey", label="S1/kHz")
plt.bar(r2, S2, color="g", width=bar_width, edgecolor="grey", label="S2/kHz")
plt.bar(r3, Coinc, color="r", width=bar_width, edgecolor="grey", label="Coinc/Hz")
plt.bar(
    r4,
    Coinc_sqrt,
    color="y",
    width=bar_width,
    edgecolor="grey",
    label="Coinc/sqrt(S1*S2) x1000",
)

# Adding labels and title
plt.xlabel("Lens", fontweight="bold")
plt.xticks([r + bar_width for r in range(len(lens))], lens)
plt.ylabel("Values")
plt.title("Values vs. Lens")
plt.legend()

# Show plot
plt.show()
