#include "rpreadbuffer.h"

/* @brief Pointer to FPGA control registers. */
static osc_fpga_reg_mem_t *g_osc_fpga_reg_mem = NULL;

/* @brief Pointer to data buffer where signal on channel A is captured.  */
static uint32_t           *g_osc_fpga_cha_mem = NULL;

/* @brief Pointer to data buffer where signal on channel B is captured.  */
static uint32_t           *g_osc_fpga_chb_mem = NULL;

/* @brief The memory file descriptor used to mmap() the FPGA space. */
static int                 g_osc_fpga_mem_fd = -1;

/* @brief Number of ADC acquisition bits.  */
const int                  c_osc_fpga_adc_bits = 14;

/* @brief Sampling frequency = 125Mspmpls (non-decimated). */
const float                c_osc_fpga_smpl_freq = 125e6;

/* @brief Sampling period (non-decimated) - 8 [ns]. */
const float                c_osc_fpga_smpl_period = (1. / 125e6);

/* Signals directly pointing at the FPGA mem space */
int                  *rp_fpga_cha_signal, *rp_fpga_chb_signal;

/* memory buffers we reserve to receive the data from the buffers */
int *chAbuff = NULL;
int *chBbuff = NULL;
rp_calib_params_t mycalib;

int cleanup_mem(void)
{
    /* optionally unmap memory regions  */
    if (g_osc_fpga_reg_mem) {
        if (munmap(g_osc_fpga_reg_mem, OSC_FPGA_BASE_SIZE) < 0) {
            fprintf(stderr, "munmap() failed: %s\n", strerror(errno));
            return -1;
        }
        /* ...and update memory pointers */
        g_osc_fpga_reg_mem = NULL;
        g_osc_fpga_cha_mem = NULL;
        g_osc_fpga_chb_mem = NULL;
    }

    /* optionally close file descriptor */
    if(g_osc_fpga_mem_fd >= 0) {
        close(g_osc_fpga_mem_fd);
        g_osc_fpga_mem_fd = -1;
    }

    if( chAbuff )
    {
	    free(chAbuff);
    }
    if( chBbuff )
    {
	    free(chBbuff);
    }

    return 0;
}

/* the following function was adapted from 'fpga.c' that was included in the
 * source code for the RP PID module */
