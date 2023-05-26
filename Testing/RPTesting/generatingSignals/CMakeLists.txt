cmake_minimum_required(VERSION 3.0)
project(ArbitrarySignals)

# Set the source file
set(SOURCE_FILE arbitrarySignals.c)

# Set the CFLAGS
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=gnu11 -Wall -O3") ## -Werror

# Specify the include directories
include_directories(/opt/redpitaya/include /opt/redpitaya/include/api250-12)

# Set the LDFLAGS
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -L/opt/redpitaya/lib")

# Set the LDLIBS
set(LDLIBS -static -lrp -lm -lstdc++ -lpthread)

# Add the executable target
add_executable(${CMAKE_PROJECT_NAME} ${SOURCE_FILE})

# Link against the required libraries
target_link_libraries(${CMAKE_PROJECT_NAME} ${LDLIBS})
