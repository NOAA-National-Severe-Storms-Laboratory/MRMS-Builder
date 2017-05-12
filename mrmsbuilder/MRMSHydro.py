#!/bin/python

# Robert Toomey May 2017
# Classes to build MRMS Hydro

import os,sys
import buildtools as b
from builder import Builder

HYDRO = "MRMSHydro"

class buildHydro(Builder):
  """ Build Hydro library """
  def stuff():
    pass

def getBuilders(l, f):
  """ Get the builders from this module """
  l.append(buildHydro("hydro", f))

def checkout(target):
  b.checkoutSVN("/MRMS_hydro/trunk", target+"/"+HYDRO)


# Run main
if __name__ == "__main__":
  print "Run the main build script...\n"