int osc_fpga_init(void)
{
    void *page_ptr;
    long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);
    int ret;

    /* If maybe needed, cleanup the FD & memory pointer */
    if(cleanup_mem() < 0)
        return -1;
    
    ret = rp_read_calib_params(&mycalib);
    if ( ret==-1 )
    {
	    printf("error in reading the RP calibration. Exiting.\n");
	    return -1;
    } else if ( ret!=0 ) {
	    printf("unknown error. Exiting.\n");
	    return -1;
    }
    printf("calibration DC offset, ch1: %d\n", mycalib.fe_ch1_dc_offs);
    printf("calibration DC offset, ch2: %d\n", mycalib.fe_ch2_dc_offs);

    g_osc_fpga_mem_fd = open("/dev/mem", O_RDONLY);
    if(g_osc_fpga_mem_fd < 0) {
        fprintf(stderr, "open(/dev/mem) failed: %s\n", strerror(errno));
        return -1;
    }

    page_addr = OSC_FPGA_BASE_ADDR & (~(page_size-1));
    page_off  = OSC_FPGA_BASE_ADDR - page_addr;

    page_ptr = mmap(NULL, OSC_FPGA_BASE_SIZE, PROT_READ,
                          MAP_SHARED, g_osc_fpga_mem_fd, page_addr);
    if((void *)page_ptr == MAP_FAILED) {
     fprintf(stderr, "mmap() failed: %s\n", strerror(errno));
        cleanup_mem();
        return -1;
    }
    g_osc_fpga_reg_mem = page_ptr + page_off;
    g_osc_fpga_cha_mem = (uint32_t *)g_osc_fpga_reg_mem +
        (OSC_FPGA_CHA_OFFSET / sizeof(uint32_t));
    g_osc_fpga_chb_mem = (uint32_t *)g_osc_fpga_reg_mem +
        (OSC_FPGA_CHB_OFFSET / sizeof(uint32_t));

    osc_fpga_get_sig_ptr(&rp_fpga_cha_signal, &rp_fpga_chb_signal);

    chAbuff = (int *)malloc(sizeof(int) * OSC_FPGA_SIG_LEN);
    if ( chAbuff == NULL )
    {
       fprintf(stderr, "malloc failed for channel A: %s\n", strerror(errno));
       cleanup_mem();
       return -1;
    }
    chBbuff = (int *)malloc(sizeof(int) * OSC_FPGA_SIG_LEN);
    if ( chBbuff == NULL )
    {
       fprintf(stderr, "malloc failed for channel B: %s\n", strerror(errno));
       cleanup_mem();
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
int osc_fpga_get_sig_ptr(int **cha_signal, int **chb_signal)
{
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
int osc_fpga_get_wr_ptr(int *wr_ptr_curr, int *wr_ptr_trig)
{
    if(wr_ptr_curr)
        *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
    if(wr_ptr_trig)
        *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
    return 0;
}

/*----------------------------------------------------------------------------*/
/**
 * @brief Converts ADC counts to voltage [V]
 *
 * Function is used to publish captured signal data to external world in user units.
 * Calculation is based on maximal voltage, which can be applied on ADC inputs and
 * calibrated and user defined DC offsets.
 *
 * @param[in] cnts           Captured Signal Value, expressed in ADC counts
 * @param[in] adc_max_v      Maximal ADC voltage, specified in [V]
 * @param[in] calib_dc_off   Calibrated DC offset, specified in ADC counts
 * @param[in] user_dc_off    User specified DC offset, specified in [V]
 * @retval    double         Signal Value, expressed in user units [V]
 */
double osc_fpga_cnv_cnt_to_v(int cnts, double adc_max_v, int calib_dc_off, double user_dc_off)
{
    int m;
    double ret_val;

    /* check sign */
    if(cnts & (1<<(c_osc_fpga_adc_bits-1))) {
        /* negative number */
        m = -1 *((cnts ^ ((1<<c_osc_fpga_adc_bits)-1)) + 1);
    } else {
        /* positive number */
        m = cnts;
    }

    /* adopt ADC count with calibrated DC offset */
    m += calib_dc_off;

    /* map ADC counts into user units */
    if(m < (-1 * (1<<(c_osc_fpga_adc_bits-1))))
        m = (-1 * (1<<(c_osc_fpga_adc_bits-1)));
    else if(m > (1<<(c_osc_fpga_adc_bits-1)))
        m =  (1<<(c_osc_fpga_adc_bits-1));

    ret_val =  (m * adc_max_v /
                (double)(1<<(c_osc_fpga_adc_bits-1)));

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
int osc_cnv_cnt_to_v_chA(double *chAout, double adc_max_v, int calib_dc_off)
{
    int m, i, 
	cnm1 = 1<<(c_osc_fpga_adc_bits-1), 
	cn = 1<<(c_osc_fpga_adc_bits); 
    double r, f;
    f = adc_max_v/((double)cnm1); 
    //printf("f: %f\n",f);

    for (i=0; i<OSC_FPGA_SIG_LEN; i++)
    {
      /* check sign */
      if(chAbuff[i] & cnm1) {
          /* negative number */
          m = -1 *((chAbuff[i] ^ (cn-1)) + 1);
      } else {
          /* positive number */
          m = chAbuff[i];
      }

      /* adopt ADC count with calibrated DC offset */
      m += calib_dc_off;

      /* map ADC counts into user units */
      if(m < (-1 * cnm1))
      {
          m = (-1 * cnm1);
      }else if(m > cnm1) {
          m = cnm1;
      }

      r =  f*m;

      /* and adopt the calculation with user specified DC offset */
      chAout[i] = r;

    }

    return 0;
}


/* the following calls osc_fpga_cnv_cnt_to_v for all elements we copied from
 * the buffer to our own buffer memories (chAbuff and chBbuff), and it 
 * puts the results in the arrays pointed to by chAout and chBout. 
 *
 * The buffers in that output pointers MUST be sufficiently long!!!
 */
int osc_cnv_cnt_to_v_chs(double *chAout, double *chBout, double adc_max_v, int calib_dc_off)
{
    int m, i, 
	cnm1 = 1<<(c_osc_fpga_adc_bits-1), 
	cn = 1<<(c_osc_fpga_adc_bits); 
    double r, f;
    f = adc_max_v/((double)cnm1); 
    //printf("f: %f\n",f);

    for (i=0; i<OSC_FPGA_SIG_LEN; i++)
    {
      /* check sign */
      if(chAbuff[i] & cnm1) {
          /* negative number */
          m = -1 *((chAbuff[i] ^ (cn-1)) + 1);
      } else {
          /* positive number */
          m = chAbuff[i];
      }

      /* adopt ADC count with calibrated DC offset */
      m += calib_dc_off;

      /* map ADC counts into user units */
      if(m < (-1 * cnm1))
      {
          m = (-1 * cnm1);
      }else if(m > cnm1) {
          m = cnm1;
      }

      r =  f*m;
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
      if(chBbuff[i] & cnm1) 
      {
          /* negative number */
          m = -1 *((chBbuff[i] ^ (cn-1)) + 1);
      } else {
          /* positive number */
          m = chBbuff[i];
      }

      /* adopt ADC count with calibrated DC offset */
      m += calib_dc_off;

      /* map ADC counts into user units */
      if(m < (-1 * cnm1))
          m = (-1 * cnm1);
      else if(m > cnm1)
          m = cnm1;

      r =  f*m;
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
int osc_cnv_cnt_to_v_chs_backup(double *chAout, double *chBout, double adc_max_v, int calib_dc_off, double user_dc_off)
{
    int m, i, 
	cnm1 = 1<<(c_osc_fpga_adc_bits-1), 
	cn = 1<<(c_osc_fpga_adc_bits); 
    double r, f;
    f = adc_max_v/((double)cnm1); 
    //printf("f: %f\n",f);

    for (i=0; i<OSC_FPGA_SIG_LEN; i++)
    {
      /* check sign */
      if(chAbuff[i] & cnm1) {
          /* negative number */
          m = -1 *((chAbuff[i] ^ (cn-1)) + 1);
      } else {
          /* positive number */
          m = chAbuff[i];
      }

      /* adopt ADC count with calibrated DC offset */
      m += calib_dc_off;

      /* map ADC counts into user units */
      if(m < (-1 * cnm1))
      {
          m = (-1 * cnm1);
      }else if(m > cnm1) {
          m = cnm1;
      }

      r =  f*m;
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
      if(chBbuff[i] & cnm1) 
      {
          /* negative number */
          m = -1 *((chBbuff[i] ^ (cn-1)) + 1);
      } else {
          /* positive number */
          m = chBbuff[i];
      }

      /* adopt ADC count with calibrated DC offset */
      m += calib_dc_off;

      /* map ADC counts into user units */
      if(m < (-1 * cnm1))
          m = (-1 * cnm1);
      else if(m > cnm1)
          m = cnm1;

      r =  f*m;
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

int rp_get_signalA(double* chA, int* wr_ptr_curr, int* wr_ptr_trig, double factor)
{
  if(!wr_ptr_curr || !wr_ptr_trig)
  {
    return -1; // those should be valid references
  }
  for(int i=0; i<OSC_FPGA_SIG_LEN; i++)
  {
    chAbuff[i] = rp_fpga_cha_signal[i];
    if ( i==g_osc_fpga_reg_mem->wr_ptr_cur )
    {
      *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
      *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
    }
  }
  //osc_cnv_cnt_to_v_chA(chA, factor, -mycalib.fe_ch1_dc_offs);
  osc_cnv_cnt_to_v_chA(chA, factor, 0);

  return 0;
}

int rp_get_signals(double* chA, double* chB, int* wr_ptr_curr, int* wr_ptr_trig, double factor)
{
  if(!wr_ptr_curr || !wr_ptr_trig)
  {
    return -1; // those should be valid references
  }
  for(int i=0; i<OSC_FPGA_SIG_LEN; i++)
  {
    chAbuff[i] = rp_fpga_cha_signal[i];
    chBbuff[i] = rp_fpga_chb_signal[i];
    if ( i==g_osc_fpga_reg_mem->wr_ptr_cur )
    {
      *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
      *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
    }
  }
  osc_cnv_cnt_to_v_chs(chA, chB, factor, 0);

  return 0;
}

int rp_copy_signals(int* chA, int* chB, int* rpChA, int* rpChB)
{
memcpy(chA, rpChA, sizeof(int)*OSC_FPGA_SIG_LEN);
memcpy(chB, rpChB, sizeof(int)*OSC_FPGA_SIG_LEN);

return 0;
}

int rp_get_fast_new(double* chA, double* chB, int* wr_ptr_curr, int* wr_ptr_trig, double factor)
{
  if(!wr_ptr_curr || !wr_ptr_trig)
  {
    return -1; // those should be valid references
  }
  *wr_ptr_curr = g_osc_fpga_reg_mem->wr_ptr_cur;
  *wr_ptr_trig = g_osc_fpga_reg_mem->wr_ptr_trigger;
  memcpy((void *)chAbuff, (void *)g_osc_fpga_cha_mem, sizeof(int)*OSC_FPGA_SIG_LEN);
  memcpy((void *)chBbuff, (void *)g_osc_fpga_chb_mem, sizeof(int)*OSC_FPGA_SIG_LEN);

  osc_cnv_cnt_to_v_chs(chA, chB, factor, 0);

  printf("factor: %f\n",factor);
  printf("size of float: %d\n", (int)sizeof(float));
  printf("size of double: %d\n", (int)sizeof(double));
  /*
  for(int i=0; i<OSC_FPGA_SIG_LEN; i++)
  {
    chA[i] = osc_fpga_cnv_cnt_to_v(chAbuff[i], (float)(1<<(c_osc_fpga_adc_bits-1)), 0, 0);
    chB[i] = osc_fpga_cnv_cnt_to_v(chBbuff[i], (float)(1<<(c_osc_fpga_adc_bits-1)), 0, 0);
  }
  */
  //memcpy((void*)chA, (void*)rp_fpga_cha_signal, sizeof(int)*OSC_FPGA_SIG_LEN);
  //memcpy((void*)chB, (void*)rp_fpga_chb_signal, sizeof(int)*OSC_FPGA_SIG_LEN);

  return 0;
}
