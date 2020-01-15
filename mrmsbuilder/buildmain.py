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
from .WG2 import WG2Build
from .WG2 import autoGUI2Check as autoGUI2Check

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
coff = "\033[0m"

MAJOR_VERSION = 1
MINOR_VERSION = 2

line = "------------------------------------------------"

def getTargetPaths():
  """ Return list of default paths for install """
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

  return[homePathDate, homePath, relativePathDate, relativePath]
  
def validateAvailablePath(aPath):
  """ Return true if path writable/changable and doesn't exist """
  good = True
  if os.path.exists(aPath):
    print("\n")
    print("Folder already exists, maybe a old or failed build.")
    print("Path: " +aPath)
    print("For build safety I won't build over it. Remove it and rerun script or change folder name.")
    print("\n")
    good = False
  else:
    try:
      os.makedirs(aPath)
    except:
      print("I couldn't create directory "+aPath)
      good = False

    # Try to access directory...
    if not os.access(aPath, os.W_OK):
      print("...but I can't _access_ "+aPath+". Permission settings?")
      good = False

  return good

def validatePath(aPath):
  """ Return true if path writable/changable """
  good = True
  # Try to create directory...
  if not os.path.exists(aPath):
    try:
      os.makedirs(aPath)
    except:
      print("I couldn't create directory "+aPath)
      good = False

  # Try to access directory...
  if not os.access(aPath, os.W_OK):
    print("...but I can't _access_ "+aPath+". Permission settings?")
    good = False

  return good

def getBuildFolder():
  """ Get the build folder """
  global theConf
  o = theConf.getString("TARGET", "", "")
  if o != "":
    theConf.addHistory("TARGET", "Target location", o)
    return o  

  [homePathDate, homePath, relativePathDate, relativePath] = getTargetPaths()

  myPrompts = [
               "Use Home Dated: " + green+homePathDate+coff,
               "Use Home: " + green+homePath+coff,
               "Use Relative Dated: " + green+relativePathDate+coff,
               "Use Relative: " + green+relativePath+coff,
              ]
  myOptions = ["1", "2", "3", "4"]
  mainPrompt = red+"Where"+coff+" would you like the build/work done? (You can type a path as well)"
            
  while True:
    good = True

    o = b.pickOption1(mainPrompt, myPrompts, myOptions, "1", False, True)
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

    good = validateAvailablePath(wanted)

    if good:
      theConf.addHistory("TARGET", "Target location", wanted)
      return wanted

def addBuilder(aList, aBuilder, aBuildItFlag):
  """ Convenience function for adding builder """
  if aBuildItFlag:
    #aBuilder.setBuild(aBuildItFlag)
    aList.append(aBuilder)
  return aBuilder

def doGetBuilders(theConf):
  """ Get the list of top builders we will build """
  bl = []
  buildThird = theConf.getBoolean("THIRDPARTY", "Build all third party packages?", "yes")
  buildWDSS2 = theConf.getBoolean("WDSS2", "Build WDSS2 packages?", "yes")
  buildHydro = theConf.getBoolean("HYDRO", "Build Hydro packages after WDSS2?", "yes")
  buildGUI2 = theConf.getBooleanAuto("GUI2", "Build the WG2 java display gui? (requires ant 1.9 and java)", "yes", autoGUI2Check)

  thirdparty = addBuilder(bl, ThirdPartyBuild(theConf), buildThird | buildWDSS2 | buildHydro)
  mrmssevere = addBuilder(bl, MRMSSevereBuild(), buildWDSS2 | buildHydro)
  mrmshydro = addBuilder(bl, MRMSHydroBuild(), buildHydro)
  wg2builder = addBuilder(bl, WG2Build(), buildGUI2)
  return bl

def doPreCheckoutConfig(aBuilderList, theConf):
  """ Configuration checks we can do before checking out code """
  req = True
  for bg in aBuilderList:
     bg.preCheckoutConfig(theConf)
     req = req & bg.checkRequirements()
  if req == False:
    print("Missing installed libraries or rpms to build, contact IT to install.")
    sys.exit(1)

def doPostCheckoutConfig(aBuilderList, theConf, target):
  """ Build everything wanted (order matters here) """
  for bg in aBuilderList:
     bg.postCheckoutConfig(theConf, target)

def doBuild(aBuilderList, target):
  """ Build everything wanted (order matters here) """
  for bg in aBuilderList:
     bg.build(target)

def doCheckRequirements(aBuilderList):
  """ Check local system for requirements for building """
  req = True
  for bg in aBuilderList:
     req = req & bg.checkRequirements()
  if req == False:
    print("Missing installed libraries or rpms to build, contact IT to install.")
    sys.exit(1)

