##
## sdk.cmake
## Login : <ctaf@ctaf-maptop>
## Started on  Sat Oct 10 21:06:18 2009 Cedric GESTES
## $Id$
##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2009 Aldebaran Robotics
##

#WORK IN PROGRESS, ALL FUNCTION ARE MOSTLY INTERNAL AND SHOULD NOT BE DOCUMENTED
#PLEASE REFER TO THE STAGE_* DOCUMENTATION

#iterate over each EXTRA_SDK_DIRS, over each subdirs, and include root.cmake if available
function(find_sdk)
  message("find_sdk")
endfunction(find_sdk)

function(create_cmakemodule_lib _target _NAME)
  debug("SDK: create_cmakemodule_lib: (${_target}, ${_NAME})")

  set(_MODULE_NAME        ${_NAME})
  set(_MODULE_TARGET      ${_target})
  set(_MODULE_SUBFOLDER   ${${_target}_SUBFOLDER})
  set(_MODULE_DEPENDS     ${${_target}_DEPENDS})
  set(_MODULE_INCLUDE_DIR "${ARGN}")
  get_directory_property(_MODULE_DEFINITIONS COMPILE_DEFINITIONS)

  #build folder should include header from the source folder
  get_target_property(_tdebug ${_target} "LOCATION_DEBUG")
  get_target_property(_topti ${_target}  "LOCATION_RELEASE")
  string(REGEX REPLACE ".dll$" ".lib" _tdebug "${_tdebug}")
  string(REGEX REPLACE ".dll$" ".lib" _topti "${_topti}")
  set(_MODULE_LIBRARIES "optimized;${_topti};debug;${_tdebug}")
  configure_file("${T001CHAIN_DIR}/cmake/templates/findmodule.lib.cmake.in"
                 "${SDK_DIR}/${_SDK_CMAKE_MODULES}/${_NAME}Config.cmake" @ONLY)


  #TODO: use relative path (otherwize layout dont work)
  set(_MODULE_INCLUDE_DIR "\${_ROOT_DIR}/../../../${_SDK_INCLUDE}/")
  if (${_NAME}_HEADER_SUBFOLDER)
    foreach(_h ${${_NAME}_HEADER_SUBFOLDER})
      set(_MODULE_INCLUDE_DIR "\${_ROOT_DIR}/../../../${_SDK_INCLUDE}/${_h}/" ${_MODULE_INCLUDE_DIR})
    endforeach(_h ${${_NAME}_HEADER_SUBFOLDER})
  endif (${_NAME}_HEADER_SUBFOLDER)

  configure_file("${T001CHAIN_DIR}/cmake/templates/findmodule.lib.cmake.sdk.in"
                 "${CMAKE_BINARY_DIR}/${_SDK_CMAKE_MODULES}/sdk/${_NAME}Config.cmake" @ONLY)
  if (${_target}_NO_INSTALL)
    debug("target ${_NAME} is not to be installed")
  else()
    install_cmake("modules/" "${CMAKE_BINARY_DIR}/${_SDK_CMAKE_MODULES}/sdk/${_NAME}Config.cmake")
  endif()
endfunction(create_cmakemodule_lib)


function(create_cmakemodule_header _NAME)
  debug("SDK: create_cmakemodule_header: (${_NAME})")

  set(_MODULE_NAME        ${_NAME})
  set(_MODULE_TARGET      ${_target})
  set(_MODULE_SUBFOLDER   ${${_target}_SUBFOLDER})
  set(_MODULE_INCLUDE_DIR "${ARGN}")
  get_directory_property(_MODULE_DEFINITIONS COMPILE_DEFINITIONS)

  configure_file("${T001CHAIN_DIR}/cmake/templates/findmodule.header.cmake.in"
                 "${SDK_DIR}/${_SDK_CMAKE_MODULES}/${_NAME}Config.cmake" @ONLY)


  # set(_MODULE_INCLUDE_DIR "\${_ROOT_DIR}/../../../${_SDK_INCLUDE}")
  set(_MODULE_INCLUDE_DIR "\${_ROOT_DIR}/../../../${_SDK_INCLUDE}/")
  if (${_NAME}_HEADER_SUBFOLDER)
    foreach(_h ${${_NAME}_HEADER_SUBFOLDER})
      set(_MODULE_INCLUDE_DIR "\${_ROOT_DIR}/../../../${_SDK_INCLUDE}/${_h}/" ${_MODULE_INCLUDE_DIR})
    endforeach(_h ${${_NAME}_HEADER_SUBFOLDER})
  endif (${_NAME}_HEADER_SUBFOLDER)
  configure_file("${T001CHAIN_DIR}/cmake/templates/findmodule.header.cmake.sdk.in"
                 "${CMAKE_BINARY_DIR}/${_SDK_CMAKE_MODULES}/sdk/${_NAME}Config.cmake" @ONLY)
  install_cmake("modules/" "${CMAKE_BINARY_DIR}/${_SDK_CMAKE_MODULES}/sdk/${_NAME}Config.cmake")
