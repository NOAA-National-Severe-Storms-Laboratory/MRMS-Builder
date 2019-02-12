#!/usr/bin/env python

# Robert Toomey May 2017
# Class for building 'something'
# until I figure where best to put it
from . import buildtools as b

class Builder:
  """ Build a individual package such as 'netcdf' """
  def __init__(self, key):
    self.key = key
    self.cppflags = ""
    self.makeflags = ""
  def setCPPFlags(self, stuff):
    """ Set extra flags for cppflags """
    self.cppflags = stuff
  def setMakeFlags(self, stuff):
    """ Set extra flags for make """
    self.makeflags = stuff
  def clean(self):
    """ Clean up.  For example, Third party removes the uncompressed folder. """
    pass 
  def copy(self, target):
    """ Copy self to destination """
    pass
  def unzip(self):
    """ Do any unpacking needed.  Third party libraries are typically compressed """
    pass
  def build(self, target):
    """ Run all build commands. target, config/autogen options, make options """
    pass
  def showkey(self):
    """ Debug show our passed in key.  Third party uses this as the main name """
    print("The key is "+self.key)
  def getKey(self):
    """ Get the key for this builder """
    return self.key
  def checkRequirements(self):
    """ return false if requirements not met """
    return True
  def localInclude(self, target):
    """ Stock cpp option that include our build include (always use our source first) """
    return "-I"+target+"/include/ -Wl,-rpath="+target+"/lib "+self.cppflags
  def localLink(self, target):
    """ Stock ldflags that include our build lib (always use our libs first) """
    return "-L"+target+"/lib/"
  def cppFlags(self, target):
    """ Get cppflags """
    cppflags = self.localInclude(target)
    if cppflags != "":
      cppflags = " CPPFLAGS='"+cppflags+"'"
    return cppflags
  def ldFlags(self, target):
    """ Get ldflags """
    ldflags = self.localLink(target)
    if ldflags != "":
      ldflags = " LDFLAGS='"+ldflags+"'"
    return ldflags
  def shareFlags(self):
    """ Flags for share/static build """
    return " --enable-shared"
  def prefixFlags(self, target):
    """ Flags for prefix """
    return " --prefix="+target
  def autogen(self, prefix, target):
    """ Append all flags to prefix given """
    cppflags = self.cppFlags(target)
    ldflags = self.ldFlags(target)
    prefixflags = self.prefixFlags(target)
    shareFlags = self.shareFlags()
    return prefix+prefixflags+cppflags+ldflags+shareFlags
  def markRebuild(self, command):
    """ Write the build command to a script we can call if debugging a failed build """
    rerun = open("rebuild.sh", "w")
    rerun.write(command)
    rerun.write("\n")
    rerun.close()
    b.runOptional("chmod a+x rebuild.sh")
  def runBuildSetup(self, command):
    """ Read command for setup in directory and make a file for rerunning it """
    b.run(command)
    markRebuild(command)
  def makeInstall(self):
    """ Do the stock make and make install in a build """
    b.run("make "+self.makeflags)
    b.run("make install")

class BuilderGroup:
  """ Build a logical group of packages, such as hydro or third party or severe """
  def __init__(self):
    self.myBuilders = []
  def preCheckoutConfig(self, theConf):
    """ Configuration questions just for this builder """
    # Default to -j for all builds for speed
    cpus = theConf.getJobs() 
    makeFlags = "--jobs="+cpus   # extra make flags
    for build in self.myBuilders:
       build.setMakeFlags(makeFlags)
  def postCheckoutConfig(self, theConf, target):
    """ Configuration questions just for this builder """
    pass
  def requireSVN(self):
    """ Do we require svn credentials? """
    return True
  def removeBuilder(self, key):
    """ Remove builder with given key name """
    newlist = []
    for build in self.myBuilders:
       aKey = build.getKey()
       if (aKey == key):
         #print("Removing builder " +key + " from builder list")
         pass
       else:
         newlist.append(build)
    self.myBuilders = newlist

  def listBuilders(self):
    """ List all builder keys """
    for build in self.myBuilders:
      print("Builder: "+build.getKey())
  def setCPPFlags(self, stuff):
    """ Set extra flags for cppflags """
    for build in self.myBuilders:
      build.setCPPFlags(stuff)
  def setMakeFlags(self, stuff):
    """ Set extra flags for make """
    for build in self.myBuilders:
      build.setMakeFlags(stuff)
  def checkRequirements(self):
    """ Check requirements for this builder. """
    req = True
    for build in self.myBuilders:
       req = req & build.checkRequirements()
    return req
  def checkout(self, target, scriptroot, password, svnoptions):
    pass
  def build(self, target):
    pass
