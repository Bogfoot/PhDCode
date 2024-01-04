# quTAG (standard) Python Wrapper of time-to-digital library tdcbase.dll
#
# Author: qutools GmbH
# Last edited: June 2021
#
# Tested with python 3.7 (32bit & 64bit), Windows 10 (64bit)
#
# This is demo code. Use at your own risk. No warranties.
#
# It may be used and modified with no restriction; raw copies as well as
# modified versions may be distributed without limitation.


# This code shows different device settings and their usage. For additional information see the documentation of TDCBase.


##
# @mainpage quTAG Python Wrapper for DLL usage
#
# @section description_main Description
# The Python script quTAG*.py wrapps all DLL functions of the quTAG DLL tdcbase*.dll \n
# Tdcbase is a library that allows custom programming for the TDC time-to-digital converter. It allows to configure the device, aquire timestamps, and calculate start stop histograms. \n
# The quTAG*.py wrapps these DLL functions in the class QuTAG by its own Python functions.
#
#
# @section notes_main Notes
# - Ensure to match Python bit version with DLL bit version
# - Import the wrapper quTAG*.py in your script and initialize the quTAG by e.g. qutag = QuTAG.QuTAG()
# - Tested with Python3 and Windows 10 (32bit & 64bit)
# - See also the different example files for usage
# - Author: qutools GmbH, May 2021
#
#
# It may be used and modified with no restriction; raw copies as well as
# modified versions may be distributed without limitation.
##


import ctypes
import os
import platform
import sys
import time

try:
    import numpy as np
except:
    print("The wrapper QuTAG.py needs numpy for arrays, please install.")


