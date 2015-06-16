##
## Copyright (C) 2008 Aldebaran Robotics

include("${TOOLCHAIN_DIR}/cmake/libfind.cmake")

#get the root folder of this sdk
get_filename_component(_ROOT_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)
include("${_ROOT_DIR}/../boostutils.cmake")

set(_libname "serialization")
set(_suffix "SERIALIZATION")

clean(BOOST_${_suffix}-STATIC)
fpath(BOOST_${_suffix}-STATIC boost)

boost_flib_static(${_suffix}-STATIC ${_libname})
export_lib(BOOST_${_suffix}-STATIC)
