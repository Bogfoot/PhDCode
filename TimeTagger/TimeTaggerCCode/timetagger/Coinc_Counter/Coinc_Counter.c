#include "Coinc_Counter.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to coincidence histograms
int64_t determineCoincidenceHistogram(Event events[], int64_t valid,
                                      int64_t ch1, int64_t ch2, double dt,
                                      double T1, double T2, int64_t *hist,
                                      int64_t histlen) {
  double baseunit = 1e-12;
  double baseF = 1 / baseunit;
  // Had to change this due to compiler shenanigance
  int64_t mul = dt * baseF;
  int64_t T1int, T2int, maxt1, mmod, Tmin1, Tmin2, Tmax1, Tmax2, maxDelayInt,
      dtInt = round(mul), DTint;
  int64_t i, j, t1, t2, m;

  if (dtInt <= 0) {
    printf("ERROR: dt has to be positive.\n");
    return -1;
  }
  if ((ch1 < 0) || (ch2 < 0) || (ch1 > 4) || (ch2 > 4)) {
    printf("ERROR: please supply proper channel numbers - exiting\n");
    return -2;
  }

  if (valid < 2) {
    printf("ERROR: if valid is not at least 2, you'll never get "
           "coincidences...\n");
    return -3;
  }

  if (histlen < 1) {
    printf("ERROR: If you discover how to make a histogram using %ld bins, let "
           "me know. Bye.",
           histlen);
    return -4;
  }

  if (T1 < 0 || T2 < 0 || T2 < T1) {
    printf(
        "ERROR: T1 and T2 should be positive, and we should have T2 > T1.\n");
    return -5;
  }

  // Had to change this due to compiler shenanigance
  mul = T1 * baseF;
  T1int = round(mul);
  mul = T2 * baseF;
  T2int = round(mul);
  free(mul);
  maxDelayInt = T2int - T1int;
  DTint = maxDelayInt / histlen;

  // Initialize the histogram array
  for (i = 0; i < histlen; i++) {
    hist[i] = 0;
  }
  Tmax1 = LONG_MIN;
  Tmax2 = Tmax1;
  Tmin1 = LONG_MAX;
  Tmin2 = Tmin1;

  // First, go through all events and check the min and max times to see what to
  // use as upper limit for t1
  for (i = 0; i < valid; i++) {
    if (events[i].channel == ch1) {
      if (events[i].timestamp < Tmin1) {
        Tmin1 = events[i].timestamp;
      } else if (events[i].timestamp > Tmax1) {
        Tmax1 = events[i].timestamp;
      }
    } else if (events[i].channel == ch2) {
      if (events[i].timestamp < Tmin2) {
        Tmin2 = events[i].timestamp;
      } else if (events[i].timestamp > Tmax2) {
        Tmax2 = events[i].timestamp;
      }
    }
  }
  maxt1 = Tmax2 - maxDelayInt;

  // Loop through events to determine coincidences and fill the histogram
  for (i = 0; i < valid; i++) {
    if (events[i].channel != ch1) {
      continue;
    }
    if (i % (valid / 100) == 0) {
      // printf("progress: %f\n", 100.0 * (((double)i) / ((double)valid)));
    }
    for (j = i; j < valid; j++) {
      if (events[j].channel != ch2) {
        continue;
      }
      t1 = events[i].timestamp;
      t2 = events[j].timestamp;
      if (t2 - t1 > maxDelayInt || t1 > maxt1) {
        break;
      }

      if (t2 - t1 > T1int) {
        m = (t2 - t1 - T1int) / DTint;
        mmod = (t2 - t1 - T1int) % DTint;
        if (m < histlen && t2 - t1 - T1int && mmod < dtInt) {
          hist[m]++;
          // printf("hist[m]: %ld\n", hist[m]);
        }
      }
    }
    if (t1 > maxt1) {
      break;
    }
  }
  printf("INFO: concluding histogram function\n");

  return 0; // No error
}
// Function to determine coincidences
int64_t determineCoincidences(Event events[], int64_t valid, int64_t ch1,
                              int64_t ch2, double dt, double T, double maxT) {
  double baseunit = 1e-12, baseF = 1 / baseunit;
  int64_t Tmax1, Tmax2, Tmin1, Tmin2, maxt1;
  int64_t maxDelayInt = round(baseF * maxT);
  int64_t Tint = round(baseF * T);
  int64_t dtInt = round(baseF * dt);
  int64_t cs, i, j, t1, t2;

  if ((ch1 < 0L) || (ch2 < 0L) || (ch1 > 4L) || (ch2 > 4L)) {
    printf("please supply proper channel numbers - exiting\n");
    return -2L;
  }

  if (valid < 2L) {
    printf("if valid is not at least 2, you'll never get coincidences...\n");
    return -3L;
  }

  cs = 0L;
  Tmax1 = LONG_MIN;
  Tmax2 = Tmax1;
  Tmin1 = LONG_MAX;
  Tmin2 = Tmin1;

  for (i = 0L; i < valid; i++) {
    if (events[i].channel == ch1) {
      if (events[i].timestamp < Tmin1) {
        Tmin1 = events[i].timestamp;
      }
      if (events[i].timestamp > Tmax1) {
        Tmax1 = events[i].timestamp;
      }
    }
    if (events[i].channel == ch2) {
      if (events[i].timestamp < Tmin2) {
        Tmin2 = events[i].timestamp;
      }
      if (events[i].timestamp > Tmax2) {
        Tmax2 = events[i].timestamp;
      }
    }
  }
  maxt1 = Tmax2 - maxDelayInt;
  // printf("Tmax1: %ld, Tmax2: %ld, maxt1: %ld\n", Tmax1, Tmax2, maxt1);
  t1 = 0;
  t2 = 0;

  for (i = 0; i < valid; i++) {
    if (events[i].channel != ch1) {
      continue;
    }
    for (j = i; j < valid; j++) {
      if (events[j].channel != ch2) {
        continue;
      }
      t1 = events[i].timestamp;
      t2 = events[j].timestamp;
      if (t2 - t1 > maxDelayInt || t1 > maxt1) {
        break;
      }
      if (abs(t2 - t1 - Tint) < dtInt) {
        cs++;
        // printf("Found a hit.\n");
      }
    }
    if (t1 > maxt1) {
      break;
    }
  }

  return cs;
}