def doCheckoutSVN(aFolder, scriptroot, aBuilderList):
  """ Checkout the code repository from SVN """

  # Do we require SVN credentials?
  needSVN = False
  for bg in aBuilderList:
    if bg.requireSVN():
      needSVN = True
      break
  password = ""
  revision = ""
  user = "."

  if needSVN:
    uprompt ="What "+red+"username"+coff+" for SVN? (Use . for anonymous checkout if you aren't going to commit code.)"
    user = theConf.getString("USERNAME", uprompt, getpass.getuser())
    b.setupSVN(user, False) # Change user now
    if user == ".":
      password = "" # anonymous shouldn't ask for password
    else:
      passPrompt = "To checkout I might need your "+green+"NSSL"+coff+" password (I'll keep it secret)"
      password = theConf.getPassword("PASSWORD", passPrompt, user)
    revision = theConf.getString("REVISION", "What SVN --revision so you want?", "HEAD")
    revision = "-r "+revision

  print(blue+"Checking out code..."+coff)
  for bg in aBuilderList:
    bg.checkout(aFolder, scriptroot, password, revision)
  print(blue+"Check out success."+coff)
  return [user, revision]

def doCheckoutGIT(checkmode, aFolder, scriptroot, aBuilderList):
  """ Checkout the code repository from GIT """
  gitcommand = "git clone "+checkmode+" MRMS-GIT"
  print(blue+"Checking out code from GIT... "+coff)
  print("GIT command:"+gitcommand)
  oldpwd = os.getcwd()
  b.chdir(aFolder+"/")
  b.run(gitcommand)
  b.chdir(aFolder+"/MRMS-GIT")
  #  Allow classes to move stuff where needed
  for bg in aBuilderList:
    bg.checkoutPostGIT(aFolder, scriptroot)
  # Hack subfolders into better location
  b.runOptional("mv ANC ../.")
  b.runOptional("mv FLASH ../.")
  b.runOptional("mv NCO_config ../.")
  b.runOptional("rm -rf "+aFolder+"/MRMS-GIT/util_3rd_party")
  # Leave other stuff for now (this will fail ok if anything left)
  b.runOptional("rmdir "+aFolder+"/MRMS-GIT")
  os.chdir(oldpwd)

  # Let non main build svn stuff still do custom checkouts, such as WG2
  print(blue+"Checking out other non-svn code..."+coff)
  for bg in aBuilderList:
    if not bg.requireSVN():
      bg.checkout(aFolder, scriptroot, "", "")
  print(blue+"Check out success."+coff)
  return ["none", ""]

def doCheckout(aFolder, scriptroot, aBuilderList):
  """ Checkout the code repository """

  # This is messy.  Either full checkout from a single git for MRMS, or
  # each of the SVNs
  repo ="Where are we checking MRMS code out from? SVN or give GIT origin url."
  checkmode = theConf.getString("CHECKFROM", repo, "SVN")
  if (checkmode == "SVN" or checkmode == "svn"):
    print("--->SVN checkout-----")
    return doCheckoutSVN(aFolder, scriptroot, aBuilderList)
  else:
    print("--->GIT checkout-----")
    return doCheckoutGIT(checkmode, aFolder, scriptroot, aBuilderList)

def doMarkFinishedBuild(aFolder):
  """ Mark file for a finished build """
  # Calculate stuff for version 
  dateraw = datetime.datetime.now();
  mydate = dateraw.strftime("%Y-%m-%d-%H-%M-%S-%f")
  machine = os.uname()
  redhat = b.getFirst(["cat","/etc/redhat-release"])
  envuser = getpass.getuser()
  good = validatePath(aFolder+"/bin/") # make sure directory exists.
  # Dump VERSION file to bin
  if good:
    aFile = open(aFolder+"/bin/VERSION", "w")
    aFile.write("MRMS built using the MRMS_builder python scripts.\n")
    aFile.write("\tDate completed: "+mydate+"\n")
    aFile.write("\tRun by user: "+envuser+"\n")
    aFile.write("\tRun on machine:\n\t  ")
    for x in machine:
      aFile.write(x+" ")
    aFile.write("\n")
    aFile.write("\tRedhat info:\n\t  "+redhat+"\n")
    aFile.write("Options:\n")
    theConf.printFileHistory(aFile)
    aFile.close()
    good = validatePath(aFolder+"/lib/") # make sure directory exists.
    if good:
      b.runOptional("cp "+aFolder+"/bin/VERSION "+aFolder+"/lib/VERSION")

