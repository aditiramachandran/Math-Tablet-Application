from distutils.core import setup
import os
import sys
import shutil

import distutils.sysconfig
on_win = False
if sys.platform.startswith("win"):
    on_win = True

prefix = sys.prefix
py_version = distutils.sysconfig.get_python_version()

if on_win:
    python_lib_dir = os.path.join(prefix, "DLLS")
    data_files     = [(python_lib_dir, ["_inaoqi.pyd"])]
else:
    python_lib_dir = os.path.join(prefix, "lib", "python" + py_version , "lib-dynload")
    data_files     = [(python_lib_dir, ["_inaoqi.so"])]

py_modules = [
    "naoqi",
    "inaoqi",
    "ALProxy",
    "allib",
    "altools",
    "motion",
    "naoconfig",
    "vision_definitions",
]

setup(name         = 'naoqi',
      version      =  "1.6.13",
      url          = "git://git,aldebaran.lan/makeversion/build-tools.git",
      author       = "Aldebaran Robotics",
      author_email = "<merejkowsky@aldebaran-robotics.com",
      description  = "Python interface for NaoQi",
      py_modules   = py_modules,
      data_files   = data_files,
)

