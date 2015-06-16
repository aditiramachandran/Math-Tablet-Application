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
#get the root folder of this sdk
get_filename_component(_ROOT_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)
set(TOOLCHAIN_PC_ROOT ${_ROOT_DIR}/../../)

clean(OGRE)
fpath(OGRE OgreRoot.h PATH_SUFFIXES ogre)
flib(OGRE OPTIMIZED NAMES OgreMain Ogre)
flib(OGRE DEBUG     NAMES OgreMain_d OgreMain Ogre)
export_lib(OGRE)
