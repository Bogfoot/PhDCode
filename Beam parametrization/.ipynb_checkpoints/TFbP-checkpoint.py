
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def func(r, P0, r0, w, Poffset):
    return P0/2 * tf.math.erfc((r - r0)/(w/tf.sqrt(2))) + Poffset

def custom_loss(y_true, y_pred):
    residuals = y_true - y_pred
    return tf.reduce_mean(tf.square(residuals))

# Load the data
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

# define initial parameter values and bounds
initial_params = [1.5, 2, 0.1, 0.5]
bounds = ([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf])

# define the optimizer
optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

# define the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(4, activation='linear'),
])

# compile the model
model.compile(optimizer=optimizer, loss=custom_loss)

# train the model
model.fit(data1[:,0], data1[:,1], epochs=500)

# extract the optimized parameters
P0, r0, w, Poffset = model.get_weights()[0]

# print the optimized parameters
print(f'P0={P0:.3f}, r0={r0:.3f}, w={w:.3f}, Poffset={Poffset:.3f}')

# plot the original data
plt.plot(data1[:,0], data1[:,1], 'bo', label='Data')

# generate the fitted curve
r_vals = np.linspace(0, 4, 100)
y_vals = func(r_vals, P0, r0, w, Poffset)

# plot the fitted curve
plt.plot(r_vals, y_vals, 'r-', label='Fit')

# add axis labels and a legend
plt.xlabel('r')
plt.ylabel('P(r)')
plt.legend()

# display the plot
plt.show()
