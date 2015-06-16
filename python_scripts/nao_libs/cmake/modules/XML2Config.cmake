##
## Login : <ctaf@localhost.localdomain>
## Started on  Thu Jun 12 15:19:44 2008 Cedric GESTES
## $Id$
##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2008 Aldebaran Robotics

include("${TOOLCHAIN_DIR}/cmake/libfind.cmake")

clean(XML2)
fpath(XML2 libxml/parser.h PATH_SUFFIXES libxml2)
flib(XML2 xml2)
if (TARGET_HOST STREQUAL "TARGET_HOST_MACOSX")
  depend(XML2 REQUIRED Z)
endif (TARGET_HOST STREQUAL "TARGET_HOST_MACOSX")
export_lib(XML2)