def buildMRMS(scriptroot):
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

  # Gather all builders we we use for building MRMS
  package = theConf.getString("PACKAGE", "", "NONE")  # Don't prompt for it at moment if missing
  print(line)
  version = str(MAJOR_VERSION)+"."+str(MINOR_VERSION)
  print("Welcome to the "+green+"MRMS project builder V"+version+coff)
  print("Using config file: "+configFile+" "+red+confResult+coff)

  # This can prompt for individual builder options
  #wantAdvanced = theConf.getBoolean("ADVANCED", "Do you want to see advanced options and tools?", "no")

  # The source tar option just gathers stuff together
  if (package == "SOURCETAR"):
    print("I'm building a package for remote building (PACKAGE=SOURCETAR)\n")
    print(line)
    bl = doGetBuilders(theConf) # can prompt so don't pull above
    checkout = False
    remote = False

    folder = getBuildFolder()

    # FIXME: should probably share all date now functions globally to sync
    dateraw = datetime.datetime.now();
    mydate = dateraw.strftime("%Y%m%d-%H%M")
    name = "MRMSSource-"+mydate
    filename = name+".tar.gz"

    buildroot = name
    code = folder+"/"+buildroot+"/CODE" # or append better
    b.chdir(folder)
    b.run("mkdir -p "+buildroot+"/CODE")

    # Copy the build script itself into that folder...
    # Note: this must update if we add files to root script
    b.chdir(buildroot)
    b.run("cp "+scriptroot+"/build.py .");
    b.run("cp "+scriptroot+"/default.cfg .");
    b.run("cp -r "+scriptroot+"/mrmsbuilder .");

    # Try to remove package lines from the default.cfg replace with REMOTE
    # This means the PACKAGE line HAS to exist in the default.cfg..which 
    # could bug out if the config has been heavily modified.
    b.run("sed -i 's/^PACKAGE=.*/PACKAGE=REMOTE/g' default.cfg"); 

    # Fill in the source code directory with checkouts...
    #b.run("touch MRMSpackage.txt")

    # Checkout all code into 'CODE' directory.  This will be copied to build in
    # the REMOTE stage
    b.chdir(code)
    [user, revision] = doCheckout(code, scriptroot, bl)

    # Now at top level, compress it all
    b.chdir(folder)
    b.runOptional("rm -rf "+code+"/WDSS2/.svn") # Silly svn stuff is worthless on remote machine
    b.runOptional("rm -rf "+code+"/HMET/.svn")
    b.run("tar cvfz "+filename+" "+buildroot)
    b.run("rm -rf "+buildroot)

    print("Successfully Created "+blue+filename+coff+" in "+blue+"working directory "+coff+folder)
    print("Copy to remote machine, run "+blue+"tar cvfz "+filename+coff+", then run "+blue+"build.py"+coff+" inside that folder.\n")
    sys.exit(0)
  elif (package == "REMOTE"):
    print("I'm building from a previous created tar package (PACKAGE=REMOTE)\n")
    print(line)
    bl = doGetBuilders(theConf) # can prompt so don't pull above
    checkout = False
    remote = True
  else:
    print(line)
    print("Hi, "+blue+user+coff+", I'm your hopefully helpful builder.")
    print("Modify default.cfg and/or answer questions below:\n")
    bl = doGetBuilders(theConf) # can prompt so don't pull above
    remote = False
    checkout = theConf.getBoolean("CHECKOUT", "Checkout all code from SVN repository?", "yes")
    
  #####################################################
  # BUILD HERE (Could be a function called.  REMOTE and regular build fall through here)

  # Handle configuration options for each builder that can be handled
  # before checkout.  Since checkout is long, we want to break as quick
  # as we can to save user time.
  doPreCheckoutConfig(bl, theConf)

  # Folder wanted for building in
  folder = getBuildFolder()

  # User/password for SVN and checkout
  if checkout:
    [user, revision] = doCheckout(folder, scriptroot, bl)
  if remote:
    # Copy from our builder to destination location
    b.chdir(scriptroot)
    b.run("cp -r CODE/* "+folder)

  # Anything post checkout (for example, WDSSII needs checkout in order
  # to use the stock keys for configuration
  doPostCheckoutConfig(bl, theConf, folder)

  # Build everything wanted (order matters here)
  doBuild(bl, folder)

  # Global mark build and finish
  doMarkFinishedBuild(folder)
  theConf.printHistory()
  b.setupSVN(user, True)

if __name__ == "__main__":
  print("Run the ./build.py script to execute")
