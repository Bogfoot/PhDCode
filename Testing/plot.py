import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np

filename = sys.argv[1]
df = pd.read_csv(filename, header=None)
x = np.linspace(0, len(df), len(df))
plt.scatter(x, df)
plt.show()
