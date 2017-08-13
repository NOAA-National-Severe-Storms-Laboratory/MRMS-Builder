#!/bin/python

# Robert Toomey May 2017
# Classes to build MRMS Hydro

import os,sys
import buildtools as b
from builder import Builder
from builder import BuilderGroup

HYDRO = "HMET"

class buildHydro(Builder):
  """ Build Hydro library """
  def build(self, t, c, m):
    hbase = t+"/"+HYDRO+"/"
    b.chdir(hbase)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    self.makeInstall(m)

class MRMSHydroBuild(BuilderGroup):
  """ Build all of MRMS Hydro """
  def __init__(self):
    """ Get the builders from this module """
    l = []
    l.append(buildHydro("hydro"))
    self.myBuilders = l

  def checkout(self, target, password):
    b.checkoutSVN("/MRMS_hydro/trunk", target+"/"+HYDRO, password)

  def build(self, target, configFlags, makeFlags):
    """ Build HYDRO (MRMS_Hydro) """
    print("\nBuilding HYDRO (MRMS_Hydro) libraries...")

    # Use our new m4 to static link third
    #b.runOptional("rm "+target+"/"+WDSS2+"/config/w2.m4")
    #relativePath = os.path.dirname(os.path.realpath(__file__))
    #b.run("cp "+relativePath+"/newm4.m4 "+target+"/"+WDSS2+"/config/newm4.m4")

    # Build all builders...
    for build in self.myBuilders:
      build.build(target, configFlags, makeFlags)

    # Put a check ldd script into the bin directory
    # Maybe this shouldn't be in this code here
    #b.run("cp "+relativePath+"/check.py "+target+"/bin/check.py")

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
