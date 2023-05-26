#ifndef __RPREADANDWRITE_H
#define __RPREADANDWRITE_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/mman.h>
#include <errno.h>
#include <math.h>
#include <unistd.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <sys/ioctl.h>
//#include <stropts.h>
#include <sys/select.h>
#include "calib.h"
#include "pid.h"
#include "fpga.h"
#include "fpga_pid.h"
#include "fpga_awg.h"
#include "generate.h"
#include "worker.h"
#include "main.h"
#include "RKanalog_mixed_signals.h"

#ifndef HK_FPGA_BASE_ADDR 
/** Starting address of FPGA registers for housekeeping. */
#define HK_FPGA_BASE_ADDR      0x40000000
#endif


#ifndef AMS_FPGA_BASE_ADDR
/** Starting address of FPGA registers for analog mixed signals. */
#define AMS_FPGA_BASE_ADDR      0x40400000
#endif

#ifndef OSC_FPGA_BASE_ADDR
/** Starting address of FPGA registers handling Oscilloscope module. */
#define OSC_FPGA_BASE_ADDR      0x40100000
#endif

#ifndef HK_FPGA_BASE_SIZE
/** The size of FPGA registers handling  housekeeping - for our RP, for
    other types, this value will be DIFFERENT - e.g. 0x44 - see 
    housekeeping.h in the gitub examples. */
#define HK_FPGA_BASE_SIZE 0x34
#endif

#ifndef AMS_FPGA_BASE_SIZE
/** The size of FPGA registers handling analog signals. */
#define AMS_FPGA_BASE_SIZE 0x30
#endif

#ifndef OSC_FPGA_BASE_SIZE
/** The size of FPGA registers handling Oscilloscope module. */
#define OSC_FPGA_BASE_SIZE 0x30000
#endif

#ifndef OSC_FPGA_SIG_LEN
/** Size of data buffer into which input signal is captured , must be 2^n!.
 * it is written as 16 * 1024 in the original code */
#define OSC_FPGA_SIG_LEN   16384
#endif

#ifndef OSC_FPGA_CONF_ARM_BIT
/** Bit index in FPGA configuration register for arming the trigger. */
#define OSC_FPGA_CONF_ARM_BIT  1
#endif

#ifndef OSC_FPGA_CONF_RST_BIT
/** Bit index in FPGA configuration register for reseting write state machine. */
#define OSC_FPGA_CONF_RST_BIT  2
#endif

#ifndef OSC_FPGA_TRIG_SRC_MASK
/** Bit mask in the trigger_source register for depicting the trigger source type. */
#define OSC_FPGA_TRIG_SRC_MASK 0x00000007
#endif

#ifndef OSC_FPGA_CHA_THR_MASK
/** Bit mask in the cha_thr register for depicting trigger threshold on channel A. */
#define OSC_FPGA_CHA_THR_MASK  0x00003fff
#endif

#ifndef OSC_FPGA_CHB_THR_MASK
/** Bit mask in the cha_thr register for depicting trigger threshold on channel B. */
#define OSC_FPGA_CHB_THR_MASK  0x00003fff
#endif

#ifndef OSC_FPGA_TRIF_DLY_MASK
/** Bit mask in the trigger_delay register for depicting trigger delay. */
#define OSC_FPGA_TRIG_DLY_MASK 0xffffffff
#endif

#ifndef OSC_FPGA_CHA_OFFSET
/** Offset to the memory buffer where signal on channel A is captured. */
#define OSC_FPGA_CHA_OFFSET    0x10000
#endif

#ifndef OSC_FPGA_CHB_OFFSET
/** Offset to the memory buffer where signal on channel B is captured. */
#define OSC_FPGA_CHB_OFFSET    0x20000
#endif

#ifndef OSC_HYSTERESIS
/** Hysteresis register default setting */
#define OSC_HYSTERESIS 0x3F
#endif

/** @} */

