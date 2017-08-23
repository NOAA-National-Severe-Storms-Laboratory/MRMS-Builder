#!/usr/bin/env python

# Robert Toomey March 2017
# Attempt to streamline the building process
# into something easier and braindead.

# System imports
import getpass,datetime,os
import sys,re
from subprocess import Popen, PIPE
from os.path import expanduser

# Relative imports (should work on 2 and 3)
from . import buildtools as b
from . import config as config

# Import the main group builders from all modules
# You'd add a module here if needed
from .ThirdParty import ThirdPartyBuild
from .MRMSSevere import MRMSSevereBuild
from .MRMSHydro import MRMSHydroBuild

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
coff = "\033[0m"

MAJOR_VERSION = 1
MINOR_VERSION = 1

line = "------------------------------------------------"

PGUIBUILD = "Fresh checkout/build full Severe/Hydro package with "+red+"GUI"+coff
PALGBUILD = "Fresh checkout/build full Severe/Hydro package "+red+"without GUI"+coff

def getWhatAdvanced1():
  """ Get what user wants, using keys and prompts.  They will be numbered """
  myPrompts = ["guibuild", PGUIBUILD,
               "algbuild", PALGBUILD,
               "over3rdbuild", "Checkout/Build on top of existing third party",
               "build3rd", "Build third party only.", 
               "checkout", "Checkout only.",
               "rebuild", "Rebuild previous folder checked out with MRMS builder."]
            
  o = b.pickSmarter("What do you "+red+"want"+coff+" to do?", myPrompts, "guibuild", True, False)
  print("You choose option: " +o)
  return o
  
def getWhat():
  """ Get what user wants """
  myPrompts = ["guibuild", PGUIBUILD, 
               "algbuild", PALGBUILD, 
               "advanced", "Advanced Options"]
  o = b.pickSmarter("What do you "+red+"want"+coff+" to do?", myPrompts, "guibuild", True, False)
  print("You choose option: " +o)
  if o == "advanced":
    o = getWhatAdvanced1()
  return o

def getBuildFolder():
  """ Get the build folder """
  #global date

  # Get Timestamp
  today = datetime.date.today()
  date = today.strftime("%Y%m%d")

  # Relative to script location (option 1)
  relativePath = os.path.dirname(os.path.realpath(__file__))
  oldpwd = os.getcwd()
  os.chdir(relativePath)
  os.chdir("..")
  os.chdir("..")
  relativePath = os.getcwd()
  os.chdir(oldpwd)

  # Paths
  relativePath = relativePath+"/MRMS"
  relativePathDate = relativePath+"_"+date
  homePath = expanduser("~")+"/"+"MRMS"
  homePathDate = homePath+"_"+date

  myPrompts = [
               "Use Home Dated: " + green+homePathDate+coff,
               "Use Home: " + green+homePath+coff,
               "Use Relative Dated: " + green+relativePathDate+coff,
               "Use Relative: " + green+relativePath+coff,
              ]
  myOptions = ["1", "2", "3", "4"]
            
  while True:
    good = True

    o = b.pickOption1(red+"Where"+coff+" would you like the build placed? (You can type a path as well)", myPrompts, myOptions, "1", False, True)
    print("You choose: " +o)

    # Get the path wanted
    wanted = o 

    if (wanted == ""): # Use default of 1
      wanted = "1"

    if (wanted == "1"):
      wanted = homePathDate
    elif (wanted == "2"):
      wanted = homePath
    elif (wanted == "3"):
      wanted = relativePathDate
    elif (wanted == "4"):
      wanted = relativePath

    # Try to create directory...
    if not os.path.exists(wanted):
      try:
        os.makedirs(wanted)
      except:
        print("I couldn't create directory "+wanted)
        good = False

    # Try to access directory...
    if not os.access(wanted, os.W_OK):
      print("...but I can't _access_ "+wanted+". Permission settings?")
      good = False
 
    if good:
      return wanted

def getPassword(user):
  """ Get password for build """
  global theConf
  o = theConf.getString("PASSWORD", "", "")
  if o == "":
    print(line)
    print("To checkout I might need your "+green+"NSSL"+coff+" password (I'll keep it secret)")
    o = getpass.getpass(green+user+" Password:"+coff)
    print(green+"1.2.3.4 ... That's the password on my luggage.  Well if computers had luggage."+coff)
  return o

def addBuilder(aList, aBuilder, aBuildItFlag):
  """ Convenience function for adding builder """
  aBuilder.setBuild(aBuildItFlag)
  aList.append(aBuilder)
  return aBuilder

