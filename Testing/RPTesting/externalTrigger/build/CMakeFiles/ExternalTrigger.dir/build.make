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
CMAKE_SOURCE_DIR = /root/RPTesting/externalTrigger

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/RPTesting/externalTrigger/build

# Include any dependencies generated for this target.
include CMakeFiles/ExternalTrigger.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/ExternalTrigger.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/ExternalTrigger.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/ExternalTrigger.dir/flags.make

CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o: CMakeFiles/ExternalTrigger.dir/flags.make
CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o: ../externalTrigger.c
CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o: CMakeFiles/ExternalTrigger.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/RPTesting/externalTrigger/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o -MF CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o.d -o CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o -c /root/RPTesting/externalTrigger/externalTrigger.c

CMakeFiles/ExternalTrigger.dir/externalTrigger.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/ExternalTrigger.dir/externalTrigger.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/RPTesting/externalTrigger/externalTrigger.c > CMakeFiles/ExternalTrigger.dir/externalTrigger.c.i

CMakeFiles/ExternalTrigger.dir/externalTrigger.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/ExternalTrigger.dir/externalTrigger.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/RPTesting/externalTrigger/externalTrigger.c -o CMakeFiles/ExternalTrigger.dir/externalTrigger.c.s

# Object files for target ExternalTrigger
ExternalTrigger_OBJECTS = \
"CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o"

# External object files for target ExternalTrigger
ExternalTrigger_EXTERNAL_OBJECTS =

ExternalTrigger: CMakeFiles/ExternalTrigger.dir/externalTrigger.c.o
ExternalTrigger: CMakeFiles/ExternalTrigger.dir/build.make
ExternalTrigger: CMakeFiles/ExternalTrigger.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/RPTesting/externalTrigger/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ExternalTrigger"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ExternalTrigger.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/ExternalTrigger.dir/build: ExternalTrigger
.PHONY : CMakeFiles/ExternalTrigger.dir/build

CMakeFiles/ExternalTrigger.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ExternalTrigger.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ExternalTrigger.dir/clean

CMakeFiles/ExternalTrigger.dir/depend:
	cd /root/RPTesting/externalTrigger/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/RPTesting/externalTrigger /root/RPTesting/externalTrigger /root/RPTesting/externalTrigger/build /root/RPTesting/externalTrigger/build /root/RPTesting/externalTrigger/build/CMakeFiles/ExternalTrigger.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ExternalTrigger.dir/depend

