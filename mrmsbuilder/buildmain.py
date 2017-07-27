#!/bin/python

# Robert Toomey March 2017
# Attempt to streamline the building process
# into something easier and braindead.

import getpass,datetime,os
import sys
import subprocess
from subprocess import Popen, PIPE
from os.path import expanduser
import buildtools as b
import filecompleter
import multiprocessing
import config as config

# Import the main group builders from all modules
# You'd add a module here if needed
from ThirdParty import ThirdPartyBuild
from MRMSSevere import MRMSSevereBuild
from MRMSHydro import MRMSHydroBuild

import ThirdParty
import MRMSSevere
import MRMSHydro
import re

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
coff = "\033[0m"

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
  print "You choose option: " +o
  return o
  
def getWhat():
  """ Get what user wants """
  #myPrompts = [GUIBUILD, ALGBUILD, "Advanced Options"]
  #myOptions = ["1", "2", "3"]
  #o = b.pickOption("What do you "+red+"want"+coff+" to do?", myPrompts, myOptions, "1", True)
  #if o == "3":
  #  o = getWhatAdvanced1()
  #return o
  myPrompts = ["guibuild", PGUIBUILD, 
               "algbuild", PALGBUILD, 
               "advanced", "Advanced Options"]
  o = b.pickSmarter("What do you "+red+"want"+coff+" to do?", myPrompts, "guibuild", True, False)
  print "You choose option: " +o
  if o == "advanced":
    o = getWhatAdvanced1()
  return o
  #myOptions = ["1", "2", "3"]
  #o = b.pickOption("What do you "+red+"want"+coff+" to do?", myPrompts, myOptions, "1", True)
  #if o == "3":
  #  o = getWhatAdvanced1()
  #return o

def getBuildFolder():
  """ Get the build folder """
  #global date

  # WDSS2 folder with a timestamp
  today = datetime.date.today()
  date = today.strftime("%Y%m%d")
  folder = "WDSS2_"+date

  # Relative to script location (option 1)
  relativePath = os.path.dirname(os.path.realpath(__file__))
  oldpwd = os.getcwd()
  os.chdir(relativePath)
  os.chdir("..")
  relativePath = os.getcwd()
  os.chdir(oldpwd)
  relativePath = relativePath+"/"+folder
  static1Path = relativePath+"/MRMS"

  # Home path...(option 2)
  homePath = expanduser("~")+"/"+folder

  myPrompts = ["Use Relative: " +green+relativePath+coff,"Use Home: " + green+homePath+coff]
  #             "Use Static: " + green+static1Path+coff]
  myOptions = ["1", "2"]
            
  while True:
    good = True

    o = b.pickOption1(red+"Where"+coff+" would you like the build placed? (You can type a path as well)", myPrompts, myOptions, "1", False, True)
    print "You choose: " +o

    # Get the path wanted
    wanted = o 

    if (wanted == "1"):
      wanted = relativePath
    elif (wanted == "2"):
      wanted = homePath
    elif (wanted == ""):
      wanted = relativePath

    # Try to create directory...
    if not os.path.exists(wanted):
      try:
        os.makedirs(wanted)
      except:
        print ("I couldn't create directory "+wanted)
        good = False

    # Try to access directory...
    if not os.access(wanted, os.W_OK):
      print ("...but I can't _access_ "+wanted+". Permission settings?")
      good = False
 
    if good:
      return wanted

def getUserName():
  """ Get user name for build """
  global theConf
  o = theConf.getString("USERNAME", "")
  if o == "":
    print(line)
    user = getpass.getuser()
    o = b.pickOption("What "+red+"username"+coff+" for SVN?", [], [], user, False)
    print "Username: " +o
  return o
  
def getPassword(user):
  """ Get password for build """
  global theConf
  o = theConf.getString("PASSWORD", "")
  if o == "":
    print(line)
    print("To checkout I might need your "+green+"NSSL"+coff+" password (I'll keep it secret)")
    o = getpass.getpass(green+user+" Password:"+coff)
    print(green+"1.2.3.4 ... That's the password on my luggage.  Well if computers had luggage."+coff)
  return o

