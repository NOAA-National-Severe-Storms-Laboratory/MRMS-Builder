#!/bin/python

# Robert Toomey July 2017
# 
# Utility library class for reading pair values from a
# configuration file

import os,sys

class Configuration:
  """ Configuration options """

  def __init__(self):
    self.map1 = {}

  def cleanText(self, line):
     """ Clean text line from config file """
     l2 = line.rstrip('\n')   # Remove new lines
     l2 = l2.rstrip(' ')      # Remove end spaces
     l2 = l2.split("#", 1)[0] # Remove stuff post '#'
     return l2

  def readConfig(self, configFile):
     """ Read a configuration file, return map of values """
     map1= {}
     try:
       with open(configFile, "r") as f:
         for line in f:
           l2 = self.cleanText(line)

           # If anything left of line...
           if l2 != "":
             pair = l2.split('=')     # Get name=value pair if any
             if (len(pair) == 2):
               pair[0] = self.cleanText(pair[0])
               pair[1] = self.cleanText(pair[1])
             map1[pair[0]] = pair[1]
     except:
       return "(Couldn't read file, skipping)"
     self.map1 = map1
     return ""

  def printConfig(self):
    """ Print out configuration """
    print (self.map1)

  def getString(self, key, default_value):
    """ Get a string from configuration """
    return self.map1.get(key, default_value)
