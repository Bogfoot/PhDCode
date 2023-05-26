#include "rpreadandwrite.h"

// extern rp_ext_calib_params_t *gen_calib_params;
// extern int g_awg_fd;

/* @brief Pointer to FPGA control registers for the Osci. */
static osc_fpga_reg_mem_t *g_osc_fpga_reg_mem = NULL;

/* @brief Pointer to FPGA control registers for the AMS. */
static ams_fpga_reg_mem_t *g_ams_fpga_reg_mem = NULL;

// static rp_app_params_t       *rp_osc_params = NULL;
// static rp_app_params_t       *rp_main_params = NULL;
static rp_app_params_t rp_main_params[PARAMS_NUM + 1] = {
    {/* min_gui_time   */
     //"xmin", -1000000, 1, 0, -10000000, +10000000 },
     "xmin", 0, 1, 0, -10000000, +10000000},
    {/* max_gui_time   */
     //"xmax", +1000000, 1, 0, -10000000, +10000000 },
     "xmax", 131, 1, 0, -10000000, +10000000},
    {/* trig_mode:
      *    0 - auto
      *    1 - normal
      *    2 - single  */
     "trig_mode", 0, 1, 0, 0, 2},
    {/* trig_source:
      *    0 - ChA
      *    1 - ChB
      *    2 - ext.    */
     "trig_source", 0, 1, 0, 0, 2},
    {/* trig_edge:
      *    0 - rising
      *    1 - falling */
     "trig_edge", 0, 1, 0, 0, 1},
    {/* trig_delay     */
     "trig_delay", 0, 1, 1, -10000000, +10000000},
    {/* trig_level : Trigger level, expressed in normalized 1V  */
     "trig_level", 0, 1, 0, -8192, +8191}, // LOLO
    {                                      /* single_button:
                                            *    0 - ignore
                                            *    1 - trigger */
     "single_btn", 0, 1, 0, 0, 1},
    {/* time_range:
      *  decimation:
      *    0 - 1x
      *    1 - 8x
      *    2 - 64x
      *    3 - 1kx
      *    4 - 8kx
      *    5 - 65kx   */
     "time_range", 0, 1, 1, 0, 5},
    {/* time_unit_used:
      *    0 - [us]
      *    1 - [ms]
      *    2 - [s]     */
     "time_units", 0, 0, 1, 0, 2},
    {/* en_avg_at_dec:
      *    0 - disable
      *    1 - enable */
     "en_avg_at_dec", 0, 1, 0, 0, 1},
    {/* auto_flag:
      * Puts the controller to auto mode - the algorithm which detects input
      * signal and changes the parameters to most fit the input:
      *    0 - normal operation
      *    1 - auto button pressed */
     "auto_flag", 0, 1, 0, 0, 1},
    {/* min_y, max_y - Controller defined Y range when using auto-set or after
      * gain change y range */
     "min_y", 0, 0, 0, -1000, +1000},
    {/* min_y, max_y - Controller defined Y range when using auto-set or after
      * gain change y range */
     "max_y", 0, 0, 0, -1000, +1000},
    {/* forcex_flag:
      * Server sets this flag when X axis time units change
      * Client checks this flag, when set the server's xmin:xmax define the
      * visualization range 0 - normal operation 1 - Server forces xmin, xmax */
     "forcex_flag",
     0, 0, 0, 0, 1},
    /* Measurement parameters for both channels. All are read-only and they
     * are calculated on FPGA buffer (non decimated in SW):
     * min, max [V] - minimum and maximum value in the buffer (non-decimated)
     * amp [Vpp] - amplitude = maximum - minum
     * avg [V] - average value
     * freq [MHz] - frequency of the signal (if any, otherwise NaN)
     * period [s] - period of the signal (if any, otherwise NaN)
     **/
    {"meas_min_ch1", 0, 0, 1, -1000, +1000},
    {"meas_max_ch1", 0, 0, 1, +1000, -1000},
    {"meas_amp_ch1", 0, 0, 1, +1000, -1000},
    {"meas_avg_ch1", 0, 0, 1, +1000, -1000},
    {"meas_freq_ch1", 0, 0, 1, 0, 1e9},
    {"meas_per_ch1", 0, 0, 1, 0, 1e9},
    {"meas_min_ch2", 0, 0, 1, -1000, +1000},
    {"meas_max_ch2", 0, 0, 1, +1000, -1000},
    {"meas_amp_ch2", 0, 0, 1, +1000, -1000},
    {"meas_avg_ch2", 0, 0, 1, +1000, -1000},
    {"meas_freq_ch2", 0, 0, 1, 0, 1e9},
    {"meas_per_ch2", 0, 0, 1, 0, 1e9},
    {/* prb_att_ch1 - User probe attenuation setting for channel 1:
      *    0 - 1x
      *    1 - 10x */
     "prb_att_ch1", 0, 1, 0, 0, 1},
    {/* gain_ch1 - User jumper gain setting for channel 1:
      *    0 - high gain (0.6 [V] Full-scale)
      *    1 - low gain (15 [V] Full-scale) */
     "gain_ch1", 0, 1, 0, 0, 1},
    {/* prb_att_ch2 - User probe attenuation setting for channel 2:
      *    0 - 1x
      *    1 - 10x */
     "prb_att_ch2", 0, 1, 0, 0, 1},
    {/* gain_ch2 - User jumper gain setting for channel 2:
      *    0 - high gain (0.6 [V] Full-scale)
      *    1 - low gain (15 [V] Full-scale) */
     "gain_ch2", 0, 1, 0, 0, 1},
    {/* gui_reset_y_range - Maximum voltage range [Vpp] with current settings
      * This parameter is calculated by application and is read-only for
      * client.
      */
     "gui_reset_y_range", 28, 0, 1, 0, 2000},
    {/* gen_DC_offs_1 - DC offset for channel 1 expressed in [V] requested by
      * GUI */
     "gen_DC_offs_1", 0, 1, 0, -100, 100},
    {/* gen_DC_offs_2 - DC offset for channel 2 expressed in [V] requested by
      * GUI */
     "gen_DC_offs_2", 0, 1, 0, -100, 100},
    {/* gui_xmin - Xmin as specified by GUI - not rounded to sampling engine
        quanta. */
     "gui_xmin",
     0, 0, 1, -10000000, +10000000},
    {/* gui_xmax - Xmax as specified by GUI - not rounded to sampling engine
        quanta. */
     "gui_xmax",
     131, 0, 1, -10000000, +10000000},
    {/* min_y_norm, max_y_norm - Normalized controller defined Y range when
        using auto-set */
     "min_y_norm",
     0, 0, 0, -1000, +1000},
    {/* min_y_norm, max_y_norm - Normalized controller defined Y range when
        using auto-set */
     "max_y_norm",
     0, 0, 0, -1000, +1000},
    {/* gen_DC_norm_1 - DC offset for channel 1 expressed in normalized 1V */
     "gen_DC_norm_1", 0, 1, 0, -100, 100},
    {/* gen_DC_norm_2 - DC offset for channel 2 expressed in normalized 1V */
     "gen_DC_norm_2", 0, 1, 0, -100, 100},
    {/* scale_ch1 - Jumper & probe attenuation dependent Y scaling factor for
        Channel 1 */
     "scale_ch1",
     0, 0, 1, -1000, 1000},
    {/* scale_ch2 - Jumper & probe attenuation dependent Y scaling factor for
        Channel 2 */
     "scale_ch2",
     0, 0, 1, -1000, 1000},

    /********************************************************/
    /* Arbitrary Waveform Generator parameters from here on */
    /********************************************************/

    {/* gen_trig_mod_ch1 - Selects the trigger mode for channel 1:
      *    0 - continuous
      *    1 - single
      *    2 - external */
     "gen_trig_mod_ch1", 0, 1, 0, 0, 2},
    {/* gen_sig_type_ch1 - Selects the type of signal for channel 1:
      *    0 - sine
      *    1 - square
      *    2 - triangle
      *    3 - from file */
     "gen_sig_type_ch1", 0, 1, 0, 0, 3},
    {/* gen_enable_ch1 - Enables/disable signal generation on channel 1:
      *    0 - Channel 1 disabled
      *    1 - Channel 1 enabled */
     "gen_enable_ch1", 1, 1, 0, 0, 1},
    {/* gen_single_ch1 - Fire single trigger on generator channel 1:
      *    0 - Do not fire single trigger
      *    1 - Fire single trigger */
     "gen_single_ch1", 0, 1, 0, 0, 1},
    {/* gen_sig_amp_ch1 - Amplitude for Channel 1 in [Vpp] */
     "gen_sig_amp_ch1", 0.25, 1, 0, 0, 2.0},
    {/* gen_sig_freq_ch1 - Frequency for Channel 1 in [Hz] */
     "gen_sig_freq_ch1", 1000, 1, 0, 0, 50e6},
    {/* gen_sig_dcoff_ch1 - DC offset applied to the signal in [V] */
     "gen_sig_dcoff_ch1", 0, 1, 0, -1, 1},
    {/* gen_trig_mod_ch2 - Selects the trigger mode for channel 2:
      *    0 - continuous
      *    1 - single
      *    2 - external */
     "gen_trig_mod_ch2", 0, 1, 0, 0, 2},
    {/* gen_sig_type_ch2 - Selects the type of signal for channel 2:
      *    0 - sine
      *    1 - square
      *    2 - triangle
      *    3 - from file */
     "gen_sig_type_ch2", 0, 1, 0, 0, 3},
    {/* gen_enable_ch2 - Enables/disable signal generation on channel 2:
      *    0 - channel 2 disabled
      *    1 - channel 2 enabled */
     "gen_enable_ch2", 0, 1, 0, 0, 1},
    {/* gen_single_ch2 - Fire single trigger on generator channel 2:
      *    0 - Do not fire single trigger
      *    1 - Fire single trigger */
     "gen_single_ch2", 0, 1, 0, 0, 1},
    {/* gen_sig_amp_ch2 - Amplitude for channel 2 in [Vpp] */
     "gen_sig_amp_ch2", 0, 1, 0, 0, 2.0},
    {/* gen_sig_freq_ch2 - Frequency for channel 2 in [Hz] */
     "gen_sig_freq_ch2", 1000, 1, 0, 0.2, 50e6},
    {/* gen_sig_dcoff_ch2 - DC offset applied to the signal in [V] */
     "gen_sig_dcoff_ch2", 0, 1, 0, -1, 1},
    {/* gen_awg_refresh - Refresh AWG data from (uploaded) file.
      *     0 - Do not refresh
      *     1 - Refresh Channel 1
      *     2 - Refresh Channel 2
      */
     "gen_awg_refresh", 0, 0, 0, 0, 2},

    /******************************************/
    /* PID Controller parameters from here on */
    /******************************************/

    {/* pid_NN_enable - Enables/closes or disables/open PID NN loop:
      *    0 - PID disabled (open loop)
      *    1 - PID enabled (closed loop)    */
     "pid_11_enable", 0, 1, 0, 0, 1},
    {/* pid_NN_rst - Reset PID NN integrator:
      *    0 - Do not reset integrator
      *    1 - Reset integrator            */
     "pid_11_rst", 0, 1, 0, 0, 1},
    {/* pid_NN_sp - PID NN set-point in [ADC] counts. */
     "pid_11_sp", 0, 1, 0, -8192, 8191},
    {/* pid_NN_kp - PID NN proportional gain Kp in [ADC] counts. */
     "pid_11_kp", 0, 1, 0, -8192, 8191},
    {/* pid_NN_ki - PID NN integral gain     Ki in [ADC] counts. */
     "pid_11_ki", 0, 1, 0, -8192, 8191},
    {/* pid_NN_kd - PID NN derivative gain   Kd in [ADC] counts. */
     "pid_11_kd", 0, 1, 0, -8192, 8191},

    {/* pid_NN_enable - Enables/closes or disables/open PID NN loop:
      *    0 - PID disabled (open loop)
      *    1 - PID enabled (closed loop)    */
     "pid_12_enable", 0, 1, 0, 0, 1},
    {/* pid_NN_rst - Reset PID NN integrator:
      *    0 - Do not reset integrator
      *    1 - Reset integrator            */
     "pid_12_rst", 0, 1, 0, 0, 1},
    {/* pid_NN_sp - PID NN set-point in [ADC] counts. */
     "pid_12_sp", 0, 1, 0, -8192, 8191},
    {/* pid_NN_kp - PID NN proportional gain Kp in [ADC] counts. */
     "pid_12_kp", 0, 1, 0, -8192, 8191},
    {/* pid_NN_ki - PID NN integral gain     Ki in [ADC] counts. */
     "pid_12_ki", 0, 1, 0, -8192, 8191},
    {/* pid_NN_kd - PID NN derivative gain   Kd in [ADC] counts. */
     "pid_12_kd", 0, 1, 0, -8192, 8191},

    {/* pid_NN_enable - Enables/closes or disables/open PID NN loop:
      *    0 - PID disabled (open loop)
      *    1 - PID enabled (closed loop)    */
     "pid_21_enable", 0, 1, 0, 0, 1},
    {/* pid_NN_rst - Reset PID NN integrator:
      *    0 - Do not reset integrator
      *    1 - Reset integrator            */
     "pid_21_rst", 0, 1, 0, 0, 1},
    {/* pid_NN_sp - PID NN set-point in [ADC] counts. */
     "pid_21_sp", 0, 1, 0, -8192, 8191},
    {/* pid_NN_kp - PID NN proportional gain Kp in [ADC] counts. */
     "pid_21_kp", 0, 1, 0, -8192, 8191},
    {/* pid_NN_ki - PID NN integral gain     Ki in [ADC] counts. */
     "pid_21_ki", 0, 1, 0, -8192, 8191},
    {/* pid_NN_kd - PID NN derivative gain   Kd in [ADC] counts. */
     "pid_21_kd", 0, 1, 0, -8192, 8191},

    {/* pid_NN_enable - Enables/closes or disables/open PID NN loop:
      *    0 - PID disabled (open loop)
      *    1 - PID enabled (closed loop)    */
     "pid_22_enable", 0, 1, 0, 0, 1},
    {/* pid_NN_rst - Reset PID NN integrator:
      *    0 - Do not reset integrator
      *    1 - Reset integrator            */
     "pid_22_rst", 0, 1, 0, 0, 1},
    {/* pid_NN_sp - PID NN set-point in [ADC] counts. */
     "pid_22_sp", 0, 1, 0, -8192, 8191},
    {/* pid_NN_kp - PID NN proportional gain Kp in [ADC] counts. */
     "pid_22_kp", 0, 1, 0, -8192, 8191},
    {/* pid_NN_ki - PID NN integral gain     Ki in [ADC] counts. */
     "pid_22_ki", 0, 1, 0, -8192, 8191},
    {/* pid_NN_kd - PID NN derivative gain   Kd in [ADC] counts. */
     "pid_22_kd", 0, 1, 0, -8192, 8191},

    /*********************************************/
    /** LOCK Controller parameters from here on **/
    /*********************************************/

    // [MAINDEF DOCK]

    {"lock_oscA_sw", 1, 1, 0, 0, 31}, /** switch for muxer oscA **/
    {"lock_oscB_sw", 2, 1, 0, 0, 31}, /** switch for muxer oscB **/
    {"lock_osc1_filt_off", 1, 1, 0, 0,
     1}, /** oscilloscope control osc1_filt_off **/
    {"lock_osc2_filt_off", 1, 1, 0, 0,
     1}, /** oscilloscope control osc2_filt_off **/
    {"lock_osc_raw_mode", 0, 0, 0, 0,
     1}, /** Set oscilloscope mode in Raw (int unit instead of Volts) **/
    {"lock_osc_lockin_mode", 0, 0, 0, 0,
     1}, /** Set oscilloscope mode in lock-in (ch1 as R [V|int], ch2 as Phase
            [rad]) **/
    {"lock_trig_sw", 0, 1, 0, 0,
     255},                            /** Select the external trigger signal **/
    {"lock_out1_sw", 0, 1, 0, 0, 15}, /** switch for muxer out1 **/
    {"lock_out2_sw", 0, 1, 0, 0, 15}, /** switch for muxer out2 **/
    {"lock_slow_out1_sw", 0, 1, 0, 0, 15}, /** switch for muxer slow_out1 **/
    {"lock_slow_out2_sw", 0, 1, 0, 0, 15}, /** switch for muxer slow_out2 **/
    {"lock_slow_out3_sw", 0, 1, 0, 0, 15}, /** switch for muxer slow_out3 **/
    {"lock_slow_out4_sw", 0, 1, 0, 0, 15}, /** switch for muxer slow_out4 **/
    {"lock_lock_control", 1148, 1, 0, 0, 2047},  /** lock_control help **/
    {"lock_lock_feedback", 1148, 0, 1, 0, 2047}, /** lock_control feedback **/
    {"lock_lock_trig_val", 0, 1, 0, -8192,
     8191}, /** if lock_control ?? , this vals sets the voltage threshold that
               turns on the lock **/
    {"lock_lock_trig_time_val", 0, 1, 0, 0,
     0xffffffff}, /** if lock_control ?? , this vals sets the time threshold
                     that turns on the lock **/
    {"lock_lock_trig_sw", 0, 1, 0, 0, 15}, /** selects signal for trigger **/
    {"lock_rl_error_threshold", 0, 1, 0, 0,
     8191}, /** Threshold for error signal. Launchs relock when |error| >
               rl_error_threshold **/
    {"lock_rl_signal_sw", 0, 1, 0, 0,
     7}, /** selects signal for relock trigger **/
    {"lock_rl_signal_threshold", 0, 1, 0, -8192,
     8191}, /** Threshold for signal. Launchs relock when signal <
               rl_signal_threshold **/
    {"lock_rl_error_enable", 0, 1, 0, 0,
     1}, /** Relock enable. [enable_error_th]  **/
    {"lock_rl_signal_enable", 0, 1, 0, 0,
     1},                              /** Relock enable. [enable_signal_th]  **/
    {"lock_rl_reset", 0, 1, 0, 0, 1}, /** Relock enable. [relock_reset]  **/
    {"lock_rl_state", 0, 0, 1, 0,
     31}, /** Relock state:
             [state:idle|searching|failed,signal_fail,error_fail,locked]  **/
    {"lock_sf_jumpA", 0, 1, 0, -8192,
     8191}, /** Step function measure jump value for ctrl_A **/
    {"lock_sf_jumpB", 0, 1, 0, -8192,
     8191}, /** Step function measure jump value for ctrl_B **/
    {"lock_sf_start", 0, 1, 0, 0, 1},        /** Step function start  **/
    {"lock_sf_AfrzO", 0, 1, 0, 0, 1},        /** Step function pidA_freeze  **/
    {"lock_sf_AfrzI", 0, 1, 0, 0, 1},        /** Step function pidA_ifreeze  **/
    {"lock_sf_BfrzO", 0, 1, 0, 0, 1},        /** Step function pidB_freeze  **/
    {"lock_sf_BfrzI", 0, 1, 0, 0, 1},        /** Step function pidB_ifreeze  **/
    {"lock_signal_sw", 0, 1, 0, 0, 15},      /** Input selector for signal_i **/
    {"lock_signal_i", 0, 0, 1, -8192, 8191}, /** signal for demodulation **/
    {"lock_sg_amp1", 0, 1, 0, 0, 15},   /** amplification of Xo, Yo and F1o **/
    {"lock_sg_amp2", 0, 1, 0, 0, 15},   /** amplification of F2o **/
    {"lock_sg_amp3", 0, 1, 0, 0, 15},   /** amplification of F3o **/
    {"lock_sg_amp_sq", 0, 1, 0, 0, 15}, /** amplification of SQo **/
    {"lock_lpf_F1_tau", 0, 1, 0, 0,
     15}, /** Low Pass Filter TAU of X, Y and F1 **/
    {"lock_lpf_F1_order", 2, 1, 0, 0, 2}, /** Low Pass Filter order / off **/
    {"lock_lpf_F2_tau", 0, 1, 0, 0, 15},  /** Low Pass Filter TAU of F2 **/
    {"lock_lpf_F2_order", 2, 1, 0, 0, 2}, /** Low Pass Filter order / off **/
    {"lock_lpf_F3_tau", 0, 1, 0, 0, 15},  /** Low Pass Filter TAU of F3 **/
    {"lock_lpf_F3_order", 2, 1, 0, 0, 2}, /** Low Pass Filter order / off **/
    {"lock_lpf_sq_tau", 0, 1, 0, 0, 15},  /** Low Pass Filter TAU of Square **/
    {"lock_lpf_sq_order", 2, 1, 0, 0, 2}, /** Low Pass Filter order / off **/
    {"lock_error_sw", 0, 1, 0, 0, 7},     /** select error signal **/
    {"lock_error_offset", 0, 1, 0, -8192,
     8191},                               /** offset for the error signal **/
    {"lock_error", 0, 0, 1, -8192, 8191}, /** error signal value **/
    {"lock_error_mean", 0, 0, 1, -0x80000000,
     0x7fffffff}, /** 1 sec error mean val **/
    {"lock_error_std", 0, 0, 1, -0x80000000,
     0x7fffffff}, /** 1 sec error square sum val **/
    {"lock_gen_mod_phase", 0, 1, 0, 0,
     2519}, /** phase relation of cos_?f signals **/
    {"lock_gen_mod_phase_sq", 0, 1, 0, 0,
     0xffffffff}, /** phase relation of sq_phas signal **/
    {"lock_gen_mod_hp", 0, 1, 0, 0, 16383},       /** harmonic period set **/
    {"lock_gen_mod_sqp", 0, 1, 0, 0, 0xffffffff}, /** square signal period **/
    {"lock_ramp_A", 0, 0, 1, -8192, 8191},        /** ramp signal A **/
    {"lock_ramp_B", 0, 0, 1, -8192, 8191},        /** ramp signal B **/
    {"lock_ramp_step", 0, 1, 0, 0,
     0xffffffff}, /** period of the triangular ramp signal **/
    {"lock_ramp_low_lim", -5000, 1, 0, -8192, 8191}, /** ramp low limit **/
    {"lock_ramp_hig_lim", 5000, 1, 0, -8192, 8191},  /** ramp high limit **/
    {"lock_ramp_reset", 0, 1, 0, 0, 1},              /** ramp reset config **/
    {"lock_ramp_enable", 0, 1, 0, 0, 1}, /** ramp enable/disable switch **/
    {"lock_ramp_direction", 0, 1, 0, 0,
     1}, /** ramp starting direction (up/down) **/
    {"lock_ramp_B_factor", 4096, 1, 0, -4096,
     4096}, /** proportional factor ramp_A/ramp_B. //
               ramp_B=ramp_A*ramp_B_factor/4096 **/
    {"lock_sin_ref", 0, 0, 1, -8192,
     8191}, /** lock-in modulation sinus harmonic reference **/
    {"lock_cos_ref", 0, 0, 1, -8192,
     8191}, /** lock-in modulation cosinus harmonic reference **/
    {"lock_cos_1f", 0, 0, 1, -8192,
     8191}, /** lock-in modulation sinus harmonic signal with phase relation to
               reference **/
    {"lock_cos_2f", 0, 0, 1, -8192,
     8191}, /** lock-in modulation sinus harmonic signal with phase relation to
               reference and double frequency **/
    {"lock_cos_3f", 0, 0, 1, -8192,
     8191}, /** lock-in modulation sinus harmonic signal with phase relation to
               reference and triple frequency **/
    {"lock_sq_ref_b", 0, 0, 1, 0,
     1}, /** lock-in modulation binary reference **/
    {"lock_sq_quad_b", 0, 0, 1, 0,
     1}, /** lock-in modulation binary quadrature **/
    {"lock_sq_phas_b", 0, 0, 1, 0,
     1}, /** lock-in modulation binary with phase respect to reference **/
    {"lock_sq_ref", 0, 0, 1, -8192,
     8191}, /** lock-in modulation square signal reference **/
    {"lock_sq_quad", 0, 0, 1, -8192,
     8191}, /** lock-in modulation square signal quadrature **/
    {"lock_sq_phas", 0, 0, 1, -8192,
     8191}, /** lock-in modulation square signal with phase relation to
               reference **/
    {"lock_in1", 0, 0, 1, -8192, 8191},       /** Input signal IN1 **/
    {"lock_in2", 0, 0, 1, -8192, 8191},       /** Input signal IN2 **/
    {"lock_out1", 0, 0, 1, -8192, 8191},      /** signal for RP RF DAC Out1 **/
    {"lock_out2", 0, 0, 1, -8192, 8191},      /** signal for RP RF DAC Out2 **/
    {"lock_slow_out1", 0, 0, 1, -2048, 2047}, /** signal for RP slow DAC 1 **/
    {"lock_slow_out2", 0, 0, 1, -2048, 2047}, /** signal for RP slow DAC 2 **/
    {"lock_slow_out3", 0, 0, 1, -2048, 2047}, /** signal for RP slow DAC 3 **/
    {"lock_slow_out4", 0, 0, 1, -2048, 2047}, /** signal for RP slow DAC 4 **/
    {"lock_oscA", 0, 0, 1, -8192,
     8191}, /** signal for Oscilloscope Channel A **/
    {"lock_oscB", 0, 0, 1, -8192,
     8191}, /** signal for Oscilloscope Channel B **/
    {"lock_X", 0, 0, 1, -134217728,
     134217727}, /** Demodulated signal from sin_ref **/
    {"lock_Y", 0, 0, 1, -134217728,
     134217727}, /** Demodulated signal from cos_ref **/
    {"lock_F1", 0, 0, 1, -134217728,
     134217727}, /** Demodulated signal from cos_1f **/
    {"lock_F2", 0, 0, 1, -134217728,
     134217727}, /** Demodulated signal from cos_2f **/
    {"lock_F3", 0, 0, 1, -134217728,
     134217727}, /** Demodulated signal from cos_3f **/
    {"lock_sqX", 0, 0, 1, -134217728,
     134217727}, /** Demodulated signal from sq_ref **/
    {"lock_sqY", 0, 0, 1, -134217728,
     134217727}, /** Demodulated signal from sq_quad **/
    {"lock_sqF", 0, 0, 1, -134217728,
     134217727}, /** Demodulated signal from sq_phas **/
    {"lock_cnt_clk", 0, 0, 1, 0, 0xffffffff},  /** Clock count **/
    {"lock_cnt_clk2", 0, 0, 1, 0, 0xffffffff}, /** Clock count **/
    {"lock_read_ctrl", 0, 1, 0, 0, 7},         /** [unused,start_clk,Freeze] **/
    {"lock_pidA_sw", 0, 1, 0, 0, 31},   /** switch selector for pidA input **/
    {"lock_pidA_PSR", 3, 1, 0, 0, 4},   /** pidA PSR **/
    {"lock_pidA_ISR", 8, 1, 0, 0, 9},   /** pidA ISR **/
    {"lock_pidA_DSR", 0, 1, 0, 0, 5},   /** pidA DSR **/
    {"lock_pidA_SAT", 13, 1, 0, 0, 13}, /** pidA saturation control **/
    {"lock_pidA_sp", 0, 1, 0, -8192, 8191},  /** pidA set_point **/
    {"lock_pidA_kp", 0, 1, 0, -8192, 8191},  /** pidA proportional constant **/
    {"lock_pidA_ki", 0, 1, 0, -8192, 8191},  /** pidA integral constant **/
    {"lock_pidA_kd", 0, 1, 0, -8192, 8191},  /** pidA derivative constant **/
    {"lock_pidA_in", 0, 0, 1, -8192, 8191},  /** pidA input **/
    {"lock_pidA_out", 0, 0, 1, -8192, 8191}, /** pidA output **/
    {"lock_pidA_irst", 0, 1, 0, 0, 1},       /** pidA_irst **/
    {"lock_pidA_freeze", 0, 1, 0, 0, 1},     /** pidA_freeze **/
    {"lock_pidA_ifreeze", 0, 1, 0, 0, 1},    /** pidA_ifreeze **/
    {"lock_ctrl_A", 0, 0, 1, -8192, 8191}, /** control_A: pidA_out + ramp_A **/
    {"lock_pidB_sw", 0, 1, 0, 0, 31},   /** switch selector for pidB input **/
    {"lock_pidB_PSR", 3, 1, 0, 0, 4},   /** pidB PSR **/
    {"lock_pidB_ISR", 8, 1, 0, 0, 9},   /** pidB ISR **/
    {"lock_pidB_DSR", 0, 1, 0, 0, 5},   /** pidB DSR **/
    {"lock_pidB_SAT", 13, 1, 0, 0, 13}, /** pidB saturation control **/
    {"lock_pidB_sp", 0, 1, 0, -8192, 8191},  /** pidB set_point **/
    {"lock_pidB_kp", 0, 1, 0, -8192, 8191},  /** pidB proportional constant **/
    {"lock_pidB_ki", 0, 1, 0, -8192, 8191},  /** pidB integral constant **/
    {"lock_pidB_kd", 0, 1, 0, -8192, 8191},  /** pidB derivative constant **/
    {"lock_pidB_in", 0, 0, 1, -8192, 8191},  /** pidB input **/
    {"lock_pidB_out", 0, 0, 1, -8192, 8191}, /** pidB output **/
    {"lock_pidB_irst", 0, 1, 0, 0, 1},       /** pidB_irst **/
    {"lock_pidB_freeze", 0, 1, 0, 0, 1},     /** pidB_freeze **/
    {"lock_pidB_ifreeze", 0, 1, 0, 0, 1},    /** pidB_ifreeze **/
    {"lock_ctrl_B", 0, 0, 1, -8192, 8191}, /** control_B: pidA_out + ramp_B **/
    {"lock_aux_A", 0, 1, 0, -8192, 8191},  /** auxiliar value of 14 bits **/
    {"lock_aux_B", 0, 1, 0, -8192, 8191},  /** auxiliar value of 14 bits **/
    {"lock_ctrl_aux_lock_now", 0, 0, 0, 0, 1},         /** todo **/
    {"lock_ctrl_aux_launch_lock_trig", 0, 0, 0, 0, 1}, /** todo **/
    {"lock_ctrl_aux_pidB_enable_ctrl", 1, 0, 0, 0, 1}, /** todo **/
    {"lock_ctrl_aux_pidA_enable_ctrl", 1, 0, 0, 0, 1}, /** todo **/
    {"lock_ctrl_aux_ramp_enable_ctrl", 1, 0, 0, 0, 1}, /** todo **/
    {"lock_ctrl_aux_set_pidB_enable", 1, 0, 0, 0, 1},  /** todo **/
    {"lock_ctrl_aux_set_pidA_enable", 1, 0, 0, 0, 1},  /** todo **/
    {"lock_ctrl_aux_set_ramp_enable", 0, 0, 0, 0, 1},  /** todo **/
    {"lock_ctrl_aux_trig_type", 0, 0, 0, 0, 3},        /** todo **/
    {"lock_ctrl_aux_lock_trig_rise", 0, 0, 0, 0, 1},   /** todo **/
    {"lock_mod_sq_on", 0, 0, 0, 0, 1},                 /** todo **/
    {"lock_mod_harmonic_on", 1, 0, 0, 0, 1},           /** todo **/

    // [MAINDEF DOCK END]

    {/* Must be last! */
     NULL, 0.0, -1, -1, 0.0, 0.0}};
