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

import ThirdParty
import MRMSSevere
import MRMSHydro
import re

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
coff = "\033[0m"

line = "------------------------------------------------"

GUIBUILD = "Fresh checkout/build full package with "+red+"GUI"+coff

def getWhatAdvanced1():
  """ Get what user wants """
  myPrompts = [GUIBUILD,
               "Checkout/Build on top of existing third party",
               "Build third party only.", 
               "Checkout only.",
               "Rebuild previous folder."]
  myOptions = ["1", "2" , "3", "4", "5"]
            
  o = b.pickOption("What do you "+red+"want"+coff+" to do?", myPrompts, myOptions, "1", True)
  print "You choose option " +o
  return o
  
def getWhat():
  """ Get what user wants """
  myPrompts = [GUIBUILD, "Advanced Options"]
  myOptions = ["1", "2"]
  o = b.pickOption("What do you "+red+"want"+coff+" to do?", myPrompts, myOptions, "1", True)
  if o == "2":
    o = getWhatAdvanced1()
  return o

#               "Fresh build/checkout on top of existing third party",
#               "Build third party only", 
#               "Developer: Checkout only.",
#               "Developer: Build/Rebuild MRMS only."]
#  myOptions = ["1", "2" , "3", "4", "5"]
#            
#  o = b.pickOption("What do you "+red+"want"+coff+" to do?", myPrompts, myOptions, "1", True)
#  print "You choose option " +o
#  return o

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

def getUserName(user):
  print(line)
  """ Get user name for build """
  o = b.pickOption("What "+red+"username"+coff+" for SVN?", [], [], user, False)
  print "Username: " +o
  return o
  
def getPassword():
  print(line)
  print("To checkout I might need your "+green+"NSSL"+coff+" password (I'll keep it secret)")
  password = getpass.getpass(green+"Password:"+coff)
  print(green+"1.2.3.4 ... That's the password on my luggage.  Well if computers had luggage."+coff)
  return password

def buildhelper(checkout, buildthird, buildmain):
  """ Build stuff in order by flags """
  # Folder wanted
  folder = getBuildFolder()

  # Make sure user set always 
  user = getpass.getuser()

  # User/password for SVN and checkout
  if checkout:
    user = getUserName(user)
    b.setupSVN(user, False) # Change user now
    password = getPassword()
    print(blue+"Checking out code..."+coff)
    print("Getting the "+blue+"main WDSS2 folders"+coff+"...")
    MRMSSevere.checkout(folder)
    MRMSHydro.checkout(folder)
    print(blue+"Ok all checked out."+coff)

  # Build the third party
  if buildthird:
    print(blue+"Starting third party builder..."+coff)
    ThirdParty.build(folder)

  # Build main library
  if buildmain:
    print(blue+"Starting main build..."+coff)
    MRMSSevere.build(folder)

  b.setupSVN(user, True)

def buildMRMS():
  """ Build MRMS by checking out SVN with questions """

  user = getpass.getuser()
  b.setupSVN(user, False)

  print(line)
  print("Welcome to the "+green+"MRMS project builder"+coff+".")
  print("Version 1.0")
  print(line)
  print("Hi, "+blue+user+coff+", I'm your hopefully helpful builder.")

  what = getWhat()
  if what == "1":
    buildhelper(True, True, True)
  elif what == "2":
    buildhelper(True, False, True)
  elif what == "3":
    buildhelper(False, True, False)
  elif what == "4":
    buildhelper(True, False, False)
  elif what == "5":
    buildhelper(False, False, True)
  else:
    print ("Finished...")

if __name__ == "__main__":
  buildMRMS()
