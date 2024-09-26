#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>

// Structure to hold channel events
struct Event {
    int channel;
    long long timestamp;
};

// Function to read events from a file and extract only the specified channel
std::vector<Event> readChannelFromFile(const std::string& filename, int channelToExtract) {
    std::vector<Event> events;
    std::ifstream inFile(filename);

    if (!inFile.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return events;
    }

    std::string line;
    while (std::getline(inFile, line)) {
        std::istringstream iss(line);
        long long timestamp;
        int channel;

        // Assuming the file format is: timestamp, channel
        char comma; // To ignore the comma
        if (iss >> timestamp >> comma >> channel && channel == channelToExtract) {
            events.push_back({channel, timestamp});
        }
    }

    inFile.close();
    return events;
}

// Function to calculate singles counts per second (time bins)
std::map<long long, int> calculateSinglesPerSecond(const std::vector<Event>& events) {
    std::map<long long, int> singlesCount;

    for (const auto& event : events) {
        long long secondBin = event.timestamp / 1e12; // Convert picoseconds to seconds
        singlesCount[secondBin]++;
    }

    return singlesCount;
}

// Function to save singles counts to a file in the desired format
void saveSinglesCounts(const std::map<long long, int>& singlesCounts, const std::string& outputFilename) {
    std::ofstream outFile(outputFilename);

    if (!outFile.is_open()) {
        std::cerr << "Error opening file for writing: " << outputFilename << std::endl;
        return;
    }

    for (const auto& pair : singlesCounts) {
        outFile << pair.first << "," << pair.second << std::endl; // Save in the format "bin_n, count"
    }

    outFile.close();
    std::cout << "Singles counts saved to " << outputFilename << std::endl;
}

int main(int argc, char *argv[]) {
    std::string usage = "Usage <app> <filename> <channel> <output_file>";
    if (argc < 4) {
        std::cerr << usage << std::endl;
        return 1;
    }

    std::string filename = argv[1];
    int channel = atoi(argv[2]);
    std::string output_file = argv[3];

    // Read events for the specified channel
    std::vector<Event> events = readChannelFromFile(filename, channel);

    // Calculate singles counts per second
    std::map<long long, int> singlesCounts = calculateSinglesPerSecond(events);

    // Save the singles counts to the output file
    saveSinglesCounts(singlesCounts, output_file);

    return 0;
}
