#!/bin/python

# Robert Toomey March 2017
# Build from compressed sources.
# This is used to build a third party source directory

import os,sys
import buildtools as b
from builder import Builder
from builder import BuilderGroup

dualSet = 0

THIRD = "Third"

def pathDualpol(target):
  """ Set up header ENV for dualpol """
  global dualSet

  if dualSet == 0:
    print "******Setting path dualpol"
    os.environ["ORPGDIR"] = target
    os.environ["DUALPOLDIR"] = target
    os.environ["QPE_LIB_ONLY"] = "1"
    cfg = target+"/lib/pkgconfig"
    c = os.environ.get("PKG_CONFIG_PATH")
    if (c is None):
      os.environ["PKG_CONFIG_PATH"] = cfg
    else:
      os.environ["PKG_CONFIG_PATH"] = cfg+":"+c
    dualSet = 1
  else:
    print "Not setting path dualpol"

class BuildThird(Builder):
  """ build a third party from compressed source and stock configure """
  def clean(self):
    b.runOptional("rm -rf "+self.key)
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    r = r + " --enable-shared"
    b.run(r)
    self.makeInstall(m)

class BuildTar(BuildThird):
  """ build a third party from a stock tar.gz """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")

class buildGCTPC(BuildTar):
  """ Build ancient GCTPC projection library """
  def build(self, t, c, m):
    b.chdir(self.key)
    b.chdir("source")
    b.run("make")
    b.run("cp libgeo.a "+t+"/lib/libgeo.a")
    b.run("cp *.h "+t+"/include/.")

class buildProj4(BuildTar):
  """ Build proj4 library """
  pass

class buildWgrib2(BuildTar):
  """ Build Wgrib2 grib2 manipulation tool and library for hydro """
  def build(self, t, c, m):
    b.chdir(self.key)
    os.environ["CPPFLAGS"] = self.cppFlags(t)
    os.environ["LDFLAGS"] = self.ldFlags(t)+" -lnetcdf -lg2c_v1.6.0 -lm -ljasper -lpng -lproj -lgeo"
    b.run("make")
    b.run("cp wgrib2 "+t+"/bin/wgrib2")
    b.runOptional("mkdir "+t+"/include/wgrib2/")
    b.run("cp *.h "+t+"/include/wgrib2/.")
    os.environ["CPPFLAGS"] = ""
    os.environ["LDFLAGS"] = ""

class buildJASPER(BuildThird):
  """ Build Jasper library """
  def copy(self, t):
    b.run("cp "+self.key+".zip "+t)
  def unzip(self):
    b.run("unzip "+self.key+".zip")

class buildLIBPNG(BuildTar):
  """ Build libpng library """
  pass

class buildHMRGW2(BuildTar):
  """ Build HMRGW2 library to link hydro and w2 """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./autogen.sh", t)
    r = r + " --enable-shared"
    b.run(r)
    self.makeInstall(m)

