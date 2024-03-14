
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