/* params initialized */
// static int params_init = 0;

/* @brief Pointer to data buffer where signal on channel A is captured.  */
static uint32_t *g_osc_fpga_cha_mem = NULL;

/* @brief Pointer to data buffer where signal on channel B is captured.  */
static uint32_t *g_osc_fpga_chb_mem = NULL;

/* @brief The memory file descriptor used to mmap() the OSC FPGA space. */
static int g_osc_fpga_mem_fd = -1;

/* @brief The memory file descriptor used to mmap() the AMS FPGA space. */
// static int                 g_ams_fpga_mem_fd = -1;

/* @brief Number of ADC acquisition bits.  */
// const int                  c_osc_fpga_adc_bits = 14;

/* @brief Sampling frequency = 125Mspmpls (non-decimated). */
// const float                c_osc_fpga_smpl_freq = 125e6;

/* @brief Sampling period (non-decimated) - 8 [ns]. */
// const float                c_osc_fpga_smpl_period = (1. / 125e6);

/* Signals directly pointing at the FPGA mem space */
int *rp_fpga_cha_signal, *rp_fpga_chb_signal;

/* memory buffers we reserve to receive the data from the buffers */
int *chAbuff = NULL;
int *chBbuff = NULL;

/* the number of points we use for averaging in channels A and B*/
// the default values correspond to 1ms for a decimation of 64
uint32_t avgA = 1953, avgB = 1953;
/* the time steps between updating the pin out value(s) corresponding to an
   average over the full osci buffer(s) */
