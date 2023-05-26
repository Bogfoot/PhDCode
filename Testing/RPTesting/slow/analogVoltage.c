/* Set analog voltage on slow analog output */

/*  
 *  Rainers assignment
 *
 * */

#include <stdio.h>
#include <stdlib.h>

#include "rpreadandwrite.h"

int setVoltageToZero(void){
  float value = 0.0F;
  printf("Setting voltage back to 0.\n");
  for (uint32_t i = 0; i < 4; i++){
    int status = rp_AOpinSetValue(i, value);
    if (status != 0) { 
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
    }
     else {
       value [i] = 1.0F;
     }
     printf("Voltage setting for AO[%i] = %1.1fV\n", i, value [i]);
    }
    for (uint32_t i=0; i<4; i++) {
      int status = rp_AOpinSetValue(i, value[i]);
      printf("status: %d", status);
      if (status != 0) 
      {
       printf("Could not set AO[%i] voltage.\n", i);
      }
  } 
   getchar(); 
   setVoltageToZero();
   return EXIT_SUCCESS; 
}
