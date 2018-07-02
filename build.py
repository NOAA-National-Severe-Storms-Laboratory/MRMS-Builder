#!/usr/bin/env python
# Env gets around issue with multiple python versions
# Robert Toomey March 2017

import sys,os

print("Python version %s.%s.%s" % sys.version_info[:3])
if sys.version_info >=(2,6):
  import mrmsbuilder.buildmain as buildmain
  SCRIPTROOT = os.path.dirname(os.path.realpath(__file__))
  buildmain.buildMRMS(SCRIPTROOT)
else:
  print("This python is _ancient_, we require at least version 2.7")