// the default time step is 8ms, which approximately fits with a
// decimation of 64 (1.953 MS/s)
int avgTslow = 8;
// the default time step is 8ms, after that, we will average the input and
// output it on a fast output channel.
int avgTfast = 8;
/* this indicates the channels we are averaging. If the first bit
   is 1, we average for channel A, if the second bit is 1, we average
   channel B.
   That means, a value of 0 means we are not averaging anything, 1 or 2
   mean we average channel A or B, respectively, 3 means we do averaging
   for both channels. */
int averaging_slow = 0;
/* number of the input channel we will average to generate output */
int averaging_fast_in = -1;
/* number of the output channel we will use to output the averaged input
 * signal (0 or 1) */
int averaging_fast_out = -1;
// the following variables specify which output pin we will set voltage on
// corresponding to the averaged values on the input channels A and B
// if the value is -1, we will not produce an output
int avgApin = -1;
int avgBpin = -1;

rp_ext_calib_params_t mycalib;

/*
turning off averaging and freeing memory we reserved for that purpose
*/
int cleanupSlowAveraging(void) {
  averaging_slow = 0;
  avgTslow = 8;
  avgApin = -1;
  avgBpin = -1;
  if (ams_Release() < 0) {
    fprintf(stderr, "could not release AMS. The error was: %s\n",
            strerror(errno));
    return -1;
  }

  return 0;
}

