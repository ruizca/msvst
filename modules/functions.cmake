# Locate CFITSIO using pkg-config or use command line arguments to configure
# CFITSIO
function(find_cfitsio)
  if(CFITSIO_LIBRARIES STREQUAL "" OR NOT DEFINED CFITSIO_LIBRARIES OR
     CFITSIO_LIBRARY_DIRS STREQUAL "" OR NOT DEFINED CFITSIO_LIBRARY_DIRS OR
     CFITSIO_INCLUDE_DIRS STREQUAL "" OR NOT DEFINED CFITSIO_INCLUDE_DIRS)
    pkg_check_modules(CFITSIO REQUIRED cfitsio)
  else()
    message(STATUS "Use manually configured cfitsio")
    message(STATUS "  includes: ${CFITSIO_INCLUDE_DIRS}")
    message(STATUS "  libs: ${CFITSIO_LIBRARY_DIRS}")
    message(STATUS "  flags: ${CFITSIO_LIBRARIES}")
  endif()
  include_directories(${CFITSIO_INCLUDE_DIRS})
  link_directories(${CFITSIO_LIBRARY_DIRS})
endfunction()

# Extract target names from source files
function(find_targets targets target_path ext)
  file(GLOB src_targets "${sparse2d_SOURCE_DIR}/${target_path}/*.${ext}")
  list(TRANSFORM src_targets REPLACE "${sparse2d_SOURCE_DIR}/${target_path}/" "")
  list(TRANSFORM src_targets REPLACE ".${ext}" "")
  set(${targets} "${src_targets}" PARENT_SCOPE)
endfunction()

# Build library
function(build_lib library)
  file(GLOB src_${library} "${sparse2d_SOURCE_DIR}/src/msvst/lib${library}/*.cc")
  file(GLOB inc_${library} "${sparse2d_SOURCE_DIR}/src/msvst/lib${library}/*.h")
  include_directories("${sparse2d_SOURCE_DIR}/src/msvst/lib${library}")
  add_library(${library} STATIC ${src_${library}})
  target_link_libraries(${library} ${CFITSIO_LIBRARIES})
  INSTALL(FILES ${inc_${library}} DESTINATION include/msvst)
endfunction()

# Build library with path
function(build_pathlib library path)
  file(GLOB src_${library} "${sparse2d_SOURCE_DIR}/src/${path}/lib${library}/*.cc")
  file(GLOB inc_${library} "${sparse2d_SOURCE_DIR}/src/${path}/lib${library}/*.h")
  include_directories("${sparse2d_SOURCE_DIR}/src/${path}/lib${library}")
  add_library(${library} STATIC ${src_${library}})
  target_link_libraries(${library} ${CFITSIO_LIBRARIES})
  INSTALL(FILES ${inc_${library}} DESTINATION include/msvst)
endfunction()

# Build binary
function(build_bin program libs target_path ext)
  add_executable(${program} "${sparse2d_SOURCE_DIR}/${target_path}/${program}.${ext}")
  target_link_libraries(${program} ${CFITSIO_LIBRARIES} ${libs})
endfunction()
