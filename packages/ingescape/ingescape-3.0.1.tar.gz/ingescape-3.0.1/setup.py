# -*- coding: utf-8 -*-
#distutils: language = c
#distutils: sources = /usr/local/Frameworks/
__author__ = "vaugien"
__copyright__ = "Copyright © 2018 ingenuity."
__license__ = "All rights reserved."
__version__ = "3.0.1"

import sys
import setuptools
from distutils.core import setup, Extension
import os

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

windows_lib_dirs = ["C:/Program Files/ingescape/lib"]
windows_include_dirs =  inc_dirs = ["C:/Program Files/ingescape/include"]

unix_lib_dirs = ["/usr/local/lib"]
unix_include_dirs =  ["/usr/local/include"]

extension_ingescape = None

if sys.platform == "win32":
      sys.path.extend("C:/Program Files/ingescape/include")
      sys.path.extend("C:/Program Files/ingescape/lib",)
      extension_ingescape = Extension("ingescape", ingescape_src + ingescape_agent_src,
                  include_dirs = ingescape_agent_include + ingescape_include + windows_include_dirs + dependencies_include,
                  libraries = ["ingescape"],
                  library_dirs = windows_lib_dirs)
else:
      sys.path.extend("/usr/local/include/")
      sys.path.extend("/usr/local/lib/")

      extension_ingescape = Extension("ingescape", ingescape_src + ingescape_agent_src ,
                  include_dirs = ingescape_include + ingescape_agent_include + unix_include_dirs + dependencies_include,
                  libraries = ["ingescape"],
                  library_dirs = unix_lib_dirs)



setup(name =  "ingescape",
      author = "Natanael Vaugien",
      author_email = "vaugien@ingenuity.io",
      version =  "3.0.1",
      license =  "Copyright © 2018-2021 ingenuity. All rights reserved.",
      ext_modules = [extension_ingescape])
