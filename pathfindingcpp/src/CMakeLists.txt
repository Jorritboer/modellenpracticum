cmake_minimum_required(VERSION 3.0)
project(pathfinding)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -Wall")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

aux_source_directory(. SRC_LIST)
add_executable(${PROJECT_NAME} "${SRC_LIST}")
