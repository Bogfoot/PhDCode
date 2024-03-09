#include "Coinc_Counter.h"
#include <stdint.h>

int main() {
  // Example usage
  int64_t hist[10] = {0};
  Event events[5] = {{100, 1}, {200, 2}, {300, 1}, {400, 2}, {500, 1}};
  int64_t result =
      determineCoincidenceHistogram(events, 5, 1, 2, 0.1, 0.0, 1.0, hist, 10);

  if (result == 0) {
    printf("Histogram: ");
    for (int i = 0; i < 10; i++) {
      printf("%ld ", hist[i]);
    }
    printf("\n");
  } else {
    printf("An error occurred: %ld\n", result);
  }

  return 0;
}
