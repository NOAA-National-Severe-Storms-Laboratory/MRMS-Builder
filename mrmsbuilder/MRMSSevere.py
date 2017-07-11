#!/bin/python

# Robert Toomey May 2017
# Classes to build MRMS Severe (WDSS2)

import os,sys
import buildtools as b
from builder import Builder
from builder import BuilderGroup

WDSS2 = "MRMSSevere"

class buildW2(Builder):
  """ Build W2 library """
  def build(self, t, c, m):
    w2 = t+"/"+WDSS2+"/w2"
    b.chdir(w2)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    self.makeInstall(m)

class buildW2algs(Builder):
  """ Build W2algs library """
  def build(self, t, c, m):
    w2algs = t+"/"+WDSS2+"/w2algs"
    b.chdir(w2algs)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    self.makeInstall(m)

class buildW2ext(Builder):
  """ Build W2ext library """
  def build(self, t, c, m):
    w2ext = t+"/"+WDSS2+"/w2ext"
    b.chdir(w2ext)
    b.run("./autogen.sh --prefix="+t+" --enable-shared ")
    self.makeInstall(m)

class buildW2tools(Builder):
  """ Build W2tools library """
  def __init__(self, key):
    self.myWantGUI = True
    # New stylesuper(buildW2tools, self).__init__(key)
    Builder.__init__(self, key)

  def setWantGUI(self, flag):
    self.myWantGUI = flag
  def build(self, t, c, m):
    w2tools = t+"/"+WDSS2+"/w2tools"
    b.chdir(w2tools)
    if self.myWantGUI:
      add = " --with-gtk=yes"
    else:
      add = " --with-gtk=no"
    b.run("./autogen.sh --prefix="+t+" --enable-shared "+add)
    self.makeInstall(m)
  def checkRequirements(self):
    req = True
    if self.myWantGUI:
      req = req & b.checkRPM("gtkglext-devel")
    return req

class MRMSSevereBuild(BuilderGroup):
  """ Build all of MRMS Severe (WDSS2) """
  def __init__(self):
    """ Get the builders from this module """
    l = []
    l.append(buildW2("w2"))
    l.append(buildW2algs("w2algs"))
    l.append(buildW2ext("w2ext"))
    self.myW2Tools = buildW2tools("w2tools")
    l.append(self.myW2Tools)
    self.myBuilders = l

  def checkout(self, target, password):
    b.checkoutSVN("/WDSS2/trunk", target+"/"+WDSS2, password)

  def build(self, target):
    """ Build WDSS2 (MRMS_Severe) """
    print("\nBuilding WDSS2 (MRMS_Severe) libraries...")

    # Use our new m4 to static link third
    b.runOptional("rm "+target+"/"+WDSS2+"/config/w2.m4")
    relativePath = os.path.dirname(os.path.realpath(__file__))
    b.run("cp "+relativePath+"/newm4.m4 "+target+"/"+WDSS2+"/config/newm4.m4")

    # Build all builders...
    for build in self.myBuilders:
      build.build(target, "", "")

    # Put a check ldd script into the bin directory
    # Maybe this shouldn't be in this code here
    b.run("cp "+relativePath+"/check.py "+target+"/bin/check.py")

  def setWantGUI(self, flag):
    """ Do we want to compile the GUI? """
    self.myW2Tools.setWantGUI(flag)

# Run main
if __name__ == "__main__":
  print "Run the main build script...\n"
