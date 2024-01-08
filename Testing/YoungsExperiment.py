import sys

import matplotlib.pyplot as plt
import numpy as np


def youngs_experiment(
    wavelength, slit_width, distance_to_screen, screen_width, num_slits=2
):
    """
    Simulate Young's experiment and plot the interference pattern.

    Parameters:
    - wavelength: Wavelength of the light in nanometers
    - slit_width: Width of each slit in micrometers
    - distance_to_screen: Distance from the slits to the screen in centimeters
    - screen_width: Width of the screen in centimeters
    - num_slits: Number of slits (default is 2)

    Returns:
    - None (plots the interference pattern)
    """

    # Convert units to meters
    wavelength = wavelength * 1e-9  # nm
    slit_width = slit_width * 1e-6  # nm
    distance_to_screen = distance_to_screen * 0.01
    screen_width = screen_width * 0.01

    # Constants
    k = 2 * np.pi / wavelength  # Wave number

    # Create a grid of points on the screen
    screen_points = np.linspace(-screen_width / 2, screen_width / 2, 1000)

    # Calculate intensity at each point on the screen
    intensity = np.zeros_like(screen_points)

    for m in range(-num_slits + 1, num_slits):
        # Calculate the position of each slit
        slit_position = m * slit_width

        # Calculate the electric field contribution from each slit
        field = np.cos(k * (screen_points - slit_position))
        print(field)
    

        # Add the contribution to the total intensity
        intensity += field ** 2

    # Normalize the intensity
    intensity /= intensity.max()

    # Plot the interference pattern
    plt.figure(figsize=(10, 6))
    plt.plot(screen_points, intensity, label="Interference Pattern")
    plt.title("Young's Experiment Interference Pattern")
    plt.xlabel("Position on Screen (meters)")
    plt.ylabel("Intensity")
    plt.legend()
    plt.show()


# Example usage
# Check if there are enough command-line arguments
if len(sys.argv) == 6:
    # Extract command-line arguments
    wavelength = float(sys.argv[1])
    slit_width = float(sys.argv[2])
    distance_to_screen = float(sys.argv[3])
    screen_width = float(sys.argv[4])
    num_slits = int(sys.argv[5])

    # Call the function with user-provided data
    youngs_experiment(
        wavelength, slit_width, distance_to_screen, screen_width, num_slits
    )
else:
    print(
        "Usage: python YoungsExperiment.py wavelength slit_width distance_to_screen screen_width num_slits"
    )
    print("Example: python script_name.py 780 0.01 0.1 0.0002 2")
    youngs_experiment(
        wavelength=780,
        slit_width=0.01,
        distance_to_screen=0.1,
        screen_width=0.0002,
        num_slits=2,
    )
