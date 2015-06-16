##
## findmodule.cmake
#
## Copyright (C) 2009 Aldebaran Robotics
##
## Autogenerated by T001CHAIN.
## Do not edit


#get the current directory
get_filename_component(_ROOT_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)

clean(LIBFACTORY)
set(LIBFACTORY_INCLUDE_DIR  "${_ROOT_DIR}/../../../include/alfactory/;${_ROOT_DIR}/../../../include/" CACHE STRING "" FORCE)
set(LIBFACTORY_DEFINITIONS  "" CACHE STRING "" FORCE)
set(LIBFACTORY_DEPENDS      "LIBCORE;BOOST;PTHREAD;BOOST_SIGNALS"     CACHE STRING "" FORCE)

#cleanup this temp var
set(LIBFACTORY_tempdebug "LIBFACTORY_tempdebug-NOTFOUND" CACHE INTERNAL "Cleared." FORCE)

#try to get the debug lib
find_library(LIBFACTORY_tempdebug libfactory_d PATHS "${_ROOT_DIR}/../../" NO_DEFAULT_PATH)


if (LIBFACTORY_tempdebug)
  #use debug and optimized version
  flib(LIBFACTORY OPTIMIZED libfactory   PATHS "${_ROOT_DIR}/../../")
  flib(LIBFACTORY DEBUG     libfactory_d PATHS "${_ROOT_DIR}/../../")
else()
  #use the default lib
  flib(LIBFACTORY libfactory PATHS "${_ROOT_DIR}/../../")
endif()

export_lib(LIBFACTORY)
