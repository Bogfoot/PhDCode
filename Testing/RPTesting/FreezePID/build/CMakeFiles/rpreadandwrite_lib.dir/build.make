# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.21

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /root/RPTesting/FreezePID

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/RPTesting/FreezePID/build

# Include any dependencies generated for this target.
include CMakeFiles/rpreadandwrite_lib.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/rpreadandwrite_lib.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/rpreadandwrite_lib.dir/flags.make

CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o: ../FreezePID.c
CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o -c /root/RPTesting/FreezePID/FreezePID.c

CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/FreezePID.c > CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.i

CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/FreezePID.c -o CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.s

CMakeFiles/rpreadandwrite_lib.dir/calib.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/calib.c.o: ../calib.c
CMakeFiles/rpreadandwrite_lib.dir/calib.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/rpreadandwrite_lib.dir/calib.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/calib.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/calib.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/calib.c.o -c /root/RPTesting/FreezePID/calib.c

CMakeFiles/rpreadandwrite_lib.dir/calib.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/calib.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/calib.c > CMakeFiles/rpreadandwrite_lib.dir/calib.c.i

CMakeFiles/rpreadandwrite_lib.dir/calib.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/calib.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/calib.c -o CMakeFiles/rpreadandwrite_lib.dir/calib.c.s

CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o: ../fpga.c
CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o -c /root/RPTesting/FreezePID/fpga.c

CMakeFiles/rpreadandwrite_lib.dir/fpga.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/fpga.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/fpga.c > CMakeFiles/rpreadandwrite_lib.dir/fpga.c.i

CMakeFiles/rpreadandwrite_lib.dir/fpga.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/fpga.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/fpga.c -o CMakeFiles/rpreadandwrite_lib.dir/fpga.c.s

CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o: ../fpga_awg.c
CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o -c /root/RPTesting/FreezePID/fpga_awg.c

CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/fpga_awg.c > CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.i

CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/fpga_awg.c -o CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.s

CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o: ../fpga_lock.c
CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building C object CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o -c /root/RPTesting/FreezePID/fpga_lock.c

CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/fpga_lock.c > CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.i

CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/fpga_lock.c -o CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.s

CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o: ../fpga_pid.c
CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building C object CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o -c /root/RPTesting/FreezePID/fpga_pid.c

CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/fpga_pid.c > CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.i

CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/fpga_pid.c -o CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.s

CMakeFiles/rpreadandwrite_lib.dir/generate.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/generate.c.o: ../generate.c
CMakeFiles/rpreadandwrite_lib.dir/generate.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building C object CMakeFiles/rpreadandwrite_lib.dir/generate.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/generate.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/generate.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/generate.c.o -c /root/RPTesting/FreezePID/generate.c

CMakeFiles/rpreadandwrite_lib.dir/generate.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/generate.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/generate.c > CMakeFiles/rpreadandwrite_lib.dir/generate.c.i

CMakeFiles/rpreadandwrite_lib.dir/generate.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/generate.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/generate.c -o CMakeFiles/rpreadandwrite_lib.dir/generate.c.s

CMakeFiles/rpreadandwrite_lib.dir/lock.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/lock.c.o: ../lock.c
CMakeFiles/rpreadandwrite_lib.dir/lock.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building C object CMakeFiles/rpreadandwrite_lib.dir/lock.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/lock.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/lock.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/lock.c.o -c /root/RPTesting/FreezePID/lock.c

CMakeFiles/rpreadandwrite_lib.dir/lock.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/lock.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/lock.c > CMakeFiles/rpreadandwrite_lib.dir/lock.c.i

CMakeFiles/rpreadandwrite_lib.dir/lock.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/lock.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/lock.c -o CMakeFiles/rpreadandwrite_lib.dir/lock.c.s

CMakeFiles/rpreadandwrite_lib.dir/main.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/main.c.o: ../main.c
CMakeFiles/rpreadandwrite_lib.dir/main.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building C object CMakeFiles/rpreadandwrite_lib.dir/main.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/main.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/main.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/main.c.o -c /root/RPTesting/FreezePID/main.c

CMakeFiles/rpreadandwrite_lib.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/main.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/main.c > CMakeFiles/rpreadandwrite_lib.dir/main.c.i

CMakeFiles/rpreadandwrite_lib.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/main.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/main.c -o CMakeFiles/rpreadandwrite_lib.dir/main.c.s

CMakeFiles/rpreadandwrite_lib.dir/pid.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/pid.c.o: ../pid.c
CMakeFiles/rpreadandwrite_lib.dir/pid.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Building C object CMakeFiles/rpreadandwrite_lib.dir/pid.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/pid.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/pid.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/pid.c.o -c /root/RPTesting/FreezePID/pid.c

