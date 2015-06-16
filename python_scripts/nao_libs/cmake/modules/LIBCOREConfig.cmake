##
## findmodule.cmake
#
## Copyright (C) 2009 Aldebaran Robotics
##
## Autogenerated by T001CHAIN.
## Do not edit


#get the current directory
get_filename_component(_ROOT_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)

clean(LIBCORE)
set(LIBCORE_INCLUDE_DIR  "${_ROOT_DIR}/../../../include/alcore/;${_ROOT_DIR}/../../../include/" CACHE STRING "" FORCE)
set(LIBCORE_DEFINITIONS  "" CACHE STRING "" FORCE)
set(LIBCORE_DEPENDS      "BOOST;PTHREAD;BOOST_SIGNALS"     CACHE STRING "" FORCE)

#cleanup this temp var
set(LIBCORE_tempdebug "LIBCORE_tempdebug-NOTFOUND" CACHE INTERNAL "Cleared." FORCE)

#try to get the debug lib
find_library(LIBCORE_tempdebug libcore_d PATHS "${_ROOT_DIR}/../../" NO_DEFAULT_PATH)


if (LIBCORE_tempdebug)
  #use debug and optimized version
  flib(LIBCORE OPTIMIZED libcore   PATHS "${_ROOT_DIR}/../../")
  flib(LIBCORE DEBUG     libcore_d PATHS "${_ROOT_DIR}/../../")
else()
  #use the default lib
  flib(LIBCORE libcore PATHS "${_ROOT_DIR}/../../")
endif()

export_lib(LIBCORE)