typedef struct hk_fpga_reg_mem_s {
    /**
     * bits [0-3]  - design ID  (read)
     * bits [4-31] - reserved   (read)
    */
    uint32_t ID;
    /**
     * bits [0-31] - DNA        (read)
    */
    uint32_t dna1;
    /**
     * bits [0-24]  - DNA       (read)
     * bits [25-31] - reserved  (read)
    */
    uint32_t dna2;
    /**
     * bit [0]     - sigital loop           (read/write)
     * bits [1-31] - reserved               (read)
    */
    uint32_t dig_loop;
    /**
     * bits [0-7]  - direction or P lines   (read/write)
     * bits [8-31] - reserved               (read)
    */
    uint32_t dir_P;
    /**
     * bits [0-7]  - direction or N lines   (read/write)
     * bits [8-31] - reserved               (read)
    */
    uint32_t dir_N;
    /**
     * bits [0-7]  - output for P lines   (read/write)
     * bits [8-31] - reserved               (read)
    */
    uint32_t out_P;
    /**
     * bits [0-7]  - output for N lines   (read/write)
     * bits [8-31] - reserved               (read)
    */
    uint32_t out_N;
} hk_fpga_reg_mem_t;

typedef struct ams_fpga_reg_mem_s {
    /**
     * for each of the 32bit elements:
     * bits [0-11]  - AIF[i] value  (read)
     * bits [12-31] - reserved    (read)
    */
    uint32_t XADC_AIF[5];
    /**
    * for whatever future purpose
    */
    uint32_t reserved[3];
    /**
     * for each of the 32bit elements:
     * bits [0-15]  - bit select for PWM repetition, which have
	 * value PWM+1                               (read/write)
     * bits [16-23] - PWM value (100% == 255)    (read/write)
     * bits [24-31] - reserved                   (read)
    */
    uint32_t PWM_DAC[4];
} ams_fpga_reg_mem_t;

int cleanup_mem(void);
int my_osc_fpga_init(void);
int my_awg_fpga_init(void);
int my_osc_fpga_get_sig_ptr(int **cha_signal, int **chb_signal);
int my_osc_fpga_get_wr_ptr(int *wr_ptr_curr, int *wr_ptr_trig);
float my_osc_fpga_cnv_cnt_to_v(int cnts, float adc_max_v, int calib_dc_off, float user_dc_off);
int rp_get_signalA(float* chA, int* wr_ptr_curr, int* wr_ptr_trig, float adc_max_v, float dc_off);
int rp_get_signalA_intOff(float* chA, int* wr_ptr_curr, int* wr_ptr_trig, float adc_max_v, int dc_off);
int my_rp_get_signals(float* chA, float* chB, int* wr_ptr_curr, int* wr_ptr_trig, float factor);
int rp_get_fast_new(float* chA, float* chB, int* wr_ptr_curr, int* wr_ptr_trig, float factor);
int rp_copy_signals(int* chA, int* chB, int* rpChA, int* rpChB);
int mykbhit(void); 
int timedAO_slow(float maxVin, float maxVout, float factorB, float offsetA,
                 float offsetB);
int timedAO_fast(int chIn, int chOut, float maxVin, float offsetIn,
                 float offsetOut);
int output_average_slow(float maxVin, float maxVout, float offsetA, 
                        float offsetB);
int output_average_fast(int chIn, int chOut, float maxVin, float offsetIn, 
                        float offsetOut);
int cleanupSlowAveraging(void);
int initSlowAverage(int avgMode, int avgTime, int pinA, int pinB);
int my_generate_init(rp_calib_params_t *calib_params);
int my_rp_init(void);
/* takes the data stored in our internal buffer for channel A or B (0 or 1 for
   ch and returns the average of that buffer */
float avg_osc(int ch, float adc_max_v, int calib_dc_off, float user_dc_off);
int my_osc_cnv_cnt_to_v_chs(float *chAout, float *chBout, float adc_max_v, 
                            int calib_dc_off);
int my_osc_cnv_cnt_to_v_chs_backup(float *chAout, float *chBout, 
                       float adc_max_v, int calib_dc_off, float user_dc_off);
int my_osc_cnv_cnt_to_v_chA(float *chAout, float adc_max_v, float calib_dc_off);
int my_osc_cnv_cnt_to_v_chA_int(float *chAout, float adc_max_v, int calib_dc_off);
int my_pid_update(rp_app_params_t *params);
int set_dec(int dec);
int rp_AOpinSetValue(uint32_t pin, float value);
int ams_Release_backup(); 
int ams_Init_backup();
int ams_Release(); 
int ams_Init();
#endif
