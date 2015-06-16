##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2009 Aldebaran Robotics
##

use(QT-TOOLS)

#Create a choregraphe plugin (see cho/plugins/*/CMakeLists.txt for an example use)
function(create_choregraphe_plugin name)
  subargs_parse_args("SRC" "SRC;MOC" _srcs _arg0 ${ARGN})
  subargs_parse_args("MOC" "SRC;MOC" _mocs _arg1 ${_arg0})

  verbose(STATUS "creating choregraphe plugin [${name}]")
  debug(STATUS "creating choregraphe plugin [${name}] (src: ${_srcs}, moc: ${_mocs})")

  #this is needed for MOC/US, moc need to find header of choregraphe-plugins
  find(CHOREGRAPHE-PLUGINS)
  include_directories(${CHOREGRAPHE-PLUGINS_INCLUDE_DIR})

  qt4_wrap_cpp(_bamlesmocs ${_mocs})
  create_lib("${name}" NOBINDLL SUBFOLDER choregraphe SHARED ${_bamlesmocs} ${_srcs})
  set_target_properties("${name}" PROPERTIES
    COMPILE_DEFINITIONS_RELEASE "QT_SHARED;QT_PLUGIN;QT_NO_DEBUG"
    COMPILE_DEFINITIONS_DEBUG   "QT_SHARED;QT_PLUGIN;QT_DEBUG"
    )
endfunction(create_choregraphe_plugin)
