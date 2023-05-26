cmake_minimum_required(VERSION 3.0)
project(rpreadandwrite)

# Add all .c files in the current directory as source files
file(GLOB SOURCES "*.c")

# Generate the shared library from the source files
add_library(rpreadandwrite_lib SHARED ${SOURCES})

# Specify the include directories for the library
target_include_directories(rpreadandwrite_lib PUBLIC .)

# Link against the rpreadandwrite library
target_link_libraries(rpreadandwrite_lib rpreadandwrite)

# Add the main.c file as the source file
add_executable(rpreadandwrite main.c)

# Link against the rpreadandwrite library
target_link_libraries(rpreadandwrite rpreadandwrite_lib)

# Install the shared library and header files
install(TARGETS rpreadandwrite_lib DESTINATION /opt/redpitaya/lib)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/rpreadandwrite.h DESTINATION /opt/redpitaya/include)

# Install the executable
install(TARGETS rpreadandwrite DESTINATION /opt/redpitaya/bin)