endfunction(create_cmakemodule_header)


function(create_cmakemodule_bin _target _NAME)
  debug("SDK: create_cmakemodule_bin: (${_target}, ${_NAME})")

  set(_MODULE_NAME        ${_NAME})
  set(_MODULE_TARGET      ${_target})
  set(_MODULE_SUBFOLDER   ${${_target}_SUBFOLDER})

  #build folder should include header from the source folder
  get_target_property(_MODULE_EXECUTABLE       ${_target} "LOCATION_RELEASE")
  get_target_property(_MODULE_EXECUTABLE_DEBUG ${_target}  "LOCATION_DEBUG")
  configure_file("${T001CHAIN_DIR}/cmake/templates/findmodule.bin.cmake.in"
                 "${SDK_DIR}/${_SDK_CMAKE_MODULES}/${_NAME}Config.cmake" @ONLY)

  configure_file("${T001CHAIN_DIR}/cmake/templates/findmodule.bin.cmake.sdk.in"
                 "${CMAKE_BINARY_DIR}/${_SDK_CMAKE_MODULES}/sdk/${_NAME}Config.cmake" @ONLY)
  if (${_target}_NO_INSTALL)
    debug("target ${_NAME} is not to be installed")
  else()
    install_cmake("modules/" "${CMAKE_BINARY_DIR}/${_SDK_CMAKE_MODULES}/sdk/${_NAME}Config.cmake")
  endif()
endfunction(create_cmakemodule_bin)

function(create_cmakemodule_script _target _NAME _file)
  debug("SDK: create_cmakemodule_bin: (${_target}, ${_NAME})")

  set(_MODULE_NAME        ${_NAME})
  set(_MODULE_TARGET      ${_target})
  set(_MODULE_SUBFOLDER   ${${_target}_SUBFOLDER})

  #build folder should include header from the source folder
  set(_MODULE_EXECUTABLE       "${_file}"   CACHE INTERNAL "" FORCE)
  set(_MODULE_EXECUTABLE_DEBUG "${_file}"   CACHE INTERNAL "" FORCE)
  configure_file("${T001CHAIN_DIR}/cmake/templates/findmodule.bin.cmake.in"
                 "${SDK_DIR}/${_SDK_CMAKE_MODULES}/${_NAME}Config.cmake" @ONLY)

  configure_file("${T001CHAIN_DIR}/cmake/templates/findmodule.bin.cmake.sdk.in"
                 "${CMAKE_BINARY_DIR}/${_SDK_CMAKE_MODULES}/sdk/${_NAME}Config.cmake" @ONLY)

  if (${_target}_NO_INSTALL)
    debug("target ${_NAME} is not to be installed")
  else()
    install_cmake("modules/" "${CMAKE_BINARY_DIR}/${_SDK_CMAKE_MODULES}/sdk/${_NAME}Config.cmake")
  endif()
endfunction(create_cmakemodule_script)


function(create_root)
  debug("SDK: create_root: (${_name}, ${_prefix}, ${_header})")
  configure_file("${T001CHAIN_DIR}/cmake/templates/root.cmake.in" "${SDK_DIR}/root.cmake" @ONLY)
  install(FILES "${SDK_DIR}/root.cmake" COMPONENT "cmake" DESTINATION ".")
endfunction(create_root)

