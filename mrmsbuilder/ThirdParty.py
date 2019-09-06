#!/usr/bin/env python

# Robert Toomey March 2017
# Build from compressed sources.
# This is used to build a third party source directory

# System imports
import os,sys

# Relative imports
from . import buildtools as b
from .builder import Builder
from .builder import BuilderGroup

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
  #def build(self, target): This is too confusing at moment
  #  b.chdir(self.key)
  #  r = self.autogen("./configure", target)
  #  b.run(r)
  #  self.makeInstall()

class BuildTar(BuildThird):
  """ build a third party from a stock tar.gz """
  def copy(self, target):
    b.run("cp "+self.key+".tar.gz "+target)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar.gz")

class BuildZip(BuildThird):
  """ build a third party from a stock zip """
  def copy(self, target):
    b.run("cp "+self.key+".zip "+target)
  def unzip(self):
    b.run("unzip "+self.key+".zip")

class buildGCTPC(BuildTar):
  """ Build ancient GCTPC projection library """
  def build(self, target):
    b.chdir(self.key)
    b.chdir("source")
    b.run("make")
    b.run("cp libgeo.a "+target+"/lib/libgeo.a")
    b.run("cp *.h "+target+"/include/.")

class buildProj4(BuildTar):
  """ Build proj4 library """
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    b.run(r)
    self.makeInstall()

class buildZLIB(BuildTar):
  """ Build ZLIB library """
  def cppFlags(self, target):
    """ CPPFLAGS doesn't work with configure with zlib """
    return ""
  def ldFlags(self, target):
    """ LDFLAGS doesn't work with configure zlib """
    return ""
  def build(self, target):
    """ Build ZLIB """
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    b.run(r)
    self.makeInstall()

class buildCURL(BuildTar):
  """ Build CURL library """
  def build(self, target):
    b.chdir(self.key)
    #r = self.autogen("./configure", t)
    #r = self.autogen("./configure", t)
    r = "./configure --prefix="+target+" --with-zlib="+target
    b.run(r)
    self.makeInstall()

class buildWgrib2(BuildTar):
  """ Build Wgrib2 grib2 manipulation tool and library for hydro """
  def build(self, target):
    b.chdir(self.key)
    cpp = self.localInclude(target)
    ldd = self.localLink(target)+" -lnetcdf -lgrib2c -lm -ljasper -lpng -lproj -lgeo"
    cp = "cp wgrib2 "+target+"/bin/wgrib2"
    mk = "mkdir -p "+target+"/include/wgrib2/" # p to avoid err on exist
    cp2 = "cp *.h "+target+"/include/wgrib2/."
    cp3 = "cp libwgrib2.a "+target+"/lib/."

    # Save a rebuild script of what we do here...
    # Could maybe make a function to clean up this
    rerun = open("rebuild.sh", "w")
    rerun.write("export CPPFLAGS=\""+cpp+"\"\n") #1
    rerun.write("export LDFLAGS=\""+ldd+"\"\n")
    rerun.write("make\n") # 2
    rerun.write("make lib\n") # 2.5
    rerun.write(cp+"\n") # 3
    rerun.write(mk+"\n") # 4
    rerun.write(cp2+"\n") # 5
    rerun.write(cp3+"\n") # 6
    rerun.close()
    b.runOptional("chmod a+x rebuild.sh")

    # Run actual commands
    os.environ["CPPFLAGS"] = cpp #1
    os.environ["LDFLAGS"] = ldd
    b.run("make") # 2
    b.run("make lib") # 2.5
    b.run(cp) #3
    b.runOptional(mk) #4
    b.run(cp2) #5
    b.run(cp3) #6
    os.environ["CPPFLAGS"] = ""
    os.environ["LDFLAGS"] = ""

class buildJASPER(BuildZip):
  """ Build Jasper library """
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    r = r + " --bindir="+target+"/bin/JASPER"
    self.runBuildSetup(r)
    self.makeInstall()

class buildLIBPNG(BuildTar):
  """ Build libpng library """
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    self.runBuildSetup(r)
    self.makeInstall()

class buildHMRGW2(BuildTar):
  """ Build HMRGW2 library to link hydro and w2 """
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./autogen.sh", target)
    self.runBuildSetup(r)
    self.makeInstall()

class buildG2CLIB(BuildThird):
  """ Build g2clib library """
  def copy(self, target):
    b.run("cp "+self.key+".tar "+target)
  def unzip(self):
    b.run("tar xvf "+self.key+".tar")
  def build(self, target):
    b.chdir(self.key)
    # make sure we link to jasper here correctly
    os.environ["CPPFLAGS"] = self.localInclude(target)
    os.environ["LDFLAGS"] = self.localLink(target)+" -ljasper "
    # Brain dead g2lib doesn't have a configure.  Seriously?
    # Move the original makefile and make a new one using it...
    b.run("mv makefile makefileBASE")
    nmake = open("makefile", 'w')
    nmake.write("# Robert Toomey.  Override g2clib make for our own purposes.\n")
    nmake.write("include makefileBASE\n")
    nmake.write("INC=-I"+target+"/include\n")
    #nmake.write("CFLAGS= -O3 -g -m64 $(INC) $(DEFS) -D__64BIT__\n")
    nmake.write("CFLAGS= -fPIC -O3 -g -m64 $(INC) $(DEFS)\n")
    nmake.close()
    b.run("make")
    b.run("cp libg2c_v1.6.0.a "+target+"/lib/libgrib2c.a")
    b.run("cp *.h "+target+"/include")
    os.environ["CPPFLAGS"] = ""
    os.environ["LDFLAGS"] = ""

