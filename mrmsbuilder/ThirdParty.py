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

class BuildThirdZip(Builder):
  """ build a third party zip """
  def clean(self):
    b.runOptional("rm -rf "+self.key)

class buildJASPER(BuildThirdZip):
  """ Build Jasper library """
  def copy(self, t):
    b.run("cp "+self.key+".zip "+t)
  def unzip(self):
    b.run("unzip "+self.key+".zip")
  def build(self, t):
    b.chdir(self.key)
    b.run("./configure --prefix="+t+" --enable-shared")
    b.run("make")
    b.run("make install")

class buildLIBPNG(BuildThirdZip):
  """ Build libpng library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
  def build(self, t):
    b.chdir(self.key)
    b.run("./configure --prefix="+t+" --enable-shared")
    b.run("make")
    b.run("make install")

class buildHMRGW2(BuildThirdZip):
  """ Build HMRGW2 library to link hydro and w2 """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
  def build(self, t):
    b.chdir(self.key)
    b.run("./autogen.sh --prefix="+t+" --enable-shared")
    b.run("make")
    b.run("make install")

class buildG2CLIB(BuildThirdZip):
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

class buildUDUNITS(BuildThirdZip):
  """ Build udunits library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
  def build(self, t):
    b.chdir(self.key)
    b.run("./configure --prefix="+t+" --enable-shared")
    b.run("make")
    b.run("make install")

class buildNETCDF(BuildThirdZip):
  """ Build netcdf library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
  def build(self, t):
    b.chdir(self.key)
    b.run("./configure --prefix="+t+" --enable-shared")
    b.run("make")
    b.run("make install")

class buildNETCDFPLUS(BuildThirdZip):
  """ Build netcdf c++ library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
  def build(self, t):
    b.chdir(self.key)
    # f***** brain dead netcdfc++.  We really need to kill this library from w2 like in RAMP
    cppflags = "CPPFLAGS=-I"+t+"/include/"
    ldflags = "LDFLAGS=-L"+t+"/lib/"
    #os.environ["CPPFLAGS"] = "-I"+self.target+"/include/"
    b.run("./configure --prefix="+self.target+" "+cppflags+" " +ldflags +" --enable-shared --enable-cxx-4")
    b.run("make")
    b.run("make install")

class buildORPGINFR(BuildThirdZip):
  """ Build orpginfr library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
  def build(self, t):
    b.chdir(self.key)
    b.run("./autogen.sh --prefix="+t+" --enable-shared")
    b.run("chmod a+x ./LinkLib008")
    b.run("make")
    b.run("make install")

class buildGDAL(BuildThirdZip):
  """ Build gdal library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
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

class buildDualpol(BuildThirdZip):
  """ Build base dualpol library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
  def build(self, t):
    b.chdir(self.key)
    b.run("./autogen.sh --prefix="+t+" ")
    b.run("make install")

class buildDualpolRRDD(BuildThirdZip):
  """ Build dualpol RRDD library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
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

class buildDualpolQPE(BuildThirdZip):
  """ Build base dualpol QPE library """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")
  def build(self, t):
    b.chdir(self.key)
    pathDualpol(self.target)
    ldflags = "LDFLAGS=-L"+self.target+"/lib/"
    b.run("./autogen.sh --prefix="+self.target+" "+ldflags)
    b.run("make")
    b.run("make install")

def getBuilders(l, t):
  """ Get the builders from this module """
  l.append(buildJASPER("jasper-1.900.1", t))
#  l.append(buildLIBPNG("libpng-1.6.28", t))
  l.append(buildG2CLIB("g2clib-1.6.0", t))
  l.append(buildUDUNITS("udunits-2.2.24", t))
  l.append(buildORPGINFR("orpginfr-3.0.1", t))

  l.append(buildDualpol("dualpol-04182017", t))
  l.append(buildDualpolQPE("dualpol-QPE-04182017", t))

  # Newest at the moment
  #myBuilders.append(buildNETCDF("netcdf-4.4.1.1", t))
  #myBuilders.append(buildNETCDFPLUS("netcdf-cxx4-4.3.0", t))
  l.append(buildNETCDF("netcdf-4.3.3.1", t))
  l.append(buildNETCDFPLUS("netcdf-cxx-4.2", t))
  l.append(buildHMRGW2("hmrgw2_lib-05102017", t))

  # The monster at the end...
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
