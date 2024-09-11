import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
def load_data(file_path):
    # Assuming the first row is the header and using proper column names
    column_names = ['Time', 'S1', 'S2', 'S3', 'S4', 'C1/4', 'C1/3', 'C2/4', 'C2/3']
    data = pd.read_csv(file_path, names=column_names, skiprows=1)
    
    # Convert the 'Time' column to a datetime object
    data['Time'] = pd.to_datetime(data['Time'], format='%Y_%m_%d_%H_%M_%S')
    
    return data

# Plot the data (singles and coincidences)
def plot_data(data):
    plt.figure(figsize=(12, 8))

    # Subplot 1: Singles data (S1, S2, S3, S4)
    plt.subplot(2, 1, 1)
    plt.plot(data['Time'], data['S1'], label='S1')
    plt.plot(data['Time'], data['S2'], label='S2')
    plt.plot(data['Time'], data['S3'], label='S3')
    plt.plot(data['Time'], data['S4'], label='S4')
    plt.title('Singles over Time')
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.legend()

    # Subplot 2: Coincidences data (C1/4, C1/3, C2/4, C2/3)
    plt.subplot(2, 1, 2)
    plt.plot(data['Time'], data['C1/4'], label='C1/4')
    plt.plot(data['Time'], data['C1/3'], label='C1/3')
    plt.plot(data['Time'], data['C2/4'], label='C2/4')
    plt.plot(data['Time'], data['C2/3'], label='C2/3')
    plt.title('Coincidences over Time')
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main function to load and plot the data
if __name__ == '__main__':
    file_path = 'path_to_your_data_file.csv'  # Replace this with the actual path to your CSV file
    data = load_data(file_path)
    plot_data(data)
