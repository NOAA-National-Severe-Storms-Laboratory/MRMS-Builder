#!/usr/bin/env python

# Robert Toomey March 2017
# Build tools

# Here be the settings.  Change if needed:
SVNMACHINE = "vmrms-ark.protect.nssl"
SVNPATH ="/localdata/svn"
SVNWEBPATH = "http://"+SVNMACHINE+":18080/svn"

# System imports
import os,sys
import subprocess
import readline

# Relative imports
from . import filecompleter
from . import pexpect

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
coff = "\033[0m"

line = "------------------------------------------------"

def runRead(stuff):
  """ Run and read output.  Good for decently small comands, but does store in ram """
  try:
    #$proc = subprocess.Popen("rpm","-qi "+target, stdout=subprocess.PIPE)
    proc = subprocess.Popen(stuff,stdout=subprocess.PIPE)
    lines = []
    # Work with python 3 and 2
    while True:
      line = proc.stdout.readline()
      line = line.decode('ascii').rstrip()  # python 2.7 supports but 3 needs it
      if line == '' and proc.poll() is not None:
        break
      if line:
        lines.append(line.rstrip())
        
    return lines
  except Exception as e: #Gotta support older python
    print ("Exception trying to execute command:" + str(e))
    return []

def checkError(label, stuff, text):
  """ Print error from first line of running a command """
  string = ""
  for z in stuff:
    string = string+z+" "
  red = "\033[1;31m"
  coff = "\033[0m"
  print(red+"   (Can't build '"+label+"': Ran '"+string+"' and looked for the text '"+text+"' and didn't find it...)"+coff+"\n")
  
def getFirst(stuff):
  s = ""
  lines = runRead(stuff)
  if len(lines) > 0:
    s = lines[0]
  return s

def checkFirstList(label, stuff, aList):
  """ Run a command, check for text in the first line of output """
  s = getFirst(stuff)
  for t in aList:
   if t in s:
    return True
  return False

def checkFirst(label, stuff, text):
  """ Run a command, check for text in the first line of output """
  good = False
  s = getFirst(stuff)
  #lines = runRead(stuff)
  #if len(lines) > 0:
  #  s = lines[0]
  if text in s:
    good = True
  return good

def checkFirstText(label, stuff, text):
  """ Run a command, check for text in the first line of output, dump error automatically """
  good = checkFirst(label, stuff, text)

  # Print some error on fail to help debugging
  if good == False:
    checkError(label, stuff, text)
  return good

def runOptional(stuff):
  """ Run system command, allow failure  """
  print("Command: "+stuff)
  try:
    subprocess.check_call(stuff, shell=True)
    return False
  except:
    return True
  
def run(stuff):
  """ Run system command or fail """
  failed = runOptional(stuff)
  if failed:
    print("Failed to execute command, something is wrong. 8(")
    print("Command: "+stuff)
    sys.exit(1)

def chdir(stuff):
  print("Changing dir to " +stuff +"\n")
  os.chdir(stuff)

def getInput(defui):
  """ Get input with default option """

  # Python 3 requires input not raw_input
 # print(blue+"Choose an option or hit enter for default:"+coff)
  if sys.version_info <(3,0):
    ui = raw_input(green+defui+coff+" >")
  else:
    ui = input(green+defui+coff+" >")

  # Use default on return
  if ui == "":
    ui = defui

  return ui

def pickSmarter(prompt, promptList, defOption, restrict, flag):
  """ Choose an option from a list of paired defaults """
  half = len(promptList)/2

  # Make the default option the number found....
  o = defOption
  p = 1;
  for x in range(half):
    index = (x*2)
    if (defOption == promptList[index]):
      o = str(p)
      break
    p = p +1

  while True:

    # Print prompt
    print(prompt)
   
    # Display the options and option prompts
    # We generate the numbers
    p = 1;
    for x in range(half):
       #sys.stdout.write(green+optionList[x]+">  "+coff+promptList[x]+"\n")
       index = (x*2)+1
       sys.stdout.write(green+str(p)+">  "+coff+promptList[index]+"\n")
       p = p + 1

    if restrict:
      print(blue+"Choose one of the options or hit enter for default:"+coff)
    else:
      print(blue+"Type in option or enter for default:"+coff)
     
    # Snag user input
    if flag == True:
      comp = filecompleter.Completer()
      readline.set_completer_delims(' \t\n;')
      readline.parse_and_bind("tab: complete")
      readline.set_completer(comp.complete)
      newo = getInput(o)
    else:
      readline.set_completer_delims('')
      readline.parse_and_bind("")
      readline.set_completer(None)
      newo = getInput(o)

    # The option might have to match the given choices
    # Humm just match number
    if restrict:
      try:
        index = int(newo)
        if (index > 0) and (index <= half):
          return promptList[(index-1)*2]
      except Exception as e: 
        print("Exception: "+str(e))
        # It's ok, just ask for another choise
        pass
    # Otherwise take whatever...
    else:
      return newo

def pickOption1(prompt, promptList, optionList, defOption, restrict, flag):
  """ Choose an option from a list of default """
  o = defOption

  while True:

    # Print prompt
    print(prompt)
   
    # Display the options and option prompts
    for x in range(len(promptList)):
       sys.stdout.write(green+optionList[x]+">  "+coff+promptList[x]+"\n")

    if restrict:
      print(blue+"Choose one of the options or hit enter for default:"+coff)
    else:
      print(blue+"Type in option or enter for default:"+coff)
     
    # Snag user input
    if flag == True:
      comp = filecompleter.Completer()
      readline.set_completer_delims(' \t\n;')
      readline.parse_and_bind("tab: complete")
      readline.set_completer(comp.complete)
      newo = getInput(o)
    else:
      readline.set_completer_delims('')
      readline.parse_and_bind("")
      readline.set_completer(None)
      newo = getInput(o)

    # The option might have to match the given choices
    if restrict:
      found = False
      for x in range(len(optionList)):
        if optionList[x] == newo:
           found = True
           break 
      if found:
        return newo
    # Otherwise take whatever...
    else:
      return newo

