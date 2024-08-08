cmake_minimum_required(VERSION 3.10)
project(Example0Project)

# Specify the target executable
set(TARGET example0)

# Add the executable
add_executable(${TARGET} ${TARGET}.c)

# Include directories
target_include_directories(${TARGET} PRIVATE ../inc)

# Link directories (not needed in this case since the library is in the same directory)
# link_directories(.)  # This line can be omitted

# Link libraries
target_link_libraries(${TARGET} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/libtdcbase.so)

# Copy the shared library to the binary directory
add_custom_command(TARGET ${TARGET} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/libtdcbase.so $<TARGET_FILE_DIR:${TARGET}>
)
