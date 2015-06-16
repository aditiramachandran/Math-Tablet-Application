##
## findmodule.cmake
#
## Copyright (C) 2009 Aldebaran Robotics
##
## Autogenerated by T001CHAIN.
## Do not edit


#get the current directory
get_filename_component(_ROOT_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)

clean(LIBLAUNCHER)
set(LIBLAUNCHER_INCLUDE_DIR  "${_ROOT_DIR}/../../../include/allauncher/;${_ROOT_DIR}/../../../include/" CACHE STRING "" FORCE)
set(LIBLAUNCHER_DEFINITIONS  "TIXML_USE_STL;TIXML_USE_STL;TIXML_USE_STL;TIXML_USE_STL" CACHE STRING "" FORCE)
set(LIBLAUNCHER_DEPENDS      "LIBCORE;BOOST;PTHREAD;BOOST_SIGNALS;TOOLS;BOOST_FILESYSTEM;ALVALUE;ALCOMMON;LIBIPPC;BOOST_SERIALIZATION;BOOST_DATE_TIME;BOOST_THREAD;LIBFINDIPPC;DL;PROXIES;LIBSOAP;TINYXML;RTTOOLS;LIBTHREAD;BOOST_PROGRAM_OPTIONS;LIBFACTORY;PYTHON-STATIC"     CACHE STRING "" FORCE)

#cleanup this temp var
set(LIBLAUNCHER_tempdebug "LIBLAUNCHER_tempdebug-NOTFOUND" CACHE INTERNAL "Cleared." FORCE)

#try to get the debug lib
find_library(LIBLAUNCHER_tempdebug liblauncher_d PATHS "${_ROOT_DIR}/../../" NO_DEFAULT_PATH)


if (LIBLAUNCHER_tempdebug)
  #use debug and optimized version
  flib(LIBLAUNCHER OPTIMIZED liblauncher   PATHS "${_ROOT_DIR}/../../")
  flib(LIBLAUNCHER DEBUG     liblauncher_d PATHS "${_ROOT_DIR}/../../")
else()
  #use the default lib
  flib(LIBLAUNCHER liblauncher PATHS "${_ROOT_DIR}/../../")
endif()

export_lib(LIBLAUNCHER)
