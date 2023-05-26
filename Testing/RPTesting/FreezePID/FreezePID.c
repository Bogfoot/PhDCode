#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "rp.h"
//#include "rpreadandwrite.h"

 // Function to freeze the PID output
 void freezePIDOutput() {
 // Code to modify the PID+Lock module parameters to freeze the output
 // Implementation depends on the specific PID+Lock module API
 // Ya no **** Sherlock
 // If voltage at output 2 is > 0.5V - tell Luda code to freeze PID for a period
 // of time
}

// Function to unfreeze the PID output
void unfreezePIDOutput() {
 // Code to modify the PID+Lock module parameters to unfreeze the output
 // Implementation depends on the specific PID+Lock module API
 // Ya no **** Sherlock
 // Tell Luda code to unfreeze
}


int main() { // Initialize Red Pitaya API
  float voltage;
  if (rp_Init() != RP_OK) {
    fprintf(stderr, "Red Pitaya API initialization failed!\n");
    return EXIT_FAILURE;
  } 

  // Main loop
  while (1) {
      // Read voltage from PID
      if (rp_AIpinGetValue(RP_CH_2, &voltage) != RP_OK) {
        fprintf(stderr, "Failed to read voltage from Input 2!\n");
        break;
      }

      // Make this async
      // Check if voltage is above the threshold
      if (voltage > 0.5F) {
        // Freeze the PID output
        freezePIDOutput();
      }
      else {
      // Unfreeze the PID output
        unfreezePIDOutput();
      }
    // Sleep before the next iteration : us
      usleep(1);
    }
  rp_Release();

return EXIT_SUCCESS;
}
