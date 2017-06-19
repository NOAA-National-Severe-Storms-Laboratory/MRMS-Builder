#!/bin/python

# Robert Toomey May 2017
# Classes to build MRMS Hydro

import os,sys
import buildtools as b
from builder import Builder

HYDRO = "MRMSHydro"

class buildHydro(Builder):
  """ Build Hydro library """
  def build(self, t):
    hbase = t+"/"+HYDRO+"/"
    b.chdir(hbase)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    b.run("make")
    b.run("make install")

def getBuilders(l, f):
  """ Get the builders from this module """
  l.append(buildHydro("hydro", f))

def checkout(target, password):
  b.checkoutSVN("/MRMS_hydro/trunk", target+"/"+HYDRO, password)

def build(target):
  """ Build HYDRO (MRMS_Hydro) """
  print("\nBuilding HYDRO (MRMS_Hydro) libraries...")

  # Use our new m4 to static link third
  #b.runOptional("rm "+target+"/"+WDSS2+"/config/w2.m4")
  #relativePath = os.path.dirname(os.path.realpath(__file__))
  #b.run("cp "+relativePath+"/newm4.m4 "+target+"/"+WDSS2+"/config/newm4.m4")

  # Build all builders...
  blist = []
  getBuilders(blist, target)
  for build in blist:
    build.build(target)

  # Put a check ldd script into the bin directory
  # Maybe this shouldn't be in this code here
  #b.run("cp "+relativePath+"/check.py "+target+"/bin/check.py")

# Run main

# Run main
if __name__ == "__main__":
  print "Run the main build script...\n"
