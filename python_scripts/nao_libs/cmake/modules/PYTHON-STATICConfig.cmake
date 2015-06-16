## Copyright (C) 2008 Aldebaran Robotics


if(WIN32)
  message(FATAL_ERROR "Sorry, no static python on windows")
  return()
endif()

# Use the python-static from system
if(APPLE)
  set(CMAKE_FIND_FRAMEWORK "NEVER")
  flib(PYTHON-STATIC python2.5 PATH_SUFFIXES "python2.5/config" SYSTEM)
  fpath(PYTHON-STATIC Python.h PATH_SUFFIXES "python2.5" SYSTEM)
  export_lib(PYTHON-STATIC)
  set(CMAKE_FIND_FRAMEWORK)
  return()
endif()

if(UNIX AND NOT APPLE)
  clean(PYTHON-STATIC)
  fpath(PYTHON-STATIC Python.h PATH_SUFFIXES "python2.6")
  flib(PYTHON-STATIC python2.6-static PATH_SUFFIXES "python2.6")
  export_lib(PYTHON-STATIC)
  return()
endif()