def buildMRMS():
  """ Build MRMS by checking out SVN with questions """
  global theConf

  # Try to use default cfg or one passed by user
  configFile = "default.cfg"
  if len(sys.argv) > 1:
    configFile = sys.argv[1]
  theConf = config.Configuration()
  confResult = theConf.readConfig(configFile)

  # Basic fall back user name/SVN settings
  user = getpass.getuser()
  b.setupSVN(user, False)

  print(line)
  #print("Welcome to the "+green+"MRMS project builder V1.0"+coff)
  version = str(MAJOR_VERSION)+"."+str(MINOR_VERSION)
  print("Welcome to the "+green+"MRMS project builder V"+version+coff)
  print("Using config file: "+configFile+" "+red+confResult+coff)
  print(line)
  print("Hi, "+blue+user+coff+", I'm your hopefully helpful builder.")

  #wantAdvanced = theConf.getBoolean("ADVANCED", "Do you want to see advanced options and tools?", "no")
  checkout = True
  checkout = theConf.getBoolean("CHECKOUT", "Checkout all code from SVN repository?", "yes")
  buildThird = theConf.getBoolean("THIRDPARTY", "Build all third party packages?", "yes")
  buildWDSS2 = theConf.getBoolean("WDSS2", "Build WDSS2 packages?", "yes")
  buildHydro = theConf.getBoolean("HYDRO", "Build Hydro packages after WDSS2?", "yes")
  buildGUI = theConf.getBoolean("GUI", "Build the WG display gui (requires openGL libraries installed)?", "yes")

  # Builder group packages, add in dependency order
  # To add a new module, add an 'from' import at top and add a line here
  bl = []
  thirdparty = addBuilder(bl, ThirdPartyBuild(), buildThird)
  mrmssevere = addBuilder(bl, MRMSSevereBuild(), buildWDSS2)
  mrmssevere.setWantGUI(buildGUI)
  mrmshydro = addBuilder(bl, MRMSHydroBuild(), buildHydro)

  ###################################################
  # Try to do stuff that could 'break' if misconfigured here before checking out...
  # Get all the "-D" cppflag options Lak spammed us with (see below)
  if buildWDSS2 == True:
    ourDFlags = theConf.getOurDFlags()
    print("DEBUG:Ok OUR cppflags are:"+str(ourDFlags))
    #print("Expire flags: '"+expireFlags+"'")
    #  $ENV{CXXFLAGS} = "$required_flags $optimized $debug $sunrise $sunset $export_flags ${key_flags} $param{cxxflags}";

  # Get make flags here early in case it dies
  cpus = theConf.getJobs() 
  makeFlags = "--jobs="+cpus   # extra make flags

  # Check requirements for each wanted module
  #print ("Checking requirements for build...\n")
  req = True
  for bg in bl:
     if bg.getBuild():  # Only check if we're building it?
       req = req & bg.checkRequirements()
  if req == False:
    print("Missing installed libraries or rpms to build, contact IT to install.")
    sys.exit(1)
  ###################################################

  # Folder wanted.  Currently asked for...but could have 'smart' option
  folder = getBuildFolder()

  # User/password for SVN and checkout
  if checkout:
    #user = getUserName() user = getpass.getuser()
    uprompt ="What "+red+"username"+coff+" for SVN?"
    user = theConf.getString("USERNAME", uprompt, getpass.getuser())
    b.setupSVN(user, False) # Change user now
    password = getPassword(user)
    print(blue+"Checking out code..."+coff)
    for bg in bl:
      bg.checkout(folder, password)
    print(blue+"Check out success."+coff)

  w2cppflags = ""
  if buildWDSS2 == True:
    # Basically we use any -D values from Lak's auth files, overridden
    # by anything we express in our configure...and all these go to 
    # cppflags on make command line... 
    isResearch = False
    keypath = mrmssevere.getKeyLocation(folder, isResearch)
    authFileDFlags = theConf.getAuthFileDItems(keypath)
    map1 = theConf.mergeConfigLists(ourDFlags, authFileDFlags) # 2nd overrides...
    w2cppflags = theConf.listToDFlags(map1)
    mrmssevere.setCPPFlags(w2cppflags)
    #print "DEBUG: CPPFLAGS= "+w2cppflags

  # Build everything wanted (order matters here)
  for bg in bl:
     if bg.getBuild():
       # All using same make flags for now at least
       bg.setMakeFlags(makeFlags)
       bg.build(folder)

  b.setupSVN(user, True)

if __name__ == "__main__":
  print("Run the ./build.py script to execute")
