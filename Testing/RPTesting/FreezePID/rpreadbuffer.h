#ifndef __RPREADBUFFER_H
#define __RPREADBUFFER_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/mman.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include "calib.h"
#include "pid.h"
#include "fpga.h"
#include "fpga_pid.h"
#include "worker.h"
#include "main.h"

#ifndef OSC_FPGA_BASE_ADDR
/** Starting address of FPGA registers handling Oscilloscope module. */
#define OSC_FPGA_BASE_ADDR      0x40100000
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


int cleanup_mem(void);
int my_osc_fpga_init(void);
int my_osc_fpga_get_sig_ptr(int **cha_signal, int **chb_signal);
int my_osc_fpga_get_wr_ptr(int *wr_ptr_curr, int *wr_ptr_trig);
double my_osc_fpga_cnv_cnt_to_v(int cnts, double adc_max_v, int calib_dc_off, double user_dc_off);
int my_osc_cnv_cnt_to_v_chA(double *chAout, double adc_max_v, double calib_dc_off);
int my_osc_cnv_cnt_to_v_chA_int(double *chAout, double adc_max_v, int calib_dc_off);
int my_osc_cnv_cnt_to_v_chs(double *chAout, double *chBout, double adc_max_v, int calib_dc_off);
int my_osc_cnv_cnt_to_v_chs_backup(double *chAout, double *chBout, double adc_max_v, int calib_dc_off, double user_dc_off);
int rp_get_signalA(double* chA, int* wr_ptr_curr, int* wr_ptr_trig, double adc_max_v, double dc_off);
int rp_get_signalA_intOff(double* chA, int* wr_ptr_curr, int* wr_ptr_trig, double adc_max_v, int dc_off);
int my_rp_get_signals(double* chA, double* chB, int* wr_ptr_curr, int* wr_ptr_trig, double factor);
int rp_get_fast_new(double* chA, double* chB, int* wr_ptr_curr, int* wr_ptr_trig, double factor);
int rp_copy_signals(int* chA, int* chB, int* rpChA, int* rpChB);

#endif
