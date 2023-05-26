#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "rp.h"

int ledToZero(void){
	int i;
	for (i = 0; i < 8; i++) {
	   rp_DpinSetState(i, RP_LOW);
	}
	return 0;
}

int ledBarForward(int unsigned led, int unsigned period) {
  period = period * 1000000; // uS
  led = RP_LED0;
  for(led; led < 8; led++)
      {
        printf("Blinking LED[%u]\n", led);
        rp_DpinSetState(led, RP_HIGH);
        usleep(period/4);
      }
  ledToZero();
  return 0;
}

int ledBarReverse(int unsigned led, int unsigned period) {
  period = period * 1000000; // uS
  for(led; led >= 0; led--)
      {
        printf("Blinking LED[%u]\n", led);
        rp_DpinSetState(led, RP_LOW);
        usleep(period);
        if(led == 0)
          break;
      }
  return 0;
}


int main (int argc, char **argv) {
    int unsigned led;
    int unsigned led2;

    // index of blinking LED can be provided as an argument
    if (argc > 2) {
        led = atoi(argv[1]);
        led += RP_LED0;
        led2 = atoi(argv[2]);
        led2 +=RP_LED0;
    // otherwise LED 0 will blink
    } else {
        led = RP_LED0;
        led2 = RP_LED7;
    }

    // Initialization of API
    if (rp_Init() != RP_OK) {
        fprintf(stderr, "Red Pitaya API init failed!\n");
        return EXIT_FAILURE;
    }

    int i=0;
    for(i;i<2;i++){
      ledBarForward(led, 1);
      ledBarReverse(led2, 2);
    }

    // Releasing resources
    rp_Release();

    return EXIT_SUCCESS;
}
