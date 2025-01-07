#!/usr/bin/env python

# Robert Toomey May 2017
# Classes to build MRMS Hydro

# System imports
import os,sys

# Relative imports
from . import buildtools as b
from .builder import Builder
from .builder import BuilderGroup

HYDRO = "HMET"

class buildHydro(Builder):
  """ Build Hydro library """
  def __init__(self, key, r):
    self.rapio = r
    Builder.__init__(self, key)

  """ Build Hydro library """
  def build(self, target):
    hbase = target+"/"+HYDRO+"/"
    b.chdir(hbase)
    r = "./autogen.sh --prefix="+target+" --enable-shared "
    # Conditional RAPIO algs
    # Since we can layer builds, check if folder there
    # because we might have built in a previous run
    if os.path.isdir(target+"/RAPIO"):
      r += "--with-rapio "
    self.runBuildSetup(r)
    self.makeInstall()

class buildFortran(Builder):
  """ Build little fortran programs """
  def checkRequirements(self):
    req = True
    # Test 1: Check for gfortran
    if not b.checkFirstText("GFORTRAN HYDRO APPS",["which", "gfortran"], "gfortran"):
      req = False
    return req
  def build(self, target):
    hbase = target+"/"+HYDRO+"/"

    b.chdir(hbase)
    b.chdir("algs/solar_zenith")
    b.run("make")
    b.run("cp solar_zenith "+target+"/bin/solar_zenith")

    b.chdir(hbase)
    b.chdir("tools/convert_goes16_for_anc")
    b.run("make")
    b.run("cp convert_goes16_for_anc "+target+"/bin/convert_goes16_for_anc")

class MRMSHydroBuild(BuilderGroup):
  """ Build all of MRMS Hydro """
  def __init__(self, theConf, mrmsVersion, r):
    """ Get the builders from this module """
    self.mrmsVersion = mrmsVersion
    self.theConf = theConf
    if self.mrmsVersion == "mrms12":
      self.rapio = False
    else:
      self.rapio = r
    l = []
    l.append(buildHydro("hydro", self.rapio))
    buildlittle = theConf.getBoolean("HYDROFORTRAN", "Build HYDRO fortran apps?", "no")
    if buildlittle:
      l.append(buildFortran("hydrofortran"))
    self.myBuilders = l

  def checkout(self, target, scriptroot, password, options):
    b.checkoutSVN("/MRMS_hydro/trunk", target+"/"+HYDRO, password, options)

  def checkoutGIT(self, target, scriptroot, password, options):
    gitssh = "-c core.sshCommand='ssh -i "+password+"'";
    hydro = target+"/"+HYDRO
    gitcommand = "git "+gitssh+" clone git@github.com:NOAA-National-Severe-Storms-Laboratory/MRMS-hydro.git  "+hydro
    b.run(gitcommand)

  def checkoutPostGIT(self, target, scriptroot):
    b.run("mv HMET/src "+target+"/"+HYDRO)
    b.run("rm -rf HMET")

  def build(self, target):
    """ Build HYDRO (MRMS_Hydro) """
    print("\nBuilding HYDRO (MRMS_Hydro) libraries...")

    # Note switching to cmake will vaporize the majority of
    # our scripts here.
    hydro = target+"/"+HYDRO
    b.chdir(hydro)
    b.run("mkdir BUILD")
    b.chdir(hydro+"/BUILD")
    b.run("cmake .. -DCMAKE_INSTALL_PREFIX=../..");
    cpus = self.theConf.getJobs()
    if (cpus == ""):
      b.run("make install")
    else:
      b.run("make -j"+cpus+" install")

    # Use our new m4 to static link third
    #b.runOptional("rm "+target+"/"+WDSS2+"/config/w2.m4")
    #relativePath = os.path.dirname(os.path.realpath(__file__))
    #b.run("cp "+relativePath+"/newm4.m4 "+target+"/"+WDSS2+"/config/newm4.m4")

    # Build all builders...
    #for build in self.myBuilders:
    #  build.build(target)

    # Put a check ldd script into the bin directory
    # Maybe this shouldn't be in this code here
    #b.run("cp "+relativePath+"/check.py "+target+"/bin/check.py")

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