/*
    this sets everything up to average the signal(s) on one or more of
    the osci channels.  
    this indicates the channels we are averaging. If the first bit
    is 1, we average for channel A, if the second bit is 1, we average
    channel B.
    That means, a value of 0 means we are not averaging anything, 1 or 2
    mean we average channel A or B, respectively, 3 means we do averaging
    for both channels.  
    the averaging time is in MILLISECONDS 
*/
int initSlowAverage(int avgMode, int avgTime, int pinA, int pinB) {
  uint32_t dec = g_osc_fpga_reg_mem->data_dec;
  float dt;

  if (avgMode == 0) {
    cleanupSlowAveraging();
    return 0; // no error
  }
  if (avgTime < 1) {
    fprintf(stderr, "The averaging time has to be positive.\n");
    return -1;
  }
  if (pinA > 3 || pinB > 3) {
    fprintf(stderr,
            "one of the pin numbers (%d,%d) you supplied is"
            " invalid. Has to be in [0,3].\n",
            pinA, pinB);
    return -1;
  }

  avgApin = pinA;
  avgBpin = pinB;
  averaging_slow = avgMode;

  switch (dec) {
  case 0:
    dt = 1 / (1.25e8);
    break;
  case 8:
    dt = 1 / (1.56e7);
    break;
  case 64:
    dt = 1 / (1.953e6);
    break;
  case 1024:
    dt = 1 / (1.2207e5);
    break;
  case 8192:
    dt = 1 / (1.5258e4);
    break;
  case 65536:
    dt = 1 / (1.907e3);
    break;
  default:
    fprintf(stderr,
            "Something is wrong with the decimation "
            "factor we got: %u.\n The error was: %s\n",
            dec, strerror(errno));
    return -1;
  }
  // get the averaging time from the decimation. Because avgT is in ms
  // and dt is in seconds, we need to multiply dt by 1e3
  avgTslow = dt * 1e3 * ((float)OSC_FPGA_SIG_LEN);
  fprintf(stderr, "set an averaging time of %d ms.\n", avgTslow);

  if (ams_Init() < 0) {

    fprintf(stderr, "could not init AMS. The error was: %s\n", strerror(errno));
    return -1;
  }

  return 0;
}

int cleanup_mem(void) {
  int ret = 0;

  cleanupSlowAveraging();

  /* optionally unmap memory regions  */
  if (g_osc_fpga_reg_mem) {
    if (munmap(g_osc_fpga_reg_mem, OSC_FPGA_BASE_SIZE) < 0) {
      fprintf(stderr, "munmap() failed: %s\n", strerror(errno));
      ret = -1;
    } else {
      /* ...and update memory pointers */
      g_osc_fpga_reg_mem = NULL;
      g_osc_fpga_cha_mem = NULL;
      g_osc_fpga_chb_mem = NULL;
    }
  }

  /* optionally close file descriptor */
  if (g_osc_fpga_mem_fd >= 0) {
    close(g_osc_fpga_mem_fd);
    g_osc_fpga_mem_fd = -1;
  }

  if (__awg_cleanup_mem() != 0) {
    if (ret == -1) {
      ret = -3;
    } else {
      ret = -2;
    }
  }

  if (chAbuff) {
    free(chAbuff);
  }
  if (chBbuff) {
    free(chBbuff);
  }

  return ret;
}

