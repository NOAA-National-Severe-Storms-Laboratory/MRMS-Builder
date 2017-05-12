#!/usr/bin/python

# ldd all files in directory checking for arg 1
# 
# Thie is copied to the bin folder as a tool for me
# to check ldd linkage of libraies on a build...
#
# Robert Toomey April 2017

from os import listdir
from os.path import isfile, join
import os
import sys
import subprocess

if len(sys.argv) < 2:
  print "Need at least one argument"
  sys.exit(1)

thing = sys.argv[1]
mypath = os.path.dirname(os.path.realpath(__file__))
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print "Looking for " +thing
for z in onlyfiles:
  filename = mypath+"/"+z
  #print " "+filename
  #os.system("ldd "+filename+" | grep libnss3")
  stuff = "ldd "+filename+" | grep "+thing
  DEVNULL = open(os.devnull, 'wb')
  
  try:
    out = subprocess.check_output(stuff, shell=True)
    sys.stdout.write(filename + ": "+out)
  except:
    pass
