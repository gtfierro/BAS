import sys
import os
import re
import pickle
import suds
sys.path.append('../')
import node_types
from generate_geo import *
from collections import defaultdict
from fuzzywuzzy import process
from pprint import pprint

url = "https://emsalc.berkeley.edu/_common/webservices/Eval?wsdl"
client = suds.client.Client(url, username="akrioukov", password="Tangle57")

def get_children(path):
    global client
    return client.service.getFilteredChildren(path, "WEB_GEO")

def get_value(path):
    global client
    return client.service.getValue(path)

alc_children = []

def store_child(path):
    children = get_children(path)
    if len(children) == 0:
      alc_children.append(path)
      print path
    for c in children:
        c = c.referenceName
        child_path = path + c if path == '/' else path + '/' + c
        store_child(child_path)

store_child('#doe_library')


class DictGen(object):
  """ 
  generates the dictionary before we hand it off to the Formatter to actually
  generate the file.

  We will index the dictionary by relational name ('hvac','lights',etc), which
  contains a list of object types ('VAV','AHU','LIG',etc), each of which
  contains a list of object names ('vav 1','ahu 3', 'light bank 4'), each of
  which contains a dictionary of location: 'doe_library','doe_4th_floor', etc
  points: ('m304',discharge air temp),('asdf',high_temp_request), etc.
  """

  def __init__(self, building_name):
    """
    [building_name] is a string of the name of the building
    """
    self.building_name = building_name
    self.building_dict = defaultdict(lambda : defaultdict(lambda : defaultdict(dict)))
    #get dictionary of children so we only have to access SOAP the one time
    print('generating dictionary of points and children...')
    self.children_dict = {}
    for v in alc_children:
      #fancy status bar because I was bored
      sys.stdout.write('\r'+str((alc_children.index(v)+1) * 100.0  / float(len(alc_children))) + '%')
      sys.stdout.flush()
      path = '/'.join(v.split('/')[:-1])
      self.children_dict[v] = client.service.getFilteredChildren(path,'WEB_GEO')

  def make_building(self):
    """
    uses generate_geo.py along with alc_children to create the geodjango objects
    based on the geo paths exposed by ALC
    """
    #define regex for recognizing components
    building = lambda x: re.search('(#doe_library)',x)
    floor = lambda x: re.search('#doe_library/#doe_([\w\d_]+_floor|penthouse|basement)/',x) 
    #loop through file.itervalues(), call building(l).groups() to get the building name, etc

    buildings = []
    floors = []
    areas = []

    for v in alc_children:
      res = building(v)
      if res:
        bu = res.groups()[0]
        if bu not in buildings:
          buildings.append(bu)
      res = floor(v)
      if res:
        fl = res.groups()[0]
        if fl not in floors:
          floors.append(fl)
    print 'Buildings:',buildings
    print 'Floors:',floors
    for b in buildings:
      b = Building(b, floors)
      for hvaczone in self.building_dict['hvac']['VAV']:
        print self.building_dict['hvac']['VAV'][hvaczone]['location'][-2]
        b.add_area(self.building_dict['hvac']['VAV'][hvaczone]['location'][-2][5:],hvaczone,'hvac')
      b.register()

  def generate_dict(self, keyword,type,relational):
    """
    take keyword (search argument) and search the children_dict for strings
    containing it. Then cast these to objects of type [type] and put it in the
    building_dict under relational [relational] For example, use the keyword
    'vav' with type 'VAV' to look for vavs.
    Will return a dictionary like so:
    'VAV': {
        'vav 1': {
          'location': ['doe_library','doe_4th_floor']
          'points': [('m304',discharge air temp),('asdf',high_temp_request)]
          },
        'vav 2: {
          ...
    """
    d = defaultdict(lambda : defaultdict(list))
    for v in alc_children:
      if keyword in v:
        string = filter(lambda x: keyword in x, v.split('/'))[0]
        point = v.split('/')[-1]
        d[string]['location'] = v.split('/')[:v.split('/').index(string)]
        children = self.children_dict[v]
        val = filter(lambda x: x.referenceName == point, children)[0]
        d[string]['points'].append( (point,str(val.displayName)) )
    self.building_dict[relational][type] = d
    return d


class Formatter(object):
  """
  explicitly handles *only* writing to the file by using an input dictionary (supplied
  in constructor)
  """

  def __init__(self, building):
    self.building = building
    self.building_dict = pickle.load(open(building+'.db'))
    with open('test.py','wb') as f:
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

  def build_objects(self):
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

if __name__=='__main__':
  d = DictGen('Bancroft Library')
  d.generate_dict('vav','VAV','hvac')
  d.generate_dict('ah', 'AHU','hvac')
  d.make_building()
  pickle.dump(d.building_dict,open('alc_bancroft.db','w'))
  f = Formatter('Bancroft Library')



