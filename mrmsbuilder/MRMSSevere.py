#!/bin/python

# Robert Toomey May 2017
# Classes to build MRMS Severe (WDSS2)

import os,sys
import buildtools as b
from builder import Builder

WDSS2 = "MRMSSevere"

class buildW2(Builder):
  """ Build W2 library """
  def build(self, t):
    w2 = t+"/"+WDSS2+"/w2"
    b.chdir(w2)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    b.run("make")
    b.run("make install")

class buildW2algs(Builder):
  """ Build W2algs library """
  def build(self, t):
    w2algs = t+"/"+WDSS2+"/w2algs"
    b.chdir(w2algs)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    b.run("make")
    b.run("make install")

class buildW2ext(Builder):
  """ Build W2ext library """
  def build(self, t):
    w2ext = t+"/"+WDSS2+"/w2ext"
    b.chdir(w2ext)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    b.run("make")
    b.run("make install")

class buildW2tools(Builder):
  """ Build W2tools library """
  def build(self, t):
    w2tools = t+"/"+WDSS2+"/w2tools"
    b.chdir(w2tools)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    b.run("make")
    b.run("make install")

def getBuilders(l, f):
  """ Get the builders from this module """
  l.append(buildW2("w2", f))
  l.append(buildW2algs("w2algs", f))
  l.append(buildW2ext("w2ext", f))
  l.append(buildW2tools("w2tools", f))

def checkout(target, password):
  b.checkoutSVN("/WDSS2/trunk", target+"/"+WDSS2, password)

def build(target):
  """ Build WDSS2 (MRMS_Severe) """
  print("\nBuilding WDSS2 (MRMS_Severe) libraries...")

  # Use our new m4 to static link third
  b.runOptional("rm "+target+"/"+WDSS2+"/config/w2.m4")
  relativePath = os.path.dirname(os.path.realpath(__file__))
  b.run("cp "+relativePath+"/newm4.m4 "+target+"/"+WDSS2+"/config/newm4.m4")

  # Build all builders...
  blist = []
  getBuilders(blist, target)
  for build in blist:
    build.build(target)

  # Put a check ldd script into the bin directory
  # Maybe this shouldn't be in this code here
  b.run("cp "+relativePath+"/check.py "+target+"/bin/check.py")

# Run main
if __name__ == "__main__":
  print "Run the main build script...\n"
