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

/** Starting address of FPGA registers handling Oscilloscope module. */
#define OSC_FPGA_BASE_ADDR      0x40100000
/** The size of FPGA registers handling Oscilloscope module. */
#define OSC_FPGA_BASE_SIZE 0x30000
/** Size of data buffer into which input signal is captured , must be 2^n!.
 * it is written as 16 * 1024 in the original code */
#define OSC_FPGA_SIG_LEN   16384


/** Bit index in FPGA configuration register for arming the trigger. */
#define OSC_FPGA_CONF_ARM_BIT  1
/** Bit index in FPGA configuration register for reseting write state machine. */
#define OSC_FPGA_CONF_RST_BIT  2

/** Bit mask in the trigger_source register for depicting the trigger source type. */
#define OSC_FPGA_TRIG_SRC_MASK 0x00000007
/** Bit mask in the cha_thr register for depicting trigger threshold on channel A. */
#define OSC_FPGA_CHA_THR_MASK  0x00003fff
/** Bit mask in the cha_thr register for depicting trigger threshold on channel B. */
#define OSC_FPGA_CHB_THR_MASK  0x00003fff
/** Bit mask in the trigger_delay register for depicting trigger delay. */
#define OSC_FPGA_TRIG_DLY_MASK 0xffffffff

/** Offset to the memory buffer where signal on channel A is captured. */
#define OSC_FPGA_CHA_OFFSET    0x10000
/** Offset to the memory buffer where signal on channel B is captured. */
#define OSC_FPGA_CHB_OFFSET    0x20000

/** Hysteresis register default setting */
#define OSC_HYSTERESIS 0x3F

/** @brief FPGA registry structure for Oscilloscope core module.
 *
 * This structure is direct image of physical FPGA memory. It assures
 * direct read/write FPGA access when it is mapped to the appropriate memory address
 * through /dev/mem device.
 */
typedef struct osc_fpga_reg_mem_s {
    /** @brief  Configuration:
     * bit     [0] - arm_trigger
     * bit     [1] - rst_wr_state_machine
     * bits [31:2] - reserved 
     */
    uint32_t conf;

    /** @brief  Trigger source:
     * bits [ 2 : 0] - trigger source:
     *   1 - trig immediately
     *   2 - ChA positive edge
     *   3 - ChA negative edge
     *   4 - ChB positive edge 
     *   5 - ChB negative edge
     *   6 - External trigger 0
     *   7 - External trigger 1 
     * bits [31 : 3] -reserved
     */
    uint32_t trig_source;

    /** @brief  ChA threshold:
     * bits [13: 0] - ChA threshold
     * bits [31:14] - reserved
     */
    uint32_t cha_thr;

    /** @brief  ChB threshold:
     * bits [13: 0] - ChB threshold
     * bits [31:14] - reserved
     */
    uint32_t chb_thr;

    /** @brief  After trigger delay:
     * bits [31: 0] - trigger delay 
     * 32 bit number - how many decimated samples should be stored into a buffer.
     * (max 16k samples)
     */
    uint32_t trigger_delay;

    /** @brief  Data decimation
     * bits [16: 0] - decimation factor, legal values:
     *   1, 8, 64, 1024, 8192 65536
     *   If other values are written data is undefined 
     * bits [31:17] - reserved
     */
    uint32_t data_dec;

    /** @brief  Write pointers - both of the format:
     * bits [13: 0] - pointer
     * bits [31:14] - reserved
     * Current pointer - where machine stopped writing after trigger
     * Trigger pointer - where trigger was detected 
     */
    uint32_t wr_ptr_cur;
    uint32_t wr_ptr_trigger;

    /** @brief  ChA & ChB hysteresis - both of the format:
     * bits [13: 0] - hysteresis threshold
     * bits [31:14] - reserved
     */
    uint32_t cha_hystersis;
    uint32_t chb_hystersis;

    /** @brief
     * bits [0] - enable signal average at decimation
     * bits [31:1] - reserved
     */
    uint32_t other;
    
    uint32_t reseved;
    
    /** @brief ChA Equalization filter
     * bits [17:0] - AA coefficient (pole)
     * bits [31:18] - reserved
     */
    uint32_t cha_filt_aa;    
    
    /** @brief ChA Equalization filter
     * bits [24:0] - BB coefficient (zero)
     * bits [31:25] - reserved
     */
    uint32_t cha_filt_bb;    
    
    /** @brief ChA Equalization filter
     * bits [24:0] - KK coefficient (gain)
     * bits [31:25] - reserved
     */
    uint32_t cha_filt_kk;  
    
    /** @brief ChA Equalization filter
     * bits [24:0] - PP coefficient (pole)
     * bits [31:25] - reserved
     */
    uint32_t cha_filt_pp;     
    
    
    

    /** @brief ChB Equalization filter
     * bits [17:0] - AA coefficient (pole)
     * bits [31:18] - reserved
     */
    uint32_t chb_filt_aa;    
    
    /** @brief ChB Equalization filter
     * bits [24:0] - BB coefficient (zero)
     * bits [31:25] - reserved
     */
    uint32_t chb_filt_bb;    
    
    /** @brief ChB Equalization filter
     * bits [24:0] - KK coefficient (gain)
     * bits [31:25] - reserved
     */
    uint32_t chb_filt_kk;  
    
    /** @brief ChB Equalization filter
     * bits [24:0] - PP coefficient (pole)
     * bits [31:25] - reserved
     */
    uint32_t chb_filt_pp;            
    
    
    /** @brief  ChA & ChB data - 14 LSB bits valid starts from 0x10000 and
     * 0x20000 and are each 16k samples long */
} osc_fpga_reg_mem_t;

/** @} */


int cleanup_mem(void);
int osc_fpga_init(void);
int osc_fpga_get_sig_ptr(int **cha_signal, int **chb_signal);
int osc_fpga_get_wr_ptr(int *wr_ptr_curr, int *wr_ptr_trig);
double osc_fpga_cnv_cnt_to_v(int cnts, double adc_max_v, int calib_dc_off, double user_dc_off);
int osc_cnv_cnt_to_v_chA(double *chAout, double adc_max_v, int calib_dc_off);
int osc_cnv_cnt_to_v_chs(double *chAout, double *chBout, double adc_max_v, int calib_dc_off);
int osc_cnv_cnt_to_v_chs_backup(double *chAout, double *chBout, double adc_max_v, int calib_dc_off, double user_dc_off);
int rp_get_signalA(double* chA, int* wr_ptr_curr, int* wr_ptr_trig, double factor);
int rp_get_signals(double* chA, double* chB, int* wr_ptr_curr, int* wr_ptr_trig, double factor);
int rp_get_fast_new(double* chA, double* chB, int* wr_ptr_curr, int* wr_ptr_trig, double factor);
int rp_copy_signals(int* chA, int* chB, int* rpChA, int* rpChB);

#endif
