#!/bin/python

# Robert Toomey May 2017
# Class for building 'something'
# until I figure where best to put it

class Builder:
  """ build something """
  def __init__(self, key, target):
    #print ("Key incoming is "+key)
    self.key = key
    self.target = target
  def clean(self):
    pass 
  def copy(self, t):
    pass
  def unzip(self):
    pass
  def build(self, t):
    pass
  def showkey(self):
    print("The key is "+self.key)

