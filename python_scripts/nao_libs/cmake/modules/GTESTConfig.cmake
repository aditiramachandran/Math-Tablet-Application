## Author: David Coz <dcoz@aldebaran-robotics.com>
##
## Copyright (C) 2009 Aldebaran Robotics

include("${TOOLCHAIN_DIR}/cmake/libfind.cmake")

clean(GTEST)
fpath(GTEST gtest/gtest.h)

if (WIN32)
  flib(GTEST OPTIMIZED gtest)
  flib(GTEST OPTIMIZED gtest_main-md)
  flib(GTEST DEBUG     gtestd)
  flib(GTEST DEBUG     gtest_main-mdd)
else()
  flib(GTEST gtest)
  flib(GTEST gtest_main)
endif()

export_lib(GTEST)
