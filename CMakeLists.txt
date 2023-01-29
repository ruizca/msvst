#################
#     MSVST     #
#################

cmake_minimum_required(VERSION 3.0.0)
project(msvst)

# Include modules in CMake module path
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/modules/")

# Load CMake tools
include(ExternalProject)
include(FindPkgConfig)

# Load custom CMake functions
include(functions)

# Set build type
if(CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE "Release")
endif()
message(STATUS "CMake Build Type: ${CMAKE_BUILD_TYPE}")

# ----------------- #
# Find Dependencies #
# ----------------- #

# Locate OpenMP
if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "AppleClang")
  find_package(BigMac 0.0.1 REQUIRED)
else()
  find_package(OpenMP REQUIRED)
endif()

# Locate CFITSIO
find_cfitsio()

set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}/msvst/")

# Set compilation flags
set(CMAKE_CXX_FLAGS
  "${CMAKE_CXX_FLAGS} -DNO_DISP_IO -fPIC -Wno-write-strings\
  ${OpenMP_CXX_FLAGS} ${BigMac_NOWARN}"
)
set(CMAKE_CXX_FLAGS_RELEASE
  "${CMAKE_CXX_FLAGS_RELEASE} -g0 -fomit-frame-pointer"
)
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0")

# ----- #
# MSVST #
# ------#

include(FetchContent)
FetchContent_Declare(
  Sparse2D
  GIT_REPOSITORY https://github.com/CosmoStat/Sparse2D.git
)
FetchContent_Populate(Sparse2D)
message(STATUS ${sparse2d_SOURCE_DIR})

# Build MSVST lib
set(msvst_libs msvst tools)
build_pathlib(msvst msvst)
build_pathlib(tools sparse)

# Find all MSVST targets
find_targets(msvst_targets src/msvst/msvstmain cc)

# Build binaries
foreach(program ${msvst_targets})
  build_bin(${program} "${msvst_libs}" src/msvst/msvstmain cc)
endforeach(program)

# Install libraries
install(TARGETS ${msvst_libs} DESTINATION lib EXPORT msvst_libs)
install(EXPORT msvst_libs DESTINATION lib/cmake)

# Install binaries
install(TARGETS ${msvst_targets} DESTINATION bin)
