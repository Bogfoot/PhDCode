#include "Coinc_Counter.h"
// #include <Python.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to count coincidences
int64_t countCoincidences(Event events[], int size, long long threshold,
                          char *unit) {
  int64_t factor = 1;

  // Convert the unit to picoseconds
  switch (unit[0]) {
  case 'ns':
    factor = 1000;
    break;
  case 'us':
    factor = 1000000;
    break;
  case 'ms':
    factor = 1000000000;
    break;
  case 's':
    factor = 1000000000000;
    break;
  default:
    factor = 1;
  }

  threshold *= factor;

  int64_t count = 0;

  for (int i = 0; i < size; i++) {
    for (int j = i + 1; j < size; j++) {
      if (labs(events[i].timestamp - events[j].timestamp) <= threshold) {
        count++;
      }
    }
  }

  return count;
}

int64_t determineCoincidenceHistogram(Event events[], int64_t valid,
                                      int64_t ch1, int64_t ch2, double dt,
                                      double T1, double T2, int64_t *hist,
                                      int64_t histlen) {
  double baseunit = 1e-12;
  double baseF = 1 / baseunit;
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

  mul = T1 * baseF;
  T1int = round(mul);
  mul = T2 * baseF;
  T2int = round(mul);
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
      printf("progress: %f\n", 100.0 * (((double)i) / ((double)valid)));
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
