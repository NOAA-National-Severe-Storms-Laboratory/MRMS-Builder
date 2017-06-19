#!/bin/python

# Robert Toomey March 2017
# Build tools

import os,sys
import subprocess
import pexpect
import filecompleter
import readline

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
coff = "\033[0m"

line = "------------------------------------------------"

def runOptional(stuff):
  """ Run system command, allow failure  """
  print "Command: "+stuff
  try:
    subprocess.check_call(stuff, shell=True)
    return False
  except:
    return True
  
def run(stuff):
  """ Run system command or fail """
  failed = runOptional(stuff)
  if failed:
    print "Failed to execute command, something is wrong. 8("
    print "Command: "+stuff
    sys.exit(1)

def chdir(stuff):
  print("Changing dir to " +stuff +"\n")
  os.chdir(stuff)

def getInput(defui):
  """ Get input with default option """

  # Python 3 requires input not raw_input
 # print blue+"Choose an option or hit enter for default:"+coff
  if sys.version_info <(3,0):
    ui = raw_input(green+defui+coff+" >")
  else:
    ui = input(green+defui+coff+" >")

  # Use default on return
  if ui == "":
    ui = defui

  return ui

def pickOption1(prompt, promptList, optionList, defOption, restrict, flag):
  """ Choose an option from a list of default """
  o = defOption

  while True:

    # Print prompt
    print prompt
   
    # Display the options and option prompts
    for x in range(len(promptList)):
       sys.stdout.write(green+optionList[x]+">  "+coff+promptList[x]+"\n")

    if restrict:
      print blue+"Choose one of the options or hit enter for default:"+coff
    else:
      print blue+"Type in option or enter for default:"+coff
     
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

  # I'm just gonna set the things
  global SVNROOT 
  global SVN_RSH

  SVN_RSH = "svn+ssh"
  SVNROOT = "svn+ssh://"+user+"@tensor.protect.nssl/var/svn"
  os.environ["SVNROOT"] = SVNROOT
  os.environ["SVN_RSH"] = SVN_RSH

  if printit:
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
    i = child.expect([u'Password: ',     # 0
                      u'Account cannot', # 1
                      u'(yes/no)',       # 2
                      u'\r\n',           # 3
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

    # Got a newline back...we'll print out every so often so user doesn't think
    # we're hung up.  Don't really need 'all' the svn output to spam us
    elif i == 3:
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
      return

def checkoutSVN(what,where, password):
  """ Checkout a single SVN repository """

  global SVNROOT
  whatfull = unicode(SVNROOT+what, "utf-8")
  wherefull = unicode(where, "utf-8")
  command = (u"svn co "+whatfull+u" "+wherefull)
  print command
  sys.exit(1)
  child = pexpect.spawnu(command)

  # This is nice for debugging, but it will print your password 
  # to screen so fair warning..
  # Will add it after the password check
  #child.logfile=sys.stdout

  #print("Running checkout...give me a minute to download sources...\n")
  checkoutSingle(child, command, password)

  # Dump rest of unread or not?  This should be the revision info on success
  print child.read()

