import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from scipy.special import erfc


# Define the model function
def model_function(r, P0, r0, w, Poffset):
    return P0 / 2 * erfc((r - r0) / (w / np.sqrt(2))) + Poffset


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
x = data1[:, 0]
y = data1[:, 1]

# Create a TensorFlow model
model = tf.keras.Sequential([tf.keras.layers.Dense(units=4, input_shape=[1])])
model.add(keras.layers.Dense(units=1, activation="linear", input_shape=[1]))
model.add(keras.layers.Dense(units=64, activation="relu"))
model.add(keras.layers.Dense(units=64, activation="relu"))
model.add(keras.layers.Dense(units=1, activation="linear"))
# Compile the model with mean squared error as the loss function and Adam as the optimizer
model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=0.01))

# Define the inputs and outputs for the model
inputs = x.reshape(-1, 1)
outputs = y.reshape(-1, 1)

# Train the model for 100 epochs
history = model.fit(inputs, outputs, epochs=300)

# Extract the fitted parameters
weights = model.get_weights()[0]
print(weights)

# Generate predictions using the fitted model
y_pred = model.predict(inputs)

# Plot the data and the model predictions
plt.plot(x, y, "bo", label="Data")
plt.plot(x, y_pred, "r-", label="Model")
plt.xlabel("r")
plt.ylabel("P")
plt.legend()
plt.show()
model.summary()
