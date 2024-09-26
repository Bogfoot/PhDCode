#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <cmath>
#include <cstdlib>  // For std::atoll
#include <iomanip>  // For std::setprecision

struct Event {
    int channel;
    long long timestamp;
};

// Function to read data from a CSV file
std::pair<std::vector<Event>, int> readCSV(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<Event> events;
    std::string line;
    int validTimestampCount = 0;  // Count of non-zero timestamps

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string channelStr, timestampStr;
        std::getline(ss, channelStr, ',');
        std::getline(ss, timestampStr, ',');

        int channel = std::stoi(channelStr);
        long long timestamp = std::stoll(timestampStr);

        if (channel >= 1 && channel <= 8) {  // Only consider valid channel numbers
            if (timestamp != 0) {  // Only store non-zero timestamps
                events.push_back({channel, timestamp});
                validTimestampCount++;  // Increment count for non-zero timestamps
            }
        }
    }

    return {events, validTimestampCount};  // Return both events and count
}

// Function to find coincidences between two channels with a time window (delta)
// It also applies a delay (in picoseconds) to one of the channels before finding coincidences.
int countCoincidencesWithDelay(const std::vector<Event>& channel1, const std::vector<Event>& channel2, long long delta, long long delay) {
    int coincidenceCount = 0;
    size_t i = 0, j = 0;

    while (i < channel1.size() && j < channel2.size()) {
        long long t1 = channel1[i].timestamp - delay;  // Apply the delay to channel1's timestamp
        long long t2 = channel2[j].timestamp;

        if (std::abs(t1 - t2) <= delta) {
            coincidenceCount++;  // Found a coincidence
            ++i;  // Move to the next event in channel1
        } else if (t1 < t2) {
            ++i;  // Move to the next event in channel1
        } else {
            ++j;  // Move to the next event in channel2
        }
    }

    return coincidenceCount;
}

// Function to create a histogram of coincidences for a range of delay values
void createCoincidenceHistogram(const std::vector<Event>& channel1, const std::vector<Event>& channel2, long long delta, float delayStart, float delayEnd, float delayStep) {
    // Iterate over the delay range

	std::ofstream outFile("output.txt");  // Open or create a file named "output.txt"

	// Check if the file is open
	if (!outFile.is_open()) {
		std::cerr << "Error opening file!" << std::endl;
		return;  // Return error code if file couldn't be opened
	}

    for (float delayNs = delayStart; delayNs <= delayEnd; delayNs += delayStep) {
        long long delayPs = static_cast<long long>(delayNs * 1000);  // Convert delay from nanoseconds to picoseconds
        int coincidences = countCoincidencesWithDelay(channel1, channel2, delta, delayPs);

        // Print the delay and the number of coincidences
        std::cout << "Delay: " << std::fixed << std::setprecision(2) << delayNs << " ns (" << delayPs << " ps) -> Coincidences: " << coincidences << '\n';

		// Write some text to the file
		outFile << delayNs << ',' <<coincidences << std::endl;
    }

	// Close the file
	outFile.close();
}

int main(int argc, char* argv[]) {
    // Check if enough arguments are passed
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <csv_file> <delta> <delay_start> <delay_end> <delay_step>\n";
        return 1;
    }

    // Read command-line arguments
    std::string filename = argv[1];
    long long delta = std::atoll(argv[2]);  // Convert delta to long long (in picoseconds)
    float delayStart = std::atof(argv[3]);  // Delay start in nanoseconds
    float delayEnd = std::atof(argv[4]);    // Delay end in nanoseconds
    float delayStep = std::atof(argv[5]);   // Delay step in nanoseconds

    // Read CSV data
    auto [events, validTimestampCount] = readCSV(filename);

    // Separate events by channel
    std::map<int, std::vector<Event>> channels;
    for (const Event& event : events) {
        channels[event.channel].push_back(event);
    }

    // Output the count of valid timestamps
    std::cout << "Number of valid timestamps (non-zero): " << validTimestampCount << '\n';

    // Check if both channels have data
    if (channels.find(1) != channels.end() && channels.find(2) != channels.end()) {
        // Create a histogram of coincidences for different delay values between Channel 1 and Channel 2
        createCoincidenceHistogram(channels[1], channels[2], delta, delayStart, delayEnd, delayStep);
    } else {
        std::cerr << "Channels 1 or 2 do not have sufficient data.\n";
    }

    return 0;
}
