# -*- coding: utf-8 -*-
#distutils: language = c
#distutils: sources = /usr/local/Frameworks/
__author__ = "vaugien"
__copyright__ = "Copyright © 2018 ingenuity."
__license__ = "All rights reserved."
__version__ = "3.0.2"

import sys
import setuptools
from distutils.core import setup, Extension
import os
import platform

ingescape_src = ["ingescape_python.c", "ingescape/src/admin.c",
            "ingescape/src/data.c",  "ingescape/src/definition.c",
            "ingescape/src/mapping.c", "ingescape/src/freezecallback.c",
            "ingescape/src/init.c", "ingescape/src/input.c",
            "ingescape/src/observecallback.c", "ingescape/src/output.c",
            "ingescape/src/parameter.c", "ingescape/src/start.c",
            "ingescape/src/stopcallback.c", "ingescape/src/advanced.c",
            "ingescape/src/service.c", "ingescape/src/agentEvent.c"]
ingescape_include = ["./ingescape/include"]

ingescape_agent_src =["ingescape_agent/src/agent_definition.c",
            "ingescape_agent/src/agent_init.c", "ingescape_agent/src/agent_network.c",
            "ingescape_agent/src/agent_mapping.c", "ingescape_agent/src/agent_service.c",
            "ingescape_agent/src/agent_split.c"]
ingescape_agent_include = ["./ingescape_agent/include"]

dependencies_include = ["dependencies/"]

unix_lib_dirs = ["/usr/local/lib"]
unix_include_dirs =  ["/usr/local/include"]
windows_lib_dirs = []
windows_include_dirs = []

extension_ingescape = None

if sys.platform == "win32":
      if platform.machine().endswith('64'):
            windows_lib_dirs = ["C:/Program Files/ingescape/lib"]
            windows_include_dirs = ["C:/Program Files/ingescape/include"]
      else:
            windows_lib_dirs = ["C:/Program Files (x86)/ingescape/lib"]
            windows_include_dirs = ["C:/Program Files (x86)/ingescape/include"]

path_to_ingescape = None
if '--path' in sys.argv:
    index = sys.argv.index('--path')
    sys.argv.pop(index)
    path_to_ingescape = sys.argv.pop(index)

if path_to_ingescape is not None:
      if sys.platform == "win32":
        windows_lib_dirs = [path_to_ingescape+"/lib/"]
        windows_include_dirs = [path_to_ingescape+"/include/"]
      else:
        unix_lib_dirs = [path_to_ingescape+"/lib/"]
        unix_include_dirs = [path_to_ingescape+"/include/"]


if sys.platform == "win32":
      sys.path.extend(windows_include_dirs)
      sys.path.extend(windows_lib_dirs)

      extension_ingescape = Extension("ingescape", ingescape_src + ingescape_agent_src,
                  include_dirs = ingescape_agent_include + ingescape_include + windows_include_dirs + dependencies_include,
                  libraries = ["ingescape"],
                  library_dirs = windows_lib_dirs)
else:
      sys.path.extend(unix_include_dirs)
      sys.path.extend(unix_lib_dirs)

      extension_ingescape = Extension("ingescape", ingescape_src + ingescape_agent_src ,
                  include_dirs = ingescape_include + ingescape_agent_include + unix_include_dirs + dependencies_include,
                  libraries = ["ingescape"],
                  library_dirs = unix_lib_dirs)



setup(name =  "ingescape",
      author = "Natanael Vaugien",
      author_email = "vaugien@ingenuity.io",
      version =  "3.0.2",
      license =  "Copyright © 2018-2021 ingenuity. All rights reserved.",
      ext_modules = [extension_ingescape])
