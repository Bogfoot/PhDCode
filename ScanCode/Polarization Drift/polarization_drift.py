import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_name = "polarization_drift.csv"
df = pd.read_csv(file_name)

# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Get the column names
columns = df.columns
last_two_columns = columns[-2:]
first_columns = columns[1:-2]  # Exclude 'Date' and the last two columns

# Set the style and color palette
sns.set(style="whitegrid")
colors = sns.color_palette("husl", len(first_columns) + len(last_two_columns))

# Create a new figure with two side-by-side subplots
fig, axs = plt.subplots(1, 2, figsize=(16, 8), sharex=True)

# Set a large title for the entire figure
fig.suptitle("Polarization Drift Trends", fontsize=22, fontweight='bold', ha='center')

# Plot the first set of columns in the first subplot
for i, column in enumerate(first_columns):
    axs[0].plot(df['Date'].values, df[column].values, marker='o', linestyle='-', color=colors[i], label=column, linewidth=2)
axs[0].set_title("Singles", fontsize=16, fontweight='bold')
axs[0].set_ylabel("Values", fontsize=14)
axs[0].legend(loc='upper left', fontsize=12)
axs[0].grid(True, linestyle='--', alpha=0.7)
axs[0].tick_params(axis='both', which='major', labelsize=12)
axs[0].tick_params(axis='x', rotation=45)  # Rotate x-axis ticks for the first subplot

# Plot the last two columns in the second subplot
for i, column in enumerate(last_two_columns, start=len(first_columns)):
    axs[1].plot(df['Date'].values, df[column].values, marker='s', linestyle='-', color=colors[i], label=column, linewidth=2)
axs[1].set_title("Coincidences", fontsize=16, fontweight='bold')
axs[1].set_ylabel("Values", fontsize=14)
axs[1].legend(loc='upper left', fontsize=12)
axs[1].grid(True, linestyle='--', alpha=0.7)
axs[1].tick_params(axis='both', which='major', labelsize=12)
axs[1].tick_params(axis='x', rotation=45)  # Rotate x-axis ticks for the second subplot

# Add common xlabel
plt.xlabel("Date", fontsize=14)

# Adjust layout to fit the title and plots
plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # Adjust to make space for the suptitle

# Save the plot with a transparent background
plt.savefig("polarization_drift_plot.jpeg", format='jpeg', transparent=True, bbox_inches='tight')

# Show plot
plt.show()