/* the following function was adapted from 'fpga.c' that was included in the
 * source code for the RP PID module */
int my_osc_fpga_init(void) {
  void *page_ptr;
  long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);
  int ret;

  /* If maybe needed, cleanup the FD & memory pointer */
  if (cleanup_mem() < 0)
    return -1;

  if (osc_fpga_init() < 0) {
    return -1;
  }

  ret = rp_read_calib_params(&mycalib);
  if (ret == -1) {
    printf("error in reading the RP calibration. Exiting.\n");
    return -1;
  } else if (ret != 0) {
    printf("unknown error. Exiting.\n");
    return -1;
  }
  printf("calibration DC offset, ch1: %d\n", mycalib.fe_ch1_dc_offs);
  printf("calibration DC offset, ch2: %d\n", mycalib.fe_ch2_dc_offs);

  g_osc_fpga_mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
  if (g_osc_fpga_mem_fd < 0) {
    fprintf(stderr, "open(/dev/mem) failed: %s\n", strerror(errno));
    return -1;
  }

  page_addr = OSC_FPGA_BASE_ADDR & (~(page_size - 1));
  page_off = OSC_FPGA_BASE_ADDR - page_addr;

  page_ptr = mmap(NULL, OSC_FPGA_BASE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
                  g_osc_fpga_mem_fd, page_addr);
  if ((void *)page_ptr == MAP_FAILED) {
    fprintf(stderr, "mmap() failed: %s\n", strerror(errno));
    cleanup_mem();
    return -1;
  }
  g_osc_fpga_reg_mem = page_ptr + page_off;
  g_osc_fpga_cha_mem =
      (uint32_t *)g_osc_fpga_reg_mem + (OSC_FPGA_CHA_OFFSET / sizeof(uint32_t));
  g_osc_fpga_chb_mem =
      (uint32_t *)g_osc_fpga_reg_mem + (OSC_FPGA_CHB_OFFSET / sizeof(uint32_t));

  my_osc_fpga_get_sig_ptr(&rp_fpga_cha_signal, &rp_fpga_chb_signal);

  chAbuff = (int *)malloc(sizeof(int) * OSC_FPGA_SIG_LEN);
  if (chAbuff == NULL) {
    fprintf(stderr, "malloc failed for channel A: %s\n", strerror(errno));
    cleanup_mem();
    return -1;
  }
  chBbuff = (int *)malloc(sizeof(int) * OSC_FPGA_SIG_LEN);
  if (chBbuff == NULL) {
    fprintf(stderr, "malloc failed for channel B: %s\n", strerror(errno));
    cleanup_mem();
    return -1;
  }

  return 0;
}

/*----------------------------------------------------------------------------------*/
/** @brief Initialize Arbitrary Signal Generator module
 *
 * A function is intended to be called within application initialization. It's
 * purpose is to remember a specified pointer to calibration parameters, to
 * initialie Arbitrary Waveform Generator module and to calculate maximal
 * voltage, which can be applied on DAC device on individual channel.
 *
 * @param[in]  calib_params  pointer to calibration parameters
 * @retval     -1 failure, error message is reported on standard error
 * @retval      0 successful initialization
 */

int my_generate_init(rp_ext_calib_params_t *calib_params) {
  if (fpga_awg_init() < 0) {
    return -1;
  }

  ch1_max_dac_v = fpga_awg_calc_dac_max_v(calib_params->be_ch1_fs);
  ch2_max_dac_v = fpga_awg_calc_dac_max_v(calib_params->be_ch2_fs);
  return 0;
}

int my_rp_init(void) {
  fprintf(stderr, "initializing RP\n");

  rp_default_calib_params(&rp_main_calib_params);
  if (rp_read_calib_params(&rp_main_calib_params) < 0) {
    fprintf(stderr, "rp_read_calib_params() failed, using default"
                    "parameters\n");
  }

  fprintf(stderr, "I will now initialize the Osci on the RP\n");

  if (my_osc_fpga_init() < 0) {
    fprintf(stderr, "osc initialization failed.\n");
    return -1;
  }
  fprintf(stderr, "I will now initialize the Worker on the RP\n");
  if (rp_osc_worker_init(&rp_main_params[0], PARAMS_NUM,
                         &rp_main_calib_params) < 0) {
    return -1;
  }
  // using the second output for outputting the voltage for the
  // slow lock
  fprintf(stderr, "I will now initialize the AWG on the RP\n");
  if (generate_init(&rp_main_calib_params) < 0) {
    fprintf(stderr, "awg initialization failed.\n");
    return -1;
  }

  return 0;
}

/**
 * @brief Retrieve the address of channel A,B memory buffers
 *
 * NOTE: no check is made if argumments are correctly specified.
 *
 * @param[out] cha_signal Pointer to channel A memory buffer
 * @param[out] chb_signal Pointer to channel B memory buffer
 * @retval 0 Success, never fails
 */
int my_osc_fpga_get_sig_ptr(int **cha_signal, int **chb_signal) {
  *cha_signal = (int *)g_osc_fpga_cha_mem;
  *chb_signal = (int *)g_osc_fpga_chb_mem;
  return 0;
}

/*----------------------------------------------------------------------------*/
/**
 * @brief Retrieve Memory buffer Write pointer information
 *
 * @param[out] wr_ptr_curr offset to the currently captured signal atom
 * @param[out] wr_ptr_trig offset to signal atom, captured at detected trigger
 * @retval 0 Success, never fails
 */
int my_osc_fpga_get_wr_ptr(int *wr_ptr_curr, int *wr_ptr_trig) {
  if (wr_ptr_curr)
    *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
  if (wr_ptr_trig)
    *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
  return 0;
}

/* takes the data stored in our internal buffer for channel A or B (0 or 1 for
   ch and returns the average of that buffer */
float avg_osc(int ch, float adc_max_v, int calib_dc_off, float user_dc_off) {
  int m, i, *mybuff, cnm1 = 1 << (c_osc_fpga_adc_bits - 1),
                     cn = 1 << (c_osc_fpga_adc_bits);
  float f, val = 0.0;
  f = adc_max_v / ((float)cnm1);

  if (ch) {
    mybuff = rp_fpga_chb_signal;
  } else {
    mybuff = rp_fpga_cha_signal;
  }

  for (i = 0; i < OSC_FPGA_SIG_LEN; i++) {
    /* check sign */
    if (mybuff[i] & cnm1) {
      /* negative number */
      m = -1 * ((mybuff[i] ^ (cn - 1)) + 1);
    } else {
      /* positive number */
      m = mybuff[i];
    }

    /* adopt ADC count with calibrated DC offset */
    m += calib_dc_off;

    /* map ADC counts into user units */
    if (m < (-1 * cnm1)) {
      m = (-1 * cnm1);
    } else if (m > cnm1) {
      m = cnm1;
    }

    val += f * m + user_dc_off;
  }

  return val / ((float)OSC_FPGA_SIG_LEN);
}

/*----------------------------------------------------------------------------*/
/**
 * @brief Converts ADC counts to voltage [V]
 *
 * Function is used to publish captured signal data to external world in user
 * units. Calculation is based on maximal voltage, which can be applied on ADC
 * inputs and calibrated and user defined DC offsets.
 *
 * @param[in] cnts           Captured Signal Value, expressed in ADC counts
 * @param[in] adc_max_v      Maximal ADC voltage, specified in [V]
 * @param[in] calib_dc_off   Calibrated DC offset, specified in ADC counts
 * @param[in] user_dc_off    User specified DC offset, specified in [V]
 * @retval    float         Signal Value, expressed in user units [V]
 */
float my_osc_fpga_cnv_cnt_to_v(int cnts, float adc_max_v, int calib_dc_off,
                               float user_dc_off) {
  int m;
  float ret_val;

  /* check sign */
  if (cnts & (1 << (c_osc_fpga_adc_bits - 1))) {
    /* negative number */
    m = -1 * ((cnts ^ ((1 << c_osc_fpga_adc_bits) - 1)) + 1);
  } else {
    /* positive number */
    m = cnts;
  }

  /* adopt ADC count with calibrated DC offset */
  m += calib_dc_off;

  /* map ADC counts into user units */
  if (m < (-1 * (1 << (c_osc_fpga_adc_bits - 1))))
    m = (-1 * (1 << (c_osc_fpga_adc_bits - 1)));
  else if (m > (1 << (c_osc_fpga_adc_bits - 1)))
    m = (1 << (c_osc_fpga_adc_bits - 1));

  ret_val = (m * adc_max_v / (float)(1 << (c_osc_fpga_adc_bits - 1)));

  /* and adopt the calculation with user specified DC offset */
  ret_val += user_dc_off;
  return ret_val;
}

/* the following calls osc_fpga_cnv_cnt_to_v for all elements we copied from
 * the buffer to our own buffer memories (chAbuff and chBbuff), and it
 * puts the results in the arrays pointed to by chAout and chBout.
 *
 * The buffers in that output pointers MUST be sufficiently long!!!
 */
