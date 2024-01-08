import numpy as np
import matplotlib.pyplot as plt

def youngs_experiment_2d(wavelength, slit_width, distance_to_screen, screen_width, num_slits=2):
    """
    Simulate Young's experiment in 2D and plot the interference pattern.

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
    wavelength = wavelength * 1e-9
    slit_width = slit_width * 1e-6
    distance_to_screen = distance_to_screen * 0.01
    screen_width = screen_width * 0.01

    # Constants
    k = 2 * np.pi / wavelength  # Wave number

    # Create a grid of points on the screen
    screen_points_x = np.linspace(-screen_width / 2, screen_width / 2, 1000)
    screen_points_y = np.linspace(-screen_width / 2, screen_width / 2, 1000)

    # Create a meshgrid for 2D positions
    screen_x, screen_y = np.meshgrid(screen_points_x, screen_points_y)

    # Calculate intensity at each point on the screen
    intensity = np.zeros_like(screen_x)

    for m in range(-num_slits + 1, num_slits):
        # Calculate the position of each slit
        slit_position = m * slit_width

        # Calculate the electric field contribution from each slit
        field = np.cos(k * (np.sqrt((screen_x - slit_position)**2 + screen_y**2)))

        # Add the contribution to the total intensity
        intensity += field ** 2

    # Normalize the intensity
    intensity /= intensity.max()

    # Plot the interference pattern in 2D
    plt.figure(figsize=(10, 6))
    plt.imshow(intensity, extent=[-screen_width / 2, screen_width / 2, -screen_width / 2, screen_width / 2], origin='lower', cmap='hot', aspect='auto')
    plt.colorbar(label='Intensity')
    plt.title("Young's Experiment Interference Pattern (2D)")
    plt.xlabel('Position on Screen (meters)')
    plt.ylabel('Position on Screen (meters)')
    plt.show()

# Example usage
youngs_experiment_2d(wavelength=650, slit_width=0.03, distance_to_screen=100, screen_width=0.002, num_slits=2)
