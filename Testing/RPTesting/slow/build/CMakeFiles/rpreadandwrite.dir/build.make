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
CMAKE_SOURCE_DIR = /root/slow

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/slow/build

# Include any dependencies generated for this target.
include CMakeFiles/rpreadandwrite.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/rpreadandwrite.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/rpreadandwrite.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/rpreadandwrite.dir/flags.make

CMakeFiles/rpreadandwrite.dir/main.c.o: CMakeFiles/rpreadandwrite.dir/flags.make
CMakeFiles/rpreadandwrite.dir/main.c.o: ../main.c
CMakeFiles/rpreadandwrite.dir/main.c.o: CMakeFiles/rpreadandwrite.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/slow/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/rpreadandwrite.dir/main.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/rpreadandwrite.dir/main.c.o -MF CMakeFiles/rpreadandwrite.dir/main.c.o.d -o CMakeFiles/rpreadandwrite.dir/main.c.o -c /root/slow/main.c

CMakeFiles/rpreadandwrite.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/rpreadandwrite.dir/main.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /root/slow/main.c > CMakeFiles/rpreadandwrite.dir/main.c.i

CMakeFiles/rpreadandwrite.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/rpreadandwrite.dir/main.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /root/slow/main.c -o CMakeFiles/rpreadandwrite.dir/main.c.s

# Object files for target rpreadandwrite
rpreadandwrite_OBJECTS = \
"CMakeFiles/rpreadandwrite.dir/main.c.o"

# External object files for target rpreadandwrite
rpreadandwrite_EXTERNAL_OBJECTS =

rpreadandwrite: CMakeFiles/rpreadandwrite.dir/main.c.o
rpreadandwrite: CMakeFiles/rpreadandwrite.dir/build.make
rpreadandwrite: librpreadandwrite_lib.so
rpreadandwrite: CMakeFiles/rpreadandwrite.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/slow/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable rpreadandwrite"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rpreadandwrite.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/rpreadandwrite.dir/build: rpreadandwrite
.PHONY : CMakeFiles/rpreadandwrite.dir/build

CMakeFiles/rpreadandwrite.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/rpreadandwrite.dir/cmake_clean.cmake
.PHONY : CMakeFiles/rpreadandwrite.dir/clean

CMakeFiles/rpreadandwrite.dir/depend:
	cd /root/slow/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/slow /root/slow /root/slow/build /root/slow/build /root/slow/build/CMakeFiles/rpreadandwrite.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/rpreadandwrite.dir/depend

