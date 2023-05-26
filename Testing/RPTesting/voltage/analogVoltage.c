/* Set analog voltage on slow analog output */ 
/*  
 *  Rainers assignment
 *
 * */

#include <stdio.h>
#include <stdlib.h> 
#include "rp.h"

int setVoltageToZero(void){
  float value = 0.0F;
  printf("Setting voltage back to 0.\n");
  for (int i = 0; i < 4; i++){
    int pin = RP_AOUT0 + i;
    int status = rp_AOpinSetValue(pin, value);
    if (status != RP_OK) { 
      printf("Could not set AO[%i] voltage.\n", i);
  }
}
  return 0;
}

int main (int argc, char **argv) {
    float value [4];
    for (int i=0; i<4; i++) {
     if (argc > (1+i)) {
       value [i] = atof(argv[1+i]);
    } else {
       value [i] = 1.0;
     } printf("Voltage setting for AO[%i] = %1.1fV\n", i, value [i]); } 
    if(rp_Init() != RP_OK) {
      fprintf(stderr, "Red Pitaya API init failed!\n");
      return EXIT_FAILURE; } 
    for (int i=0; i<4; i++) {
      int pin = RP_AOUT0 + i;
      int status = rp_AOpinSetValue(pin, value[i]);
      if (status != RP_OK) 
      { printf("Could not set AO[%i] voltage.\n", i); } } 
   getchar(); 
   setVoltageToZero();
   rp_Release();
   return EXIT_SUCCESS; 
}
