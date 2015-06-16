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

clean(OPENCV)
fpath(OPENCV opencv/cv.h)
if(NOT APPLE)
  flib(OPENCV NAMES cv      cv200)
  flib(OPENCV NAMES cvaux   cvaux200)
  flib(OPENCV NAMES cxcore  cxcore200)
  flib(OPENCV NAMES highgui highgui200)
  flib(OPENCV NAMES ml      ml200)
else(NOT APPLE)
  flib(OPENCV NAMES "OpenCV")
endif(NOT APPLE)
export_lib(OPENCV)
