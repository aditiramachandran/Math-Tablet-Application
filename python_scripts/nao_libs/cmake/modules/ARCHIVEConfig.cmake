##
## Login : <ctaf@localhost.localdomain>
## Started on  Mon Oct  6 18:19:18 2008 Cedric GESTES
## $Id$
##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2008 Aldebaran Robotics

include("${TOOLCHAIN_DIR}/cmake/libfind.cmake")

#get the root folder of this sdk
get_filename_component(_ROOT_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)
set(TOOLCHAIN_PC_ROOT ${_ROOT_DIR}/../../)

clean(ARCHIVE)
fpath(ARCHIVE archive.h PATH_SUFFIXES archive)
flib(ARCHIVE archive)
if (TARGET_HOST STREQUAL "TARGET_HOST_MACOSX")
  depend(ARCHIVE REQUIRED Z)
endif (TARGET_HOST STREQUAL "TARGET_HOST_MACOSX")
flib(ARCHIVE DEBUG NAMES archive_d archive)
export_lib(ARCHIVE)