class QuTAG:
    # ----------------------------------------------------
    # lifetime histogram structure
    class TDC_LftFunction(ctypes.Structure):
        """Data structure of lifetime function"""

        _fields_ = [
            ("capacity", ctypes.c_int32),
            ("size", ctypes.c_int32),
            ("binWidth", ctypes.c_int32),
            ("values", ctypes.c_double),
        ]

    # hbt histogram structure
    class TDC_HbtFunction(ctypes.Structure):
        """Data structure of HBT / correlation function"""

        _fields_ = [
            ("capacity", ctypes.c_int32),
            ("size", ctypes.c_int32),
            ("binWidth", ctypes.c_int32),
            ("indexOffset", ctypes.c_int32),
            ("values", ctypes.c_double),
        ]

    def __init__(self):
        """Initializing the quTAG \n\n
        Checking the bit version of Python to load the corresponding DLL \n
        Loading 32 or 64 bit DLL: make sure the wrapper finds the matching DLL in the same folder  \n
        Declary API  \n
        Connect the device by the function QuTAG.Initialize()  \n
        Set some parameters
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        # load Lib -------------------------------------------
        if platform.system() == "Windows":
            file_path = os.path.dirname(os.path.abspath(__file__))
            dll_name = "tdcbase.dll"
            # check Python bit version
            if sys.maxsize > 2 ** 32:
                # load DLL 64 Bit -------------------------------------------
                full_path = file_path + os.path.sep + os.path.join("DLL_64bit")
                # print("Python 64 Bit - loading 64 Bit DLL")
            else:
                # load DLL 32 Bit -------------------------------------------
                full_path = file_path + os.path.sep + os.path.join("DLL_32bit")
                # print("Python 32 Bit - loading 32 Bit DLL")

            # add DLL folder to environment PATH
            os.environ["PATH"] += ";"
            os.environ["PATH"] += full_path

            # check Python bit version
            if sys.maxsize > 2 ** 32:
                # load DLL 64 Bit -------------------------------------------
                full_path = file_path + os.path.sep + os.path.join("DLL_64bit")
                # print("Python 64 Bit - loading 64 Bit DLL")
            else:
                # load DLL 32 Bit -------------------------------------------
                full_path = file_path + os.path.sep + os.path.join("DLL_32bit")
                # print("Python 32 Bit - loading 32 Bit DLL")

            # load DLL -------------------------------------------
            self.tdclib = ctypes.windll.LoadLibrary(dll_name)

        if platform.system() == "Linux":
            self.tdclib = ctypes.cdll.LoadLibrary("libtdcbase.so")
            self.coincLib = ctypes.cdll.LoadLibrary(
                "qutag_histogram.so"
            )

        self.declareAPI()
        self.dev_nr = -1

        # wrapper function Initiallize to connect to quTAG
        self.Initialize()

        self._bufferSize = 1000000
        self.setBufferSize(self._bufferSize)

        self._deviceType = self.getDeviceType()
        self._timebase = self.getTimebase()

        self._StartStopBinCount = 100000

        self._featureHBT = self.checkFeatureHBT()
        self._featureLifetime = self.checkFeatureLifetime()

        self._HBTBufferSize = 256
        self._LFTBufferSize = 256

        # print("Found "+self.devtype_dict[self._deviceType]+" device.")

        # Get infos about device
        devType = self._deviceType
        if devType == self.DEVTYPE_QUTAG:
            print("Found " + self.devtype_dict[self._deviceType] + " device.")
        else:
            print("No suitable device found - demo mode activated")
        if platform.system() == "Windows":
            print("Initialized with QuTAG DLL v%f" % (self.getVersion()))
        if platform.system() == "Linux":
            print("Initialized with QuTAG Linux library v%f" % (self.getVersion()))

    def declareAPI(self):
        """Declare the API of the DLL with its functions and dictionaries. Should not be executed from the user."""
        # ------- tdcbase.h --------------------------------------------------------
        self.TDC_QUTAG_CHANNELS = 5
        self.TDC_COINC_CHANNELS = 31
        self.TDC_MAX_CHANNEL_NO = 20

        # Device types ---------------------------------------
        self.devtype_dict = {0: "DEVTYPE_QUTAG", 1: "DEVTYPE_NONE"}
        self.DEVTYPE_QUTAG = 0  # quTAG
        self.DEVTYPE_NONE = 1  # simulated device

        # (Output) Fileformats ----------------------------------------
        self.fileformat_dict = {
            0: "ASCII",  # ASCII format
            1: "BINARY",  # uncompressed binary format (40B header, 10B/time tag)
            2: "COMPRESSED",  # compressed binary format (40B header, 5B/time tag)
            3: "RAW",  # uncompressed binary without header (for compatibility)
            4: "NONE",
        }

        self.FILEFORMAT_ASCII = 0
        self.FILEFORMAT_BINARY = 1
        self.FILEFORMAT_COMPRESSED = 2
        self.FILEFORMAT_RAW = 3
        self.FILEFORMAT_NONE = 4
        # Signal conditioning --------------------------------
        self.signalcond_dict = {
            1: "LVTTL",  # for LVTTL signals: Trigger at 2V rising edge
            2: "NIM",  # for NIM signals: Trigger at -0.6V falling edge
            3: "MISC",  # other signal type: conditioning on, everything optional
            4: "NONE",
        }

        self.SCOND_LVTTL = 1
        self.SCOND_NIM = 2
        self.SCOND_MISC = 3
        self.SCOND_NONE = 4
        # Type of generated timestamps ----------------------------
        self.simtype_dict = {
            0: "FLAT",  # time diffs and channels numbers uniformly ditributed
            1: "NORMAL",  # time diffs normally distributed, channels uniformly
            2: "NONE",
        }

        self.SIMTYPE_FLAT = 0
        self.SIMTYPE_NORMAL = 1
        self.SIMTYPE_NONE = 2

        # Error types (tdcdecl.h) ----------------------------------------
        self.err_dict = {
            -1: "unspecified error",
            0: "OK, no error",
            1: "Receive timed out",
            2: "No connection was established",
            3: "Error accessing the USB driver",
            4: "Unknown Error",
            5: "Unknown Error",
            6: "Unknown Error",
            7: "Can" "t connect device because already in use",
            8: "Unknown error",
            9: "Invalid device number used in call",
            10: "Parameter in fct. call is out of range",
            11: "Failed to open specified file",
            12: "Library has not been initialized",
            13: "Requested Feature is not enabled",
            14: "Requested Feature is not available",
        }

        # function definitions
        self.tdclib.TDC_getVersion.argtypes = None
        self.tdclib.TDC_getVersion.restype = ctypes.c_double
        self.tdclib.TDC_perror.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_perror.restype = ctypes.POINTER(ctypes.c_char_p)
        self.tdclib.TDC_getTimebase.argtypes = [ctypes.POINTER(ctypes.c_double)]
        self.tdclib.TDC_getTimebase.restype = ctypes.c_int32
        self.tdclib.TDC_init.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_init.restype = ctypes.c_int32
        self.tdclib.TDC_deInit.argtypes = None
        self.tdclib.TDC_deInit.restype = ctypes.c_int32
        self.tdclib.TDC_getDevType.argtypes = None
        self.tdclib.TDC_getDevType.restype = ctypes.c_int32
        self.tdclib.TDC_checkFeatureHbt.argtypes = None
        self.tdclib.TDC_checkFeatureHbt.restype = ctypes.c_int32
        # self.tdclib.TDC_checkFeatureLifeTime.argtypes = None
        # self.tdclib.TDC_checkFeatureLifeTime.restype = ctypes.c_int32
        self.tdclib.TDC_getFiveChannelMode.argtypes = None
        self.tdclib.TDC_getFiveChannelMode.restype = ctypes.c_int32
        self.tdclib.TDC_setFiveChannelMode.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_setFiveChannelMode.restype = ctypes.c_int32
        self.tdclib.TDC_getFiveChannelMode.argtypes = [ctypes.POINTER(ctypes.c_int32)]
        self.tdclib.TDC_getFiveChannelMode.restype = ctypes.c_int32
        self.tdclib.TDC_preselectSingleStop.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_preselectSingleStop.restype = ctypes.c_int32
        self.tdclib.TDC_getSingleStopPreselection.argtypes = [
            ctypes.POINTER(ctypes.c_int32)
        ]
        self.tdclib.TDC_getSingleStopPreselection.restype = ctypes.c_int32
        self.tdclib.TDC_enableChannels.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_enableChannels.restype = ctypes.c_int32
        self.tdclib.TDC_getChannelsEnabled.argtypes = [ctypes.POINTER(ctypes.c_int32)]
        self.tdclib.TDC_getChannelsEnabled.restype = ctypes.c_int32
        self.tdclib.TDC_enableMarkers.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_enableMarkers.restype = ctypes.c_int32
        self.tdclib.TDC_configureSignalConditioning.argtypes = [
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_double,
        ]
        self.tdclib.TDC_configureSignalConditioning.restype = ctypes.c_int32
        self.tdclib.TDC_getSignalConditioning.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_double),
        ]
        self.tdclib.TDC_getSignalConditioning.restype = ctypes.c_int32
        self.tdclib.TDC_configureSyncDivider.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.tdclib.TDC_configureSyncDivider.restype = ctypes.c_int32
        self.tdclib.TDC_getSyncDivider.argtypes = [
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getSyncDivider.restype = ctypes.c_int32
        self.tdclib.TDC_setCoincidenceWindow.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_setCoincidenceWindow.restype = ctypes.c_int32
        self.tdclib.TDC_setExposureTime.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_setExposureTime.restype = ctypes.c_int32
        self.tdclib.TDC_getDeviceParams.argtypes = [
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getDeviceParams.restype = ctypes.c_int32
        self.tdclib.TDC_setChannelDelays.argtypes = [ctypes.POINTER(ctypes.c_int32)]
        self.tdclib.TDC_setChannelDelays.restype = ctypes.c_int32
        self.tdclib.TDC_getChannelDelays.argtypes = [ctypes.POINTER(ctypes.c_int32)]
        self.tdclib.TDC_getChannelDelays.restype = ctypes.c_int32
        self.tdclib.TDC_setDeadTime.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.tdclib.TDC_setDeadTime.restype = ctypes.c_int32
        self.tdclib.TDC_getDeadTime.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getDeadTime.restype = ctypes.c_int32
        self.tdclib.TDC_configureSelftest.argtypes = [
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
        ]
        self.tdclib.TDC_configureSelftest.restype = ctypes.c_int32
        self.tdclib.TDC_getDataLost.argtypes = [ctypes.POINTER(ctypes.c_int32)]
        self.tdclib.TDC_getDataLost.restype = ctypes.c_int32
        self.tdclib.TDC_setTimestampBufferSize.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_setTimestampBufferSize.restype = ctypes.c_int32
        self.tdclib.TDC_getTimestampBufferSize.argtypes = [
            ctypes.POINTER(ctypes.c_int32)
        ]
        self.tdclib.TDC_getTimestampBufferSize.restype = ctypes.c_int32
        self.tdclib.TDC_enableTdcInput.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_enableTdcInput.restype = ctypes.c_int32
        self.tdclib.TDC_freezeBuffers.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_freezeBuffers.restype = ctypes.c_int32
        self.tdclib.TDC_getCoincCounters.argtypes = [
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getCoincCounters.restype = ctypes.c_int32
        self.tdclib.TDC_getLastTimestamps.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.POINTER(ctypes.c_int8),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getLastTimestamps.restype = ctypes.c_int32
        self.tdclib.TDC_writeTimestamps.argtypes = [ctypes.c_char_p, ctypes.c_int32]
        self.tdclib.TDC_writeTimestamps.restype = ctypes.c_int32
        self.tdclib.TDC_inputTimestamps.argtypes = [
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.POINTER(ctypes.c_int8),
            ctypes.c_int32,
        ]
        self.tdclib.TDC_inputTimestamps.restype = ctypes.c_int32
        self.tdclib.TDC_readTimestamps.argtypes = [ctypes.c_char_p, ctypes.c_int32]
        self.tdclib.TDC_readTimestamps.restype = ctypes.c_int32
        self.tdclib.TDC_generateTimestamps.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_int32,
        ]
        self.tdclib.TDC_generateTimestamps.restype = ctypes.c_int32

        self.coincLib.determineCoincidencesStartBlock.argtypes = [
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.POINTER(ctypes.c_int8),
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_double,
            ctypes.c_double,
        ]
        self.coincLib.determineCoincidencesStartBlock.restype = ctypes.c_int32

        self.coincLib.determineCoincidenceBlock.argtypes = [
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.POINTER(ctypes.c_int8),
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_double,
            ctypes.c_double,
        ]
        self.coincLib.determineCoincidenceBlock.restype = ctypes.c_int32

        self.coincLib.determineCoincidences.argtypes = [
            ctypes.POINTER(ctypes.c_int64),
            ctypes.POINTER(ctypes.c_int8),
            ctypes.c_int64,
            ctypes.c_int64,
            ctypes.c_int64,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
        ]
        self.coincLib.determineCoincidences.restype = ctypes.c_int64

        # July 18th, 2022: I changed the following two lines to fit the
        # changed arguments of the C function. Note that I changed the
        # int arguments to Int64, and that I replaced the T1, T2 we had
        # earlier with integer references T1out and T2out, such that we do not
        # supply these values, but we receive them from the function - it
        # looks at the time tags we have and then determines the minimum
        # and maximum time delays we can encounter in our data
        self.coincLib.determineCoincidenceHistogram.argtypes = [
            ctypes.POINTER(ctypes.c_int64),
            ctypes.POINTER(ctypes.c_int8),
            ctypes.c_int64,
            ctypes.c_int64,
            ctypes.c_int64,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.POINTER(ctypes.c_int64),
            ctypes.c_int64,
        ]
        self.coincLib.determineCoincidenceHistogram.restype = ctypes.c_int64

        # ------- tdcmultidev.h ------------------------------------------------------
        self.tdclib.TDC_discover.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
        self.tdclib.TDC_discover.restype = ctypes.c_int32
        self.tdclib.TDC_getDeviceInfo.argtypes = [
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getDeviceInfo.restype = ctypes.c_int32
        self.tdclib.TDC_connect.argtypes = [ctypes.c_uint32]
        self.tdclib.TDC_connect.restype = ctypes.c_int32
        self.tdclib.TDC_disconnect.argtypes = [ctypes.c_uint32]
        self.tdclib.TDC_disconnect.restype = ctypes.c_int32
        self.tdclib.TDC_addressDevice.argtypes = [ctypes.c_uint32]
        self.tdclib.TDC_addressDevice.restype = ctypes.c_int32
        self.tdclib.TDC_getCurrentAddress.argtypes = [ctypes.c_uint32]
        self.tdclib.TDC_getCurrentAddress.restype = ctypes.c_int32

        # ------- tdcstartstop.h -----------------------------------------------------
        self.tdclib.TDC_enableStartStop.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_enableStartStop.restype = ctypes.c_int32
        self.tdclib.TDC_addHistogram.argtypes = [
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
        ]
        self.tdclib.TDC_addHistogram.restype = ctypes.c_int32
        self.tdclib.TDC_setHistogramParams.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.tdclib.TDC_setHistogramParams.restype = ctypes.c_int32
        self.tdclib.TDC_getHistogramParams.argtypes = [
            ctypes.POINTER(ctypes.c_int32),
            ctypes.c_int32,
        ]
        self.tdclib.TDC_getHistogramParams.restype = ctypes.c_int32
        self.tdclib.TDC_clearAllHistograms.argtypes = None
        self.tdclib.TDC_clearAllHistograms.restype = ctypes.c_int32
        self.tdclib.TDC_getHistogram.argtypes = [
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_longlong),
        ]
        self.tdclib.TDC_getHistogram.restype = ctypes.c_int32

        # ------- tdchbt.h -----------------------------------------------------------
        # type of a HBT model function
        self.fcttype_dict = {
            0: "NONE",
            1: "COHERENT",
            2: "THERMAL",
            3: "SINGLE",
            4: "ANTIBUNCH",
            5: "THERM_JIT",
            6: "SINGLE_JIT",
            7: "ANTIB_JIT",
            8: "THERMAL_OFS",
            9: "SINGLE_OFS",
            10: "ANTIB_OFS",
            11: "THERM_JIT_OFS",
            12: "SINGLE_JIT_OFS",
            13: "ANTIB_JIT_OFS",
        }

        self.FCTTYPE_NONE = 0
        self.FCTTYPE_COHERENT = 1
        self.FCTTYPE_THERMAL = 2
        self.FCTTYPE_SINGLE = 3
        self.FCTTYPE_ANTIBUNCH = 4
        self.FCTTYPE_THERM_JIT = 5
        self.FCTTYPE_SINGLE_JIT = 6
        self.FCTTYPE_ANTIB_JIT = 7
        self.FCTTYPE_THERMAL_OFS = 8
        self.FCTTYPE_SINGLE_OFS = 9
        self.FCTTYPE_ANTIB_OFS = 10
        self.FCTTYPE_THERM_JIT_OFS = 11
        self.FCTTYPE_SINGLE_JIT_OFS = 12
        self.FCTTYPE_ANTIB_JIT_OFS = 13
        # ----------------------------------------------------
        # function definitions
        self.tdclib.TDC_enableHbt.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_enableHbt.restype = ctypes.c_int32
        self.tdclib.TDC_setHbtParams.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.tdclib.TDC_setHbtParams.restype = ctypes.c_int32
        self.tdclib.TDC_getHbtParams.argtypes = [
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getHbtParams.restype = ctypes.c_int32
        self.tdclib.TDC_setHbtDetectorParams.argtypes = [ctypes.c_double]
        self.tdclib.TDC_setHbtDetectorParams.restype = ctypes.c_int32
        self.tdclib.TDC_getHbtDetectorParams.argtypes = [
            ctypes.POINTER(ctypes.c_double)
        ]
        self.tdclib.TDC_getHbtDetectorParams.restype = ctypes.c_int32
        self.tdclib.TDC_setHbtInput.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.tdclib.TDC_setHbtInput.restype = ctypes.c_int32
        self.tdclib.TDC_getHbtInput.argtypes = [
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getHbtInput.restype = ctypes.c_int32
        self.tdclib.TDC_resetHbtCorrelations.argtypes = None
        self.tdclib.TDC_resetHbtCorrelations.restype = ctypes.c_int32
        self.tdclib.TDC_getHbtEventCount.argtypes = [
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.POINTER(ctypes.c_longlong),
            ctypes.POINTER(ctypes.c_double),
        ]
        self.tdclib.TDC_getHbtEventCount.restype = ctypes.c_int32
        self.tdclib.TDC_getHbtIntegrationTime.argtypes = [
            ctypes.POINTER(ctypes.c_double)
        ]
        self.tdclib.TDC_getHbtIntegrationTime.restype = ctypes.c_int32
        self.tdclib.TDC_getHbtCorrelations.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(QuTAG.TDC_HbtFunction),
        ]
        self.tdclib.TDC_getHbtCorrelations.restype = ctypes.c_int32
        self.tdclib.TDC_calcHbtG2.argtypes = [ctypes.POINTER(QuTAG.TDC_HbtFunction)]
        self.tdclib.TDC_calcHbtG2.restype = ctypes.c_int32
        self.tdclib.TDC_fitHbtG2.argtypes = [
            ctypes.POINTER(QuTAG.TDC_HbtFunction),
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_fitHbtG2.restype = ctypes.c_int32
        self.tdclib.TDC_getHbtFitStartParams.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_double),
        ]
        self.tdclib.TDC_getHbtFitStartParams.restype = ctypes.POINTER(ctypes.c_double)
        self.tdclib.TDC_calcHbtModelFct.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(QuTAG.TDC_HbtFunction),
        ]
        self.tdclib.TDC_calcHbtModelFct.restype = ctypes.c_int32
        self.tdclib.TDC_generateHbtDemo.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_double,
        ]
        self.tdclib.TDC_generateHbtDemo.restype = ctypes.c_int32
        self.tdclib.TDC_createHbtFunction.argtypes = None
        self.tdclib.TDC_createHbtFunction.restype = ctypes.POINTER(
            QuTAG.TDC_HbtFunction
        )
        self.tdclib.TDC_releaseHbtFunction.argtypes = [
            ctypes.POINTER(QuTAG.TDC_HbtFunction)
        ]
        self.tdclib.TDC_releaseHbtFunction.restype = None
        self.tdclib.TDC_analyseHbtFunction.argtypes = [
            ctypes.POINTER(QuTAG.TDC_HbtFunction),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_int32,
        ]
        self.tdclib.TDC_analyseHbtFunction.restype = ctypes.c_int32

        # ------- tdclifetm.h --------------------------------------------------------
        self.LFT_PARAM_SIZE = 4
        # type of a lifetime model function
        self.lfttype_dict = {0: "NONE", 1: "EXP", 2: "DBL_EXP", 3: "KOHLRAUSCH"}
        self.LFTTYPE_NONE = 0
        self.LFTTYPE_EXP = 1
        self.LFTTYPE_DBL_EXP = 2
        self.LFTTYPE_KOHLRAUSCH = 3

        # function definitions
        self.tdclib.TDC_enableLft.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_enableLft.restype = ctypes.c_int32
        self.tdclib.TDC_setLftStartInput.argtypes = [ctypes.c_int32]
        self.tdclib.TDC_setLftStartInput.restype = ctypes.c_int32
        self.tdclib.TDC_addLftHistogram.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.tdclib.TDC_addLftHistogram.restype = ctypes.c_int32
        self.tdclib.TDC_getLftStartInput.argtypes = [ctypes.POINTER(ctypes.c_int32)]
        self.tdclib.TDC_getLftStartInput.restype = ctypes.c_int32
        self.tdclib.TDC_setLftParams.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self.tdclib.TDC_setLftParams.restype = ctypes.c_int32
        self.tdclib.TDC_getLftParams.argtypes = [
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_getLftParams.restype = ctypes.c_int32
        self.tdclib.TDC_resetLftHistograms.argtypes = None
        self.tdclib.TDC_resetLftHistograms.restype = ctypes.c_int32
        self.tdclib.TDC_createLftFunction.argtypes = None
        self.tdclib.TDC_createLftFunction.restype = ctypes.POINTER(
            QuTAG.TDC_LftFunction
        )
        self.tdclib.TDC_releaseLftFunction.argtypes = [
            ctypes.POINTER(QuTAG.TDC_LftFunction)
        ]
        self.tdclib.TDC_releaseLftFunction.restype = None
        self.tdclib.TDC_analyseLftFunction.argtypes = [
            ctypes.POINTER(QuTAG.TDC_LftFunction),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_int32,
        ]
        self.tdclib.TDC_analyseLftFunction.restype = None
        self.tdclib.TDC_getLftHistogram.argtypes = [
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.POINTER(QuTAG.TDC_LftFunction),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_longlong),
        ]
        self.tdclib.TDC_getLftHistogram.restype = ctypes.c_int32
        self.tdclib.TDC_calcLftModelFct.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(QuTAG.TDC_LftFunction),
        ]
        self.tdclib.TDC_calcLftModelFct.restype = ctypes.c_int32
        self.tdclib.TDC_generateLftDemo.argtypes = [
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_double,
        ]
        self.tdclib.TDC_generateLftDemo.restype = ctypes.c_int32
        self.tdclib.TDC_fitLftHistogram.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_int32,
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_int32),
        ]
        self.tdclib.TDC_fitLftHistogram.restype = ctypes.c_int32

        if platform.system() == "Windows":
            # ------- tdchg2.h --------------------------------------------------------
            self.tdclib.TDC_enableHg2.restype = ctypes.c_int32
            self.tdclib.TDC_enableHg2.argtypes = [ctypes.c_int32]
            self.tdclib.TDC_getHg2Input.restype = ctypes.c_int32
            self.tdclib.TDC_getHg2Input.argtypes = [
                ctypes.POINTER(ctypes.c_int32),
                ctypes.POINTER(ctypes.c_int32),
                ctypes.POINTER(ctypes.c_int32),
            ]
            self.tdclib.TDC_getHg2Params.restype = ctypes.c_int32
            self.tdclib.TDC_getHg2Params.argtypes = [
                ctypes.POINTER(ctypes.c_int32),
                ctypes.POINTER(ctypes.c_int32),
            ]
            self.tdclib.TDC_getHg2Raw.restype = ctypes.c_int32
            self.tdclib.TDC_getHg2Raw.argtypes = [
                ctypes.POINTER(ctypes.c_longlong),
                ctypes.POINTER(ctypes.c_longlong),
                ctypes.POINTER(ctypes.c_longlong),
                ctypes.POINTER(ctypes.c_longlong),
                ctypes.POINTER(ctypes.c_int32),
            ]
            self.tdclib.TDC_resetHg2Correlations.restype = ctypes.c_int32
            self.tdclib.TDC_resetHg2Correlations.argtypes = None
            self.tdclib.TDC_setHg2Input.restype = ctypes.c_int32
            self.tdclib.TDC_setHg2Input.argtypes = [
                ctypes.c_int32,
                ctypes.c_int32,
                ctypes.c_int32,
            ]
            self.tdclib.TDC_setHg2Params.restype = ctypes.c_int32
            self.tdclib.TDC_setHg2Params.argtypes = [ctypes.c_int32, ctypes.c_int32]
            self.tdclib.TDC_calcHg2G2.restype = ctypes.c_int32
            self.tdclib.TDC_calcHg2G2.argtypes = [
                ctypes.POINTER(ctypes.c_double),
                ctypes.POINTER(ctypes.c_int32),
                ctypes.c_int32,
            ]
            self.tdclib.TDC_calcHg2Tcp.argtypes = [
                ctypes.POINTER(ctypes.POINTER(ctypes.c_longlong)),
                ctypes.c_int32,
            ]
            self.tdclib.TDC_calcHg2Tcp.restype = ctypes.c_int32

    # Init --------------------------------------------------------------
    def Initialize(self):
        """Initializing the quTAG by DLL cunction TDC_init with device number -1 \n

        @rtype: string
        @return: Returns error code via dictionary

        """
        ans = self.tdclib.TDC_init(self.dev_nr)

        if ans != 0:
            print("Error in TDC_init: " + self.err_dict[ans])
        return ans

    def deInitialize(self):
        """Deinitializing the quTAG by DLL cunction TDC_deInit \n
        Important to clear the connection to reconnect to the device \n
        Return error code via dictionary
        """
        ans = self.tdclib.TDC_deInit()

        if ans != 0:  # from the documentation: "never fails"
            print("Error in TDC_deInit: " + self.err_dict[ans])
        return ans

    # Device Info -------------------------------------------------------------
    def getVersion(self):
        return self.tdclib.TDC_getVersion()

    def getTimebase(self):
        timebase = ctypes.c_double()
        ans = self.tdclib.TDC_getTimebase(ctypes.byref(timebase))
        if ans != 0:
            print("Error in TDC_getTimebase: " + self.err_dict[ans])
        return timebase.value

    def getDeviceType(self):
        ans = self.tdclib.TDC_getDevType()
        return ans

    def checkFeatureHBT(self):
        ans = self.tdclib.TDC_checkFeatureHbt()
        return ans == 1

    def checkFeatureLifetime(self):
        ans = self.tdclib.TDC_checkFeatureLifeTime()
        return ans == 1

    def checkFeatureFiveChan(self):
        ans = self.tdclib.TDC_checkFeatureFiveChan()
        return ans == 1

    def getFiveChannelMode(self):
        enable = ctypes.c_int32()
        ans = self.tdclib.TDC_getFiveChannelMode(ctypes.byref(enable))
        if ans != 0:
            print("Error in TDC_getFiveChannelMode: " + self.err_dict[ans])
        return enable.value == 1

    def getSingleStopPreselection(self):
        enable = ctypes.c_int32()
        ans = self.tdclib.TDC_getSingleStopPreselection(ctypes.byref(enable))
        if ans != 0:
            print("Error in TDC_getSingleStopPreselection: " + self.err_dict[ans])
        return enable.value == 1

    def preselectSingleStop(self, boolsch):
        """
        The input parameter of the Python function is a bool and gets changed to integer 0 or 1 for TDC_preselectSingleStop \n
        @type single: bool
        @param single: True and False for enable or disable

        @rtype: string
        @return: Returns the error code via the dictionary
        """
        if boolsch:
            enable = 1
        else:
            enable = 0
        ans = self.tdclib.TDC_preselectSingleStop(enable)
        if ans != 0:
            print("Error in TDC_preselectSingleStop: " + self.err_dict[ans])
        return self.err_dict[ans]

    # multiple devices ---------------------------------
    def addressDevice(self, deviceNumber):
        ans = self.tdclib.TDC_addressDevice(deviceNumber)
        if ans != 0:
            print("Error in TDC_addressDevice: " + self.err_dict[ans])
        return ans

    def connect(self, deviceNumber):
        ans = self.tdclib.TDC_connect(deviceNumber)
        if ans != 0:
            print("Error in TDC_connect: " + self.err_dict[ans])
        return ans

    def disconnect(self, deviceNumber):
        ans = self.tdclib.TDC_disconnect(deviceNumber)
        if ans != 0:
            print("Error in TDC_disconnect: " + self.err_dict[ans])
        return ans

    def discover(self):
        devCount = ctypes.c_uint32()
        ans = self.tdclib.TDC_discover(ctypes.byref(devCount))
        if ans != 0:
            print("Error in TDC_discover: " + self.err_dict[ans])
        return devCount.value

    def getCurrentAddress(self):
        devNo = ctypes.c_unit32()
        ans = self.tdclib.TDC_getCurrentAddress(ctypes.byref(devNo))
        if ans != 0:
            print("Error in TDC_getCurrentAddress: " + self.err_dict[ans])
        return devNo.value

    def getDeviceInfo(self, deviceNumber):
        devicetype = ctypes.c_int32()
        deviceid = ctypes.c_int32()
        serialnumber = ctypes.c_char_p()
        connected = ctypes.c_int32()

        ans = self.tdclib.TDC_getDeviceInfo(
            deviceNumber,
            ctypes.byref(devicetype),
            ctypes.byref(deviceid),
            ctypes.byref(serialnumber),
            ctypes.byref(connected),
        )

        if ans != 0:
            print("Error in TDC_getDeviceInfo: " + self.err_dict[ans])

        return (devicetype.value, deviceid.value, serialnumber.value, connected.value)

    # Configure Channels ----------------------------------------------------------------
    def getSignalConditioning(self, channel):
        edg = ctypes.c_int32()
        threshold = ctypes.c_double()

        ans = self.tdclib.TDC_getSignalConditioning(
            channel, ctypes.byref(edg), ctypes.byref(threshold)
        )

        if ans != 0:
            print("Error in TDC_getSignalConditioning: " + self.err_dict[ans])

        return (edg.value == 1, threshold.value)

    def setSignalConditioning(self, channel, conditioning, edge, threshold):
        if edge:
            edge_value = 1  # True: Rising
        else:
            edge_value = 0  # False: Falling

        ans = self.tdclib.TDC_configureSignalConditioning(
            channel, conditioning, edge_value, threshold
        )
        if ans != 0:
            print("Error in TDC_configureSignalConditioning: " + self.err_dict[ans])
        return ans

    def getDivider(self):
        divider = ctypes.c_int32()
        reconstruct = ctypes.c_bool()
        ans = self.tdclib.TDC_getSyncDivider(
            ctypes.byref(divider), ctypes.byref(reconstruct)
        )

        if ans != 0:
            print("Error in TDC_getSyncDivider: " + self.err_dict[ans])

        return (divider.value, reconstruct.value)

    def setDivider(self, divider, reconstruct):
        # allowed values:
        # - quTAG: 1, 2, 4, 8
        ans = self.tdclib.TDC_configureSyncDivider(divider, reconstruct)
        if ans != 0:
            print("Error in TDC_configureSyncDivider: " + self.err_dict[ans])
        return ans

    def getChannelDelays(self):
        delays = np.zeros(int(8), dtype=np.int32)
        ans = self.tdclib.TDC_getChannelDelays(
            delays.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        )
        if ans != 0:
            print("Error in TDC_getChannelDelays: " + self.err_dict[ans])
        return delays

    def setChannelDelays(self, delays):
        ans = self.tdclib.TDC_setChannelDelays(
            delays.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        )
        if ans != 0:
            print("Error in TDC_setChannelDelays: " + self.err_dict[ans])
        return ans

    def getDeadTime(self, chn):
        # chn = ctypes.c_int32()
        deadTime = ctypes.c_int32()
        ans = self.tdclib.TDC_getDeadTime(chn, ctypes.byref(deadTime))
        if ans != 0:
            print("Error in TDC_getDeadTime: " + self.err_dict[ans])
        return deadTime.value

    def setDeadTime(self, chn, deadTime):
        ans = self.tdclib.TDC_setDeadTime(chn, deadTime)
        if ans != 0:
            print("Error in TDC_setDeadTime: " + self.err_dict[ans])
        return ans

    def setFiveChannelMode(self, enable):
        if enable:
            ena = 1
        else:
            ena = 0
        ans = self.tdclib.TDC_setFiveChannelMode(ena)
        if ans != 0:
            print("Error in TDC_setFiveChannelMode: " + self.err_dict[ans])
        return ans

    def enableTDCInput(self, enable):
        if enable:
            value = 1  # enable input
        else:
            value = 0  # disable input

        ans = self.tdclib.TDC_enableTdcInput(value)
        if ans != 0:
            print("Error in TDC_enableTdcInput: " + self.err_dict[ans])

        return ans

    def enableChannels(self, channels):
        if channels:
            bitstring = ""
            for k in range(max(channels) + 1):
                if k in channels:
                    bitstring = "1" + bitstring
                else:
                    bitstring = "0" + bitstring
        else:
            bitstring = "0"

        channelMask = int(bitstring, 2)
        ans = self.tdclib.TDC_enableChannels(channelMask)
        if ans != 0:
            print("Error in TDC_enableChannels: " + self.err_dict[ans])

        return ans

    def getChannelsEnabled(self):
        channelMask = ctypes.c_int32()
        ans = self.tdclib.TDC_getChannelsEnabled(ctypes.byref(channelMask))

        channels = [0 for i in range(self.TDC_QUTAG_CHANNELS)]
        mask = channelMask.value
        i = 1
        while mask > 0:
            # channels[self.TDC_QUTAG_CHANNELS-i] = mask.value % 2
            channels[self.TDC_QUTAG_CHANNELS - i] = mask % 2
            mask //= 2
            i += 1
            if i > self.TDC_QUTAG_CHANNELS:
                print("Error in computing channelMask (getChannelsEnabled).")
                break

        if ans != 0:
            print("Error in TDC_enableChannels: " + self.err_dict[ans])
        return channels

    def enableMarkers(self, markers):
        if markers:
            bitstring = ""
            for k in range(max(markers) + 1):
                if k in markers:
                    bitstring = "1" + bitstring
                else:
                    bitstring = "0" + bitstring
        else:
            bitstring = "0"

        markerMask = int(bitstring, 2)
        ans = self.tdclib.TDC_enableMarkers(markerMask)
        if ans != 0:
            print("Error in TDC_enableMarkers: " + self.err_dict[ans])

        return ans

    # Define Measurements -------------------------------------------------------
    def setCoincidenceWindow(self, coincWin):
        ans = self.tdclib.TDC_setCoincidenceWindow(coincWin)
        if ans != 0:
            print("Error in TDC_setCoincidenceWindows: " + self.err_dict[ans])
        return 0

    def setExposureTime(self, expTime):
        ans = self.tdclib.TDC_setExposureTime(expTime)
        if ans != 0:
            print("Error in TDC_setExposureTime: " + self.err_dict[ans])
        return ans

    def getDeviceParams(self):
        chn = ctypes.c_int32()
        coinc = ctypes.c_int32()
        exptime = ctypes.c_int32()

        ans = self.tdclib.TDC_getDeviceParams(
            ctypes.byref(coinc), ctypes.byref(exptime)
        )
        if ans != 0:
            print("Error in TDC_getDeviceParams: " + self.err_dict[ans])
        return (chn.value, coinc.value, exptime.value)

    # Self test ---------------------------------------------------------------------
    def configureSelftest(self, channels, period, burstSize, burstDist):
        if channels:
            bitstring = ""
            for k in range(max(channels) + 1):
                if k in channelsgetDeviceInfo:
                    bitstring = "1" + bitstring
                else:
                    bitstring = "0" + bitstring
        else:
            bitstring = "0"

        channelMask = int(bitstring, 2)
        ans = self.tdclib.TDC_configureSelftest(
            channelMask, period, burstSize, burstDist
        )
        if ans != 0:
            print("Error in TDC_configureSelftest: " + self.err_dict[ans])

        return ans

    def generateTimestamps(self, simtype, par, count):
        # ans = self.tdclib.TDC_generateTimestamps(simtype,ctypes.byref(par),count)
        ans = self.tdclib.TDC_generateTimestamps(simtype, par, count)
        if ans != 0:
            print("Error in TDC_generateTimestamps: " + self.err_dict[ans])
        return ans

    # Timestamping ---------------------------------------------------------
    def getBufferSize(self):
        sz = ctypes.c_int32()
        ans = self.tdclib.TDC_getTimestampBufferSize(ctypes.byref(sz))
        if ans != 0:
            print("Error in TDC_getTimestampBufferSize: " + self.err_dict[ans])
        return sz.value

    def setBufferSize(self, size):
        self._bufferSize = size
        ans = self.tdclib.TDC_setTimestampBufferSize(size)
        if ans != 0:
            print("Error in TDC_setTimestampBufferSize: " + self.err_dict[ans])
        return ans

    def getDataLost(self):
        lost = ctypes.c_int32()
        ans = self.tdclib.TDC_getDataLost(ctypes.byref(lost))
        if ans != 0:
            print("Error in TDC_getDataLost: " + self.err_dict[ans])
        return lost.value

    def freezeBuffers(self, freeze):
        if freeze:
            freeze_value = 1
        else:
            freeze_value = 0
        ans = self.tdclib.TDC_freezeBuffers(freeze_value)
        if ans != 0:
            print("Error in TDC_freezeBuffers: " + self.err_dict[ans])

        return ans

    def getLastTimestamps(self, reset):
        timestamps = np.zeros(int(self._bufferSize), dtype=np.int64)
        channels = np.zeros(int(self._bufferSize), dtype=np.int8)
        valid = ctypes.c_int32()

        ans = self.tdclib.TDC_getLastTimestamps(
            reset,
            timestamps.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
            channels.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
            ctypes.byref(valid),
        )
        if ans != 0:  # "never fails"
            print("Error in TDC_getLastTimestamps: " + self.err_dict[ans])

        return (timestamps, channels, valid.value)

    # File IO -------------------------------------------
    def writeTimestamps(self, filename, fileformat):
        filename = filename.encode("utf-8")
        ans = self.tdclib.TDC_writeTimestamps(filename, fileformat)
        if ans != 0:
            print("Error in TDC_writeTimestamps: " + self.err_dict[ans])
        return ans

    def inputTimestamps(self, timestamps, channels, count):
        ans = self.tdclib.TDC_inputTimestamps(
            ctypes.byref(timestamps), ctypes.byref(channels), count
        )
        if ans != 0:
            print("Error in TDC_inputTimestamps: " + self.err_dict[ans])
        return ans

    def readTimestamps(self, filename, fileformat):
        filename = filename.encode("utf-8")
        ans = self.tdclib.TDC_readTimestamps(filename, fileformat)
        if ans != 0:
            print("Error in TDC_readTimestamps: " + self.err_dict[ans])
        return ans

    # get a histogram of coincidences calculated using our C program using the
    # time tags + channels + the number of valid time tags as we get them when
    # we get the set of last coincidences. histlen is the number of entries in
    # the histogram the function returns a numpy array hist containing the
    # histogram for time delays in the range [T1,T2] between channels ch1 and
    # ch2. We only look at delays where events in ch2 happen after or at the
    # same time as in ch1. "n" is the block size used for generating the
    # histogram block by block from the timetags supplied
    def getCoincidenceHistogram(self, tags, chs, valid, ch1, ch2, dt, T1, T2, histlen):
        hist = np.zeros(int(histlen), dtype=np.int64)
        DT = (T2 - T1) / histlen
        delays = np.arange(histlen) * DT
        hist = np.zeros(int(histlen), dtype=np.int64)
        self.coincLib.determineCoincidenceHistogram(
            tags.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
            chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
            ctypes.c_longlong(valid),
            ctypes.c_longlong(ch1),
            ctypes.c_longlong(ch2),
            ctypes.c_double(dt),
            ctypes.c_double(T1),
            ctypes.c_double(T2),
            hist.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
            ctypes.c_longlong(histlen),
        )
        return (delays, hist)

    def getSimpleHistogram(self, tags, channels, valid, ch1, ch2, maxT, dt, bins):
        DT = maxT / bins
        delays = np.arange(bins, dtype=np.double) * DT
        coinc = np.zeros(bins, dtype=np.longlong)
        for i in np.arange(delays.size):
            if i % (delays.size / 10) == 0:
                print("histogram progress (%): ", ((100.0 * i) / (1.0 * delays.size)))
            coinc[i] = self.coincLib.determineCoincidences(
                tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
                channels.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
                valid,
                ch1,
                ch2,
                dt,
                delays[i],
                maxT,
            )
        return (delays, coinc)

    def collectSimpleHistogram(self, ch1, ch2, DT1, DT2, maxT, bins, dt, intT):
        self.setDeadTime(ch1, DT1)
        self.setDeadTime(ch2, DT2)
        delays = np.arange(bins, dtype=np.double) * dt
        coinc = np.zeros(bins, dtype=np.longlong)
        valids = np.zeros(bins, dtype=np.longlong)
        for i in np.arange(delays.size):
            print("delay (s): ", delays[i])
            (tags, chs, valids[i]) = self.getLastTimestamps(True)
            time.sleep(intT)
            (tags, chs, valids[i]) = self.getLastTimestamps(True)
            coinc[i] = self.coincLib.determineCoincidences(
                tags.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
                chs.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
                valids[i],
                ch1,
                ch2,
                dt,
                delays[i],
                maxT,
            )
            print("coinc[", i, "]: ", coinc[i])
        return (delays, coinc, valids)

    # Counting --------------------------------------------
    def getCoincCounters(self):
        data = np.zeros(int(31), dtype=np.int32)
        update = ctypes.c_int32()
        ans = self.tdclib.TDC_getCoincCounters(
            data.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), ctypes.byref(update)
        )
        if ans != 0:  # "never fails"
            print("Error in TDC_getCoincCounters: " + self.err_dict[ans])
        return (data, update.value)

    # Start-Stop --------------------------------------------------------
    def enableStartStop(self, enable):
        if enable:
            ena_value = 1
        else:
            ena_value = 0
        ans = self.tdclib.TDC_enableStartStop(ena_value)
        if ans != 0:
            print("Error in TDC_enableStartStop: " + self.err_dict[ans])
        return ans

    def addHistogram(self, startChannel, stopChannel, enable):
        self.enableStartStop(True)
        if enable:
            ena_value = 1
        else:
            ena_value = 0
        ans = self.tdclib.TDC_addHistogram(startChannel, stopChannel, ena_value)
        if ans != 0:
            print("Error in TDC_addHistogram: " + self.err_dict[ans])
        return ans

    def setHistogramParams(self, binWidth, binCount):
        self._StartStopBinCount = binCount
        ans = self.tdclib.TDC_setHistogramParams(binWidth, binCount)
        if ans != 0:
            print("Error in TDC_setHistogramParams: " + self.err_dict[ans])
        return ans

    def getHistogramParams(self):
        binWidth = ctypes.c_int32()
        binCount = ctypes.c_int32()
        ans = self.tdclib.TDC_getHistogramParams(
            ctypes.byref(binWidth), ctypes.byref(binCount)
        )
        if ans != 0:
            print("Error in TDC_getHistogramParams: " + self.err_dict[ans])
        return (binWidth.value, binCount.value)

    def clearAllHistograms(self):
        ans = self.tdclib.TDC_clearAllHistograms()
        if ans != 0:
            print("Error in TDC_clearAllHistograms: " + self.err_dict[ans])
        return ans

    def getHistogram(self, chanA, chanB, reset):
        if reset:
            reset_value = 1
        else:
            reset_value = 0
        data = np.zeros(self._StartStopBinCount, dtype=np.int32)
        count = ctypes.c_int32()
        tooSmall = ctypes.c_int32()
        tooLarge = ctypes.c_int32()
        starts = ctypes.c_int32()
        stops = ctypes.c_int32()
        expTime = ctypes.c_longlong()
        ans = self.tdclib.TDC_getHistogram(
            chanA,
            chanB,
            reset_value,
            data.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
            ctypes.byref(count),
            ctypes.byref(tooSmall),
            ctypes.byref(tooLarge),
            ctypes.byref(starts),
            ctypes.byref(stops),
            ctypes.byref(expTime),
        )
        if ans != 0:
            print("Error in TDC_getHistogram: " + self.err_dict[ans])

        return (
            data,
            count.value,
            tooSmall.value,
            tooLarge.value,
            starts.value,
            stops.value,
            expTime.value,
        )

    # Lifetime ----------------------------------------------------------
    def enableLFT(self, enable):
        if enable:
            ena = 1
        else:
            ena = 0
        ans = self.tdclib.TDC_enableLft(ena)
        if ans != 0:
            print("Error in TDC_enableLft: " + self.err_dict[ans])
        return ans

    def setLFTParams(self, binWidth, binCount):
        self._LFTBufferSize = binCount
        ans = self.tdclib.TDC_setLftParams(binWidth, binCount)
        if ans != 0:
            print("Error in TDC_setLftParams: " + self.err_dict[ans])
        return ans

    def getLFTParams(self):
        binWidth = ctypes.c_int32()
        binCount = ctypes.c_int32()
        ans = self.tdclib.TDC_getLftParams(
            ctypes.byref(binWidth), ctypes.byref(binCount)
        )
        if ans != 0:
            print("Error in TDC_getLftParams: " + self.err_dict[ans])
        return binWidth.value, binCount.value

    def setLFTStartInput(self, startChannel):
        ans = self.tdclib.TDC_setLftStartInput(startChannel)
        if ans != 0:
            print("Error in TDC_setLftStartInput: " + self.err_dict[ans])
        return ans

    def getLFTStartInput(self):
        startChannel = ctypes.c_int32()
        ans = self.tdclib.TDC_getLFTStartInput(ctypes.byref(startChannel))
        if ans != 0:
            print("Error in TDC_getLFTStartInput: " + self.err_dict[ans])
        return startChannel.value

    def resetLFTHistograms(self):
        ans = self.tdclib.TDC_resetLftHistograms()
        if ans != 0:
            print("Error in TDC_resetLftHistrograms: " + self.err_dict[ans])
        return ans

    def createLFTFunction(self):
        LFTfunction = self.tdclib.TDC_createLftFunction()
        return LFTfunction

    def releaseLFTFunction(self, LFTfunction):
        self.tdclib.TDC_releaseLftFunction(LFTfunction)
        return 0

    def addLFTHistogram(self, stopchannel, enable):
        if enable:
            ena = 1
        else:
            ena = 0

        ans = self.tdclib.TDC_addLftHistogram(stopchannel, ena)
        if ans != 0:
            print("Error in TDC_addLftHistogram: " + self.err_dict[ans])
        return ans

    def analyseLFTFunction(self, lft):
        capacity = ctypes.c_int32()
        size = ctypes.c_int32()
        binWidth = ctypes.c_int32()
        values = np.zeros(self._LFTBufferSize, dtype=np.double)

        self.tdclib.TDC_analyseLftFunction(
            lft,
            ctypes.byref(capacity),
            ctypes.byref(size),
            ctypes.byref(binWidth),
            values.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            self._LFTBufferSize,
        )
        return (capacity.value, size.value, binWidth.value, values)

    def getLFTHistogram(self, channel, reset, lft):
        print("getLFTHistogram")
        tooBig = ctypes.c_int32()
        startevt = ctypes.c_int32()
        stopevt = ctypes.c_int32()
        expTime = ctypes.c_longlong()
        if reset:
            resetvalue = 1
        else:
            resetvalue = 0

        ans = self.tdclib.TDC_getLftHistogram(
            channel,
            resetvalue,
            lft,
            ctypes.byref(tooBig),
            ctypes.byref(startevt),
            ctypes.byref(stopevt),
            ctypes.byref(expTime),
        )
        if ans != 0:
            print("Error in TDC_getLFTHistogram: " + self.err_dict[ans])
        return (tooBig.value, startevt.value, stopevt.value, expTime.value, lft)

    def calcLFTModelFCT(self, lfttype, params, lftfunction):
        c_params = np.zeros(self.LFT_PARAM_SIZE, dtype=np.double)
        for i in range(len(params)):
            if i < self.LFT_PARAM_SIZE:
                c_params[i] = params[i]
            else:
                break
        ans = self.qutools.TDC_calcLftModelFct(
            lfttype,
            c_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            lftfunction,
        )
        if ans != 0:
            print("Error in TDC_calcLftModelFct: " + self.err_dict[ans])
        return ans

    def generateLFTDemo(self, lfttype, params, noiseLv):
        c_params = np.zeros(self.LFT_PARAM_SIZE, dtype=np.double)
        for i in range(len(params)):
            if i < self.LFT_PARAM_SIZE:
                c_params[i] = params[i]
            else:
                break
        ans = self.qutools.TDC_generateLftDemo(
            lfttype, c_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), noiseLv
        )
        if ans != 0:
            print("Error in TDC_generateLftDemo: " + self.err_dict[ans])
        return ans

    def fitLFTHistogram(self, lft, lfttype, startParams):
        c_params = np.zeros(self.LFT_PARAM_SIZE, dtype=np.double)
        for i in range(len(startParams)):
            if i < self.LFT_PARAM_SIZE:
                c_params[i] = startParams[i]
            else:
                break
        fitParams = np.zeros(4, dtype=np.double)
        iterations = ctypes.c_int32()

        ans = self.tdclib.TDC_fitLftHistogram(
            lft,
            lfttype,
            c_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            fitParams.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            ctypes.byref(iterations),
        )
        if ans != 0:
            print("Error in TDC_fitLftHistogram: " + self.err_dict[ans])
        return (fitParams, iterations.value)

    # HBT ---------------------------------------------------------------
    def enableHBT(self, enable):
        if enable:
            ena_value = 1
        else:
            ena_value = 0
        ans = self.tdclib.TDC_enableHbt(ena_value)
        if ans != 0:
            print("Error in TDC_enableHbt: " + self.err_dict[ans])
        return ans

    def setHBTParams(self, binWidth, binCount):
        ans = self.tdclib.TDC_setHbtParams(binWidth, binCount)
        self._HBTBufferSize = binCount * 2 - 1
        if ans != 0:
            print("Error in TDC_setHbtParams: " + self.err_dict[ans])
        return ans

    def getHBTParams(self):
        binWidth = ctypes.c_int32()
        binCount = ctypes.c_int32()
        ans = self.tdclib.TDC_setHbtParams(
            ctypes.byref(binWidth), ctypes.byref(binCount)
        )
        if ans != 0:
            print("Error in TDC_getHbtParams: " + self.err_dict[ans])
        return (binWidth.value, binCount.value)

    def setHBTDetectorParams(self, jitter):
        ans = self.tdclib.TDC_setHbtDetectorParams(jitter)
        if ans != 0:
            print("Error in TDC_setHbtDetectorParams: " + self.err_dict[ans])
        return ans

    def getHBTDetectorParams(self):
        jitter = ctypes.c_double()
        ans = self.tdclib.TDC_getHbtDetectorParams(ctypes.byref(jitter))
        if ans != 0:
            print("Error in TDC_getHbtdetectorParams: " + self.err_dict[ans])
        return jitter.value

    def setHBTInput(self, channel1, channel2):
        ans = self.tdclib.TDC_setHbtInput(channel1, channel2)
        if ans != 0:
            print("Error in TDC_setHbtInput: " + self.err_dict[ans])
        return ans

    def getHBTInput(self):
        channel1 = ctypes.c_int32()
        channel2 = ctypes.c_int32()
        ans = self.tdclib.TDC_getHbtInput(
            ctypes.byref(channel1), ctypes.byref(channel2)
        )
        if ans != 0:
            print("Error in TDC_getHbtInput: " + self.err_dict[ans])
        return (channel1.value, channel2.value)

    def resetHBTCorrelations(self):
        ans = self.tdclib.TDC_resetHbtCorrelations()
        if ans != 0:
            print("Error in TDC_resetHbtCorrelations: " + self.err_dict[ans])
        return ans

    def getHBTEventCount(self):
        totalCount = ctypes.c_longlong()
        lastCount = ctypes.c_longlong()
        lastRate = ctypes.c_double()
        ans = self.tdclib.TDC_getHbtEventCount(
            ctypes.byref(totalCount), ctypes.byref(lastCount), ctypes.byref(lastRate)
        )
        if ans != 0:
            print("Error in TDC_getHbtEventCount: " + self.err_dict[ans])
        return (totalCount.value, lastCount.value, lastRate.value)

    def getHBTIntegrationTime(self):
        intTime = ctypes.c_double()
        ans = self.tdclib.TDC_getHbtIntegrationTime(ctypes.byref(intTime))
        if ans != 0:
            print("Error in TDC_getHbtIntegrationTime: " + self.err_dict[ans])
        return intTime.value

    def getHBTCorrelations(self, forward, hbtfunction):
        ans = self.tdclib.TDC_getHbtCorrelations(forward, hbtfunction)
        if ans != 0:
            print("Error in TDC_getHbtCorrelations: " + self.err_dict[ans])
        return ans

    def calcHBTG2(self, hbtfunction):
        ans = self.tdclib.TDC_calcHbtG2(hbtfunction)
        if ans != 0:
            print("Error in TDC_calcHbtG2: " + self.err_dict[ans])
        return ans

    def fitHBTG2(self, hbtfunction, fitType, startParams):
        c_params = np.zeros(self.HBT_PARAM_SIZE, dtype=np.double)
        for i in range(len(startParams)):
            if i < self.HBT_PARAM_SIZE:
                c_params[i] = startParams[i]
            else:
                break
        fitParams = np.zeros(self.HBT_PARAM_SIZE, dtype=np.double)
        iterations = ctypes.c_int32()

        ans = self.tdclib.TDC_fitHbtG2(
            hbtfunction,
            fitType,
            c_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            fitParams.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            ctypes.byref(iterations),
        )
        if ans != 0:
            print("Error in TDC_fitHbtG2: " + self.err_dict[ans])
        return (fitParams, iterations.value)

    def getHBTFitStartParams(self, fctType):
        fitParams = np.zeros(self.HBT_PARAM_SIZE, dtype=np.double)
        ans = self.tdclib.TDC_getHbtFitStartParams(
            fctType, fitParams.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        )
        if ans != 0:
            print("Error in TDC_getHbtFitStartParams: " + self.err_dict[ans])
        return fitParams

    def calcHBTModelFct(self, fctType, params, hbtfunction):
        c_params = np.zeros(self.HBT_PARAM_SIZE, dtype=np.double)
        for i in range(len(params)):
            if i < self.HBT_PARAM_SIZE:
                c_params[i] = params[i]
            else:
                break
        ans = self.tdclib.TDC_calcHbtModelFct(
            fctType,
            c_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            hbtfunction,
        )
        if ans != 0:
            print("Error in TDC_calcHbtModelFct: " + self.err_dict[ans])
        return ans

    def generateHBTDemo(self, fctType, params, noiseLv):
        c_params = np.zeros(self.HBT_PARAM_SIZE, dtype=np.double)
        for i in range(len(params)):
            if i < self.HBT_PARAM_SIZE:
                c_params[i] = params[i]
            else:
                break
        ans = self.tdclib.TDC_generateHbtDemo(
            fctType, c_params.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), noiseLv
        )
        if ans != 0:
            print("Error in TDC_generateHbtDemo: " + self.err_dict[ans])
        return ans

    def createHBTFunction(self):
        return self.tdclib.TDC_createHbtFunction()

    def releaseHBTFunction(self, hbtfunction):
        self.tdclib.TDC_releaseHbtFunction(hbtfunction)
        return 0

    def analyzeHBTFunction(self, hbtfunction):
        capacity = ctypes.c_int32()
        size = ctypes.c_int32()
        binWidth = ctypes.c_int32()
        iOffset = ctypes.c_int32()
        values = np.zeros(self._HBTBufferSize, dtype=np.double)
        self.tdclib.TDC_analyseHbtFunction(
            hbtfunction,
            ctypes.byref(capacity),
            ctypes.byref(size),
            ctypes.byref(binWidth),
            ctypes.byref(iOffset),
            values.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            self._HBTBufferSize,
        )

        return (capacity.value, size.value, binWidth.value, iOffset.value, values)

    # Heralded g(2) ----------------------------------------------------------
    def enableHg2(self, enable):
        if enable:
            ena = 1
        else:
            ena = 0
        ans = self.tdclib.TDC_enableHg2(ena)
        if ans != 0:
            print("Error in TDC_enableLft: " + self.err_dict[ans])
        return self.err_dict[ans]

    def setHg2Params(self, binWidth, binCount):
        ans = self.tdclib.TDC_setHg2Params(binWidth, binCount)
        if ans != 0:
            print("Error in TDC_setHg2Params: " + self.err_dict[ans])
        return self.err_dict[ans]

    def getHg2Params(self):
        binWidth = ctypes.c_int32()
        binCount = ctypes.c_int32()
        ans = self.tdclib.TDC_getHg2Params(
            ctypes.byref(binWidth), ctypes.byref(binCount)
        )
        if ans != 0:
            print("Error in TDC_getHg2Params: " + self.err_dict[ans])
        return (binWidth.value, binCount.value)

    def setHg2Input(self, idler, channel1, channel2):
        ans = self.tdclib.TDC_setHg2Input(idler, channel1, channel2)
        if ans != 0:
            print("Error in TDC_setHg2Input: " + self.err_dict[ans])
        return self.err_dict[ans]

    def getHg2Input(self):
        idler = ctypes.c_int32()
        channel1 = ctypes.c_int32()
        channel2 = ctypes.c_int32()
        ans = self.tdclib.TDC_getHg2Input(
            ctypes.byref(idler), ctypes.byref(channel1), ctypes.byref(channel2)
        )
        if ans != 0:
            print("Error in TDC_getHg2Input: " + self.err_dict[ans])
        return (idler.value, channel1.value, channel2.value)

    def resetHg2Correlations(self):
        ans = self.tdclib.TDC_resetHg2Correlations()
        if ans != 0:
            print("Error in TDC_resetHg2Correlations: " + self.err_dict[ans])
        return self.err_dict[ans]

    def calcHg2G2(self, reset):
        if reset:
            resetvalue = 1
        else:
            resetvalue = 0
        binCount = self.getHg2Params()[1]
        buffer = np.zeros(binCount, dtype=np.double)
        bufSize = ctypes.c_int32(binCount)

        ans = self.tdclib.TDC_calcHg2G2(
            buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            ctypes.byref(bufSize),
            resetvalue,
        )
        if ans != 0:
            print("Error in TDC_calcHg2G2: " + self.err_dict[ans])
        return buffer

    def diffMatrix(self, a):
        x = np.reshape(a, (len(a), 1))
        return x - x.transpose()

    def getCoincidences(self, ch1, ch2, n, dt, T):
        """
        get the latest time tags, if there are more than n time tags, only take into account n
        NOTE: n should not be too large, otherwise the memory usage will become horrendous

        ch1 and ch2 are integers specifying the cannels to monitor for coincidences
        dt is the coincidence window (in seconds)
        T is the time delay between the channels (in seconds)
        """
        t0 = time.time()
        (tags, chs, valid) = self.getLastTimestamps(True)
        t1 = time.time()
        print("t1 (ms): ", (t1 - t0) * 1e3)
        baseunit = 1e-12
        baseF = 1 / baseunit
        Tint = np.int(baseF * T)
        dtInt = np.int(baseF * dt)
        if ch1 < 0 or ch2 < 0 or ch1 > 4 or ch2 > 4:
            print("please supply proper channel numbers - exiting")
            return -1  # error code
        chDiff = ch2 - ch1
        tagsNZ = tags[
            chs != 104
        ]  # the time tagger regulary (every 1ms) records time stamps in channel 104 - might be for testing purposes.
        # We get rid of those
        t2 = time.time()
        print("t2 (ms): ", (t2 - t1) * 1e3)
        chsNZ = chs[chs != 104]  # also of the corresponding channels
        t3 = time.time()
        print("t3(ms): ", (t3 - t2) * 1e3)
        if n > 100000:
            print("the 'n' you chose is too large for my taste - aborting")
            return -1  # error code
        elif n < 1:
            print("the parameter 'n' should be at least 1 - aborting")
            return -1  # error code
        mytags = tagsNZ[:n]
        t4 = time.time()
        print("t4 (ms): ", (t4 - t3) * 1e3)
        mychs = chsNZ[:n]
        t5 = time.time()
        print("t5 (ms): ", (t5 - t4) * 1e3)
        diffs = self.diffMatrix(mytags)
        t6 = time.time()
        print("t6 (ms): ", (t6 - t5) * 1e3)
        diffchs = self.diffMatrix(mychs)
        t7 = time.time()
        print("t7 (ms): ", (t7 - t6) * 1e3)
        cs = np.sum(np.abs(diffs[diffchs == chDiff] - Tint) < dtInt)
        t8 = time.time()
        print("t8 (ms): ", (t8 - t7) * 1e3)
        return (
            cs  # indicate success by returning (a nonnegative number of coincidences)
        )

    def calcHg2Tcp1D(self, reset):
        if reset:
            resetvalue = 1
        else:
            resetvalue = 0
        binCount = self.getHg2Params()[1]
        binCount2 = binCount * binCount
        buffer = np.zeros(binCount2, dtype=np.int64)
        bufSize = ctypes.c_int32(binCount2)

        ans = self.tdclib.TDC_calcHg2Tcp1D(
            buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
            ctypes.byref(bufSize),
            resetvalue,
        )
        if ans != 0:
            print("Error in TDC_calcHg2Tcp1D: " + self.err_dict[ans])
        return buffer

    def getHg2Raw(self):
        evtIdler = ctypes.c_longlong()
        evtCoinc = ctypes.c_longlong()
        binCount = self.getHg2Params()[1]
        bufSsi = np.zeros(binCount, dtype=np.int64)
        bufS2i = np.zeros(binCount, dtype=np.int64)
        bufSize = ctypes.c_int32(binCount)

        ans = self.tdclib.TDC_getHg2Raw(
            ctypes.byref(evtIdler),
            ctypes.byref(evtCoinc),
            bufSsi.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
            bufS2i.ctypes.data_as(ctypes.POINTER(ctypes.c_longlong)),
            ctypes.byref(bufSize),
        )
        if ans != 0:
            print("Error in TDC_getHg2Raw: " + self.err_dict[ans])
        return (evtIdler.value, evtCoinc.value, bufSsi, bufS2i)