def pickOption(prompt, promptList, optionList, defOption, restrict):
  return pickOption1(prompt, promptList, optionList, defOption, restrict, False)

def pickFileOption(prompt, promptList, optionList, defOption, restrict):
  return pickOption1(prompt, promptList, optionList, defOption, restrict, True)

def setupSVN(user, printit):
  """ Setup the SVN settings """
  global SVNMACHINE
  global SVNPATH
  global SVNWEBPATH

  # I'm just gonna set the things
  global SVNROOT 
  global SVN_RSH

  if user == ".":
    # This assumes the current user and asks for their password..bleh
    #SVN_RSH = "svn+ssh"
    #SVNROOT = "svn+ssh://"+SVNMACHINE+SVNPATH
    SVN_RSH = ""
    SVNROOT = SVNWEBPATH
  else:
    SVN_RSH = "svn+ssh"
    SVNROOT = "svn+ssh://"+user+"@"+SVNMACHINE+SVNPATH
  os.environ["SVNROOT"] = SVNROOT
  os.environ["SVN_RSH"] = SVN_RSH

  if printit:
    if user == ".":
      print(blue+"Anonymous checkout and build for read only complete."+coff)
    else:
      print(blue+"Validate this in your shell settings if you plan to change code:"+coff)
      print("SVN_RSH = \""+SVN_RSH+"\"")
      print("SVNROOT = \""+SVNROOT+"\"")

def checkoutSingle(child, command, password):
  """ Checkout a single SVN repository with password """
  print(green+command+coff) 
  # Try to run a checkout command.  This will expect
  # a possible password request and then stuff up to a 'Checked out' line...or
  # even another EOF and unknown stuff
  spamcount = 0
  maxspam = 30
  t = 1
  maxtries = 3
  # Handle all output from the svn/password checkout
  child.logfile=sys.stdout
  while True:
    # Warning on these strings.  They can't show up exactly in the svn output..possible future bug
    # Need more advanced coding to 100% make sure the checkout doesn't 'hit' any of these lines.  Works
    # at the moment
    i = child.expect([u'Password: ',          # 0 
                      u'Account cannot',      # 1
                      u'(yes/no)',            # 2
                      u'Unable to connect',   # 3 svn failure
                      u'No repository found', # 4 svn failure
                      u' expire',             # 5 Hope this snags expired passwords
                      u'\r\n',                # 6
                      pexpect.EOF ], 
                      timeout=600)
    if i==0:
      sys.stdout.write('password sent...\n') 
      #print(child.before) # This would be password prompt from ssh
      #print(">>I sent password to ssh or svn repository...")
      child.logfile=None # Turn off screen dump to not show password
      child.sendline(password)
      child.logfile=sys.stdout
      #print("After1 is " +child.after)
      # I don't want to be locking accounts.  
      if (t >= maxtries):
        print ("Tried to log in {0} times, and password doesn't seem to work.".format(t))
        print ("Too many attempts can temporarily lock your password, so I stopped.")
        sys.exit()
      t = t + 1

    elif i == 1:
      print(child.before)
      print (">>Account issue.")
      sys.exit()

    # The wonderful first time Are you sure you want to continue connecting ssh crap...
    elif i == 2: 
      child.sendline("yes") # We sure dooz wantz to logz inz

    elif ((i == 3) or (i == 4)): 
      print(">>Svn failure...aborting..")
      return 1

    elif (i == 5): 
      print(">>Password possibly expired...log in and change it and retry...aborting..")
      sys.exit()

    # Got a newline back...we'll print out every so often so user doesn't think
    # we're hung up.  Don't really need 'all' the svn output to spam us
    elif i == 6:
      if spamcount == 0:
        print(child.before) # Print every maxspam checkout line
        #sys.stdout.write('.')
        sys.stdout.flush()
        # Print actual line print(">>At:"+child.before)
      spamcount = spamcount + 1
      if spamcount > maxspam:
        spamcount = 0

    else:
      print(child.before)
      #print("We got EOF!\n")
      return 0

def checkoutSVN(what,where, password, options):
  """ Checkout a single SVN repository """

  global SVNROOT
  if sys.version_info <(3,0):
    whatfull = unicode(SVNROOT+what, "utf-8")
    wherefull = unicode(where, "utf-8")
    svnoptions = unicode(options, "utf-8")
  else:
    whatfull = SVNROOT+what
    wherefull = where
    svnoptions = options
  #command = (u"svn co "+whatfull+u" "+wherefull)
  command = (u"svn co "+svnoptions+" "+whatfull+u" "+wherefull)
  child = pexpect.spawnu(command)

  # This is nice for debugging, but it will print your password 
  # to screen so fair warning..
  # Will add it after the password check
  #child.logfile=sys.stdout

  #print("Running checkout...give me a minute to download sources...\n")
  svntry = 1
  maxsvn = 2
  while True:
    back = checkoutSingle(child, command, password)
    if back == 1: # magic number svn error
      if svntry >= 2:
        print("Tried svn {0} times, failed.".format(svntry))
        sys.exit()
      svntry = svntry + 1
    else:
      break  # Good to go

  # Dump rest of unread or not?  This should be the revision info on success
  print(child.read())

