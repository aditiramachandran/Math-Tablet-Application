##
## Login : <ctaf@localhost.localdomain>
## $Id$
##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2008 Aldebaran Robotics


#configure preferences
#copy each .xml
#todo: take an argument to specify another prefs folder
function (create_prefs)
#message(STATUS "Tac Tac bourico")
  if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/prefs/")
    if (NOT EXISTS "${SDK_DIR}/${_SDK_CONF}/")
      file(MAKE_DIRECTORY "${SDK_DIR}/${_SDK_CONF}/")
    endif (NOT EXISTS "${SDK_DIR}/${_SDK_CONF}/")

    file(GLOB _listprefs "${CMAKE_CURRENT_SOURCE_DIR}/prefs/*.xml")
    foreach(_prefs ${_listprefs})
      # get_filename_component(_prefsname "${_prefs}" NAME)
      copy_with_depend("${_prefs}" "${_SDK_CONF}/")
      install(FILES ${_prefs} COMPONENT conf DESTINATION "${_SDK_CONF}/")
    endforeach(_prefs ${_listprefs})
  endif (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/prefs/")
endfunction (create_prefs)


function (create_module moduleName)
  string(TOUPPER ${moduleName} MODULENAME)
  project(${MODULENAME})

  create_prefs()
  verbose( STATUS "...:::: Configuration - ${MODULENAME} ::::..." )

  find(GIT QUIET)

  # Quick and dirty hack:
  # Given a revision 1.4.14-rc2-92-ae452i
  # (which change at every commit), set compile flag to
  # 1.4.14-rc2, to that we don't recompile everything at each commit

  # TODO:
  # Instead of using a compile flag, configure a main.cpp.
  # (this of course assumes that every module has a main.cpp ...)
  gitversion(${CMAKE_CURRENT_SOURCE_DIR} FULL)

  # Note: this is the same regexp as used in set_cpack_version_from_git in
  # toolchain/cmake/misc.cmake
  string(REGEX MATCH "v?([0-9]*\\.[0-9]*)\\.([0-9]*(-rc[0-9]+)?)[\\.\\-]?(.*)" _out ${FULL_REVISION})


  set(INCOMPLETE_REVISION "${CMAKE_MATCH_1}.${CMAKE_MATCH_2}" )
  add_definitions(" -D${MODULENAME}_REVISION=\\\"${INCOMPLETE_REVISION}\\\"")
  add_definitions(" -D${MODULENAME}_IS_REMOTE=\\\"${${MODULENAME}_IS_REMOTE}\\\"")

  option(${MODULENAME}_IS_REMOTE "module is compile as a remote module (ON or OFF)" OFF)

  if (${MODULENAME}_IS_REMOTE)
    add_definitions(" -D${MODULENAME}_IS_REMOTE_ON ")
  else (${MODULENAME}_IS_REMOTE)
    add_definitions(" -D${MODULENAME}_IS_REMOTE_OFF ")
  endif (${MODULENAME}_IS_REMOTE)

endfunction(create_module)


function (configure_src_module moduleName)
  string(TOUPPER ${moduleName} MODULENAME)

  if (${MODULENAME}_IS_REMOTE STREQUAL "OFF")
    create_lib(${moduleName} NOBINDLL SUBFOLDER naoqi SHARED ${ARGN})
    if(APPLE)
      # On mac, ALError does not work through static libraries.
      # See FS#2827 for more information:
      # Also : http://gcc.gnu.org/wiki/Visibility
      #  |_ Problems with C++ exceptions (please read!)
      set_target_properties(${moduleName}
        PROPERTIES
          LINK_FLAGS "-Wl,-flat_namespace"
      )
    endif()
  else(${MODULENAME}_IS_REMOTE STREQUAL "OFF")
    create_bin(${moduleName} ${ARGN})
  endif( ${MODULENAME}_IS_REMOTE STREQUAL "OFF" )
endfunction(configure_src_module)


function (configure_naoqi_tests)
  #the first time we call configure_naoqi_tests before staging(NAOQI)
  #the function will fail, next call to cmake or make will be ok...
  #so who really cares?
  find(NAOQI        QUIET)
  find(NAOQITESTRUN QUIET)
  find(NAOQISCRIPT  QUIET)

  if (NOT WIN32)
    set(NAOQI "${NAOQISCRIPT_EXECUTABLE}" CACHE PATH "" FORCE)
  else()
    set(NAOQI "${NAOQI_EXECUTABLE}"       CACHE PATH "" FORCE)
  endif()

  set(TEST_RUN "${NAOQITESTRUN_EXECUTABLE}" CACHE PATH "" FORCE)
  # This variable was used in tests.cmake, but not accessible from
  # python scripts just now
  set(REMOTETEST OFF                      PARENT_SCOPE)

endfunction (configure_naoqi_tests)

function (AL_CLEAN_EXAMPLE)
	file(WRITE  "${CMAKE_CURRENT_BINARY_DIR}/src/examples.h" "")
endfunction (AL_CLEAN_EXAMPLE)


function (AL_ADD_TEST _name)
	file(READ ${CMAKE_CURRENT_SOURCE_DIR}/test/${_name}.py fcontent)
	string(REPLACE "\"" "\\\""  fcontent ${fcontent})
	string(REPLACE "\n" "\\n"  fcontent ${fcontent})
	set(fcontent "const std::string ${_name} = \"${fcontent} \" ; ")
	set(fcontent "${fcontent}\n \; \n")
	file(APPEND  "${CMAKE_CURRENT_BINARY_DIR}/src/examples.h" ${fcontent})
	include_directories(${CMAKE_CURRENT_BINARY_DIR}/src/)
endfunction (AL_ADD_TEST name)
