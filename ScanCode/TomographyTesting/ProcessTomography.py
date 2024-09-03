import pandas as pd

# Load the CSV file
dir_name = "Data/Tomography/"
file_path = "../Data/Tomography/DataForTomography_2024-08-22_10_45_35.csv"  # Replace with your actual file path
data = pd.read_csv(file_path)

# Calculate the average for each data column for each combination of angles
averaged_data = data.groupby(["angle", "other_angle"]).mean().reset_index()

# Drop the measurement_number column as it is not needed for the averages
averaged_data = averaged_data.drop(columns=["# measurement_number"])

output_file_path = f"Data/Tomography/Processed_Tomography_Data_{file_path[-23:-4]}.csv"  # Replace with your desired output file path
averaged_data.to_csv(output_file_path, index=False)

# Display the results
print("Averaged data has been saved to:", output_file_path)
# Display the results
print(averaged_data)