def netcdfCheck():
  """ Check for netcdf stuff... """
  good = True

  
class buildUDUNITS(BuildTar):
  """ Build udunits library """
  def checkRequirements(self):
    req = True
    # Test 1: Check expat-devel XML library UDUNITS2 wants the expat-devel XML library
    if not b.checkFirstText("UDUNITS",["rpm", "-qi", "expat-devel"], "Name"):
      req = False
    return req
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    # Only one binary in here, lol
    #r = r + " --bindir="+t+"/bin/UDUNITS"
    self.runBuildSetup(r)
    self.makeInstall()

class buildHDF5(BuildTar):
  """ Kill HDF5 warnings hack """
  def HDF5KillWarnings(self):
    # Hack: hdf5 has a crazy amount of warnings.  Sure it's good to turn it all on, but only
    # if your coders actually fix it.  We don't care about warnings with third party, out of
    # our control..so turn them all off.
    # FIXME: Is there an easier way to turn this off..hdf5 has some confusing scripts for configuring.

    replaceIt = "-Wall -Wextra -Wundef -Wshadow -Wpointer-arith -Wbad-function-cast -Wcast-qual -Wcast-align -Wwrite-strings -Wconversion -Waggregate-return -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -Wredundant-decls -Wnested-externs -Winline -Wfloat-equal -Wmissing-format-attribute -Wmissing-noreturn -Wpacked -Wdisabled-optimization -Wformat=2 -Wunreachable-code -Wendif-labels -Wdeclaration-after-statement -Wold-style-definition -Winvalid-pch -Wvariadic-macros -Winit-self -Wmissing-include-dirs -Wswitch-default -Wswitch-enum -Wunused-macros -Wunsafe-loop-optimizations -Wc++-compat -Wstrict-overflow -Wlogical-op -Wlarger-than=2048 -Wvla -Wsync-nand -Wframe-larger-than=16384 -Wpacked-bitfield-compat -Wstrict-overflow=5 -Wjump-misses-init -Wunsuffixed-float-constants -Wdouble-promotion -Wsuggest-attribute=const -Wtrampolines -Wstack-usage=8192 -Wvector-operation-performance -Wsuggest-attribute=pure -Wsuggest-attribute=noreturn -Wsuggest-attribute=format"
    #r = "sed -i 's/"+replaceIt+"/-w/' Makefile" 
    rbase = "sed -i 's/"+replaceIt+"/-w/' " 

    # Find each Makefile from top of tree..
    base = os.getcwd()
    matches = []
    for root, dirnames, filenames in os.walk(base):
      for filename in filenames:
        if filename.endswith("Makefile"):
          matches.append(os.path.join(root, filename))

    # Replace massive g++ warning string in every makefile
    # Note: Maybe we can replace it before makefile
    for i in matches:
      r = rbase+i
      b.run(r)
    
  """ Build HDF5 library """
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    r = r + " --bindir="+target+"/bin/HDF5"
    self.runBuildSetup(r)
    self.HDF5KillWarnings()
    self.makeInstall()

class buildNETCDF(BuildTar):
  """ Build netcdf library """
  def build(self, target):
    """ Build netcdf library """
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    #r = r + " --bindir="+t+"/bin/NETCDF"  # See below too
    """ Make sure the base netcdf library has netcdf4 support built in. """
    r = r + " --enable-netcdf-4"
    self.runBuildSetup(r)
    # Hack: Turn off --jobs flags for netcdf build..it currently has a race condition
    # in it's build (bug in 4.6.1 at least).  Downside is we build slower
    self.setMakeFlags("")
    self.makeInstall()
    # If we put NETCDF into own folder, put a link to ncdump in bin
    #b.runOptional("ln -s "+t+"/NETCDF/ncdump "+t+"/bin/ncdump")

class buildNETCDFPLUS(BuildTar):
  """ Build netcdf c++ library """
  def build(self, target):
    """ Build netcdf library """
    """ Add special flag to get netcdf4 support. """
    self.cppflags += "-DUSE_NETCDF4"
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    #r = r + " --bindir="+t+"/bin/NETCDF"
    self.runBuildSetup(r)
    self.makeInstall()

class buildORPGINFR(BuildTar):
  """ Build orpginfr library """
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./autogen.sh", target)
    self.runBuildSetup(r)
    b.run("chmod a+x ./LinkLib008")
    self.makeInstall()

