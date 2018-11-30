#!/usr/bin/env python

# Robert Toomey Jan 2018
# Build WG2 from github

# System imports
import os,sys,time,datetime

# Relative imports
from . import buildtools as b
from .builder import Builder
from .builder import BuilderGroup
from .ThirdParty import THIRD
from . import wget

def autoGUI2Check():
  """ Passed for 'auto' mode for the GUI flag """
  good = True

  # Test 1: We just check for ant version 1.9 or above
  # ant 1.9 requires java 1.5 or later so we should have it as well
  # then...
  antcheck = ["ant", "-version"]
  ant = b.checkFirstList("GUI2",antcheck, ["1.9", "1.10"])
  if not ant:
    b.checkError("GUI2", antcheck, "Version 1.9 or 1.10")
  good &= ant

  return good

def getFirstDirectory(topdir):
  """Find first directory given top """
  for root, dirs, files in os.walk(topdir):
    if (len(dirs)== 1):
      print(dirs[0])
      return(dirs[0])
    else:
      print("The directory structure isn't what I expect from github in "+topdir)
      print("Maybe permissions or drive space?\n")
      return("")
  
class buildWG2(Builder):
  """ Build wg2 gui """
  def checkRequirements(self):
    return autoGUI2Check()

  def build(self, target):
    pass
    #print("We would try to build WG2..yay!")
    #print ("target is "+target)

class WG2Build(BuilderGroup):
  """ Build WG2 and related stuff """
  def __init__(self):
    """ Get the builders from this module """
    l = []
    l.append(buildWG2("WG2"))

    # Do data based stuff once on creation
    dateraw = datetime.datetime.now();
    self.mydate = dateraw.strftime("%Y-%m-%d-%H-%M-%S-%f")
    # The filename for downloading
    self.goodDownload = False
    self.gitsha = "master"
    self.myBuilders= l
    self.filename = "WG2-master.zip"

  def preCheckoutConfig(self, theConf):
    """ Snag git sha version for github pull """

    # If not building we don't checkout (at moment), so basically ignore sha question
    if self.myBuild == True:
      self.gitsha = theConf.getString("GUI2GIT", "Github SHA for WG2?  master for latest.  c997377 (worldwind archive version)", "c997377")
    # Don't use date stamp with checkout since we might be remote building later
    self.filename = "WG2-"+self.gitsha+".zip"

  def uncompressWG2(self, mydate, filename):
    """ Uncompress a WG2.zip """

    # FIXME: really need to check for failures here better....
    if os.path.isfile(filename):

      # Create unique output directory and unzip to it
      outdir = "WG2-"+self.gitsha
      outtmp = outdir+"tmp"

      # Unzip to tmp dated directory and simplify folder layout
      b.run("unzip \""+filename+"\" -d "+outtmp)
      folder = getFirstDirectory(outtmp)
      if folder == "":
        return
      folder2 = outtmp+"/"+folder
      b.run("mkdir "+outdir)

      # Find out if it's the old netbeans build.xml or the newer
      # eclipse one.  This is based on location of the file
      print("Looking for "+folder2+"/build.xml\n")
      if os.path.isfile(folder2+"/build.xml"):
        print("Found new style build.xml...\n")
        newbuild = True
      else:
        print("Looking for "+folder2+"/netbeans/WG2/build.xml\n")
        if os.path.isfile(folder2+"/netbeans/WG2/build.xml"):
          print("Found old style build.xml...\n")
          newbuild = False
        else:
          print("WG2 build fail.  Couldn't find build.xml in the checkout, maybe drive space?\n")
          return

      if newbuild:
        # Build ant in the WG2-master folder in the tmp location
        cwd = os.getcwd()
        b.chdir(outtmp+"/"+folder+"/")
        b.runOptional("ant")

        # Move everything in build to the outfolder
        b.chdir(cwd)
        b.run("mv "+outtmp+"/"+folder+"/dist/* "+outdir+"/.")

        # Remove old tmp directory
        b.run("rm -rf "+outtmp)
      else:
        # build.xml is in netbeans/WG2 so ant works there
        b.run("mv "+outtmp+"/"+folder+"/netbeans/WG2/* "+outdir+"/.")

        # Remove old tmp directory
        b.run("rm -rf "+outtmp)

        b.chdir(outdir)

        # Build the java package
        b.runOptional("ant")

        # Move the dist/WG2.jar into the root directory...so it can find the
        # release folder...
        b.run("mv dist/WG2.jar WG2.jar")

        # Move the running scripts to the root directory
        b.run("mv -f util/run/* .");

        # Change run permissions for the run scripts...
        b.runOptional("chmod a+x linux.sh windows.bat mac.sh");
        # Create/modify a desktop shortcut for gnome....

  def requireSVN(self):
    """ Do we require svn credentials? """
    return False
    
  def checkout(self, target, scriptroot, password, svnoptions):
    """ Checkout WG2 to the target directory """

    # Since checkout flag is global...
    if self.myBuild == False:
      print("Skipping WG2 git pull since we aren't building it\n")
      return

    # Script base and source within it
    base = os.getcwd()

    # We'll stick our github zip in the third party folder
    tbase = target+"/"+THIRD 

    # Script base and source within it
    myVersion = self.gitsha
    self.filename = "WG2-"+myVersion+".zip"
    theURL = "https://github.com/retoomey/WG2/archive/"+myVersion+".zip"
    print("Trying to pull WG2 (sha "+myVersion+") from git repository...")
    b.runOptional("mkdir -p "+tbase)
    b.chdir(tbase)
    goodfile = wget.download(theURL, self.filename)
    self.filename = goodfile
    if goodfile != "":
      print("Successfully downloaded github zip to "+goodfile)
      self.goodDownload = True
    else:
      self.goodDownload = False
      print("Couldn't download the WG2 package from github...sorry")
    b.chdir(base)

  def build(self, target):
    """ Build WG2 """
    print("Building WG2: " +target) 
    base = os.getcwd()
    tbase = target+"/"+THIRD 
    b.chdir(tbase)
    corename = "WG2-"+self.gitsha
    self.filename = corename+".zip"
    self.uncompressWG2(self.mydate, self.filename)
    b.chdir(base)

    # Make a runnable file
    b.runOptional("mkdir "+target+"/bin") # Just in case
    wg2file = target+"/bin/wg2"
    aFile = open(wg2file, "w")
    aFile.write("cd ../Third/"+corename+"\n")
    aFile.write("java -jar WG2.jar\n")
    aFile.close()
    b.runOptional("chmod a+x "+wg2file)

    #for build in self.myBuilders:
    #  build.build(target)

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