function(add_multiarch_bin_sdk _dir)
  set(_found FALSE)
  foreach(_target ${_firsttarget} ${ARGN})
    if ("${_target}" STREQUAL "${SDK_ARCH}")

      message(STATUS "SDK[multiarch]: ${_dir}")
      set(_INTERNAL_SDK_DIRS ${_INTERNAL_SDK_DIRS} "${_dir}/${_SDK_CMAKE_MODULES}" CACHE INTERNAL "" FORCE)

      set(BIN_PREFIX "${_dir}/${TARGET_ARCH}/bin/"
        "${_dir}/${TARGET_ARCH}-${TARGET_SUBARCH}/bin/"
        ${BIN_PREFIX} CACHE INTERNAL "" FORCE)

      set(LIB_PREFIX     "${_dir}/${TARGET_ARCH}/lib"
        "${_dir}/${TARGET_ARCH}-${TARGET_SUBARCH}/lib"
        ${LIB_PREFIX} CACHE INTERNAL "" FORCE)

      set(INCLUDE_PREFIX "${_dir}/${TARGET_ARCH}/include/"
        "${_dir}/${TARGET_ARCH}-${TARGET_SUBARCH}/include/"
        "${_dir}/common/include/"
        ${INCLUDE_PREFIX} CACHE INTERNAL "" FORCE)

      if (APPLE)
        set(FRAMEWORK_PREFIX "${_dir}/${TARGET_ARCH}/Frameworks/"
          ${FRAMEWORK_PREFIX} CACHE INTERNAL "" FORCE)
      endif (APPLE)
      set(_found TRUE)
      break()
    endif ("${_target}" STREQUAL "${SDK_ARCH}")

  endforeach()
  if (NOT _found)
    warning(
      " Not including sdk with bad target arch.\n"
      "WARNING: SDK: ${_dir} is only for [${_firsttarget} ${ARGN}]\n"
      "WARNING: Your current sdk arch is : ${SDK_ARCH}")
  endif (NOT _found)

endfunction()

function(add_sdk _dir _firsttarget)
  set(_found FALSE)
  foreach(_target ${_firsttarget} ${ARGN})
    if ("${_target}" STREQUAL "${SDK_ARCH}")
      message(STATUS "SDK: ${_dir}")
      set(_INTERNAL_SDK_DIRS ${_INTERNAL_SDK_DIRS} "${_dir}/${_SDK_CMAKE_MODULES}" CACHE INTERNAL "" FORCE)
      set(BIN_PREFIX     ${BIN_PREFIX}     "${_dir}/${_SDK_BIN}"                   CACHE INTERNAL "" FORCE)
      set(LIB_PREFIX     ${LIB_PREFIX}     "${_dir}/${_SDK_LIB}"                   CACHE INTERNAL "" FORCE)
      set(INCLUDE_PREFIX ${INCLUDE_PREFIX} "${_dir}/${_SDK_INCLUDE}"               CACHE INTERNAL "" FORCE)
      if (APPLE)
        set(FRAMEWORK_PREFIX ${FRAMEWORK_PREFIX} "${_dir}/${_SDK_FRAMEWORK}"       CACHE INTERNAL "" FORCE)
      endif(APPLE)

      set(_found TRUE)
      break()
    endif ("${_target}" STREQUAL "${SDK_ARCH}")
  endforeach()
  if (NOT _found)
    warning(
      " Not including sdk with bad target arch.\n"
      "WARNING: SDK: ${_dir} is only for [${_firsttarget} ${ARGN}]\n"
      "WARNING: Your current sdk arch is : ${SDK_ARCH}")
  endif (NOT _found)

endfunction(add_sdk)

#CTAF:TODO: Use Me!
# SET(CMAKE_FIND_ROOT_PATH
#   ${EXTRA_SDK_DIRS}
# #   ${OE_CROSS_DIR}/staging/${OE_PREFIX}/
# #   ${OE_CROSS_DIR}/cross
#   )

#iterate over sdk_dir
#include all root.cmake found in folder or subfolder
function(find_sdk)
  foreach(_sdk ${SDK_EXTRA_DIRS})
    debug("exploring : ${_sdk}")
    if (EXISTS "${_sdk}/root.cmake")
      verbose("found : ${_sdk}/root.cmake")
      include("${_sdk}/root.cmake")
    else (EXISTS "${_sdk}/root.cmake")
      message(STATUS "WARNING: ${_sdk} is not a valid sdk folder.")
    endif (EXISTS "${_sdk}/root.cmake")

#     file(GLOB _subsdkdirs RELATIVE "${_sdk}/" "[^.]*")
#     foreach(_subsdk ${_subsdkdirs})
#       message(STATUS "subexploring : /${_subsdk}/")
#       if (EXISTS "${_sdk}/${_subsdk}/root.cmake")
#         message(STATUS "found : ${_sdk}/${_subsdk}/root.cmake")
#       endif (EXISTS "${_sdk}/${_subsdk}/root.cmake")
#     endforeach(_subsdk ${_subsdkdirs})

  endforeach(_sdk ${SDK_EXTRA_DIRS})
endfunction(find_sdk)
