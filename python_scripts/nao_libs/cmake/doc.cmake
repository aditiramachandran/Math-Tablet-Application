##
## doc.cmake
## Login : <ctaf@ctaf-maptop>
## Started on  Sun Oct 18 02:34:09 2009 Cedric GESTES
## $Id$
##
## Author(s):
##  - Cedric GESTES <cgestes@aldebaran-robotics.com>
##
## Copyright (C) 2009 Cedric GESTES
##

#yeah we need asciidoc, we assume asciidoc is provided by the system
find(ASCIIDOC)
find(DOXYGEN QUIET)


#target for documentation, doc is a superset of doxygen and asciidoc
#create only if target doesnt exists
if (NOT TARGET "doc")
  add_custom_target("doc")
endif (NOT TARGET "doc")

if (NOT TARGET "doxydoc")
  add_custom_target("doxydoc")
  add_dependencies("doc" "doxydoc")
endif (NOT TARGET "doxydoc")

if (NOT TARGET "asciidoc")
  add_custom_target("asciidoc")
  add_dependencies("doc" "asciidoc")
endif (NOT TARGET "asciidoc")


####################################################################
#
# compile a set of asciidoc documentation
#
####################################################################
function(create_asciidoc subfoldername)
  if(ASCIIDOC_FOUND)
    make_directory("${SDK_DIR}/share/doc/${subfoldername}/")
    foreach(_file ${ARGN})
      get_filename_component(_file_we ${_file} NAME_WE)
      set(_in   "${_file_we}-asciidoc")
      set(_out  "${SDK_DIR}/${_SDK_DOC}/${subfoldername}/${_file_we}.html")
      #set(_rout "${SDK_DIR}/share/doc/${subfoldername}/${_file_we}.html")
      set(_fin  "${CMAKE_CURRENT_SOURCE_DIR}/${_file}")

      debug("Adding asciidoc: ${_out} : ${_in}")

      install(FILES "${_out}" COMPONENT doc DESTINATION "${_SDK_DOC}/${subfoldername}/")

      # way to go, but asciidoc leave the file in the filesystem even on error
      # So when an error occur, the next time you try to build, cmake think the previous
      # build is ok (the erronous file is at the right place) and continue building
      # # debug("DOC: file: ${_file}, input: ${_fin}, output: ${_out}")
      # add_custom_command(
      #         OUTPUT "${_out}"
      #         COMMAND "${ASCIIDOC_EXECUTABLE}" -a toc -o "${_out}" "${_fin}"
      #         DEPENDS "${_fin}"
      #         COMMENT "Asciidoc ${_in}"
      #         )
      #       add_custom
      # #a target is needed to have depends (the doc taret wont work otherwize)
      # add_custom_target("${_in}" DEPENDS "${_out}")

      #ATM always rebuild the doc... or find a way to correct asciidoc
      add_custom_target("${_in}"
           #             DEPENDS "${_out}"
                        COMMAND "${ASCIIDOC_EXECUTABLE}" -a toc -o "${_out}" "${_fin}"
                        COMMENT "Asciidoc ${_in}")

      add_dependencies("asciidoc" "${_in}")
    endforeach(_file)
  else(ASCIIDOC_FOUND)
    message(STATUS "###### WARNING ######")
    message(STATUS "No asciidoc will be generated: asciidoc binary not found")
    message(STATUS "Please install asciidoc")
    message(STATUS "###### WARNING ######")
  endif(ASCIIDOC_FOUND)
endfunction(create_asciidoc foldername)


####################################################################
#
# generate doxygen
#
####################################################################
function(create_doxygen)
  if(DOXYGEN_EXECUTABLE)
    #TODO: make it work
    add_custom_target(doc COMMAND ${DOXYGEN_EXECUTABLE} hal.doxy WORKING_DIRECTORY ${HAL_ROOT})
  endif()
endfunction(create_doxygen)
