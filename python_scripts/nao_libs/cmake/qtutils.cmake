####
# Useful things for qt.
#

function(qt_flib _suffix _libame)
   flib(QT_${_suffix} OPTIMIZED
    NAMES
      "${_libame}"
      "${_libame}4")

   flib(QT_${_suffix} DEBUG
    NAMES
      "${_libame}"
      "${_libame}d4")

   #we want to be able to #include <QtLib>
   fpath(QT_${_suffix} ${_libame})

   #we want to be able to #include <QtLib/QtLib>
   fpath(QT_${_suffix} ${_libame}
         PATH_SUFFIXES ${_libame})

endfunction()
