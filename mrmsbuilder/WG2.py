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
import wget.wget as wget

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
    self.filename = "WG2-"+self.mydate+".zip"
    self.goodDownload = False
    self.myBuilders= l

  def uncompressWG2(self, mydate, filename):
    """ Uncompress a WG2.zip """

    # FIXME: really need to check for failures here better....
    if os.path.isfile(filename):

      # Create unique output directory and unzip to it
      outdir = "WG2-"+mydate
      outtmp = "WG2-"+mydate+"tmp"

      # Unzip to tmp dated directory and simplify folder layout
      b.run("unzip "+filename+" -d "+outtmp)
      b.run("mkdir "+outdir)
      b.run("mv "+outtmp+"/WG2-master/netbeans/WG2/* "+outdir+"/.")

      # Remove old tmp directory
      b.run("rm -rf "+outtmp)

      # We need to create a jar file from the source....
      # FIXME: check java version, etc...
      #run("java cf WG2"+mydate+".jar "+outdir+"/src/*.class")
      #os.chdir(outdir)
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
    
      # Should be runable now


  def checkout(self, target, password, svnoptions):
    """ Checkout WG2 to the target directory """

    # Script base and source within it
    base = os.getcwd()

    # We'll stick our github zip in the third party folder
    tbase = target+"/"+THIRD 

    # Script base and source within it
    theURL = "https://github.com/retoomey/WG2/archive/master.zip"
    print("Trying to pull latest WG2 from git repository...")
    print("This can take about a minute to download.")
    b.runOptional("mkdir -p "+tbase)
    b.chdir(tbase)
    goodfile = wget.download(theURL, self.filename)
    self.filename = goodfile
    if goodfile != "":
      print("Successfully downloaded github zip to "+goodfile)
      self.goodDownload = True
      #print("Attempting to build..."+goodfile)
      #self.uncompressWG2(self.mydate, goodfile)
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
    self.uncompressWG2(self.mydate, self.filename)
    b.chdir(base)

    # Make a runnable file
    wg2file = target+"/bin/wg2"
    aFile = open(wg2file, "w")
    aFile.write("cd ../Third/WG2-"+self.mydate+"\n")
    aFile.write("java -jar WG2.jar\n")
    aFile.close()
    b.runOptional("chmod a+x "+wg2file)

    #for build in self.myBuilders:
    #  build.build(target)

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
