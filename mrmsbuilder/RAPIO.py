#!/usr/bin/env python

# Robert Toomey Sept 2020
# Build RAPIO from github

# System imports
import os,sys

# Relative imports
from . import buildtools as b
from .builder import Builder
from .builder import BuilderGroup
from .ThirdParty import THIRD
from . import wget

class buildRAPIO(Builder):
  """ Build RAPIO """
  def checkRequirements(self):
    # Check for git?
    return True

  def build(self, target):
    rapio = target+"/RAPIO"
    b.chdir(rapio)

    r = "./autogen.sh --prefix="+target
    r = r + " --enable-shared"

    self.runBuildSetup(r)

    # Have to build in the BUILD directory, right?
    b.chdir(rapio+"/BUILD")
    self.makeInstall()

class RAPIOBuild(BuilderGroup):
  """ Build WG2 and related stuff """
  def __init__(self):
    """ Get the builders from this module """
    l = []
    l.append(buildRAPIO("RAPIO"))
    self.myBuilders = l

  def requireSVN(self):
    """ Do we require svn credentials? """
    return False
    
  def checkout(self, target, scriptroot, password, svnoptions):
    """ Checkout RAPIO to the target directory """

    # Script base and source within it
    base = os.getcwd()

    # Pull to target directory
    tbase = target+"/" 
    theURL = "https://github.com/retoomey/RAPIO/"
    print("Trying to pull RAPIO from git repository...")
    b.chdir(tbase)
    b.run("git clone "+theURL)

  def checkoutGIT(self, target, scriptroot, password, options):
    gitssh = "-c core.sshCommand='ssh -i "+password+"'";
    rapio = target+"/RAPIO"
    gitcommand = "git "+gitssh+" clone git@github.com:retoomey/RAPIO.git "+rapio
    b.run(gitcommand)

  def build(self, target):
    """ Build RAPIO """
    # Build all builders...
    for build in self.myBuilders:
      build.build(target)

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