int my_osc_cnv_cnt_to_v_chA_int(float *chAout, float adc_max_v,
                                int calib_dc_off) {
  int m, i, cnm1 = 1 << (c_osc_fpga_adc_bits - 1),
            cn = 1 << (c_osc_fpga_adc_bits);
  float r, f;
  f = adc_max_v / ((float)cnm1);
  // printf("f: %f\n",f);

  for (i = 0; i < OSC_FPGA_SIG_LEN; i++) {
    /* check sign */
    if (chAbuff[i] & cnm1) {
      /* negative number */
      m = -1 * ((chAbuff[i] ^ (cn - 1)) + 1);
    } else {
      /* positive number */
      m = chAbuff[i];
    }

    /* adopt ADC count with calibrated DC offset */
    m += calib_dc_off;

    /* map ADC counts into user units */
    if (m < (-1 * cnm1)) {
      m = (-1 * cnm1);
    } else if (m > cnm1) {
      m = cnm1;
    }

    r = f * m;

    /* and adopt the calculation with user specified DC offset */
    chAout[i] = r;
  }

  return 0;
}

/* the following calls osc_fpga_cnv_cnt_to_v for all elements we copied from
 * the buffer to our own buffer memories (chAbuff and chBbuff), and it
 * puts the results in the arrays pointed to by chAout and chBout.
 *
 * the OFFSET in this case is a float because it is directly added to the
 * converted voltage value - not to the integer value
 *
 * The buffers in that output pointers MUST be sufficiently long!!!
 */
int my_osc_cnv_cnt_to_v_chA(float *chAout, float adc_max_v, float dc_off) {
  int m, i, cnm1 = 1 << (c_osc_fpga_adc_bits - 1),
            cn = 1 << (c_osc_fpga_adc_bits);
  float r, f;
  f = adc_max_v / ((float)cnm1);
  // printf("f: %f\n",f);

  for (i = 0; i < OSC_FPGA_SIG_LEN; i++) {
    /* check sign */
    if (chAbuff[i] & cnm1) {
      /* negative number */
      m = -1 * ((chAbuff[i] ^ (cn - 1)) + 1);
    } else {
      /* positive number */
      m = chAbuff[i];
    }

    /* map ADC counts into user units */
    if (m < (-1 * cnm1)) {
      m = (-1 * cnm1);
    } else if (m > cnm1) {
      m = cnm1;
    }

    r = f * m + dc_off;

    if (r < adc_max_v) {
      r = adc_max_v;
    } else if (r > adc_max_v) {
      r = -adc_max_v;
    }

    /* and adopt the calculation with user specified DC offset */
    chAout[i] = f * m + dc_off;
  }

  return 0;
}

/* the following calls osc_fpga_cnv_cnt_to_v for all elements we copied from
 * the buffer to our own buffer memories (chAbuff and chBbuff), and it
 * puts the results in the arrays pointed to by chAout and chBout.
 *
 * The buffers in that output pointers MUST be sufficiently long!!!
 */
int my_osc_cnv_cnt_to_v_chs(float *chAout, float *chBout, float adc_max_v,
                            int calib_dc_off) {
  int m, i, cnm1 = 1 << (c_osc_fpga_adc_bits - 1),
            cn = 1 << (c_osc_fpga_adc_bits);
  float r, f;
  f = adc_max_v / ((float)cnm1);
  // printf("f: %f\n",f);

  for (i = 0; i < OSC_FPGA_SIG_LEN; i++) {
    /* check sign */
    if (chAbuff[i] & cnm1) {
      /* negative number */
      m = -1 * ((chAbuff[i] ^ (cn - 1)) + 1);
    } else {
      /* positive number */
      m = chAbuff[i];
    }

    /* adopt ADC count with calibrated DC offset */
    m += calib_dc_off;

    /* map ADC counts into user units */
    if (m < (-1 * cnm1)) {
      m = (-1 * cnm1);
    } else if (m > cnm1) {
      m = cnm1;
    }

    r = f * m;
    /*if ( i==0 )
    {
      printf("branch 1: %d\n", m);
      printf("dc offs: %f\n", user_dc_off);
      printf("r before: %f\n", r);
    }*/

    /* and adopt the calculation with user specified DC offset */
    chAout[i] = r;
    /*if ( i==0 )
    {
      printf("r after: %f\n", r);
      printf("chBout[0]: %f\n", chBout[i]);
    }*/

    /* check sign */
    if (chBbuff[i] & cnm1) {
      /* negative number */
      m = -1 * ((chBbuff[i] ^ (cn - 1)) + 1);
    } else {
      /* positive number */
      m = chBbuff[i];
    }

    /* adopt ADC count with calibrated DC offset */
    m += calib_dc_off;

    /* map ADC counts into user units */
    if (m < (-1 * cnm1))
      m = (-1 * cnm1);
    else if (m > cnm1)
      m = cnm1;

    r = f * m;
    /*if ( i==0 )
    {
      printf("branch 2: %d\n", m);
      printf("dc offs: %f\n", user_dc_off);
      printf("r before: %f\n", r);
    }*/

    /* and adopt the calculation with user specified DC offset */
    chBout[i] = r;
    /*if ( i==0 )
    {
      printf("r after: %f\n", r);
      printf("chBout[0]: %f\n", chBout[i]);
    }*/
  }

  return 0;
}

/* the following calls osc_fpga_cnv_cnt_to_v for all elements we copied from
 * the buffer to our own buffer memories (chAbuff and chBbuff), and it
 * puts the results in the arrays pointed to by chAout and chBout.
 *
 * The buffers in that output pointers MUST be sufficiently long!!!
 */
int my_osc_cnv_cnt_to_v_chs_backup(float *chAout, float *chBout,
                                   float adc_max_v, int calib_dc_off,
                                   float user_dc_off) {
  int m, i, cnm1 = 1 << (c_osc_fpga_adc_bits - 1),
            cn = 1 << (c_osc_fpga_adc_bits);
  float r, f;
  f = adc_max_v / ((float)cnm1);
  // printf("f: %f\n",f);

  for (i = 0; i < OSC_FPGA_SIG_LEN; i++) {
    /* check sign */
    if (chAbuff[i] & cnm1) {
      /* negative number */
      m = -1 * ((chAbuff[i] ^ (cn - 1)) + 1);
    } else {
      /* positive number */
      m = chAbuff[i];
    }

    /* adopt ADC count with calibrated DC offset */
    m += calib_dc_off;

    /* map ADC counts into user units */
    if (m < (-1 * cnm1)) {
      m = (-1 * cnm1);
    } else if (m > cnm1) {
      m = cnm1;
    }

    r = f * m;
    /*if ( i==0 )
    {
      printf("branch 1: %d\n", m);
      printf("dc offs: %f\n", user_dc_off);
      printf("r before: %f\n", r);
    }*/

    /* and adopt the calculation with user specified DC offset */
    r += user_dc_off;
    chAout[i] = r;
    /*if ( i==0 )
    {
      printf("r after: %f\n", r);
      printf("chBout[0]: %f\n", chBout[i]);
    }*/

    /* check sign */
    if (chBbuff[i] & cnm1) {
      /* negative number */
      m = -1 * ((chBbuff[i] ^ (cn - 1)) + 1);
    } else {
      /* positive number */
      m = chBbuff[i];
    }

    /* adopt ADC count with calibrated DC offset */
    m += calib_dc_off;

    /* map ADC counts into user units */
    if (m < (-1 * cnm1))
      m = (-1 * cnm1);
    else if (m > cnm1)
      m = cnm1;

    r = f * m;
    /*if ( i==0 )
    {
      printf("branch 2: %d\n", m);
      printf("dc offs: %f\n", user_dc_off);
      printf("r before: %f\n", r);
    }*/

    /* and adopt the calculation with user specified DC offset */
    r += user_dc_off;
    chBout[i] = r;
    /*if ( i==0 )
    {
      printf("r after: %f\n", r);
      printf("chBout[0]: %f\n", chBout[i]);
    }*/
  }

  return 0;
}

/* adc_max_v is 1 for the +/- 1V range, and 20 for the +/- 20V range */
int rp_get_signalA(float *chA, int *wr_ptr_curr, int *wr_ptr_trig,
                   float adc_max_v, float dc_off) {
  if (!wr_ptr_curr || !wr_ptr_trig) {
    return -1; // those should be valid references
  }
  for (int i = 0; i < OSC_FPGA_SIG_LEN; i++) {
    chAbuff[i] = rp_fpga_cha_signal[i];
    if (i == g_osc_fpga_reg_mem->wr_ptr_cur) {
      *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
      *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
    }
  }
  // osc_cnv_cnt_to_v_chA(chA, factor, -mycalib.fe_ch1_dc_offs);
  my_osc_cnv_cnt_to_v_chA(chA, adc_max_v, dc_off);

  return 0;
}

/* adc_max_v is 1 for the +/- 1V range, and 20 for the +/- 20V range */
int rp_get_signalA_intOff(float *chA, int *wr_ptr_curr, int *wr_ptr_trig,
                          float adc_max_v, int dc_off) {
  if (!wr_ptr_curr || !wr_ptr_trig) {
    return -1; // those should be valid references
  }
  for (int i = 0; i < OSC_FPGA_SIG_LEN; i++) {
    chAbuff[i] = rp_fpga_cha_signal[i];
    if (i == g_osc_fpga_reg_mem->wr_ptr_cur) {
      *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
      *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
    }
  }
  // osc_cnv_cnt_to_v_chA(chA, factor, -mycalib.fe_ch1_dc_offs);
  my_osc_cnv_cnt_to_v_chA_int(chA, adc_max_v, dc_off);

  return 0;
}

