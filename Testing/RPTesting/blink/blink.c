#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "rp.h"

int ledToZero(void){
	int i;
	for (i = 0; i < 7; i++) {
	   rp_DpinSetState(i, RP_LOW);
	}
	return 0;
}

int main (int argc, char **argv) {
    int unsigned period = 1000000; // uS
    int unsigned led;

    // index of blinking LED can be provided as an argument
    if (argc > 1) {
        led = atoi(argv[1]);
    // otherwise LED 0 will blink
    } else {
        led = 0;
    }
    printf("Blinking LED[%u]\n", led);
    led += RP_LED0;

    // Initialization of API
    if (rp_Init() != RP_OK) {
        fprintf(stderr, "Red Pitaya API init failed!\n");
        return EXIT_FAILURE;
    }

    int unsigned retries = 10;
    while (retries--){
	if(led > 7)
	{
	 led = RP_LED0;
	}
        rp_DpinSetState(led, RP_HIGH);
        usleep(period/2);
        rp_DpinSetState(led, RP_LOW);
        usleep(period/2);
	led++;
    }
    ledToZero();

    // Releasing resources
    rp_Release();

    return EXIT_SUCCESS;
}
