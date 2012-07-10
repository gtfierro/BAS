import sys
sys.path.append('..')
import pickle
import suds
import node_types
from collections import defaultdict
from fuzzywuzzy import process

url = "https://emsalc.berkeley.edu/_common/webservices/Eval?wsdl"
client = suds.client.Client(url, username="akrioukov", password="Tangle57")

allbancroft = pickle.load(open('geopath.db')) #dict of key = alc point, value = geotree path to that point e.g.  u'vfd_min': u'#doe_library/#doe_penthouse/#doe_cooling_towers/vfd_min',

def get_dict(keyword):
  """
  creates something like:
   vav_locs = { 'vav_b-4' : { 'location': ['doe_library','doe_4th_floor'],
                              'points': ['m304','asdf'...]
                              'point_names': ['discharge air temp','high_temp_request'...]}}
  """
  d = defaultdict(lambda : defaultdict(list))
  for v in allbancroft.itervalues():
    print v
    if keyword in v:
      string = filter(lambda x: keyword in x, v.split('/'))[0]
      point = v.split('/')[-1]
      d[string]['location'] = v.split('/')[:v.split('/').index(string)]
      d[string]['points'].append(point)
      path = '/'.join(v.split('/')[:-1])
      children = client.service.getFilteredChildren(path,'WEB_GEO')
      val = filter(lambda x: x.referenceName == point, children)[0]
      d[string]['point_names'].append(str(val.displayName))
  return d

def dict_to_interface(d,type):
  """
  [d] = dict (described below)
  [type] = what type of object we're dealing with ('VAV','LIG',etc)
  [interface] = reference to the interface we're implementing

  takes in dict as returned by get_dict(keyword)
  dict = {'vav1' : { 'location': ['#doe_library','asdfasd'],
                     'points': ['m304','m199'],
                     'point_names': ['dat flow','etc']}}
  
  and returns it as a:
  list = [(obj_type, name, (location,tagging,data), (tag_name, tag_type, device_name, tag_path)),
          etc...]
  example:
  obj_type: LIG
  name: 'light bank 1'
  tag_name: 'lo_rel',
  tag_type: 'bacnetREL'
  device_name: 'low relay'
  tag_path '/ws86007/relay12'
  (location,tagging,data): comma separated list of the geo tagging attributes. Optional for the
                            tag parts; inherits from the outer list if not specified
  """
  ret = []
  for key in d:
    item = [type,key,tuple(d[key]['location'])]
    req_points = node_types.get_required_points(type,True)
    for rp in req_points:
      best_match = process.extractOne(rp, d[key]['point_names'])[0]
      tag_name = node_types.get_required_points(type)[req_points.index(rp)]
      tag_type = node_types.tag_to_class(tag_name).__name__
      device_name = best_match
      tag_path = d[key]['points'][d[key]['point_names'].index(best_match)] #BACnet point path
      item.append((tag_name,tag_type,device_name, tag_path))
    ret.append(tuple(item))
  return ret

def main():
  vavs = get_dict('vav')
  vav_dict = dict_to_interface(vavs,'VAV')
  pickle.dump(vav_dict,open('vav.db','wb'))

if __name__=="__main__":
  main()
