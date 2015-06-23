##
## findmodule.cmake
#
## Copyright (C) 2009 Aldebaran Robotics
##
## Autogenerated by T001CHAIN.
## Do not edit


#get the current directory
get_filename_component(_ROOT_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)

clean(LIBFACTORY-STATIC)
set(LIBFACTORY-STATIC_INCLUDE_DIR  "${_ROOT_DIR}/../../../include/" CACHE STRING "" FORCE)
set(LIBFACTORY-STATIC_DEFINITIONS  "" CACHE STRING "" FORCE)
set(LIBFACTORY-STATIC_DEPENDS      "LIBCORE;BOOST;PTHREAD;BOOST_SIGNALS"     CACHE STRING "" FORCE)

#cleanup this temp var
set(LIBFACTORY-STATIC_tempdebug "LIBFACTORY-STATIC_tempdebug-NOTFOUND" CACHE INTERNAL "Cleared." FORCE)

#try to get the debug lib
find_library(LIBFACTORY-STATIC_tempdebug libfactory-static_d PATHS "${_ROOT_DIR}/../../" NO_DEFAULT_PATH)


if (LIBFACTORY-STATIC_tempdebug)
  #use debug and optimized version
  flib(LIBFACTORY-STATIC OPTIMIZED libfactory-static   PATHS "${_ROOT_DIR}/../../")
  flib(LIBFACTORY-STATIC DEBUG     libfactory-static_d PATHS "${_ROOT_DIR}/../../")
else()
  #use the default lib
  flib(LIBFACTORY-STATIC libfactory-static PATHS "${_ROOT_DIR}/../../")
endif()

export_lib(LIBFACTORY-STATIC)