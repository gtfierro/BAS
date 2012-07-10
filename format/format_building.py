"""
takes in a list like this:
    list = [(obj_type, name, (location,tagging,data), (tag_name, tag_type, device_name, tag_path)),
              etc...]
"""
import sys
import os
import pickle
import node_types

class Formatter(object):

  def __init__(self, building):
    self.building = building
    with open(self.building+'.py','wb') as f:
      #write all the imports
      f.write("""from node import Relational
from generic_objects import *
from bacnet_devices import *
import networkx as nx
import gis
import node_types

gis.NodeLink.objects.all().delete()\n""")


  def setlist(self, list_file):
    self.list_file = pickle.load(open(list_file))

  def setrelational(self, relational_type):
    self.relational_type = relational_type
    with open(self.building+'.py','a') as f:
      f.write("%s = relational('%s')\n" % (relational_type,relational_type))

  def build(self):
    f = open(self.building+'.py','a')

    for line in self.list_file:
      type=line[0]
      name=line[1].replace('-','_').replace(':','_').replace(' ','_').replace('#','')
      location=line[2]
      line_string = "%s = %s(%s, '%s', {\n" % (name,type,self.relational_type,name)
      if len(line) > 3:
        for item in line[3:]:
          tag_name, tag_type, device_name, tag_path = item
          if tag_type:
            line_string += "'%s' : %s( '%s','%s'),\n" % (tag_name, tag_type, device_name, tag_path)
      line_string += '})\n'
      f.write(line_string)

    f.close()
