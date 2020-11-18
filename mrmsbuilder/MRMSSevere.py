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
dualSet2 = 0

# Duplicated in Third.  FIXME: pull out dualpol stuff
def pathDualpol2(target):
  """ Set up header ENV for dualpol """
  global dualSet2

  if dualSet2 == 0:
    print("******Setting path dualpol")
    os.environ["ORPGDIR"] = target
    os.environ["DUALPOLDIR"] = target
    os.environ["QPE_LIB_ONLY"] = "1"
    cfg = target+"/lib/pkgconfig"
    c = os.environ.get("PKG_CONFIG_PATH")
    if (c is None):
      os.environ["PKG_CONFIG_PATH"] = cfg
    else:
      os.environ["PKG_CONFIG_PATH"] = cfg+":"+c
    dualSet2 = 1
  else:
    print("Not setting path dualpol")

class buildW2(Builder):
  """ Build W2 library """
  def __init__(self, key, mrmsVersion):
    self.mrmsVersion = mrmsVersion
    Builder.__init__(self, key)

  def build(self, target):
    w2 = target+"/"+WDSS2+"/w2"
    b.chdir(w2)
    r = self.autogen("./autogen.sh", target)

    # Add orpginfr.  This doesn't build after mrms12
    #r += " --with-orpginfr="
    #if self.mrmsVersion == "mrms12":
    #  r += "yes"
    #else:
    #  r += "no"

    self.runBuildSetup(r)
    self.makeInstall()

class buildW2algs(Builder):
  """ Build W2algs library """
  def __init__(self, key, mrmsVersion):
    self.mrmsVersion = mrmsVersion
    Builder.__init__(self, key)

  def build(self, target):
    w2algs = target+"/"+WDSS2+"/w2algs"
    b.chdir(w2algs)
    r = self.autogen("./autogen.sh", target)

    # Add orpginfr.  This doesn't build after mrms12
    #r += " --with-orpginfr="
    #if self.mrmsVersion == "mrms12":
    #  r += "yes"
    #else:
    #  r += "no"

    self.runBuildSetup(r)
    self.makeInstall()

class buildDualpol(Builder):
  """ Build Krause's dualpol within w2algs library """
  def __init__(self, key, mrmsVersion):
    self.mrmsVersion = mrmsVersion
    Builder.__init__(self, key)
  def build(self, target):
    # This used a tar in mrms12
    if self.mrmsVersion == "mrms12":
      return
    # Build what's in the src folder
    dualpol = target+"/"+WDSS2+"/w2algs/kdualpol/dualpol"
    b.chdir(dualpol)
    r = self.autogen("./autogen.sh", target)
    self.runBuildSetup(r)
    self.makeInstall()

class buildDualpolQPE(Builder):
  """ Build Krause's QPE dualpol within w2algs library """
  def __init__(self, key, mrmsVersion):
    self.mrmsVersion = mrmsVersion
    Builder.__init__(self, key)
  def build(self, target):
    # This used a tar in mrms12
    if self.mrmsVersion == "mrms12":
      return
    # Build what's in the src folder
    dualpol = target+"/"+WDSS2+"/w2algs/kdualpol/dualpol-QPE"
    pathDualpol2(target)
    b.chdir(dualpol)
    r = self.autogen("./autogen.sh", target)
    self.runBuildSetup(r)
    self.makeInstall()

class buildW2ext(Builder):
  """ Build W2ext library """
  def __init__(self, key, mrmsVersion):
    self.mrmsVersion = mrmsVersion
    Builder.__init__(self, key)

  def build(self, target):
    w2ext = target+"/"+WDSS2+"/w2ext"
    b.chdir(w2ext)
    r = self.autogen("./autogen.sh", target)
    self.runBuildSetup(r)
    self.makeInstall()

class buildW2tools(Builder):
  """ Build W2tools library """
  def __init__(self, key, mrmsVersion):
    self.mrmsVersion = mrmsVersion
    # New stylesuper(buildW2tools, self).__init__(key)
    Builder.__init__(self, key)

  def build(self, target):
    w2tools = target+"/"+WDSS2+"/w2tools"
    b.chdir(w2tools)
    r = self.autogen("./autogen.sh", target)

    self.runBuildSetup(r)
    self.makeInstall()

  def checkRequirements(self):
    req = True
    return req

class MRMSSevereBuild(BuilderGroup):
  """ Build all of MRMS Severe (WDSS2) """
  def __init__(self, theConf, mrmsVersion):
    """ Get the builders from this module """
    self.mrmsVersion = mrmsVersion
    self.ourDFlags = {}
    l = []
    l.append(buildW2("w2", mrmsVersion))
    # Build krause dualpol
    l.append(buildDualpol("kdualpol", mrmsVersion))
    l.append(buildDualpolQPE("kdualpol-QPE", mrmsVersion))
    l.append(buildW2algs("w2algs", mrmsVersion))
    l.append(buildW2ext("w2ext", mrmsVersion))
    self.myW2Tools = buildW2tools("w2tools", mrmsVersion)
    l.append(self.myW2Tools)
    self.myBuilders = l
    self.isResearch = False
    self.isExport = False

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

  def checkout(self, target, scriptroot, password, options):
    b.checkoutSVN("/WDSS2/trunk", target+"/"+WDSS2, password, options)

  def checkoutPostGIT(self, target, scriptroot):
    b.run("mv WDSS2/src "+target+"/"+WDSS2)
    b.run("rm -rf WDSS2")

  def build(self, target):
    """ Build WDSS2 (MRMS_Severe) """
    print("\nBuilding WDSS2 (MRMS_Severe) libraries...")

    # Copy m4 into the location needed
    relativePath = BuilderGroup.setupWDSS2M4(self, target, WDSS2)

    # Build all builders...
    for build in self.myBuilders:
      build.build(target)

    # Put a check ldd script into the bin directory
    # Maybe this shouldn't be in this code here
    b.run("cp "+relativePath+"/check.py "+target+"/bin/check.py")

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
