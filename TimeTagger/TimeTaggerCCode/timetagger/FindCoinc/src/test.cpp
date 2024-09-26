#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <sstream>

// Structure to hold channel events
struct Event {
    int channel;
    long long timestamp;
};

// Function to read events from a file and extract only channel 1
std::vector<Event> readChannelFromFile(const std::string& filename, int channelToExtract) {
    std::vector<Event> events;
    std::ifstream inFile(filename);

    if (!inFile.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return events;
    }

	std::cout << filename << std::endl;
    std::string line;
	long long firstTimeStamp;
	bool isFirstTimeTag = true;
    while (std::getline(inFile, line)) {
        std::istringstream iss(line);
        int channel;
        long long timestamp;
		if (isFirstTimeTag){
			char comma; // To ignore the comma
			if (iss >> timestamp >> comma >> channel  && channel == channelToExtract && timestamp != 0) {

				firstTimeStamp = timestamp;
				events.push_back({channel, 0});
				isFirstTimeTag = false;
			}
		}

        // Assuming the file format is: channel_number, timestamp
        char comma; // To ignore the comma
        if (iss >> timestamp >> comma >> channel  && channel == channelToExtract && timestamp != 0) {
			timestamp -= firstTimeStamp;
            events.push_back({channel, timestamp});
        }
		// Debugging
		// std::cout << timestamp << std::endl;
    }

    inFile.close();
    return events;
}

// Function to find coincidences with a delay
int countCoincidencesWithDelay(const std::vector<Event>& channel1, const std::vector<Event>& channel2, long long delta, long long delay) {
    int coincidenceCount = 0;
    size_t i = 0, j = 0;

    while (i < channel1.size() && j < channel2.size()) {
        long long t1 = channel1[i].timestamp + delay;  // Apply the delay to channel1's timestamp
        long long t2 = channel2[j].timestamp;

        if (std::abs(t1 - t2) <= delta) {
            coincidenceCount++;
            ++i;
            ++j;
        } else if (t1 < t2) {
            ++i;
        } else {
            ++j;
        }
    }

	std::cout << "Coincidences between " << channel1[0].channel << " and " << channel2[0].channel << " for delay of " << delay << " are " << coincidenceCount << std::endl;
    return coincidenceCount;
}

// Function to write coincidences to a single line in the file
void findCoincidencesAndWrite(const std::string& outputFilename, const std::vector<Event>& channel1, const std::vector<Event>& channel2, long long delta, float delayStart, float delayEnd, float delayStep) {
    std::ofstream outFile(outputFilename);  // Open file for writing

    if (!outFile.is_open()) {
        std::cerr << "Error opening file for writing: " << outputFilename << std::endl;
        return;
    }

    // Iterate over the delay range and collect histogram data
    for (float delayNs = delayStart; delayNs <= delayEnd; delayNs += delayStep) {
        long long delayPs = static_cast<long long>(delayNs * 1000);  // Convert delay from ns to ps
        int coincidences = countCoincidencesWithDelay(channel1, channel2, delta, delayPs);

        // Write delay and coincidence count on the same line, separated by commas
        outFile << delayNs << ',' << coincidences << std::endl;

        // Add a comma after each pair except the last one
    }
    outFile.close();  // Close the file after writing
    std::cout << "Coincidences written to " << outputFilename << std::endl;
}

int main(int argc, char *argv[]) {
    // Read the channel 1 events from both files

	std::string usage = "Usage <app> <filename_1> <channel> <filename_2> <channel> <coincidence_window in ps> <delayStart in ns> <delayEnd in ns> <delayStep in ns>" ;
	if(argc<7){
	std::cerr << usage << std::endl;
	return 1;
	}

	std::string filename_1 = argv[1];
    int channel1 = atoi(argv[2]);  // Time window in picoseconds for coincidences
	std::string filename_2 = argv[3];
    int channel2 = atoi(argv[4]);  // Time window in picoseconds for coincidences

    long long delta = atoll(argv[5]);  // Time window in picoseconds for coincidences
    float delayStart = atof(argv[6]);
    float delayEnd = atof(argv[7]);
    float delayStep = atof(argv[8]);


    std::vector<Event> channel1_11_03 = readChannelFromFile(filename_1, channel1);
    std::vector<Event> channel1_11_07 = readChannelFromFile(filename_2, channel2);


    // Write coincidences to an output file "coincidences_output.txt"
    findCoincidencesAndWrite("coincidences_output.txt", channel1_11_03, channel1_11_07, delta, delayStart, delayEnd, delayStep);

    return 0;
}
