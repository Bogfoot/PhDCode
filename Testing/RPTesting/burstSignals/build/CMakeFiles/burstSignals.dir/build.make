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
CMAKE_SOURCE_DIR = /root/RPTesting/burstSignals

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/RPTesting/burstSignals/build

# Include any dependencies generated for this target.
include CMakeFiles/burstSignals.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/burstSignals.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/burstSignals.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/burstSignals.dir/flags.make

CMakeFiles/burstSignals.dir/burstSignals.c.o: CMakeFiles/burstSignals.dir/flags.make
CMakeFiles/burstSignals.dir/burstSignals.c.o: ../burstSignals.c
CMakeFiles/burstSignals.dir/burstSignals.c.o: CMakeFiles/burstSignals.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/burstSignals/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/burstSignals.dir/burstSignals.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/burstSignals.dir/burstSignals.c.o -MF CMakeFiles/burstSignals.dir/burstSignals.c.o.d -o CMakeFiles/burstSignals.dir/burstSignals.c.o -c /root/RPTesting/burstSignals/burstSignals.c

CMakeFiles/burstSignals.dir/burstSignals.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/burstSignals.dir/burstSignals.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/burstSignals/burstSignals.c > CMakeFiles/burstSignals.dir/burstSignals.c.i

CMakeFiles/burstSignals.dir/burstSignals.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/burstSignals.dir/burstSignals.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/burstSignals/burstSignals.c -o CMakeFiles/burstSignals.dir/burstSignals.c.s

# Object files for target burstSignals
burstSignals_OBJECTS = \
"CMakeFiles/burstSignals.dir/burstSignals.c.o"

# External object files for target burstSignals
burstSignals_EXTERNAL_OBJECTS =

burstSignals: CMakeFiles/burstSignals.dir/burstSignals.c.o
burstSignals: CMakeFiles/burstSignals.dir/build.make
burstSignals: CMakeFiles/burstSignals.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/RPTesting/burstSignals/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable burstSignals"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/burstSignals.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/burstSignals.dir/build: burstSignals
.PHONY : CMakeFiles/burstSignals.dir/build

CMakeFiles/burstSignals.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/burstSignals.dir/cmake_clean.cmake
.PHONY : CMakeFiles/burstSignals.dir/clean

CMakeFiles/burstSignals.dir/depend:
	cd /root/RPTesting/burstSignals/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/RPTesting/burstSignals /root/RPTesting/burstSignals /root/RPTesting/burstSignals/build /root/RPTesting/burstSignals/build /root/RPTesting/burstSignals/build/CMakeFiles/burstSignals.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/burstSignals.dir/depend

