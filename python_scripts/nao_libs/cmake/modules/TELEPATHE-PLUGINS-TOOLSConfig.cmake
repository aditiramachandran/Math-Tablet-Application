##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2009 Aldebaran Robotics
##

function(create_telepathe_plugin _name)
  subargs_parse_args("SRC" "SRC;MOC;UI" _srcs _arg0 ${ARGN})
  subargs_parse_args("MOC" "SRC;MOC;UI" _mocs _arg1 ${_arg0})
  subargs_parse_args("UI" "SRC;MOC;UI"  _uis  _arg2 ${_arg1})
  string(TOUPPER ${_name} _NAME)

  verbose(STATUS "creating telepathe plugin [${name}]")
  debug(STATUS "creating telepathe plugin [${name}] (src: ${_srcs}, moc: ${_mocs}, ui: ${_uis})")

  find(GIT QUIET)
  gitversion(${CMAKE_CURRENT_SOURCE_DIR} {_NAME})
  add_definitions(" -D${_NAME}_REVISION=\\\"${${_NAME}_REVISION}\\\"")

  use(QT-TOOLS)

  #needed by some MOC header
  find(TELEPATHE-PLUGINS)
  include_directories(${TELEPATHE-PLUGINS_INCLUDE_DIR})

  qt4_wrap_cpp(_bamlesmocs ${_mocs} OPTIONS -DDOING_MOC)

  #needed by UI
  include_directories(${CMAKE_CURRENT_BINARY_DIR})
  qt4_wrap_ui(_bamlesuih ${_uis})

  create_lib(${_name} SHARED NOBINDLL SUBFOLDER telepathe ${_srcs} ${_bamlesmocs} ${_bamlesuih})

  set_target_properties("${_name}" PROPERTIES
    COMPILE_DEFINITIONS_RELEASE "QT_SHARED;QT_PLUGIN;QT_NO_DEBUG"
    COMPILE_DEFINITIONS_DEBUG   "QT_SHARED;QT_PLUGIN;QT_DEBUG"
    )

  use_lib(${_name} ALCOMMON QT_QTCORE QT_QTNETWORK QT_QTGUI DESKTOP TELEPATHE-PLUGINS)
endfunction(create_telepathe_plugin _name)


