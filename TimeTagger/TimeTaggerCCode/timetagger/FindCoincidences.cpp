#include <cmath>
#include <cstdlib> // For std::atoll (converts string to long long)
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <vector>

// Structure to hold channel events
struct Event {
  int channel;
  long long timestamp;
};

// Function to read data from a CSV file
std::vector<Event> readCSV(const std::string &filename) {
  std::ifstream file(filename);
  std::vector<Event> events;
  std::string line;

  while (std::getline(file, line)) {
    std::stringstream ss(line);
    std::string channelStr, timestampStr;
    std::getline(ss, channelStr, ',');
    std::getline(ss, timestampStr, ',');

    int channel = std::stoi(channelStr);
    long long timestamp = std::stoll(timestampStr);

    if (channel >= 1 && channel <= 8) { // Only consider valid channel numbers
      events.push_back({channel, timestamp});
    }
  }
  return events;
}

// Function to find coincidences between two channels with a time window
// (coincidenceWindow)
std::vector<std::pair<Event, Event>>
findCoincidences(const std::vector<Event> &channel1,
                 const std::vector<Event> &channel2,
                 long long coincidenceWindow) {
  std::vector<std::pair<Event, Event>> coincidences;
  size_t i = 0, j = 0;

  while (i < channel1.size() && j < channel2.size()) {
    long long t1 = channel1[i].timestamp;
    long long t2 = channel2[j].timestamp;

    // Check if events are within coincidenceWindow time window
    if (std::abs(t1 - t2) <= coincidenceWindow) {
      coincidences.push_back({channel1[i], channel2[j]});
      ++i; // Move to the next event in channel1
    } else if (t1 < t2) {
      ++i; // Move to the next event in channel1
    } else {
      ++j; // Move to the next event in channel2
    }
  }

  return coincidences;
}

int main(int argc, char *argv[]) {
  // Check if enough arguments are passed
  if (argc < 3) {
    std::cerr << "Usage: " << argv[0] << " <csv_file> <coincidenceWindow>\n";
    return 1;
  }

  // Read command-line arguments
  std::string filename = argv[1];
  long long coincidenceWindow =
      std::atoll(argv[2]); // Convert coincidenceWindow to long long

  // Read CSV data
  std::vector<Event> events = readCSV(filename);

  // Separate events by channel
  std::map<int, std::vector<Event>> channels;
  for (const Event &event : events) {
    channels[event.channel].push_back(event);
  }

  // Find coincidences between channel 1 and channel 2
  if (channels.find(1) != channels.end() &&
      channels.find(2) != channels.end()) {
    std::vector<std::pair<Event, Event>> coincidences =
        findCoincidences(channels[1], channels[2], coincidenceWindow);

    // Output the number of coincidences
    std::cout << "Number of coincidences between Channel 1 and Channel 2: "
              << coincidences.size() << '\n';

    // Optional: Output details of coincidences
    for (const auto &pair : coincidences) {
      std::cout << "Channel 1 Event: " << pair.first.timestamp
                << " , Channel 2 Event: " << pair.second.timestamp << '\n';
    }
  } else {
    std::cout << "Not enough data in channels 1 and 2.\n";
  }

  return 0;
}