int my_rp_get_signals(float *chA, float *chB, int *wr_ptr_curr,
                      int *wr_ptr_trig, float factor) {
  if (!wr_ptr_curr || !wr_ptr_trig) {
    return -1; // those should be valid references
  }
  for (int i = 0; i < OSC_FPGA_SIG_LEN; i++) {
    chAbuff[i] = rp_fpga_cha_signal[i];
    chBbuff[i] = rp_fpga_chb_signal[i];
    if (i == g_osc_fpga_reg_mem->wr_ptr_cur) {
      *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
      *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
    }
  }
  my_osc_cnv_cnt_to_v_chs(chA, chB, factor, 0);

  return 0;
}

int rp_copy_signals(int *chA, int *chB, int *rpChA, int *rpChB) {
  memcpy(chA, rpChA, sizeof(int) * OSC_FPGA_SIG_LEN);
  memcpy(chB, rpChB, sizeof(int) * OSC_FPGA_SIG_LEN);

  return 0;
}

int rp_get_fast_new(float *chA, float *chB, int *wr_ptr_curr, int *wr_ptr_trig,
                    float factor) {
  if (!wr_ptr_curr || !wr_ptr_trig) {
    return -1; // those should be valid references
  }
  *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
  *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
  memcpy((void *)chAbuff, (void *)g_osc_fpga_cha_mem,
         sizeof(int) * OSC_FPGA_SIG_LEN);
  memcpy((void *)chBbuff, (void *)g_osc_fpga_chb_mem,
         sizeof(int) * OSC_FPGA_SIG_LEN);

  my_osc_cnv_cnt_to_v_chs(chA, chB, factor, 0);

  printf("factor: %f\n", factor);
  printf("size of float: %d\n", (int)sizeof(float));
  printf("size of double: %d\n", (int)sizeof(double));
  /*
  for(int i=0; i<OSC_FPGA_SIG_LEN; i++)
  {
    chA[i] = osc_fpga_cnv_cnt_to_v(chAbuff[i],
  (float)(1<<(c_osc_fpga_adc_bits-1)), 0, 0); chB[i] =
  osc_fpga_cnv_cnt_to_v(chBbuff[i], (float)(1<<(c_osc_fpga_adc_bits-1)), 0, 0);
  }
  */
  // memcpy((void*)chA, (void*)rp_fpga_cha_signal,
  // sizeof(int)*OSC_FPGA_SIG_LEN); memcpy((void*)chB,
  // (void*)rp_fpga_chb_signal, sizeof(int)*OSC_FPGA_SIG_LEN);

  return 0;
}

/**
 * GET current PID settings
 *
 *
 * @param[in] params  Pointer to overall configuration parameters
 * @retval -1 failure, error message is repoted on standard error device
 * @retval  0 succesful update
 */
int my_pid_update(rp_app_params_t *params) {
  int i;

  pid_param_t pid[NUM_OF_PIDS] = {{0}};
  uint32_t ireset = 0;

  for (i = 0; i < NUM_OF_PIDS; i++) {
    /* PID enabled? */
    if (params[PID_11_ENABLE + i * PARAMS_PER_PID].value == 1) {
      pid[i].kp = (int)params[PID_11_KP + i * PARAMS_PER_PID].value;
      pid[i].ki = (int)params[PID_11_KI + i * PARAMS_PER_PID].value;
      pid[i].kd = (int)params[PID_11_KD + i * PARAMS_PER_PID].value;
    }

    g_pid_reg->pid[i].setpoint =
        (int)params[PID_11_SP + i * PARAMS_PER_PID].value;
    g_pid_reg->pid[i].kp = pid[i].kp;
    g_pid_reg->pid[i].ki = pid[i].ki;
    g_pid_reg->pid[i].kd = pid[i].kd;

    if (params[PID_11_RESET + i * PARAMS_PER_PID].value == 1) {
      ireset |= (1 << i);
    }
  }

  g_pid_reg->configuration = ireset;

  return 0;
}

// maxVin is the max voltage (1V or 20V) on the input
// maxVout is the max voltage (1V or 20V) on the output
int output_average_fast(int chIn, int chOut, float maxVin, float offsetIn,
                        float offsetOut) {
  float maxVout = 1.0, av = 0.0, f = 1.0, k_norm = 1.0;
  int32_t dc_offs = 0;
  const int c_dac_max = (1 << (c_awg_fpga_dac_bits - 1)) - 1;
  const int c_dac_min = -(1 << (c_awg_fpga_dac_bits - 1));
  int mode_mask = 0, awgoffsgain=0, step = 0, wrap = 0, offsgain = 0, user_dc_off_cnt = 0,
      outdata = 0;
  uint32_t state_machine = 0;
  double freq = 1e3 / avgTfast; // avg frequency in Hz

  f = maxVout / maxVin;
  if (maxVin < 1.0) {
    fprintf(stderr,
            "you supplied a wrong maximum voltage - should be"
            "1V or 20V. You supplied %f V.\n",
            maxVin);
    return -1;
  }
  if (chIn < 0 || chIn > 1 || chOut < 0 || chOut > 1) {
    fprintf(stderr,
            "you supplied faulty channel numbers: chIn == %d, "
            "chOut == %d.\n",
            chIn, chOut);
    return -1;
  }
  if (offsetIn < -maxVin || offsetIn > maxVin) {
    fprintf(stderr, "you supplied a weird offset (%f V).", offsetIn);
    return -1;
  }
  if (chIn == 0) {
    dc_offs = mycalib.fe_ch1_dc_offs;
    user_dc_off_cnt =
        round((1 << (c_awg_fpga_dac_bits - 1)) * offsetIn / ch1_max_dac_v);
  }
  if (chIn == 1) {
    dc_offs = mycalib.fe_ch2_dc_offs;
    user_dc_off_cnt =
        round((1 << (c_awg_fpga_dac_bits - 1)) * offsetIn / ch2_max_dac_v);
  }
  if (g_awg_reg) {
    state_machine = g_awg_reg->state_machine_conf;
  }

  offsgain = dc_offs + user_dc_off_cnt;
  offsgain = (offsgain > c_dac_max) ? c_dac_max : offsgain;
  offsgain = (offsgain < c_dac_min) ? c_dac_min : offsgain;
  awgoffsgain = (offsgain << 16) | 0x2000;
  step = round(65536.0 * freq / c_awg_smpl_freq * ((float)AWG_SIG_LEN));
  wrap = round(65536 * (AWG_SIG_LEN - 1));
  // wrap = 0;

  fprintf(stderr, "I will now get and average the input data\n");
  av = avg_osc(chIn, (float)1.0, dc_offs, offsetIn);
  fprintf(stderr, "that worked\n");

  mode_mask = 0x11;

  if (chOut == 0) {
    if (g_awg_reg) {
      k_norm = (float)(c_dac_max) / ch1_max_dac_v;

      state_machine &= ~0xff;
      // fprintf(stderr, "in chA, pos 1\n");
      g_awg_reg->state_machine_conf = state_machine | 0xC0;
      // fprintf(stderr, "in chA, pos 2\n");
      g_awg_reg->cha_scale_off = awgoffsgain;
      // fprintf(stderr, "in chA, pos 3\n");
      g_awg_reg->cha_count_wrap = wrap;
      // fprintf(stderr, "in chA, pos 4\n");
      g_awg_reg->cha_count_step = step;
      // fprintf(stderr, "in chA, pos 5\n");
      // g_awg_reg->cha_start_off      = 0;
      // fprintf(stderr, "in chA, pos 6 - writing data now\n");
      outdata = (int)round(av * k_norm);
      if (outdata > c_dac_max) {
        outdata = c_dac_max;
      } else if (outdata < c_dac_min) {
        outdata = c_dac_min;
      }
      for (int i = 0; i < AWG_SIG_LEN; i++) {
        g_awg_cha_mem[i] = outdata;
      }
      // fprintf(stderr, "in chA, pos 7\n");
      g_awg_reg->state_machine_conf = state_machine | mode_mask;
      // fprintf(stderr, "in chA, pos 8\n");
    } else {
      fprintf(stderr, "g_awg_reg is NULL - skipping the signal generation.\n");
    }
  }
  if (chOut == 1) {
    if (g_awg_reg) {
      k_norm = (float)(c_dac_max) / ch2_max_dac_v;

      state_machine &= ~0xff0000;

      g_awg_reg->state_machine_conf = state_machine | 0xC00000;
      g_awg_reg->chb_scale_off = awgoffsgain;
      g_awg_reg->chb_count_wrap = wrap;
      g_awg_reg->chb_count_step = step;
      g_awg_reg->chb_start_off = 0;
      outdata = (int)round(av * k_norm);
      if (outdata > c_dac_max) {
        outdata = c_dac_max;
      } else if (outdata < c_dac_min) {
        outdata = c_dac_min;
      }
      for (int i = 0; i < AWG_SIG_LEN; i++) {
        g_awg_chb_mem[i] = outdata;
      }
      g_awg_reg->state_machine_conf = state_machine | (mode_mask << 16);
    } else {
      fprintf(stderr, "g_awg_reg is NULL - skipping the signal generation.\n");
    }
  }

  printf("output %f V in output %d for %f V average in input %d. int out:"
         " %d\n",
         f * av + offsetOut, chOut, av, chIn, (int)round(av * k_norm));

  return 0;
}