int64_t determineCoincidencesWithBlocks(Event events[], int64_t valid,
                                        int64_t ch1, int64_t ch2, int64_t n,
                                        double dt, double T) {
  double baseunit = 1e-12, baseF = 1 / baseunit;
  int64_t Tint = round(baseF * T);
  int64_t dtInt = round(baseF * dt);
  int64_t cs, i, j, t1, t2;

  if ((ch1 < 0) || (ch2 < 0) || (ch1 > 8) || (ch2 > 8)) {
    printf("please supply proper channel numbers - exiting\n");
    return -1;
  }

  if (n < 2) {
    n = valid;
    return -2;
  }

  if (valid < 2) {
    printf("if valid is not at least 2, you'll never get coincidences...\n");
    return -3;
  }

  printf("everything seems to be fine\n");
  cs = 0;

  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      if (events[i].channel == ch1) {
        if (events[j].channel == ch2) {
          t1 = events[i].timestamp;
          t2 = events[j].timestamp;
        } else {
          continue;
        }
      } else if (events[i].channel == ch2) {
        if (events[j].channel == ch1) {
          t1 = events[j].timestamp;
          t2 = events[i].timestamp;
        } else {
          continue;
        }
      } else {
        continue;
      }
      if (abs(Tint + t2 - t1) < dtInt) {
        cs++;
      }
    }
  }

  return cs;
}

// Function to split events into separate arrays based on channel numbers
void splitEventsByChannel(Event events[], int size, Event **channel1,
                          int *channel1Size, Event **channel2,
                          int *channel2Size) {
  // Count occurrences of channel 1 events
  int countChannel1 = 0;
  for (int i = 0; i < size; i++) {
    if (events[i].channel == 1) {
      countChannel1++;
    }
  }

  // Calculate size of channel 2 array
  int countChannel2 = size - countChannel1;

  // Allocate memory for channel 1 and channel 2 arrays
  *channel1 = (Event *)malloc(countChannel1 * sizeof(Event));
  *channel2 = (Event *)malloc(countChannel2 * sizeof(Event));

  // Initialize sizes of channel 1 and channel 2 arrays
  *channel1Size = 0;
  *channel2Size = 0;

  // Populate channel 1 and channel 2 arrays
  for (int i = 0; i < size; i++) {
    if (events[i].channel == 1) {
      (*channel1)[(*channel1Size)++] = events[i];
    } else {
      (*channel2)[(*channel2Size)++] = events[i];
    }
  }
}

// Function to count coincidences between channel 1 and channel 2 events
int countCoincidences(Event channel1[], int size1, Event channel2[], int size2,
                      long long coincidanceWindow) {
  int count = 0;
  for (int i = 0; i < size1; i++) {
    for (int j = 0; j < size2; j++) {
      if (abs(channel1[i].timestamp - channel2[j].timestamp) <=
          coincidanceWindow) {
        count++;
      } else {
        break; // Break the inner loop if time difference exceeds threshold
      }
    }
  }
  return count;
}
