#!/usr/bin/env python

# Robert Toomey Oct 2020
# Build WG with new standalone autogen

# System imports
import os,sys
import os.path

# Relative imports
from . import buildtools as b
from .builder import Builder
from .builder import BuilderGroup
from .ThirdParty import THIRD
from . import wget

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

class buildWG(Builder):
  """ Build WG """
  def checkRequirements(self):
    return autoGUICheck()

  def build(self, target):
    wg = target+"/"+WDSS2+"/w2tools/wxDisplay"
    b.chdir(wg)

    r = self.autogen("./autogen.sh", target)
    r = r + " --enable-shared"

    self.runBuildSetup(r)
    self.makeInstall()

class WGBuild(BuilderGroup):
  """ Build WG and related stuff """
  def __init__(self, theConf, mrmsVersion):
    """ Get the builders from this module """
    self.mrmsVersion = mrmsVersion
    self.isResearch = False
    self.isExport = False
    self.ourDFlags = {}
    l = []
    l.append(buildWG("WG"))
    self.myBuilders = l

  def preCheckoutConfig(self, theConf):
    """ Configuration questions just for this builder """
    BuilderGroup.preCheckoutConfig(self, theConf)
    self.isResearch = theConf.getBoolean("RESEARCH", "Is this a research build (no realtime, no encryption)", "no")
    if (self.isResearch):
      self.isExport = True # Research version automatically loses encryption
    else:
      self.isExport = theConf.getBoolean("EXPORT", "Is this an exported build (For outside US, turn off encryption)", "no")
    BuilderGroup.mrmsVersion(self, theConf, self.mrmsVersion, False, self.isExport);

  def postCheckoutConfig(self, theConf, target):
    """ Configuration stuff for after a successful checkout of code """
    BuilderGroup.postCheckoutConfig(self, theConf, target)
    BuilderGroup.mrmsFlags(self, theConf, target, self.mrmsVersion, self.isResearch);

  def requireSVN(self):
    """ Do we require svn credentials? """
    return True
    
  def checkout(self, target, scriptroot, password, svnoptions):
    """ Checkout WG.  Humm..condition on if the code is there already """
    if (not os.path.exists(target+"/"+WDSS2+"/w2tools/wxDisplay/wg_Product.h")):
      print("Rechecking out WG source since it's missing...")
      b.checkoutSVN("/WDSS2/trunk", target+"/"+WDSS2, password, svnoptions)
    else:
      print("----->WG already exists from a w2tools checkout")

  def build(self, target):
    """ Build WG """
    # Build all builders...
    for build in self.myBuilders:
      build.build(target)

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
