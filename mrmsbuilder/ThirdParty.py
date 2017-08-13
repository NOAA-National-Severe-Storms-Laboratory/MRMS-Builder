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
    print("******Setting path dualpol")
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
    print("Not setting path dualpol")

class BuildThird(Builder):
  """ build a third party from compressed source and stock configure """
  def clean(self):
    b.runOptional("rm -rf "+self.key)
  #def build(self, t, c, m): This is too confusing at moment
  #  b.chdir(self.key)
  #  r = self.autogen("./configure", t)
  #  b.run(r)
  #  self.makeInstall(m)

class BuildTar(BuildThird):
  """ build a third party from a stock tar.gz """
  def copy(self, t):
    b.run("cp "+self.key+".tar.gz "+t)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")

class BuildZip(BuildThird):
  """ build a third party from a stock zip """
  def copy(self, t):
    b.run("cp "+self.key+".zip "+t)
  def unzip(self):
    b.run("unzip "+self.key+".zip")

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
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    b.run(r)
    self.makeInstall(m)

class buildZLIB(BuildTar):
  """ Build ZLIB library """
  def cppFlags(self, target):
    """ CPPFLAGS doesn't work with configure with zlib """
    return ""
  def ldFlags(self, target):
    """ LDFLAGS doesn't work with configure zlib """
    return ""
  def build(self, t, c, m):
    """ Build ZLIB """
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    b.run(r)
    self.makeInstall(m)

class buildCURL(BuildTar):
  """ Build CURL library """
  def build(self, t, c, m):
    b.chdir(self.key)
    #r = self.autogen("./configure", t)
    #r = self.autogen("./configure", t)
    r = "./configure --prefix="+t+" --with-zlib="+t
    b.run(r)
    self.makeInstall(m)

class buildWgrib2(BuildTar):
  """ Build Wgrib2 grib2 manipulation tool and library for hydro """
  def build(self, t, c, m):
    b.chdir(self.key)
    os.environ["CPPFLAGS"] = self.localInclude(t)
    os.environ["LDFLAGS"] = self.localLink(t)+" -lnetcdf -lg2c_v1.6.0 -lm -ljasper -lpng -lproj -lgeo"
    b.run("make")
    b.run("cp wgrib2 "+t+"/bin/wgrib2")
    b.runOptional("mkdir "+t+"/include/wgrib2/")
    b.run("cp *.h "+t+"/include/wgrib2/.")
    os.environ["CPPFLAGS"] = ""
    os.environ["LDFLAGS"] = ""

class buildJASPER(BuildZip):
  """ Build Jasper library """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    r = r + " --bindir="+t+"/bin/JASPER"
    b.run(r)
    self.makeInstall(m)

class buildLIBPNG(BuildTar):
  """ Build libpng library """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    b.run(r)
    self.makeInstall(m)

class buildHMRGW2(BuildTar):
  """ Build HMRGW2 library to link hydro and w2 """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./autogen.sh", t)
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
  def checkRequirements(self):
    # UDUNITS2 wants the expat-devel XML library
    req = True
    req = req & b.checkRPM("expat-devel")
    return req
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    # Only one binary in here, lol
    #r = r + " --bindir="+t+"/bin/UDUNITS"
    b.run(r)
    self.makeInstall(m)

class buildHDF5(BuildTar):
  """ Build HDF5 library """
  def build(self, t, c, makeFlags):
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    r = r + " --bindir="+t+"/bin/HDF5"
    b.run(r)
    self.makeInstall(makeFlags)

class buildNETCDF(BuildTar):
  """ Build netcdf library """
  def build(self, t, c, m):
    """ Build netcdf library """
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    #r = r + " --bindir="+t+"/bin/NETCDF"  # See below too
    b.run(r)
    self.makeInstall(m)
    # If we put NETCDF into own folder, put a link to ncdump in bin
    #b.runOptional("ln -s "+t+"/NETCDF/ncdump "+t+"/bin/ncdump")

class buildNETCDFPLUS(BuildTar):
  """ Build netcdf c++ library """
  def build(self, t, c, m):
    """ Build netcdf library """
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    #r = r + " --bindir="+t+"/bin/NETCDF"
    r = r + " --enable-cxx-4"
    b.run(r)
    self.makeInstall(m)

class buildORPGINFR(BuildTar):
  """ Build orpginfr library """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./autogen.sh", t)
    b.run(r)
    b.run("chmod a+x ./LinkLib008")
    self.makeInstall(m)

class buildGDAL(BuildTar):
  """ Build gdal library """
  def build(self, t, c, m):
    b.chdir(self.key)
    r = self.autogen("./configure", t)
    r = r + " --bindir="+t+"/bin/GDAL"  # See below
    r = r + " --without-mysql --without-python --with-jpeg=no --with-gif=no --without-ogr --with-geos=no --with-pg=no --with-pic --with-ogr=no"
    r = r + " --with-libtiff=internal"    # Use internal?  RPM might be stock
    r = r + " --with-png="+t              # Use built one
    r = r + " --with-jasper="+t           # Use built one
    r = r + " --with-curl="+t             # Use built one
    r = r + " --with-hdf5="+t             # Use built one
    r = r + " --with-netcdf="+t           # Use built one
    r = r + " --without-grib"             # conflict with g2clib (Which grib2 reader is better, the library or gdal's?)
    r = r + " --with-sqlite3=no"          # Disable snagging it 
    b.run(r)
    self.makeInstall(m)
    # M4 has to find gdal-config...
    # The 'test' does GDAL_CFLAGS and GDAL_LIBS from bin/gdal-config.  Wondering if we should do it here
    # instead of m4...
    b.runOptional("ln -s "+t+"/bin/GDAL/gdal-config "+t+"/bin/gdal-config") # M4 has to find gdal-config

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

    # HDF/Netcdf requires zlib and curl (redhat five fails horribly without this)
    l.append(buildZLIB("zlib-1.2.11"))  # For Netcdf4
    l.append(buildCURL("curl-7.55.0"))  # For Netcdf4

    # Projection libraries
    l.append(buildGCTPC("gctpc")) 
    l.append(buildProj4("proj-4.9.3"))

    # Netcdf libraries
    l.append(buildHDF5("hdf5-1.8.12"))
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

    print("Finished third party...");

# Run main
if __name__ == "__main__":
  print("Run the main build script...")
