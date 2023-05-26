/* Red Pitaya C API example Generating continuous signal
 * * This application generates a specific signal */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

#include "rp.h"

int main(int argc, char **argv){
/* Print error, if rp_Init() function failed */
if(rp_Init() != RP_OK){
  fprintf(stderr, "Rp api init failed!\n");
}
/* Reset generator */
rp_GenOutDisable(RP_CH_1);
rp_GenReset();
/* Generating wave form */
rp_GenWaveform(RP_CH_1, RP_WAVEFORM_SINE);
/* Generating frequency */
rp_GenFreq(RP_CH_1, 100000.0);
/* Generating amplitude */
rp_GenAmp(RP_CH_1, 0.5);
/* Enable channel */
rp_GenOutEnable(RP_CH_1);
/* Generating trigger */
rp_GenTriggerOnly(RP_CH_1);
int unsigned period = 1000000;
usleep(5*period);
///* Releasing resources */
rp_GenOutDisable(RP_CH_1);
rp_Release();
return 0;
}
