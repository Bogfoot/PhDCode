#ifndef __COINC_COUNTER_H
#define __COINC_COUNTER_H

#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <unistd.h>

// Structure to store data
typedef struct {
  int channel;
  long long timestamp; // Using long long to accommodate large timestamps
} Event;

int64_t countCoincidences(Event events[], int size, long long threshold,
                          char *unit);

int64_t determineCoincidences(Event events[], int64_t valid, int64_t ch1,
                              int64_t ch2, double dt, double T, double maxT);

int64_t determineCoincidenceHistogram(Event events[], int64_t valid,
                                      int64_t ch1, int64_t ch2, double dt,
                                      double T1, double T2, int64_t *hist,
                                      int64_t histlen);

#endif
