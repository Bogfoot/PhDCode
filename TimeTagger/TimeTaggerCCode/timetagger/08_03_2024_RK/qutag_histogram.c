#include "qutag_histogram.h"

/*
 * Function to determine the number of coincident events with the time window
 * dt for a given time delay T
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place. "valid" indicated the number of 'valid'
 * time tags in those two initial arrays. "ch1" and "ch2" indicate the numbers
 * of the channels we want to check for coincidences. "n" is an integer that
 * can be used to limit the number of entries in the tags and channels
 * arrays used for our analysis.
 *
 * dt and T are given in seconds
 *
 *
 * EXAMPLE for calling the function in python:
 * tt.coincLib.determineCoincidencesStartBlock(tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),valid,1,3,1000,10*1e-9,-1.099*1e-6)
 *
 *
 * */
int determineCoincidencesStartBlock(Int64 *tags, Int8 *channels, int valid,
                                    int ch1, int ch2, int n, double dt,
                                    double T) {
  double baseunit = 1e-12, baseF = 1 / baseunit;
  int Tint = round(baseF * T);
  int dtInt = round(baseF * dt);
  int cs, i, j, t1, t2;

  if ((ch1 < 0) || (ch2 < 0) || (ch1 > 4) || (ch2 > 4)) {
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
      if (channels[i] == ch1) {
        if (channels[j] == ch2) {
          t1 = tags[i];
          t2 = tags[j];
        } else {
          continue;
        }
      } else if (channels[i] == ch2) {
        if (channels[j] == ch1) {
          t1 = tags[j];
          t2 = tags[i];
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

/*
 * Function to determine the number of coincident events with the time window
 * dt for a given time delay T - it takes 'valid' number of samples in the
 * arrays provided, and then it analyze the samples from n1 to n2
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place. "ch1" and "ch2" indicate the numbers
 * of the channels we want to check for coincidences.
 *
 * dt and T are given in seconds
 *
 * EXAMPLE for calling the function in python:
 * tt.coincLib.determineCoincidenceBlock(tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),valid,1,3,1000,2000,10*1e-9,-1.099*1e-6)
 *
 * */
int determineCoincidenceBlock(Int64 *tags, Int8 *channels, int valid, int ch1,
                              int ch2, int n1, int n2, double dt, double T) {
  double baseunit = 1e-12, baseF = 1 / baseunit;
  int Tint = round(baseF * T);
  int dtInt = round(baseF * dt);
  int cs, i, j, t1, t2;

  if ((n2 < n1 + 2) || (n1 < 0) || (n2 > valid)) {
    printf("The indices n1 and n2 do not make sense. Get lost.\n");
    return -1;
  }

  if ((ch1 < 0) || (ch2 < 0) || (ch1 > 4) || (ch2 > 4)) {
    printf("please supply proper channel numbers - exiting\n");
    return -2;
  }

  if (valid < 2) {
    printf("if valid is not at least 2, you'll never get coincidences...\n");
    return -3;
  }

  cs = 0;

  for (i = n1; i <= n2; i++) {
    for (j = n1; j <= n2; j++) {
      if (channels[i] == ch1) {
        if (channels[j] == ch2) {
          t1 = tags[i];
          t2 = tags[j];
        } else {
          continue;
        }
      } else if (channels[i] == ch2) {
        if (channels[j] == ch1) {
          t1 = tags[j];
          t2 = tags[i];
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

/*
 * Function to determine the number of coincident events with the time window
 * dt for a given time delay T - it takes 'valid' number of samples in the
 * arrays provided, and then it analyzes ALL of them. For this, we divide
 * the array of samples into blocks of events of size "n", which we then
 * analyse. If the length "valid" is no integer multiple of "n", the "off"
 * events will be discarded.
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place. "ch1" and "ch2" indicate the numbers
 * of the channels we want to check for coincidences.
 *
 * dt and T are given in seconds
 *
 * EXAMPLE how to call this in python:
 *
 * tt.coincLib.determineCoincidences(tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),valid,1,3,1000,10*1e-9,5.449*1e-7)
 *
 * */
Int64 determineCoincidences(Int64 *tags, Int8 *channels, Int64 valid, Int64 ch1,
                            Int64 ch2, double dt, double T, double maxT) {
  double baseunit = 1e-12, baseF = 1 / baseunit;
  Int64 Tmax1, Tmax2, Tmin1, Tmin2, maxt1;
  Int64 maxDelayInt = round(baseF * maxT);
  Int64 Tint = round(baseF * T);
  Int64 dtInt = round(baseF * dt);
  Int64 cs, i, j, t1, t2;

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
    if (channels[i] == ch1) {
      if (tags[i] < Tmin1) {
        Tmin1 = tags[i];
      }
      if (tags[i] > Tmax1) {
        Tmax1 = tags[i];
      }
    }
    if (channels[i] == ch2) {
      if (tags[i] < Tmin2) {
        Tmin2 = tags[i];
      }
      if (tags[i] > Tmax2) {
        Tmax2 = tags[i];
      }
    }
  }
  maxt1 = Tmax2 - maxDelayInt;
  printf("Tmax1: %ld, Tmax2: %ld, maxt1: %ld\n", Tmax1, Tmax2, maxt1);
  t1 = 0;
  t2 = 0;

  for (i = 0; i < valid; i++) {
    if (channels[i] != ch1) {
      continue;
    }
    for (j = i; j < valid; j++) {
      if (channels[j] != ch2) {
        continue;
      }
      t1 = tags[i];
      t2 = tags[j];
      if (t2 - t1 > maxDelayInt || t1 > maxt1) {
        break;
      }
      if (abs(t2 - t1 - Tint) < dtInt) {
        cs++;
      }
    }
    if (t1 > maxt1) {
      break;
    }
  }

  return cs;
}

/*
 * Function to determine the number of coincident events with the time window
 * dt for a given time delay T within the time tags supplied to the function.
 * It takes a 'valid' number of samples in the
 * arrays provided, and then it analyzes ALL of them.
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place. "ch1" and "ch2" indicate the numbers
 * of the channels we want to check for coincidences.
 *
 * dt and T are given in seconds
 *
 *
 *
 * EXAMPLE how to call this in python:
 *
 * tt.coincLib.determineCoincidencesSimple(tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),valid,1,3,1000,10*1e-9)
 *
 * */
Int64 determineCoincidencesSimple(Int64 *tags, Int8 *channels, Int64 valid,
                                  Int64 ch1, Int64 ch2, double dt, double T) {
  double baseunit = 1e-12, baseF = 1 / baseunit, deltaT;
  Int64 Tmax1, Tmax2, Tmin1, Tmin2, maxt1;
  Int64 Tint = round(baseF * T);
  Int64 dtInt = round(baseF * dt);
  Int64 maxDelayInt = abs(Tint + dtInt);
  Int64 cs, i, j, t1, t2;

  if ((ch1 < 0L) || (ch2 < 0L) || (ch1 > 4L) || (ch2 > 4L)) {
    printf("please supply proper channel numbers - exiting\n");
    return -2L;
  }

  if (valid < 2L) {
    printf("if valid is not at least 2, you'll never get coincidences...\n");
    return -3L;
  }

  Tmax1 = LONG_MIN;
  Tmax2 = Tmax1;
  Tmin1 = LONG_MAX;
  Tmin2 = Tmin1;

  for (i = 0L; i < valid; i++) {
    if (channels[i] == ch1) {
      if (tags[i] < Tmin1) {
        Tmin1 = tags[i];
      }
      if (tags[i] > Tmax1) {
        Tmax1 = tags[i];
      }
    }
    if (channels[i] == ch2) {
      if (tags[i] < Tmin2) {
        Tmin2 = tags[i];
      }
      if (tags[i] > Tmax2) {
        Tmax2 = tags[i];
      }
    }
  }
  maxt1 = Tmax2 - Tint;
  deltaT = ((double)(Tmax2 - Tmin1)) * 1e-12;
  printf("time covered (seconds): %f", deltaT);
  printf("Tmax1: %ld, Tmax2: %ld, maxt1: %ld\n", Tmax1, Tmax2, maxt1);
  t1 = 0L;
  t2 = 0L;
  cs = 0L;
  // printf("valid: %ld\n", valid);

  if (Tint < 0) {
    for (i = 0; i < valid; i++) {
      if (channels[i] != ch1) {
        continue;
      }
      t1 = tags[i];
      if (t1 > maxt1) {
        break;
      }
      for (j = i; j < valid; j++) {
        if (channels[j] != ch2) {
          continue;
        }
        t2 = tags[j];
        if (t2 - t1 > maxDelayInt) {
          break;
        }
        if (abs(-t2 + t1 + Tint) < dtInt) {
          cs++;
          printf("%ld - %ld - %ld = %ld < %ld\n", t2, t1, Tint,
                 (long)(abs(t2 - t1 - Tint)), dtInt);
        }
      }
    }

  } else {

    for (i = 0; i < valid; i++) {
      if (channels[i] != ch1) {
        continue;
      }
      t1 = tags[i];
      if (t1 > maxt1) {
        break;
      }
      for (j = i; j < valid; j++) {
        if (channels[j] != ch2) {
          continue;
        }
        t2 = tags[j];
        if (t2 - t1 > maxDelayInt) {
          break;
        }
        if (abs(t2 - t1 - Tint) < dtInt) {
          cs++;
          printf("%ld - %ld - %ld = %ld < %ld\n", t2, t1, Tint,
                 (long)(abs(t2 - t1 - Tint)), dtInt);
        }
      }
    }
  }

  printf("coincidences (Hz): %f\n", ((double)cs) / deltaT);

  return cs;
}

/*
 * Function to count the signles in channel 'ch' in the time tags supplied to
 * the function. It takes a 'valid' number of samples in the arrays provided,
 * and then it analyzes ALL of them.
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place.
 *
 *
 * EXAMPLE how to call this in python:
 *
 * tt.coincLib.countSingles(tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),valid,1)
 *
 * */
Int64 countSingles(Int64 *tags, Int8 *channels, Int64 valid, Int64 ch) {
  double deltaT;
  Int64 Tmax, Tmin;
  Int64 s, i;

  if ((ch < 0L) || (ch > 4L)) {
    printf("please supply proper channel numbers - exiting\n");
    return -2L;
  }

  if (valid < 1L) {
    printf("if valid is not at least 1, you'll never get counts...\n");
    return -3L;
  }

  Tmax = LONG_MIN;
  Tmin = LONG_MAX;

  for (i = 0L; i < valid; i++) {
    if (channels[i] == ch) {
      if (tags[i] < Tmin) {
        Tmin = tags[i];
      }
      if (tags[i] > Tmax) {
        Tmax = tags[i];
      }
    }
  }
  deltaT = ((double)(Tmax - Tmin)) * 1e-12;
  printf("time covered (seconds): %f", deltaT);
  printf("Tmax: %ld, Tmin: %ld\n", Tmax, Tmin);
  s = 0L;
  printf("valid: %ld\n", valid);

  for (i = 0; i < valid; i++) {
    if (channels[i] == ch) {
      s++;
    }
  }
  printf("singles (Hz): %f\n", ((double)s) / deltaT);

  return s;
}

/*
 * Function to determine the number of coincident events with the time window
 * dt for a given time delay T within the time tags supplied to the function.
 * It takes a 'valid' number of samples in the
 * arrays provided, and then it analyzes ALL of them.
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place. "ch1" and "ch2" indicate the numbers
 * of the channels we want to check for coincidences.
 *
 * dt and T are given in seconds
 *
 *
 *
 * EXAMPLE how to call this in python:
 *
 * tt.coincLib.determineCoincidencesSimple(tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),valid,1,3,1000,10*1e-9)
 *
 * */
double determineCoincidencesSimpleHz(Int64 *tags, Int8 *channels, Int64 valid,
                                     Int64 ch1, Int64 ch2, double dt,
                                     double T) {
  double baseunit = 1e-12, baseF = 1 / baseunit, deltaT, csHz;
  Int64 Tmax1, Tmax2, Tmin1, Tmin2, maxt1;
  Int64 Tint = round(baseF * T);
  Int64 dtInt = round(baseF * dt);
  Int64 maxDelayInt = Tint + dtInt;
  Int64 cs, i, j, t1, t2;

  if ((ch1 < 0L) || (ch2 < 0L) || (ch1 > 4L) || (ch2 > 4L)) {
    printf("please supply proper channel numbers - exiting\n");
    return -2L;
  }

  if (valid < 2L) {
    printf("if valid is not at least 2, you'll never get coincidences...\n");
    return -3L;
  }

  Tmax1 = LONG_MIN;
  Tmax2 = Tmax1;
  Tmin1 = LONG_MAX;
  Tmin2 = Tmin1;

  for (i = 0L; i < valid; i++) {
    if (channels[i] == ch1) {
      if (tags[i] < Tmin1) {
        Tmin1 = tags[i];
      }
      if (tags[i] > Tmax1) {
        Tmax1 = tags[i];
      }
    }
    if (channels[i] == ch2) {
      if (tags[i] < Tmin2) {
        Tmin2 = tags[i];
      }
      if (tags[i] > Tmax2) {
        Tmax2 = tags[i];
      }
    }
  }
  maxt1 = Tmax2 - Tint;
  deltaT = ((double)(Tmax2 - Tmin1)) * 1e-12;
  printf("time covered (seconds): %f", deltaT);
  printf("Tmax1: %ld, Tmax2: %ld, maxt1: %ld\n", Tmax1, Tmax2, maxt1);
  t1 = 0L;
  t2 = 0L;
  cs = 0L;
  printf("valid: %ld\n", valid);

  for (i = 0; i < valid; i++) {
    if (channels[i] != ch1) {
      continue;
    }
    t1 = tags[i];
    if (t1 > maxt1) {
      break;
    }
    for (j = i; j < valid; j++) {
      if (channels[j] != ch2) {
        continue;
      }
      t2 = tags[j];
      if (t2 - t1 > maxDelayInt) {
        break;
      }
      if (abs(t2 - t1 - Tint) < dtInt) {
        cs++;
      }
    }
  }
  csHz = ((double)cs) / deltaT;
  printf("coincidences (Hz): %f\n", csHz);

  return csHz;
}

/*
 * Function to count the signles in channel 'ch' in the time tags supplied to
 * the function. It takes a 'valid' number of samples in the arrays provided,
 * and then it analyzes ALL of them.
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place.
 *
 *
 * EXAMPLE how to call this in python:
 *
 * tt.coincLib.countSingles(tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),valid,1)
 *
 * */
double countSinglesHz(Int64 *tags, Int8 *channels, Int64 valid, Int64 ch) {
  double deltaT, sHz;
  Int64 Tmax, Tmin;
  Int64 s, i;

  if ((ch < 0L) || (ch > 4L)) {
    printf("please supply proper channel numbers - exiting\n");
    return -2L;
  }

  if (valid < 1L) {
    printf("if valid is not at least 1, you'll never get counts...\n");
    return -3L;
  }

  Tmax = LONG_MIN;
  Tmin = LONG_MAX;

  for (i = 0L; i < valid; i++) {
    if (channels[i] == ch) {
      if (tags[i] < Tmin) {
        Tmin = tags[i];
      }
      if (tags[i] > Tmax) {
        Tmax = tags[i];
      }
    }
  }
  deltaT = ((double)(Tmax - Tmin)) * 1e-12;
  printf("time covered (seconds): %f", deltaT);
  printf("Tmax: %ld, Tmin: %ld\n", Tmax, Tmin);
  s = 0L;
  printf("valid: %ld\n", valid);

  for (i = 0; i < valid; i++) {
    if (channels[i] == ch) {
      s++;
    }
  }
  sHz = ((double)s) / deltaT;
  printf("singles (Hz): %f\n", sHz);

  return sHz;
}

/*
 * Function to determine a histogram of coincidences over a varying time
 * delay in steps of DT between "T1" and "T2", which are the minimum and
 * maximum recorded delays between events happening in "ch2" and "ch1", where
 * events in channel "ch1" must occur at the same time or earlier than events
 * in "ch2". The time span "T2-T1" is then  split into "histlen" bins to form
 * the histogram. "dt" is the coincidence window. All times are in seconds.
 * We only record coincidence events where events in "ch2" occur at the same
 * time or later than events in "ch1".
 *
 * The values of "T1" and "T2" are determined by analyzing the timetags
 * supplied by the user. The results will be written into the integer
 * references "T1out" and "T2out" in units of seconds.
 *
 * The histogram will be stored in the buffer pointed to by the
 * variable "hist" - it has have sufficient memory allocated beforehand
 * otherwise you'll most likely end up with a segmentation fault.
 *
 * For the coincidences, we consider the two channels "ch1" and "ch2".
 *
 * We analyse the time tags in blocks of "n" events. If the length "valid"
 * is no integer multiple of "n", the "off" events will be discarded.
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place. "ch1" and "ch2" indicate the numbers
 * of the channels we want to check for coincidences.
 *
 *
 * EXAMPLE how to call this in python:
 *
 *
 * */
Int64 determineCoincidenceHistogram180722(Int64 *tags, Int8 *channels,
                                          Int64 valid, Int64 ch1, Int64 ch2,
                                          Int64 n, double dt, double *T1out,
                                          double *T2out, Int64 *hist,
                                          Int64 histlen) {
  double baseunit = 1e-12, baseF = 1 / baseunit;
  Int64 T1int, T2int, Tmin1, Tmin2, Tmax1, Tmax2, maxDelayInt, DTint;
  Int64 dtInt = round(baseF * dt);
  Int64 i, j, t1, t2, n1, n2, m, mmod;

  if ((n < 2) || (n > valid)) {
    printf("The given block size n does not make sense. Get lost.\n");
    return -1;
  }

  if ((ch1 < 0) || (ch2 < 0) || (ch1 > 4) || (ch2 > 4)) {
    printf("please supply proper channel numbers - exiting\n");
    return -2;
  }

  if (valid < 2) {
    printf("if valid is not at least 2, you'll never get coincidences...\n");
    return -3;
  }

  if (histlen < 1) {
    printf("If you discover how to make a histogram using %ld bins, let me "
           "know. Bye.",
           histlen);
    return -4;
  }

  Tmax1 = LONG_MIN;
  Tmax2 = Tmax1;
  Tmin1 = LONG_MAX;
  Tmin2 = Tmin1;

  /* first of all, we'll go through all timetags and check the min
   * and max times - to see whether we have to adapt T2 */
  for (i = 0; i < valid; i++) {
    if (channels[i] == ch1) {
      if (tags[i] < Tmin1) {
        Tmin1 = tags[i];
        // min1Pos = i;
      } else if (tags[i] > Tmax1) {
        Tmax1 = tags[i];
        // max1Pos = i;
      }
    } else if (channels[i] == ch2) {
      if (tags[i] < Tmin2) {
        Tmin2 = tags[i];
        // min2Pos = i;
      } else if (tags[i] > Tmax2) {
        Tmax2 = tags[i];
        // max2Pos = i;
      }
    }
  }
  T1int = Tmin2 - Tmin1;
  T2int = Tmax2 - Tmin1;

  maxDelayInt = T2int - T1int;
  DTint = maxDelayInt / histlen;

  /* Initialize the histogram array */
  for (i = 0; i < histlen; i++) {
    hist[i] = 0;
  }

  /* loop over the blocks of time tags */
  for (n1 = 0; n2 < valid - n; n1 += n) {
    n2 = n1 + n;
    for (i = n1; i <= n2; i++) {
      for (j = n1; j <= n2; j++) {
        if (channels[i] == ch1) {
          if (channels[j] == ch2) {
            t1 = tags[i];
            t2 = tags[j];
          } else {
            continue;
          }
        } else if (channels[i] == ch2) {
          if (channels[j] == ch1) {
            t1 = tags[j];
            t2 = tags[i];
          } else {
            continue;
          }
        } else {
          continue;
        }
        if (t2 - t1 > T1int && t2 - t1 < T2int) {
          mmod = (t2 - t1 - T1int) % DTint;
          m = (t2 - t1 - T1int) / DTint;
          if (mmod < dtInt && m < histlen) {
            hist[m]++;
          }
        }
        /*
         * ****   the following was to take into account
         * ****   negative time delays - I commented that out
         * ****   on July 18th, 2022
            else if ( t1>t2 && t1-t2>T1int && t1-t2<T2int )
        {
                mmod = (t1-t2-T1int) % DTint;
                m = (t1-t2-T1int) / DTint;
                if ( mmod<dtInt && m<histlen )
                {
                        hist[m]++;
                }

        }
        */
      }
    }
  }
  *T1out = T1int * baseunit;
  *T2out = T2int * baseunit;

  return 0; /* no error */
}

/*
 * Function to determine a histogram of coincidences over a varying time
 * delay in steps of DT between "T1" and "T2". Both are assumed to be positive
 * and we assume that T2>T1. These values define the range of the histogram.
 * We always assume that the delay is between events in channels "ch1" and
 * "ch2" such that events in "ch2" occur at the same time or later than the
 * events in "ch1".
 * The time span "T2-T1" is then  split into "histlen" bins to form
 * the histogram. (T2-T1)/histlen will correspond to the bin size, and this
 * will effectively correspond to the coincidence window.
 * All times are in seconds.
 *
 * The histogram will be stored in the buffer pointed to by the
 * variable "hist" - it has have sufficient memory allocated beforehand
 * otherwise you'll most likely end up with a segmentation fault.
 *
 * We analyse the time tags in blocks of "n" events. If the length "valid"
 * is no integer multiple of "n", the last events will be discarded.
 *
 * The function takes an array of time tags ("tags") and a corresponding
 * array of channel numbers ("channels") indicating in which channel of the
 * time tagger the events took place.
 *
 * EXAMPLE how to call this in python:
 *
 *
 * */
Int64 determineCoincidenceHistogram(Int64 *tags, Int8 *channels, Int64 valid,
                                    Int64 ch1, Int64 ch2, double dt, double T1,
                                    double T2, Int64 *hist, Int64 histlen) {
  double baseunit = 1e-12, baseF = 1 / baseunit;
  Int64 T1int, T2int, maxt1, mmod, Tmin1, Tmin2, Tmax1, Tmax2, maxDelayInt,
      dtInt = round(dt * baseF), DTint;
  Int64 i, j, t1, t2, m;

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
    printf("ERROR: T1 and T2 should be positive, and we should have \
				T2>T1.\n");
    return -5;
  }

  T1int = round(T1 * baseF);
  T2int = round(T2 * baseF);
  maxDelayInt = T2int - T1int;
  DTint = maxDelayInt / histlen;
  printf("INFO: T1int: %ld, T2int: %ld\n, maxDelayInt: %ld, DTint: %ld, dtInt: "
         "%ld\n",
         T1int, T2int, maxDelayInt, DTint, dtInt);

  /* Initialize the histogram array */
  for (i = 0; i < histlen; i++) {
    hist[i] = 0;
  }
  Tmax1 = LONG_MIN;
  Tmax2 = Tmax1;
  Tmin1 = LONG_MAX;
  Tmin2 = Tmin1;

  /* first of all, we'll go through all timetags and check the min
   * and max times - to see what to use as upper limit for t1 */
  for (i = 0; i < valid; i++) {
    if (channels[i] == ch1) {
      if (tags[i] < Tmin1) {
        Tmin1 = tags[i];
      } else if (tags[i] > Tmax1) {
        Tmax1 = tags[i];
      }
    } else if (channels[i] == ch2) {
      if (tags[i] < Tmin2) {
        Tmin2 = tags[i];
      } else if (tags[i] > Tmax2) {
        Tmax2 = tags[i];
      }
    }
  }
  maxt1 = Tmax2 - maxDelayInt;
  printf("INFO: Tmax1: %ld, Tmax2: %ld, maxt1: %ld\n", Tmax1, Tmax2, maxt1);
  printf("INFO: starting the loops with valid=%ld\n", valid);

  t1 = 0;
  t2 = 0;
  for (i = 0; i <= valid; i++) {
    if (channels[i] != ch1) {
      continue;
    }
    if (i % (valid / 100) == 0) {
      printf("progress: %f\n", 100.0 * (((double)i) / ((double)valid)));
    }
    for (j = i; j < valid; j++) {
      if (channels[j] != ch2) {
        continue;
      }
      t1 = tags[i];
      t2 = tags[j];
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

  return 0; /* no error */
}
