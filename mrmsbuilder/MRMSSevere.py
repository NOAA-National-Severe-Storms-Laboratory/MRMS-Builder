#!/usr/bin/env python

# Robert Toomey May 2017
# Classes to build MRMS Severe (WDSS2)

# System imports
import os,sys

# Relative imports
from . import buildtools as b
from .builder import Builder
from .builder import BuilderGroup

WDSS2 = "WDSS2"

def autoGUICheck():
  """ Passed for 'auto' mode for the GUI flag """
  good = True

  # Test 1: We just check for the gl.h header that nvidia or others put on here...
  if not b.checkFirstText("GUI",["file", "/usr/include/GL/gl.h"], "ASCII"):
    good = False

  # Test 2: Check gtkglext-devel rpm...
  if not b.checkFirstText("GUI", ["rpm","-qi","gtkglext-devel"], "Name"):
    good = False

  return good

def autoPythonDevCheck():
  """ Passed for 'auto' mode for the PYTHON flag """
  # We are checking for python c++ development libraries
  # on Redhat 7
  good = True

  # Test 1: We just check for python-devel. This will be the system
  # version of python.  We'll have work to do if we want to handle a
  # custom python install
  if not b.checkFirstText("PYTHON", ["rpm","-qi","python-devel"], "Name"):
    good = False

  return good

class buildW2(Builder):
  """ Build W2 library """
  def build(self, target):
    w2 = target+"/"+WDSS2+"/w2"
    b.chdir(w2)
    r = self.autogen("./autogen.sh", target)
    b.run(r)
    #b.run("./autogen.sh --prefix="+target+" --enable-shared ")
    self.makeInstall()

class buildW2algs(Builder):
  """ Build W2algs library """
  def build(self, target):
    w2algs = target+"/"+WDSS2+"/w2algs"
    b.chdir(w2algs)
    #b.run("./autogen.sh --prefix="+target+" --enable-shared ")
    r = self.autogen("./autogen.sh", target)
    b.run(r)
    self.makeInstall()

class buildW2ext(Builder):
  """ Build W2ext library """
  def build(self, target):
    w2ext = target+"/"+WDSS2+"/w2ext"
    b.chdir(w2ext)
    #b.run("./autogen.sh --prefix="+target+" --enable-shared ")
    r = self.autogen("./autogen.sh", target)
    b.run(r)
    self.makeInstall()

class buildW2tools(Builder):
  """ Build W2tools library """
  def __init__(self, key):
    self.myWantGUI = True
    self.myWantPythonDev = False
    # New stylesuper(buildW2tools, self).__init__(key)
    Builder.__init__(self, key)

  def setWantGUI(self, flag):
    self.myWantGUI = flag

  def build(self, target):
    w2tools = target+"/"+WDSS2+"/w2tools"
    b.chdir(w2tools)
    #b.run("./autogen.sh --prefix="+target+" --enable-shared "+add)
    r = self.autogen("./autogen.sh", target)

    # Add gtk GUI flag if needed/wanted
    r += " --with-gtk="
    if self.myWantGUI:
      r += "yes"
    else:
      r += "no"

    # Add python flag if needed/wanted
    r += " --with-pythondev="
    if self.myWantPythonDev:
      r += "yes"
    else:
      r += "no"

    b.run(r)
    self.makeInstall()
  def checkRequirements(self):
    req = True
    if self.myWantGUI:
      req = req & autoGUICheck()
    if self.myWantPythonDev:
      req = req & autoPythonDevCheck()
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

  def checkout(self, target, password, options):
    b.checkoutSVN("/WDSS2/trunk", target+"/"+WDSS2, password, options)

  def build(self, target):
    """ Build WDSS2 (MRMS_Severe) """
    print("\nBuilding WDSS2 (MRMS_Severe) libraries...")

    # Use our new m4 to static link third
    b.runOptional("rm "+target+"/"+WDSS2+"/config/w2.m4")
    relativePath = os.path.dirname(os.path.realpath(__file__))
    b.run("cp "+relativePath+"/newm4.m4 "+target+"/"+WDSS2+"/config/newm4.m4")

    # Build all builders...
    for build in self.myBuilders:
      build.build(target)

    # Put a check ldd script into the bin directory
    # Maybe this shouldn't be in this code here
    b.run("cp "+relativePath+"/check.py "+target+"/bin/check.py")

  def setWantGUI(self, flag):
    """ Do we want to compile the GUI? """
    self.myW2Tools.setWantGUI(flag)

  def getKeyLocation(self, target, isResearch):
    """ Return path to a built in authentication key """
    path = target+"/"+WDSS2+"/w2/w2config/auth/"
    if isResearch:
      path += "research/key"
    else:
      path += "default/key"
    return path

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
