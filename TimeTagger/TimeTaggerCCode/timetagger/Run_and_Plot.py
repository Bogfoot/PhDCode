import re
import subprocess

import matplotlib.pyplot as plt


# Function to run hyperfine and extract mean time
def run_benchmark(command, warmup=5, runs=100):
    result = subprocess.run(
        ["hyperfine", "--warmup", str(warmup), "-r", str(runs), command],
        stdout=subprocess.PIPE,
        text=True,
    )

    output = result.stdout
    # Use regex to find the mean time from hyperfine output
    mean_time_match = re.search(r"Time \(mean ± σ\):\s+([\d.]+) ms", output)

    if mean_time_match:
        mean_time = float(mean_time_match.group(1))
        return mean_time
    else:
        raise ValueError("Couldn't extract the mean time from the output.")


# List of program versions and their respective commands
versions = {
    "SingleThreadedV1": "./FindCoincidences tags.csv 150",
    "SingleThreadedV2": "./FindCoincidencesV2 tags.csv 150",
    "MultithreadedV1": "./MultithreadedCoincidences tags.csv 150",
}
# Dictionary to store results
results = {}

# Run benchmark for each version
for version, command in versions.items():
    print(f"Running benchmark for {version}...")
    mean_time = run_benchmark(command)
    results[version] = mean_time
    print(f"{version}: {mean_time} ms")

# Plotting the results
plt.figure(figsize=(10, 6))
bars = plt.bar(results.keys(), results.values(), color=["blue", "orange", "green"])

# Add labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        f"{yval:.2f} ms",
        ha="center",
        va="bottom",
    )

plt.ylabel("Average Time (ms)")
plt.title("Benchmark Results for Program Versions")
plt.show()