class buildG2CLIB(BuildThird):
  """ Build g2clib library """
  def copy(self, t):
    b.run("cp "+self.key+".tar "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar")
  def build(self, t, c, m):
    b.chdir(self.key)
    # Brain dead g2lib doesn't have a configure.  Seriously?
    # Move the original makefile and make a new one using it...
    b.run("mv makefile makefileBASE")
    nmake = open("makefile", 'w')
    nmake.write("# Robert Toomey.  Override g2clib make for our own purposes.\n")
    nmake.write("include makefileBASE\n")
    nmake.write("INC=-I"+t+"/include\n")
    #nmake.write("CFLAGS= -O3 -g -m64 $(INC) $(DEFS) -D__64BIT__\n")
    nmake.write("CFLAGS= -O3 -g -m64 $(INC) $(DEFS)\n")
    nmake.close()
    b.run("make")
    b.run("cp libg2c*a "+t+"/lib")
    b.run("cp *.h "+t+"/include")

class buildUDUNITS(BuildTar):
  """ Build udunits library """
  pass

class buildNETCDF(BuildTar):
  """ Build netcdf library """
  pass

class buildNETCDFPLUS(BuildTar):
  """ Build netcdf c++ library """
  def build(self, t, c, m):
    b.chdir(self.key)
    # f***** brain dead netcdfc++.  We really need to kill this library from w2 like in RAMP
    #os.environ["CPPFLAGS"] = "-I"+t+"/include/"
    r = self.autogen("./configure", t)
    r = r + " --enable-shared --enable-cxx-4"
    b.run(r)
    self.makeInstall(m)

class buildORPGINFR(BuildTar):
  """ Build orpginfr library """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./autogen.sh", t)
    r = r +" --enable-shared"
    b.run(r)
    b.run("chmod a+x ./LinkLib008")
    self.makeInstall(m)

class buildGDAL(BuildTar):
  """ Build gdal library """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    r = r + " --without-mysql --without-python --with-jpeg=no --with-gif=no --without-ogr --with-geos=no --with-pg=no --with-pic --with-hdf5=no --with-ogr=no"
    r = r + " --with-libtiff=internal"    # Use internal?  RPM might be stock
    r = r + " --with-png="+t              # Use built one
    r = r + " --with-jasper="+t           # Use built one
    r = r + " --without-grib"             # conflict with g2clib
    b.run(r)
    self.makeInstall(m)

class buildDualpol(BuildTar):
  """ Build base dualpol library """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./autogen.sh", t)
    b.run(r)
    self.makeInstall(m)

class buildDualpolRRDD(BuildTar):
  """ Build dualpol RRDD library """
  def build(self, t, c, m):
    b.chdir(self.key)
    pathDualpol(t)
    r = self.autogen("./autogen.sh", t)
    b.run(r)
    self.makeInstall(m)

class buildDualpolQPE(BuildTar):
  """ Build base dualpol QPE library """
  def build(self, t, c, m):
    b.chdir(self.key)
    pathDualpol(t)
    r = self.autogen("./autogen.sh", t)
    b.run(r)
    self.makeInstall(m)

class ThirdPartyBuild(BuilderGroup):
  """ Build all of required third party """
  def __init__(self):
    """ Get the builders from this module """
    #  l.append(buildLIBPNG("libpng-1.6.28", t))

    # --------------------------------------------
    # Tree one: Needed for grib2 manipulation for
    # various reasons.
    l = []
    l.append(buildJASPER("jasper-1.900.1"))
    l.append(buildG2CLIB("g2clib-1.6.0")) # Require jasper

    # Projection libraries
    l.append(buildGCTPC("gctpc"))
    l.append(buildProj4("proj-4.9.3"))

    # Netcdf libraries
    l.append(buildNETCDF("netcdf-4.3.3.1"))
    l.append(buildNETCDFPLUS("netcdf-cxx-4.2"))

    # Grib2 tools (Requires: projection, netcdf, jasper and g2clib)
    l.append(buildWgrib2("wgrib2-2.0.6c")) # NOTE: make sure links to current gctpc in LDFLAGS

    # --------------------------------------------
    # Tree two: Units and other stuff, order here
    # shouldn't matter

    # Units and orpginfr stuff...
    l.append(buildUDUNITS("udunits-2.2.24"))
    l.append(buildORPGINFR("orpginfr-3.0.1"))

    # Finally Krause code we use
    l.append(buildDualpol("dualpol-04182017"))
    l.append(buildDualpolQPE("dualpol-QPE-04182017"))

    # MRMSHydro to MRMSSevere datatype linking library
    l.append(buildHMRGW2("hmrgw2_lib-05102017"))

    # The monster at the end...
    # This is such a useful library, but it's a big one.
    l.append(buildGDAL("gdal-2.1.3"))
    self.myBuilders = l

  def build(self, target, configFlags, makeFlags):
    """ Build third party used by all packages """

    print("Building third party libraries: " +target) 

    # Script base and source within it
    base = os.getcwd()
    b.chdir(base+"/third")

    # Third code build base
    #tbase = target+"/src/thirdb/" 
    tbase = target+"/"+THIRD 
    b.runOptional("mkdir -p "+tbase)

    # Copy all builders...
    for build in self.myBuilders:
      build.copy(tbase)

    # Now change to target
    b.chdir(tbase)

    # Unzip all builders...
    for build in self.myBuilders:
      build.unzip()
      b.chdir(tbase)

    # Build all builders...
    for build in self.myBuilders:
      build.build(target, configFlags, makeFlags)
      b.chdir(tbase)

    # came back so mark a good build...
    #mark1= open("mark3rd.txt", "w")
    #mark1.write(target+","+date)
    #mark1.write("\n")
    #mark1.close()

    print("Finished third party...\n");

# Run main
if __name__ == "__main__":
  print "Run the main build script...\n"