// maxV is the max voltage (1V or 20V)
int output_average_slow(float maxVin, float maxVout, float offsetA,
                        float offsetB) {
  /*int wr_ptr_currA,
      wr_ptr_trigA,
      wr_ptr_currB,
      wr_ptr_trigB;*/
  float avA, avB, f, oOff;

  f = maxVout / (2 * maxVin);
  oOff = maxVout / 2;

  if (averaging_slow == 0) {
    fprintf(stderr, "you asked me to output one or multiple averages on "
                    "one or multiple output pin(s), but averaging is "
                    "deactivated. First initialize it.\n");
    return -1;
  }
  if (averaging_slow & 1 && avgApin >= 0 && avgApin <= 3) {
    for (int i = 0; i < OSC_FPGA_SIG_LEN; i++) {
      chAbuff[i] = rp_fpga_cha_signal[i];
      /*if ( i==g_osc_fpga_reg_mem->wr_ptr_cur )
      {
          wr_ptr_currA = g_osc_fpga_reg_mem->wr_ptr_cur;
          wr_ptr_trigA = g_osc_fpga_reg_mem->wr_ptr_trigger;
      }*/
    }
    avA = avg_osc(0, maxVin, mycalib.fe_ch1_dc_offs, offsetA);
    printf("output %f V on pin %d for %f V in ch. A\n", f * avA + oOff, avgApin,
           avA);
    if (rp_AOpinSetValue(avgApin, f * avA + oOff)) {
      fprintf(stderr, "error when trying to change value for pin %d.\n",
              avgApin);
      return -1;
    }
  } else {
    fprintf(stderr, "did not enter the first IF clause. The parameters \n\
                         supplied were: averaging = %d, pinA = %d, \n\
                         averaging & 1 = %d...\n",
            averaging_slow, avgApin, averaging_slow & 1);
  }
  if (averaging_slow & 2 && avgBpin >= 0 && avgBpin <= 3) {
    printf("outputting signal on pin %d for channel A\n", avgBpin);
    for (int i = 0; i < OSC_FPGA_SIG_LEN; i++) {
      chBbuff[i] = rp_fpga_chb_signal[i];
      /*if ( i==g_osc_fpga_reg_mem->wr_ptr_cur )
      {
          wr_ptr_currB = g_osc_fpga_reg_mem->wr_ptr_cur;
          wr_ptr_trigB = g_osc_fpga_reg_mem->wr_ptr_trigger;
      }*/
    }
    avB = avg_osc(1, maxVin, mycalib.fe_ch2_dc_offs, offsetB);
    if (rp_AOpinSetValue(avgBpin, f * avB + oOff)) {
      fprintf(stderr, "error when trying to change value for pin %d.\n",
              avgBpin);
      return -1;
    }
  }

  return 0;
}

int ams_Init() {
  long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);
  void *page_ptr;

  if ((g_ams_fpga_mem_fd = open("/dev/mem", O_RDWR | O_SYNC)) == -1) {
    fprintf(stderr, "open /dev/mem failed: %s\n", strerror(errno));
    return -1;
  }

  page_addr = AMS_FPGA_BASE_ADDR & (~(page_size - 1));
  page_off = AMS_FPGA_BASE_ADDR - page_addr;
  page_ptr = mmap(NULL, AMS_FPGA_BASE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
                  g_ams_fpga_mem_fd, page_addr);
  if ((void *)page_ptr == MAP_FAILED) {
    fprintf(stderr, "mmap() failed: %s\n", strerror(errno));
    // might want to call cleanup_mem();
    return -1;
  }
  g_ams_fpga_reg_mem = page_ptr + page_off;

  return 0;
}

int ams_Release() {
  if (g_ams_fpga_reg_mem) {
    if (munmap(g_ams_fpga_reg_mem, AMS_FPGA_BASE_SIZE) < 0) {
      fprintf(stderr, "munmap() failed: %s\n", strerror(errno));
      return -1;
    }
  }
  if (g_ams_fpga_mem_fd >= 0) {
    close(g_ams_fpga_mem_fd);
    g_ams_fpga_mem_fd = -1;
  }
  return 0;
}

int ams_Init_backup() {
  void **myptr = (void **)&ams;
  size_t offset = AMS_FPGA_BASE_ADDR;

  if ((g_ams_fpga_mem_fd = open("/dev/uio/api", O_RDWR | O_SYNC)) == -1) {
    fprintf(stderr, "open /dev/uio/api failed: %s\n", strerror(errno));
    return -1;
  }

  offset = (offset >> 20) * sysconf(_SC_PAGESIZE);
  *myptr = mmap(NULL, AMS_FPGA_BASE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
                g_ams_fpga_mem_fd, offset);
  if (myptr == (void *)-1) {
    fprintf(stderr, "mmap() failed: %s\n", strerror(errno));
    // might want to call cleanup_mem();
    return -1;
  }
  return 0;
}

int ams_Release_backup() {
  void **myptr = (void **)&ams;
  if (*myptr && munmap(*myptr, AMS_FPGA_BASE_SIZE) < 0) {
    fprintf(stderr, "unmap() failed for AMS: %s\n", strerror(errno));
    return -1;
  }
  // cmn_Unmap(AMS_FPGA_BASE_SIZE, (void**)&ams);
  return 0;
}

int timedAO_fast(int chIn, int chOut, float maxVin, float offsetIn,
                 float offsetOut) {
  int step = 0, myms = 0;
  char key = 'l';

  printf("press 'q' to exit.\n");
  while (key != 'q') {
    usleep(1000); // wait one ms
    step++;
    myms++;
    if (myms >= 1000) {
      myms = 0;
      printf("another second passed\n");
    }
    if (step >= avgTfast) {
      output_average_fast(chIn, chOut, maxVin, offsetIn, offsetOut);
      step = 0;
    }
    if (mykbhit()) {
      key = getchar();
    }
    switch (key) {
    case 'w':
      avgTfast++;
      printf("increased step time to %dms.\n", avgTfast);
    case 's':
      if (avgTfast > 1) {
        avgTfast--;
        printf("decreased step time to %dms.\n", avgTfast);
      }
    }
  }
  return 0;
}

int timedAO_slow(float maxVin, float maxVout, float factorB, float offsetA,
                 float offsetB) {
  int step = 0, myms = 0;
  char key = 'l';

  if (averaging_slow == 0) {
    fprintf(stderr, "you asked me to output one or multiple averages on "
                    "one or multiple output pin(s), but averaging is "
                    "deactivated. First initialize it.\n");
    return -1;
  }
  printf("press 'q' to exit.\n");
  while (key != 'q') {
    usleep(1000); // wait one ms
    step++;
    myms++;
    if (myms >= 1000) {
      myms = 0;
      printf("another second passed\n");
    }
    if (step >= avgTslow) {
      output_average_slow(maxVin, maxVout, offsetA, offsetB);
      step = 0;
    }
    if (mykbhit()) {
      key = getchar();
    }
    switch (key) {
    case 'w':
      avgTslow++;
      printf("increased step time to %dms.\n", avgTslow);
    case 's':
      if (avgTslow > 1) {
        avgTslow--;
        printf("decreased step time to %dms.\n", avgTslow);
      }
    }
  }
  return 0;
}

// code copied from organ McGuire, morgan@cs.brown.edu
int mykbhit() {
  static const int STDIN = 0;
  static int initialized = 0;

  if (!initialized) {
    // Use termios to turn off line buffering
    struct termios term;
    tcgetattr(STDIN, &term);
    term.c_lflag &= ~ICANON;
    tcsetattr(STDIN, TCSANOW, &term);
    setbuf(stdin, NULL);
    initialized = 1;
  }

  int bytesWaiting;
  ioctl(STDIN, FIONREAD, &bytesWaiting);
  return bytesWaiting;
}

/*  set the RPs decimation factor, but you DO NOT do it directly. Instead,
    you supply a number in the range [1,5], where each number corresponds to
    a decimation factor according to the following correspondence:

    0 -> decimation 1
    1 -> decimation 8
    2 -> decimation 64
    3 -> decimation 1024
    4 -> decimation 8192
    5 -> decimation 65536
 */
int set_dec(int time_range) {
  int dec = osc_fpga_cnv_time_range_to_dec(time_range);

  printf("current decimation factor: %d\n", g_osc_fpga_reg_mem->data_dec);

  if (dec < 0) {
    fprintf(stderr,
            "you supplied a wrong time range (%d) to set the "
            "decimation.\n",
            time_range);

    return -1;
  }
  printf("trying to set it to: %d\n", dec);
  g_osc_fpga_reg_mem->data_dec = dec;
  printf("success...\n");

  return 0;
}

// from rp.c, which I found in the github folder of example source code
// I modified it a bit
int rp_AOpinSetValue(uint32_t pin, float value) {
  uint32_t value_raw = (uint32_t)(((value - ANALOG_OUT_MIN_VAL) /
                                   (ANALOG_OUT_MAX_VAL - ANALOG_OUT_MIN_VAL)) *
                                  ANALOG_OUT_MAX_VAL_INTEGER);

  if (value_raw > ANALOG_OUT_MAX_VAL_INTEGER) {
    fprintf(stderr,
            "value we wanted to send to pin %u is too large "
            "(%u)\n",
            pin, value_raw);
    return -1;
  }
  if (pin > 3) {
    fprintf(stderr, "pin number %u is wrong\n", pin);
    return -1;
  }
  g_ams_fpga_reg_mem->PWM_DAC[pin] =
      ((value_raw & ANALOG_OUT_MASK) << ANALOG_OUT_BITS);
  return 0;
}