class buildGDAL(BuildTar):
  """ GDAL requirements """
  def checkRequirements(self):
    req = True
    #
    # FIXME JWB - I don't think we need this. Keep until verified.
    # FIXME JWB - far as I can tell, the xml2 stuff is not used.
    #
    # Test 1: Check expat-devel XML library UDUNITS2 wants the expat-devel XML library
    #if not b.checkFirstText("GDAL",["rpm", "-qi", "libxml2-devel"], "Name"):
    #  req = False

    # Test 2: Check xml2-config from libxml2 is in the normal path location.
    # On redhat 7 libxml2 sticks it in /bin/ as well...bleh make up mind people.
    # Probably should do a rpm list on libxml2 and compare that way to be 100% sure
    #good = b.checkFirst("GDAL",["which", "xml2-config"], "/usr/bin/xml2-config")
    #good |= b.checkFirst("GDAL",["which", "xml2-config"], "/bin/xml2-config")

    #if not good:
    #  b.checkError("GDAL", ["which", "xml2-config"], "/usr/bin/xml2-config or /bin/xml2-config");
    #  print("    Note: custom LDM installs can add to PATH which conflicts with GDAL");
    #  req = False
    return req

  """ Build gdal library """
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./configure", target)
    r = r + " --bindir="+target+"/bin/GDAL"  # See below
    r = r + " --without-mysql --without-python --with-jpeg=no --with-gif=no --without-ogr --with-geos=no --with-pg=no --with-pic --with-ogr=no"
    r = r + " --with-libtiff=internal"    # Use internal?  RPM might be stock
    r = r + " --with-png="+target         # Use built one
    r = r + " --with-jasper="+target      # Use built one
    r = r + " --with-curl="+target        # Use built one
    r = r + " --with-hdf5="+target        # Use built one
    r = r + " --with-netcdf="+target      # Use built one
    r = r + " --without-grib"             # conflict with g2clib (Which grib2 reader is better, the library or gdal's?)
    r = r + " --without-xml2"             # avoid conflicts - we don't need it
    r = r + " --with-sqlite3=no"          # Disable snagging it 
    self.runBuildSetup(r)
    self.makeInstall()
    # M4 has to find gdal-config...
    # The 'test' does GDAL_CFLAGS and GDAL_LIBS from bin/gdal-config.  Wondering if we should do it here
    # instead of m4...
    b.runOptional("ln -s "+target+"/bin/GDAL/gdal-config "+target+"/bin/gdal-config") # M4 has to find gdal-config

class buildDualpol(BuildTar):
  """ Build base dualpol library """
  def build(self, target):
    b.chdir(self.key)
    r = self.autogen("./autogen.sh", target)
    self.runBuildSetup(r)
    self.makeInstall()

class buildDualpolRRDD(BuildTar):
  """ Build dualpol RRDD library """
  def build(self, target):
    b.chdir(self.key)
    pathDualpol(target)
    r = self.autogen("./autogen.sh", target)
    self.runBuildSetup(r)
    self.makeInstall()

class buildDualpolQPE(BuildTar):
  """ Build base dualpol QPE library """
  def build(self, target):
    b.chdir(self.key)
    pathDualpol(target)
    r = self.autogen("./autogen.sh", target)
    self.runBuildSetup(r)
    self.makeInstall()

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
    #l.append(buildNETCDF("netcdf-4.3.3.1"))
    l.append(buildNETCDF("netcdf-c-4.6.1"))
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
    l.append(buildDualpol("dualpol-08152017"))
    l.append(buildDualpolQPE("dualpol-QPE-09122017"))

    # MRMSHydro to MRMSSevere datatype linking library
    l.append(buildHMRGW2("hmrgw2_lib-05102017"))

    # The monster at the end...
    # This is such a useful library, but it's a big one.
    l.append(buildGDAL("gdal-2.1.3"))
    self.myBuilders = l

  def checkout(self, target, scriptroot, password, options):
    """ Checkout for third consists of copying from builder to final """
    base = os.getcwd()

    # Input directory is our builder's third subfolder...
    ibase = scriptroot+"/third"
    b.chdir(ibase)

    # Output directory for uncompress is THIRD within the checkout location
    tbase = target+"/"+THIRD 
    b.runOptional("mkdir -p "+tbase)
    for build in self.myBuilders:
      build.copy(tbase)

    b.chdir(base)

  def build(self, target):
    """ Build third party used by all packages """

    print("Building third party libraries: " +target) 

    # Script base and source within it
#    base = os.getcwd()
#    b.chdir(base+"/third")

    # Third code build base
    #tbase = target+"/src/thirdb/" 
#    tbase = target+"/"+THIRD 
#    b.runOptional("mkdir -p "+tbase)

    # Copy all builders...
#    for build in self.myBuilders:
#      build.copy(tbase)

    # Now change to target
    tbase = target+"/"+THIRD 
    b.chdir(tbase)

    # Unzip all builders...
    for build in self.myBuilders:
      build.unzip()
      b.chdir(tbase)

    # Build all builders...
    for build in self.myBuilders:
      build.build(target)
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
