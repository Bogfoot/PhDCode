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
CMAKE_SOURCE_DIR = /root/RPTesting/generatingSignals

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/RPTesting/generatingSignals/build

# Include any dependencies generated for this target.
include CMakeFiles/GenerateSignal.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/GenerateSignal.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/GenerateSignal.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/GenerateSignal.dir/flags.make

CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o: CMakeFiles/GenerateSignal.dir/flags.make
CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o: ../GenerateSignals.c
CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o: CMakeFiles/GenerateSignal.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/generatingSignals/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o -MF CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o.d -o CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o -c /root/RPTesting/generatingSignals/GenerateSignals.c

CMakeFiles/GenerateSignal.dir/GenerateSignals.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/GenerateSignal.dir/GenerateSignals.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/generatingSignals/GenerateSignals.c > CMakeFiles/GenerateSignal.dir/GenerateSignals.c.i

CMakeFiles/GenerateSignal.dir/GenerateSignals.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/GenerateSignal.dir/GenerateSignals.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/generatingSignals/GenerateSignals.c -o CMakeFiles/GenerateSignal.dir/GenerateSignals.c.s

# Object files for target GenerateSignal
GenerateSignal_OBJECTS = \
"CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o"

# External object files for target GenerateSignal
GenerateSignal_EXTERNAL_OBJECTS =

GenerateSignal: CMakeFiles/GenerateSignal.dir/GenerateSignals.c.o
GenerateSignal: CMakeFiles/GenerateSignal.dir/build.make
GenerateSignal: CMakeFiles/GenerateSignal.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/RPTesting/generatingSignals/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable GenerateSignal"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/GenerateSignal.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/GenerateSignal.dir/build: GenerateSignal
.PHONY : CMakeFiles/GenerateSignal.dir/build

CMakeFiles/GenerateSignal.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/GenerateSignal.dir/cmake_clean.cmake
.PHONY : CMakeFiles/GenerateSignal.dir/clean

CMakeFiles/GenerateSignal.dir/depend:
	cd /root/RPTesting/generatingSignals/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/RPTesting/generatingSignals /root/RPTesting/generatingSignals /root/RPTesting/generatingSignals/build /root/RPTesting/generatingSignals/build /root/RPTesting/generatingSignals/build/CMakeFiles/GenerateSignal.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/GenerateSignal.dir/depend

