#ifndef __QUTAG_HISTOGRAM_H
#define __QUTAG_HISTOGRAM_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <limits.h>

#ifdef unix
#include "../inc/tdcbase.h"
#include "../inc/tdcdecl.h"
#include <unistd.h>
#define SLEEP(x) usleep(x*1000)
#else
/* windows.h for Sleep */
#include <windows.h>
#include "../inc\\tdcbase.h"
#include "../inc\\tdcdecl.h"
#define SLEEP(x) Sleep(x)
#endif

int determineCoincidencesStartBlock(Int64* tags, Int8* channels, int valid, int ch1, int ch2, int n, double dt, double T);
int determineCoincidenceBlock(Int64* tags, Int8* channels, int valid, int ch1, int ch2, int n1, int n2, double dt, double T);
Int64 determineCoincidences(Int64* tags, Int8* channels, Int64 valid, Int64 ch1, Int64 ch2, double dt, double T, double maxT);
Int64 determineCoincidenceHistogram180722(Int64* tags, Int8* channels, Int64 valid, Int64 ch1, Int64 ch2, Int64 n, double dt, double* T1out, double* T2out, Int64* hist, Int64 histlen);
Int64 determineCoincidenceHistogram(Int64* tags, Int8* channels, Int64 valid, Int64 ch1, Int64 ch2, double dt, double T1, double T2, Int64* hist, Int64 histlen);

#endif