def getJobs():
  """ Get job flag for all makes """
  global theConf
  o = theConf.getString("JOBS", "")
  if ((o == "CPU") or (o == "")):
    o =str(multiprocessing.cpu_count())
  return o

def buildhelper(checkout, buildthird, buildSevere, buildHydro, buildGUI):
  """ Build stuff in order by flags """

  # Builder group packages, add in dependency order
  # To add a new module, add an 'from' import at top and add
  # a line here
  bl = []
  thirdparty = ThirdPartyBuild()
  thirdparty.setBuild(buildthird)
  bl.append(thirdparty)

  mrmssevere = MRMSSevereBuild()
  mrmssevere.setBuild(buildSevere)
  mrmssevere.setWantGUI(buildGUI)
  bl.append(mrmssevere)

  mrmshydro = MRMSHydroBuild()
  mrmshydro.setBuild(buildHydro)
  bl.append(mrmshydro)

  # Check requirements for each wanted module
  #print ("Checking requirements for build...\n")
  req = True
  for bg in bl:
     if bg.getBuild():  # Only check if we're building it?
       req = req & bg.checkRequirements()
  if req == False:
    print "Missing installed libraries or rpms to build, contact IT to install.\n"
    sys.exit(1)

  # ASK USER:  Folder wanted
  folder = getBuildFolder()

  # ASK USER: User/password for SVN and checkout
  if checkout:
    user = getUserName()
    b.setupSVN(user, False) # Change user now
    password = getPassword(user)

  # Done with interactive at this point....
  if checkout:

    print(blue+"Checking out code..."+coff)
    #print("Getting the "+blue+"main WDSS2 folders"+coff+"...")
    for bg in bl:
      bg.checkout(folder, password)
    #mrmssevere.checkout(folder, password)
    #mrmshydro.checkout(folder, password)
    print(blue+"Check out success."+coff)

  # Build everything wanted (order matters here)
  configFlags = "" # extra config flags
  cpus = getJobs() 
  makeFlags = "--jobs="+cpus   # extra make flags
  for bg in bl:
     if bg.getBuild():
       bg.build(folder, configFlags, makeFlags)

  b.setupSVN(user, True)

def buildMRMS():
  """ Build MRMS by checking out SVN with questions """
  global theConf

  # Try to use default cfg or one passed by user
  configFile = "default.cfg"
  if len(sys.argv) > 1:
    configFile = sys.argv[1]
  theConf = config.Configuration()
  confResult = theConf.readConfig(configFile)
 # aName = theConf.getString("USERNAME", "")
 # print ("Name from config is "+aName)

  user = getpass.getuser()
  b.setupSVN(user, False)

  print(line)
  print("Welcome to the "+green+"MRMS project builder V1.0"+coff)
  print("Using config file: "+configFile+" "+red+confResult+coff)
  print(line)
  print("Hi, "+blue+user+coff+", I'm your hopefully helpful builder.")

  what = getWhat()

  # FIXME: still kinda messy with the flags.  Better to have set methods I think...
  if what == "guibuild":
    buildhelper(True, True, True, True, True)  # Everything
  if what == "algbuild":
    buildhelper(True, True, True, True, False) # Everything BUT GUI
  elif what == "over3rdbuild":
    buildhelper(True, False, True, True, True) # Everything over a third
  elif what == "build3rd":  # Checkout, build third party libraries only
    buildhelper(True, True, False, False, False)
  elif what == "checkout":  # Only checkout
    buildhelper(True, False, False, False, False)
  elif what == "rebuild":
    buildhelper(False, False, True, True, True) # rebuild, no third
  else:
    print ("Finished...")

if __name__ == "__main__":
  print "Run the ./build.py script to execute\n"
