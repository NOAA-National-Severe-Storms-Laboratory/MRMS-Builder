#!/usr/bin/env python
# Env gets around issue with multiple python versions
# Robert Toomey March 2017

import sys

print("Python version %s.%s.%s" % sys.version_info[:3])
if sys.version_info >=(2,6):
  import mrmsbuilder.buildmain as buildmain
  buildmain.buildMRMS()
else:
  print("This python is _ancient_, we require at least version 2.7")
