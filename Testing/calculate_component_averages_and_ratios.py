# Example usage:
# python3 calculate_component_averages_and_ratios.py /path/to/thing/ PBS

import os, sys
import numpy as np

parent_path = sys.argv[1]
component = sys.argv[2]

# Function to count the number of component folders
def count_same_name_folders(path, component):
    pbs_folders = [folder for folder in os.listdir(path) if folder.startswith(component) and os.path.isdir(os.path.join(path, folder))]
    return pbs_folders

# Function to calculate average of the 2nd column in a file
def get_file_sum(file_path):
    data = np.loadtxt(file_path, skiprows=5)  # Load data skipping the first 5 rows
    if data.size > 0:
        return np.sum(data[:, 1])  # Calculate sum of the 2nd column
    else:
        return 0

# Main function to calculate the averages for each PBS folder
def calculate_averages(path, component):
    pbs_folders = count_same_name_folders(path, component)
    ratios = []
    
    for pbs_folder in pbs_folders:
        total_h_sum = 0
        total_v_sum = 0
        total_h_count = 0
        total_v_count = 0
        
        for folder in ['H', 'V']:
            folder_path = os.path.join(path, pbs_folder, folder)
            if os.path.exists(folder_path):
                file_sum = 0
                file_count = 0
                # Loop through text files in H and V folders
                for filename in os.listdir(folder_path):
                    if filename.endswith('.txt'):
                        file_path = os.path.join(folder_path, filename)
                        file_avg = get_file_sum(file_path)
                        file_sum += file_avg
                        file_count += 1
                # Calculate average for H and V folders
                folder_avg = file_sum / file_count if file_count > 0 else 0
                if folder == 'H':
                    total_h_sum = folder_avg
                    total_h_count += 1
                elif folder == 'V':
                    total_v_sum = folder_avg
                    total_v_count += 1
        
        # Calculate average and ratio for each PBS folder
        avg_h = total_h_sum / total_h_count if total_h_count > 0 else 0
        avg_v = total_v_sum / total_v_count if total_v_count > 0 else 0
        ratio = avg_h / avg_v if avg_v != 0 else 0
        ratios.append(ratio)
        print(f'Average for {pbs_folder} - H: {avg_h}\t V: {avg_v}\t H/V Ratio: {ratio}')

    return ratios

# Plotting
import matplotlib.pyplot as plt

# Function to plot ratios as a histogram
def plot_ratios(ratios):
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, len(ratios) + 1), ratios, tick_label=[f'PBS{i}' for i in range(1, len(ratios) + 1)])
    plt.xlabel('PBS Folders')
    plt.ylabel('H/V Ratio')
    plt.title('H/V Ratios for PBS Folders')
    plt.xticks(rotation='vertical')
    plt.show()

ratios = calculate_averages(parent_path, component)
plot_ratios(ratios)
