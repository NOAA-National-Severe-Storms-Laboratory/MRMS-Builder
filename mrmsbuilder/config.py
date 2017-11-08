#!/usr/bin/env python

# Robert Toomey July 2017
# 
# Utility library class for reading pair values from a
# configuration file

# System imports
import getpass,os,sys,readline,multiprocessing
from datetime import timedelta # Time for expire function
from datetime import datetime

# Relative imports
from . import filecompleter
from . import buildtools as b

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
coff = "\033[0m"
line = "------------------------------------------------"

class Configuration:
  """ Configuration options """

  def __init__(self):
    self.map1 = {}
    self.map2 = {}
    self.history = {}

  def cleanText(self, line):
     """ Clean text line from config file """
     l2 = line.rstrip('\n')   # Remove new lines
     l2 = l2.rstrip(' ')      # Remove end spaces
     l2 = l2.split("#", 1)[0] # Remove stuff post '#'
     return l2

  def readSplitFile(self, configFile, delimiter):
     """ Read a configuration file with 'pairs' separated by delimiter, return map of values """
     map1= {}
     try:
       print("Reading file "+configFile)
       with open(configFile, "r") as f:
         for line in f:
           l2 = self.cleanText(line)

           # If anything left of line...
           if l2 != "":
             pair = l2.split(delimiter)     # Get name=value pair if any
             if (len(pair) == 2):
               pair[0] = self.cleanText(pair[0])
               pair[1] = self.cleanText(pair[1])
             map1[pair[0]] = pair[1]
     except Exception as e:  # python 2.7 up
       error = "Couldn't read file "+configFile+"\nReason:"+str(e)
       return error
     return map1
 
  def readConfig(self, configFile):
     """ Read a configuration file, return map of values """
     self.map1 = self.readSplitFile(configFile, "=")
     return ""

  def readConfig2(self, configFile):
     """ Read Lak's configuration file, return map of values """
     self.map2 = self.readSplitFile(configFile, " ")
     return ""

  def addHistory(self, key, prompt, value):
    """ Add a line to the history """
    self.history[key] = [prompt, value]
     
  def printHistory(self):
    """ Print out history of options chosen """
    print(line)
    print("Final settings:")
    for l in self.history:
      data = self.history[l]
      prompt = data[0]
      value = data[1]
      if value == False:
       value = red+str(value)+coff
      else:
       value = green+str(value)+coff
      #print(l+" "+prompt +" --> "+value)
      print(l+" --> "+value)
      #print(l)
    print(line)

  def printConfig(self):
    """ Print out configuration """
    print (self.map1)

  def setAutoFileComplete(self, flag):
    """ Turn on/off tabbed auto folder completion in input """
    if flag == True:
      comp = filecompleter.Completer()
      readline.set_completer_delims(' \t\n;')
      readline.parse_and_bind("tab: complete")
      readline.set_completer(comp.complete)
    else:
      readline.set_completer_delims('')
      readline.parse_and_bind("")
      readline.set_completer(None)

  def printPrompt(self, key, prompt):
    """ Print prompt for a given key variable """
    print("'"+key+"' "+prompt)
   
  def promptFileDir(self, key, prompt, default_value):
    """ Prompt for a file or directory with autocomplete """
    # Make the default option the true/false given
    o = default_value

    # Loop until good option
    self.setAutoFileComplete(True)
    print(line)
    while True:

      # Print prompt
      self.printPrompt(key,prompt)

      # Get input
      newo = b.getInput(o)

      # Finish if valid input
      # FIXME: test existance of dir/file?  
      validDirFile = True
       
      if validDirFile:
        self.setAutoFileComplete(False)
        return newo

  def getFileDir(self, key, prompt, default_value):
    """ Get a file or dirname from configuration """
    # FIXME: duplicates a lot from getString (merge common code)
    v = ""
    s = self.map1.get(key, "")
    if s != "":
      v = s
    else:
     ### Not in configureation file, so prompt for it...
     if prompt == "":
       return default_value
     else:
       #v = self.promptString(prompt, default_value)
       v = self.promptFileDir(key, prompt, default_value)

    self.addHistory(key, prompt, v)
    return v

  def promptString(self, key, prompt, defOption):
    """ Prompt for a string """
    # Make the default option the true/false given
    o = defOption

    # Loop until good option
    self.setAutoFileComplete(False)
    print(line)
    while True:

      # Print prompt
      self.printPrompt(key,prompt)

      # Get input
      newo = b.getInput(o)

      # Finish if valid input
      return newo

  def getString(self, key, prompt, default_value):
    """ Get a string from configuration """
    v = ""
    s = self.map1.get(key, "")
    if s != "":
      v = s
    else:
     ### Not in configureation file, so prompt for it...
     if prompt == "":
       #return default_value
       v = default_value
     else:
       v = self.promptString(key, prompt, default_value)

    self.addHistory(key, prompt, v)
    return v

  def getPassword(self, key, prompt, user):
    """ Get a password string """
    o = self.getString(key, "", "")
    if o == "":
      print(line)
      print("To checkout I might need your "+green+"NSSL"+coff+" password (I'll keep it secret)")
      o = getpass.getpass(green+user+" Password:"+coff)
      self.addHistory(key, prompt, "{User entered}")
    else:
      self.addHistory(key, prompt, "{From configuration}")
    return o

  def promptBoolean(self, key, prompt, default_value):
    """ Prompt for a boolean value """
    # Make the default option the true/false given
    o = default_value

    # Loop until good option
    self.setAutoFileComplete(False)
    print(line)
    while True:

      # Print prompt
      self.printPrompt(key,prompt)

      # Get input
      newo = b.getInput(o)

      # Finish if valid input
      newo = newo.lower()
      if newo in ["yes","y","true"]:
        return True
      elif newo in ["no","n","false"]:
        return False

  def getBoolean(self, key, prompt, default_option):
    """ Get a boolean value from configuration """
    v = False
    s = self.map1.get(key, "")
    s = s.lower()
    if s == "yes":
      v = True
    elif s == "no":
      v = False
    elif s == "true":
      v = True
    elif s == "false":
      v = False
    elif s == "y":
      v = True
    elif s == "n":
      v = False
    else:
      ### Not in configuration file, so prompt for it...
      if prompt == "":
        return default_value
      else:
        v = self.promptBoolean(key, prompt, default_option)
  
    self.addHistory(key, prompt, v)
    return v

  def getBooleanAuto(self, key, prompt, default_option, checkRequirements):
    """ Get a boolean value from configuration with a auto check function """
    s = self.map1.get(key, "")
    s = s.lower()
    if s == "auto":
      flag = checkRequirements()
      self.addHistory(key, prompt+" (auto checking)", flag)
      return flag
    else:
      return self.getBoolean(key, prompt, default_option)
   

