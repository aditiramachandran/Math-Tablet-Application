## Copyright (C) 2008 Aldebaran Robotics

clean(PYTHON)
fpath(PYTHON Python.h PATH_SUFFIXES "python2.6")
flib(PYTHON OPTIMIZED NAMES python26   python2.6 Python)
flib(PYTHON DEBUG     NAMES python26_d python2.6 Python)
export_lib(PYTHON)