CMakeFiles/rpreadandwrite_lib.dir/pid.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/pid.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/pid.c > CMakeFiles/rpreadandwrite_lib.dir/pid.c.i

CMakeFiles/rpreadandwrite_lib.dir/pid.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/pid.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/pid.c -o CMakeFiles/rpreadandwrite_lib.dir/pid.c.s

CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o: ../rp_git.c
CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_11) "Building C object CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o -c /root/RPTesting/FreezePID/rp_git.c

CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/rp_git.c > CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.i

CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/rp_git.c -o CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.s

CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o: ../rpreadandwrite.c
CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) "Building C object CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o -c /root/RPTesting/FreezePID/rpreadandwrite.c

CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/rpreadandwrite.c > CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.i

CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/rpreadandwrite.c -o CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.s

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o: ../rpreadbuffer.c
CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_13) "Building C object CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o -c /root/RPTesting/FreezePID/rpreadbuffer.c

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/rpreadbuffer.c > CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.i

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/rpreadbuffer.c -o CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.s

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o: ../rpreadbuffer_01_08_2022.c
CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_14) "Building C object CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o -c /root/RPTesting/FreezePID/rpreadbuffer_01_08_2022.c

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/rpreadbuffer_01_08_2022.c > CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.i

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/rpreadbuffer_01_08_2022.c -o CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.s

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o: ../rpreadbuffer_backup_31_07_2022.c
CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_15) "Building C object CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o -c /root/RPTesting/FreezePID/rpreadbuffer_backup_31_07_2022.c

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/rpreadbuffer_backup_31_07_2022.c > CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.i

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/rpreadbuffer_backup_31_07_2022.c -o CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.s

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o: ../rpreadbuffer_before_04_07_2022.c
CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_16) "Building C object CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o -c /root/RPTesting/FreezePID/rpreadbuffer_before_04_07_2022.c

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/rpreadbuffer_before_04_07_2022.c > CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.i

CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/rpreadbuffer_before_04_07_2022.c -o CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.s

CMakeFiles/rpreadandwrite_lib.dir/worker.c.o: CMakeFiles/rpreadandwrite_lib.dir/flags.make
CMakeFiles/rpreadandwrite_lib.dir/worker.c.o: ../worker.c
CMakeFiles/rpreadandwrite_lib.dir/worker.c.o: CMakeFiles/rpreadandwrite_lib.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_17) "Building C object CMakeFiles/rpreadandwrite_lib.dir/worker.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite_lib.dir/worker.c.o -MF CMakeFiles/rpreadandwrite_lib.dir/worker.c.o.d -o CMakeFiles/rpreadandwrite_lib.dir/worker.c.o -c /root/RPTesting/FreezePID/worker.c

CMakeFiles/rpreadandwrite_lib.dir/worker.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite_lib.dir/worker.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/FreezePID/worker.c > CMakeFiles/rpreadandwrite_lib.dir/worker.c.i

CMakeFiles/rpreadandwrite_lib.dir/worker.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite_lib.dir/worker.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/FreezePID/worker.c -o CMakeFiles/rpreadandwrite_lib.dir/worker.c.s

# Object files for target rpreadandwrite_lib
rpreadandwrite_lib_OBJECTS = \
"CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/calib.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/generate.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/lock.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/main.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/pid.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o" \
"CMakeFiles/rpreadandwrite_lib.dir/worker.c.o"

# External object files for target rpreadandwrite_lib
rpreadandwrite_lib_EXTERNAL_OBJECTS =

librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/FreezePID.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/calib.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/fpga.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/fpga_awg.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/fpga_lock.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/fpga_pid.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/generate.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/lock.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/main.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/pid.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/rp_git.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/rpreadandwrite.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_01_08_2022.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_backup_31_07_2022.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/rpreadbuffer_before_04_07_2022.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/worker.c.o
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/build.make
librpreadandwrite_lib.so: CMakeFiles/rpreadandwrite_lib.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/RPTesting/FreezePID/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_18) "Linking C shared library librpreadandwrite_lib.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rpreadandwrite_lib.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/rpreadandwrite_lib.dir/build: librpreadandwrite_lib.so
.PHONY : CMakeFiles/rpreadandwrite_lib.dir/build

CMakeFiles/rpreadandwrite_lib.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/rpreadandwrite_lib.dir/cmake_clean.cmake
.PHONY : CMakeFiles/rpreadandwrite_lib.dir/clean

CMakeFiles/rpreadandwrite_lib.dir/depend:
	cd /root/RPTesting/FreezePID/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/RPTesting/FreezePID /root/RPTesting/FreezePID /root/RPTesting/FreezePID/build /root/RPTesting/FreezePID/build /root/RPTesting/FreezePID/build/CMakeFiles/rpreadandwrite_lib.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/rpreadandwrite_lib.dir/depend

