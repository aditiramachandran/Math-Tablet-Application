##
## tests.cmake
## Login : <ctaf@cgestes-de>
## Started on  Tue Oct 20 11:50:53 2009 Cedric GESTES
## $Id$
##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2009 Cedric GESTES
##

function(configure_tests _name)
  include("${CMAKE_CURRENT_SOURCE_DIR}/${_name}")
endfunction(configure_tests _name)
