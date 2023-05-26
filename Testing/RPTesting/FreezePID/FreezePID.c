#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "rp.h"
//#include "rpreadandwrite.h"

// Red Pitaya constants
#define INPUT1_CHANNEL RP_CH_1      // Input 1 channel for the error signal
#define INPUT2_CHANNEL RP_CH_2      // Input 2 channel for monitoring voltage
#define OUTPUT_CHANNEL RP_CH_1       // Output channel for the PID output signal
#define VOLTAGE_THRESHOLD 0.5       // Voltage threshold for freezing/unfreezing
#define RP_5V 5.0F

 // Function to freeze the PID output
 void freezePIDOutput() {
 // Code to modify the PID+Lock module parameters to freeze the output
 // Implementation depends on the specific PID+Lock module API
 // Ya no shit Sherlock
}

// Function to unfreeze the PID output
void unfreezePIDOutput() {
 // Code to modify the PID+Lock module parameters to unfreeze the output
 // Implementation depends on the specific PID+Lock module API
 // Ya no shit Sherlock
}


int main() { // Initialize Red Pitaya API
if (rp_Init() != RP_OK) {
    fprintf(stderr, "Red Pitaya API initialization failed!\n");
    return EXIT_FAILURE;
  }

// Initialize variables
  float voltage2;
  float pidOutput;

// Main loop
while (1) {
      // Read voltage from Input 2
    if (rp_AIpinGetValue(INPUT2_CHANNEL, &voltage2) != RP_OK) {
      fprintf(stderr, "Failed to read voltage from Input 2!\n");
      break;
    }
    // Check if voltage is above the threshold
    if (voltage2 > VOLTAGE_THRESHOLD) {
      // Freeze the PID output
      freezePIDOutput();
    }
    else {
    // Unfreeze the PID output
      unfreezePIDOutput();
    }

  // Read PID output from Input 1
    if (rp_AIpinGetValue(INPUT1_CHANNEL, &pidOutput) != RP_OK)
    {
      fprintf(stderr, "Failed to read PID output from Input 1!\n");
      break;
    }
    // Set the PID output as the output signal
    if (rp_AOpinSetValue(OUTPUT_CHANNEL, pidOutput) != RP_OK)
    {
      fprintf(stderr, "Failed to set PID output as the output signal!\n");
      break;
    }

  // Sleep for a small duration before the next iteration
    usleep(100);
  }
// Cleanup and close Red Pitaya API
rp_Release();

return EXIT_SUCCESS;
}
