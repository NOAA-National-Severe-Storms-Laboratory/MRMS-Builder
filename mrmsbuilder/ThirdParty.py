#!/bin/python

# Robert Toomey March 2017
# Build from compressed sources.
# This is used to build a third party source directory

import os,sys
import buildtools as b
from builder import Builder

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
  def build(self, t):
    b.chdir(self.key)
    b.run("./configure --prefix="+t+" --enable-shared")
    b.run("make")
    b.run("make install")

class BuildTar(BuildThird):
  """ build a third party from a stock tar.gz """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")

class buildGCTPC(BuildTar):
  """ Build ancient GCTPC projection library """
  def build(self, t):
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
  def build(self, t):
    b.chdir(self.key)
    os.environ["CPPFLAGS"] = "-I"+self.target+"/include/ -Wl,-rpath="+self.target+"/lib"
    os.environ["LDFLAGS"] = "-L"+self.target+"/lib/ -lnetcdf -lg2c_v1.6.0 -lm -ljasper -lpng -lproj -lgeo"
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
  def build(self, t):
    b.chdir(self.key)
    b.run("./autogen.sh --prefix="+t+" --enable-shared")
    b.run("make")
    b.run("make install")

class buildG2CLIB(BuildThird):
  """ Build g2clib library """
  def copy(self, t):
    b.run("cp "+self.key+".tar "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar")
  def build(self, t):
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
    b.run("cp libg2c*a "+self.target+"/lib")
    b.run("cp *.h "+self.target+"/include")

class buildUDUNITS(BuildTar):
  """ Build udunits library """
  pass

class buildNETCDF(BuildTar):
  """ Build netcdf library """
  pass

class buildNETCDFPLUS(BuildTar):
  """ Build netcdf c++ library """
  def build(self, t):
    b.chdir(self.key)
    # f***** brain dead netcdfc++.  We really need to kill this library from w2 like in RAMP
    cppflags = "CPPFLAGS=-I"+t+"/include/"
    ldflags = "LDFLAGS=-L"+t+"/lib/"
    #os.environ["CPPFLAGS"] = "-I"+self.target+"/include/"
    b.run("./configure --prefix="+self.target+" "+cppflags+" " +ldflags +" --enable-shared --enable-cxx-4")
    b.run("make")
    b.run("make install")

class buildORPGINFR(BuildTar):
  """ Build orpginfr library """
  def build(self, t):
    b.chdir(self.key)
    b.run("./autogen.sh --prefix="+t+" --enable-shared")
    b.run("chmod a+x ./LinkLib008")
    b.run("make")
    b.run("make install")

class buildGDAL(BuildTar):
  """ Build gdal library """
  def build(self, t):
    b.chdir(self.key)
    #b.run("./autogen.sh --prefix="+self.target+" --enable-shared")
    c = "./configure --prefix="+t+" --without-mysql --without-python --with-jpeg=no --with-gif=no --without-ogr --with-geos=no --with-pg=no --with-pic --with-hdf5=no --with-ogr=no"
    c = c + " --with-libtiff=internal"    # Use internal?  RPM might be stock
    c = c + " --with-png="+t              # Use built one
    c = c + " --with-jasper="+t           # Use built one
    c = c + " --without-grib"             # conflict with g2clib
    b.run(c)
    b.run("make")
    b.run("make install")

class buildDualpol(BuildTar):
  """ Build base dualpol library """
  def build(self, t):
    b.chdir(self.key)
    b.run("./autogen.sh --prefix="+t+" ")
    b.run("make install")

class buildDualpolRRDD(BuildTar):
  """ Build dualpol RRDD library """
  def build(self, t):
    b.chdir(self.key)
    pathDualpol(self.target)
    cppflags = "CPPFLAGS=-I"+self.target+"/include/"
    ldflags = "LDFLAGS=-L"+self.target+"/lib/"
    #os.environ["CPPFLAGS"] = "-I"+self.target+"/include/"
    b.run("./autogen.sh --prefix="+self.target+" "+cppflags+" " +ldflags +" ")
    #b.run("./autogen.sh --prefix="+self.target+" ")
    b.run("make")
    b.run("make install")

class buildDualpolQPE(BuildTar):
  """ Build base dualpol QPE library """
  def build(self, t):
    b.chdir(self.key)
    pathDualpol(self.target)
    ldflags = "LDFLAGS=-L"+self.target+"/lib/"
    b.run("./autogen.sh --prefix="+self.target+" "+ldflags)
    b.run("make")
    b.run("make install")

def getBuilders(l, t):
  """ Get the builders from this module """
#  l.append(buildLIBPNG("libpng-1.6.28", t))

  # --------------------------------------------
  # Tree one: Needed for grib2 manipulation for
  # various reasons.
  l.append(buildJASPER("jasper-1.900.1", t))
  l.append(buildG2CLIB("g2clib-1.6.0", t)) # Require jasper

  # Projection libraries
  l.append(buildGCTPC("gctpc", t))
  l.append(buildProj4("proj-4.9.3", t))

  # Netcdf libraries
  l.append(buildNETCDF("netcdf-4.3.3.1", t))
  l.append(buildNETCDFPLUS("netcdf-cxx-4.2", t))

  # Grib2 tools (Requires: projection, netcdf, jasper and g2clib)
  l.append(buildWgrib2("wgrib2-2.0.6c", t)) # NOTE: make sure links to current gctpc in LDFLAGS

  # --------------------------------------------
  # Tree two: Units and other stuff, order here
  # shouldn't matter

  # Units and orpginfr stuff...
  l.append(buildUDUNITS("udunits-2.2.24", t))
  l.append(buildORPGINFR("orpginfr-3.0.1", t))

  # Finally Krause code we use
  l.append(buildDualpol("dualpol-04182017", t))
  l.append(buildDualpolQPE("dualpol-QPE-04182017", t))

  # MRMSHydro to MRMSSevere datatype linking library
  l.append(buildHMRGW2("hmrgw2_lib-05102017", t))

  # The monster at the end...
  # This is such a useful library, but it's a big one.
  l.append(buildGDAL("gdal-2.1.3", t))

def build(target):
  """ Build third party used by all packages """

  print("Building third party libraries: " +target) 
  blist = []
  getBuilders(blist, target)

  # Script base and source within it
  base = os.getcwd()
  b.chdir(base+"/third")

  # Third code build base
  #tbase = target+"/src/thirdb/" 
  tbase = target+"/"+THIRD 
  b.runOptional("mkdir -p "+tbase)

  # Copy all builders...
  for build in blist:
    build.copy(tbase)

  # Now change to target
  b.chdir(tbase)

  # Unzip all builders...
  for build in blist:
    build.unzip()
    b.chdir(tbase)

  # Build all builders...
  for build in blist:
    build.build(target)
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
