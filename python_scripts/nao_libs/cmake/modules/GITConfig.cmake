##
## Login : <ctaf@localhost.localdomain>
## Started on  Thu Jun 12 15:19:44 2008 Cedric GESTES
## $Id$
##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2009 Aldebaran Robotics

# Extract version information

find_program(GIT_EXECUTABLE git)
mark_as_advanced(GIT_EXECUTABLE)

function(gitversion dir prefix)
  if (DEFINED GIT_FORCE_VERSION)
    set(${prefix}_REVISION ${GIT_FORCE_VERSION} PARENT_SCOPE)
    return()
  endif (DEFINED GIT_FORCE_VERSION)

  set(_out)
  if(GIT_EXECUTABLE)
    execute_process(
      COMMAND           ${GIT_EXECUTABLE} describe --always --tag
      WORKING_DIRECTORY ${dir}
      RESULT_VARIABLE   _result
      OUTPUT_VARIABLE   _out
      ERROR_VARIABLE    _error
      OUTPUT_STRIP_TRAILING_WHITESPACE)

    if(${_result} EQUAL 0)
      set(_rev "${_out}")
    endif(${_result} EQUAL 0)
  endif(GIT_EXECUTABLE)

  #always set a revision, fallback to the perfect revision, the one that just work!
  if (NOT _rev)
    set(_rev "42-nogit")
  endif (NOT _rev)



  # git describe --always --tags will return "tags/v1.2.45", for instance.
 # Remove the tags/ part:
  string(REGEX REPLACE "tags/" "" _result ${_rev})
  set(${prefix}_REVISION "${_result}" PARENT_SCOPE)
endfunction(gitversion)
