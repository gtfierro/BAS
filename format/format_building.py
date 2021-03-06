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

#store_child('#doe_library')

def pickilizify(ddict):
  """
  creates a pickleable version of a default dict
  """
  res = {}
  for d in ddict:
    res[d] = dict(ddict[d])
    for dd in ddict[d]:
      res[d][dd] = dict(ddict[d][dd])
  return res


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
    self.building_dict = pickle.load(open('alc_bancroft.db'))
    with open('test.py','wb') as f:
      #write all the imports
      f.write("""from node import Relational
from generic_objects import *
from bacnet_devices import *
import networkx as nx
import gis
import node_types
\n""")

  def setrelational(self, relational_type):
    self.relational_type = relational_type
    with open('test.py','a') as f:
      f.write("%s = Relational('%s')\n" % (relational_type,relational_type))

  def build(self):
    f = open('test.py','a')
    #make AHUs
    for line in filter(lambda x: 'interface' not in x, self.building_dict[self.relational_type]['AHU']):
      if line.startswith('#'):
        name = line[1:].replace('-','_').replace(':','_')
      else:
        continue
      type = node_types.tag_to_class('AHU')
      line_string = "%s = AHU(%s, '%s',{\n" % (name, self.relational_type, name)
      point_base = '/device'+get_value(line+'/~net/~parent/driver/device/object_identifier')[2:]
      line_string += "\t'OUT_AIR_DMP':BancroftAHUDMP('Outside Air Damper','BACnet point name'),\n"
      line_string += "\t'OUT_AIR_TMP_SEN':BancroftSEN('Outside Air Temp Sensor','%s'),\n"  % (point_base+'/oat')
      line_string += "\t'MIX_AIR_TMP_SEN':BancroftSEN('Mixed Air Temp Sensor','%s'),\n" % (point_base+'/aha_mat')
      line_string += "\t'RET_FAN':BACnetFAN('Return Fan','BACnet point name'),\n"
      line_string += "\t'RET_AIR_FLW_SEN':BACnetSEN('Return Air Flow Sensor','BACnet point name'),\n"
      line_string += "\t'EXH_AIR_DMP':BACnetDMP('Exhaust Air Damper','BACnet point name'),\n"
      line_string += "\t'EXH_AIR_TMP_SEN':BancroftSEN('Exhaust Air Temp Sensor','%s'),\n" % (point_base+'/dh1_eat')
      line_string += "\t'RET_AIR_HUM_SEN':BancroftSEN('Return Air Humidity Sensor','%s'),\n" % (point_base+'/avg_spc_hum')
      line_string += "\t'RET_AIR_TMP_SEN':BancroftSEN('Return Air Temp Sensor','%s'),\n" % (point_base+'/aha_rat')
      line_string += "\t'RET_AIR_DMP':BACnetDMP('Return Air Damper','BACnet point name'),\n"
      line_string += "\t'RET_AIR_PRS_SEN':BancroftSEN('Return Air Pressure Sensor','%s'),\n" % (point_base+'/a_sys_bldg_press')
      line_string += "\t'COO_VLV':BACnetVLV('Cooling Valve','%s'),\n" % (point_base+'/aha_chwv')
      line_string += "\t'SUP_AIR_FAN':BancroftFAN('Supply Air Fan','%s'),\n" % (point_base+'/m373')
      line_string += "\t'SUP_AIR_FLW_SEN':BancroftSEN('Supply Air Flow Sensor','%s'),\n" % (point_base+'/sa_cfm')
      line_string += "\t'SUP_AIR_TMP_SEN':BancroftSEN('Supply Air Temp Sensor','%s'),\n" % (point_base+'/ag_spc_temp')
      line_string += "\t'SUP_AIR_PRS_SEN':BACnetSEN('Supply Air Pressure Sensor','BACnet point name'),\n"
      line_string += "})\n"
      #location
      #line_string += "%s.areas.add(gis.buildings['Bancroft Library'])\n" % name
      f.write(line_string)


    #make VAVs
    for line in self.building_dict[self.relational_type]['VAV']:
      if line.startswith('#'):
        name = line[1:].replace('-','_').replace(':','_')
      print self.building_dict[self.relational_type]['VAV'][line]
      type = node_types.tag_to_class('VAV')
      area = re.match('.*\d(?=\w)?',line)
      full_area = re.match('.*\d\w?',line)
      #initialize VAV
      point_name = '/device'+get_value(full_area.group()+'/~net/~parent/driver/device/object_identifier')[2:]+'/flow_tab_1'
      line_string = "%s = %s(%s, '%s', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','%s')})\n" % (name,type,self.relational_type,name,point_name)
      #link gis to VAV
      line_string += "try:\n  %s.areas.add(gis.buildings['Bancroft Library']['%s']['%s'])\nexcept:\n  print 'could not link %s %s'\n" % (name,  self.building_dict['hvac']['VAV'][line]['location'][1][5:],area.group()[1:], 'VAV', area.group()[1:])
      f.write(line_string)

    #link VAVs to AHUs
    for line in filter(lambda x: 'interface' not in x, self.building_dict[self.relational_type]['AHU']):
      if line.startswith('#'):
        ahu_name = line[1:].replace('-','_').replace(':','_')
      else:
        continue
      ahu_id = re.search('(?<=ah\-)([a-z])',line).group()
      for vav in self.building_dict[self.relational_type]['VAV']:
        if line.startswith('#'):
          vav_name = vav[1:].replace('-','_').replace(':','_')
        print 'linking',vav_name
        vav_ahu_id = re.search('(?<=vav\_)([a-z])',vav).group()
        if vav_ahu_id == ahu_id:
          f.write('%s.add_child(%s)\n' % (ahu_name, vav_name))
    f.close()

if __name__=='__main__':
  #d = DictGen('Bancroft Library')
  #d.generate_dict('vav','VAV','hvac')
  #d.generate_dict('ah', 'AHU','hvac')
  #d.make_building()
  #pickle.dump(pickilizify(d.building_dict),open('alc_bancroft.db','w'))
  f = Formatter('Bancroft Library')
  f.setrelational('hvac')
  f.build()
