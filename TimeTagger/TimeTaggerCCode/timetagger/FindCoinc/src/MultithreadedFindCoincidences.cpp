#include <cmath>
#include <cstdlib> // For std::atoll
#include <fstream>
#include <future>
#include <iostream>
#include <map>
#include <mutex>
#include <sstream>
#include <thread>
#include <vector>

// Structure to hold channel events
struct Event {
  int channel;
  long long timestamp;
};

// Function to read data from a CSV file
std::pair<std::vector<Event>, int> readCSV(const std::string &filename) {
  std::ifstream file(filename);
  std::vector<Event> events;
  std::string line;
  int validTimestampCount = 0; // Count of non-zero timestamps

  while (std::getline(file, line)) {
    std::stringstream ss(line);
    std::string channelStr, timestampStr;
    std::getline(ss, channelStr, ',');
    std::getline(ss, timestampStr, ',');

    int channel = std::stoi(channelStr);
    long long timestamp = std::stoll(timestampStr);

    if (channel >= 1 && channel <= 8) { // Only consider valid channel numbers
      if (timestamp != 0) {             // Only store non-zero timestamps
        events.push_back({channel, timestamp});
        validTimestampCount++; // Increment count for non-zero timestamps
      }
    }
  }

  return {events, validTimestampCount}; // Return both events and count
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

// Thread function to find coincidences and store results
void threadFindCoincidences(const std::vector<Event> &channel1,
                            const std::vector<Event> &channel2,
                            long long coincidenceWindow,
                            std::vector<std::pair<Event, Event>> &coincidences,
                            std::mutex &mtx) {
  auto localCoincidences =
      findCoincidences(channel1, channel2, coincidenceWindow);

  // Lock and update the global coincidence list
  std::lock_guard<std::mutex> lock(mtx);
  coincidences.insert(coincidences.end(), localCoincidences.begin(),
                      localCoincidences.end());
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
  auto [events, validTimestampCount] = readCSV(filename);

  // Separate events by channel
  std::map<int, std::vector<Event>> channels;
  for (const Event &event : events) {
    channels[event.channel].push_back(event);
  }

  // Output the count of valid timestamps
  std::cout << "Number of valid timestamps (non-zero): " << validTimestampCount
            << '\n';

  // Vector to hold all coincidences across all channel pairs
  std::vector<std::pair<Event, Event>> coincidences;
  std::mutex mtx;

  // Vector of futures to handle threads
  std::vector<std::future<void>> futures;

  // Launch threads to find coincidences between each pair of channels (1-8)
  for (int ch1 = 1; ch1 <= 8; ++ch1) {
    for (int ch2 = ch1 + 1; ch2 <= 8; ++ch2) {
      // Only run the thread if both channels have data
      if (channels.find(ch1) != channels.end() &&
          channels.find(ch2) != channels.end()) {
        futures.push_back(std::async(std::launch::async, threadFindCoincidences,
                                     std::ref(channels[ch1]),
                                     std::ref(channels[ch2]), coincidenceWindow,
                                     std::ref(coincidences), std::ref(mtx)));
        std::cout << "Now doing coincidences for channels :" << ch1 << ", "
                  << ch2 << std::endl;
      }
    }
  }

  // Wait for all threads to finish
  for (auto &future : futures) {
    future.get();
  }

  // Output the total number of coincidences found
  std::cout << "Total number of coincidences across all channels: "
            << coincidences.size() << '\n';

  // Optional: Output details of coincidences (this can be commented out for
  // large datasets)
  for (const auto &pair : coincidences) {
    std::cout << "Channel 1 Event: " << pair.first.timestamp
              << " , Channel 2 Event: " << pair.second.timestamp << '\n';
  }

  return 0;
}