########################################################################
# Non 'regular configuration' file stuff.  Could be a subclass...

  def getJobs(self):
    """ Get job flag for all makes """
    o = self.getString("JOBS", "", "CPU")
    if ((o == "CPU") or (o == "")):
      o =str(multiprocessing.cpu_count())
    self.addHistory("JOBS", "Number of make jobs for build?", o)
    return o

  def getOurDFlags(self):
    """ Get expire data from configuration file """
    # Current expire is only allowed D flag?
    aMap = {}
    v = self.getString("EXPIRE", "", "")
    dateformat = "%Y-%m-%d" # 2017-Aug-18
    good = False
   
    # SUNRISE or now...
    #nowtime = datetime.utcnow()
    # Strange to match date +%s has to be now time not utcnow
    # +%s is seconds from utc 1970...is python %s not correct?
    nowtime = datetime.now() 
    #print("NOW is "+str(nowtime))
    #thestart = "-DWDSSII_SUNRISE="+nowtime.strftime("%s")
    aMap["WDSSII_SUNRISE"] = nowtime.strftime("%s")
    #final = thestart

    # Check for empty string, which means don't expire
    if good == False:
      if v == "":
        return aMap
        #return final # no expire time

    # Check for seconds as integer
    if good == False:
      try: # to get an integer
        seconds = int(v)
        thentime = nowtime+timedelta(seconds=seconds)
        #print("EXPIRING build in "+str(seconds)+" seconds...")
        good = True 
      except Exception as e:  # python 2.7 up
        pass  # Don't print first error

    # Check for full exact date given
    if good == False:
      try: # to get a date string
        thentime = datetime.strptime(v, dateformat)  # 2017-Aug-18
        # Check if date in future by at least a week:
        if (thentime-nowtime < timedelta(seconds=604800)):
          print("EXPIRE set to a date less than a week in future...")
          sys.exit()
        good = True
      except Exception as e:  # python 2.7 up
        print("Couldn't convert EXPIRE to number or date, date format is "+dateformat)
        print("exception was: "+str(e))
        sys.exit() # Do we recover?  This is probably error in config file

    if good == True:
      #final +=  " -DWDSSII_SUNSET="+thentime.strftime("%s")
      #final +=  " -DWDSSII_SUNSET="+thentime.strftime("%s")
      aMap["WDSSII_SUNSET"] = thentime.strftime("%s")
    return aMap  # Map of name to value
    #return final

  def getAuthFileDItems(self, default_path):
    """ Get auth key flags from Lak's space paired configuration file """
    v = self.getString("KEYFILE", "", "")
    if v == "WDSS2":
      v = default_path # WDSS2 internal suggested path
    elif v == "NONE": 
      return {}        # Don't want it
    elif v == "":
      v = self.getFileDir("KEYFILE", "What WDSS2 authentication file do you want to use?", default_path)
    self.readConfig2(v)
    return self.map2  # Map of name to value

  def mergeConfigLists(self, map1, map2):
    """ Merge two dictionaries where second map overrides first map """
    finalmap = {}
    for k in map1:
      finalmap[k] = map1[k]
    for k in map2:
      # Check if there already?
      try:
        v = finalmap[k]
        print("--->Overrode key '"+k+"' value of '"+v+"' to value of '"+map2[k]+"'")
      except Exception as e:  # python 2.7 up
        pass
      finalmap[k] = map2[k]
    return finalmap

  def listToDFlags(self, map1):
    """ Take a dictionary and create -D string """
    # Now create a single cppflag string with all "-D" options
    cppflags = ""
    for k in map1:
       if map1[k] == "":
         cppflags = cppflags +"-D"+k+" "
       else:
         cppflags = cppflags +"-D"+k+"="+map1[k]+" "
    return cppflags
