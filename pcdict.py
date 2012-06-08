import uuid
import sys
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from collections import defaultdict
"""
Nodes and Objects.
Objects are effectively collectons of nodes
We have functional links and attributes for the nodes and objects
"""

class BACnetPoint(object):
  def __init__(self, obj_type, name=''):
    self.type = obj_type
    self.name = name
    self.uid = uuid.uuid4()
    self.metadata = {}

  def __str__(self):
    return self.name

  def __cmp__(self, other):
    # use self.uuid to compare to other objects
    return self.uid.__cmp__(other.uid)

  def add_child(self, child):
    self.container.add_node_child(self, child)

  def add_parent(self, parent):
    self.container.add_node_parent(self, parent)

class BNode(BACnetPoint):

  def __init__(self, obj_type, container='', name=''):
    self.container = container
    self.attributes = {}
    BACnetPoint.__init__(self,obj_type,name)
    print "Node",self.name, self.uid

  def add_attribute(self, name, bacnet_point):
    self.attributes[name] = bacnet_point
  
class BObj(BACnetPoint):

  def __init__(self, obj_type, container='', name=''):
    self.nodes = []
    self._nk = nx.DiGraph()
    self.type_dict = defaultdict(list)
    BACnetPoint.__init__(self,obj_type, name)
    print ">>>Object",self.name, self.uid

  #add child to an internal node
  def add_node_child(self, node, child):
    #check if child exists as a node in our interal graph
    # if false, add the child then add the edge
    # regardless, add edge if edge doesn't exist
    if child not in self._nk:
      self._nk.add_node(child)
    if child not in self._nk[node]:
      self._nk.add_edge(node,child)
    self._populate_type_dict()

  def _populate_type_dict(self):
    for o in self._nk.nodes():
      if o not in self.type_dict[o.type]:
        self.type_dict[o.type].append(o)

  #add parent to an internal node
  def add_node_parent(self, node, parent):
    if parent not in self._nk:
      self._nk.add_node(parent)
    if node not in self._nk[parent]:
      self._nk.add_edge(parent,node)

  #for internal graph setup
  def add_nodes(self, nodes):
    extension = [nodes] if type(nodes) != list else nodes
    self.nodes.extend(extension)
    for node in extension:
      node.container = self
      self._nk.add_node(node)

class Relational(object):

  def __init__(self, name, objects=None):
    self._nk = nx.DiGraph()
    self.type_dict = defaultdict(list)
    self.name = name
    if objects:
      for obj in objects:
        obj.container = self
        self._nk.add_node(obj)
    self._populate_type_dict()

  def _populate_type_dict(self):
    for o in self._nk.nodes():
      if o not in self.type_dict[o.type]:
        self.type_dict[o.type].append(o)
      print [x.type for x in o.nodes]
      for n in o.nodes:
        if n not in self.type_dict[n.type]:
          self.type_dict[n.type].append(n)

  def extend_by_unique_uid(self, target, extend):
    extend = [extend] if type(extend) != list else extend
    to_add = [t for t in extend if t.uid not in map(lambda x: x.uid, target)]
    target.extend(to_add)

  #add child to an internal node
  def add_node_child(self, node, child):
    #check if child exists as a node in our interal graph
    # if false, add the child then add the edge
    # regardless, add edge if edge doesn't exist
    if child not in self._nk:
      self._nk.add_node(child)
    if child not in self._nk[node]:
      self._nk.add_edge(node,child)

  #add parent to an internal node
  def add_node_parent(self, node, parent):
    if parent not in self._nk:
      self._nk.add_node(parent)
    if node not in self._nk[parent]:
      self._nk.add_edge(parent,node)


  def query(self, query_string):

    #regex for matching parts of query
    find_uuid = lambda x: re.match(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', x)
    find_type = lambda x: re.match(r'^[^\d\s]+$',x) 
    find_name = lambda x: re.match(r'[\w\-\:\_\s]+',x)

    def find(token, obj):
      #searching for 'token' in 'obj'
      #TODO: fix this so that it is flexible. We want to use the domain argument
      #in order to make this find() as local as possible. It is the job of the queue
      #and the for loop to iterate through objects. 
      #below, we will iterate through everything in the scope of the part of the query
      #we are using, and then send each object/node to this find() method to see if it matches
      #the token of that query. find() does token recognition ("what type of token is it?") and
      #returns all relevant results
      #TODO: should find() also search the nodes of an object? that might be easier...and that
      #way we don't have to worry about searching nodes in the loop/queue
      #domain will be an object

      #identifies what type of token we have
      token_filter = [regex(token) for regex in [find_uuid, find_type, find_name]]
      initial_token = ("NAME", token_filter[2]) if not any(token_filter[:2]) else ("TYPE", token_filter[1]) if not token_filter[0] else ("UUID", token_filter[0])
      initial_token = (initial_token[0],initial_token[1].group())

      #search for token in the object itself and all of its internal nodes
      if initial_token[0] == "TYPE":
        #find all objects of type TYPE
        initial = obj.type_dict[initial_token[1]]
        if obj.type==initial_token[1]:
          initial.append(obj.type) 
      else:
        if initial_token[0] == "UUID":
          ftr = lambda x: str(x.uid) == initial_token[1]
        else:
          ftr = lambda x: x.name == initial_token[1]
        initial = []
        if ftr(obj):
          initial.append(obj)
        for o in obj._nk:
          if ftr(o):
            initial.append(o)
            break
      return initial
    
    tokens = [p.strip() for p in re.split(r'[<>]',query_string)]
    scopes = re.findall(r'[<>]',query_string)
    scopes.insert(0,"EOQ") #End Of Query
    new_query = zip(scopes, tokens)
    print new_query
    queue = deque()
    print [find(tokens[0],o) for o in self._nk.nodes()]
    return

    result = []
    for scope,obj_type in new_query:
      #scope is "<",">","EOQ", and
      #obj_type is "AH" or "SF" or whatever
      print ">>",scope,":",obj_type
      while len(queue):
        #get next object to start the next stage of the query with
        target = queue.pop()
        if target.type == obj_type:
          print "GOT:",target.name
          result.append(target)
        print "searching",target,
        if hasattr(t,"_nk"): #t is of type BObj
          print "(obj)"
          for node in t._nk:
            #append for a dfs of the nodes
            queue.append(node)
        else:
          print "(node)"
        if scope == "<":
          for p in target.container._nk.predecessors(target):
            #search t's parents for instances of part[1]
            queue.appendleft(p)
        elif scope == ">":
          for c in target.container._nk.successors(target):
            #search t's children for instances of part[1]
            queue.appendleft(c)
        else:
          print "EOQ!"
    return result

#ORDER OF CREATION
#create the object
#create the nodes (BNode("TYPE", container, name)
#object.add_nodes[node1,n2,n3...]
#create hierarchies for nodes: 
#n1.add_child...etc...
#create next object
#...
#link objects


#create nodes
"""
Air Handler:              Chilled Water Loop:         Hot Water Loop:
-supply fan (SF)          -chiller (CH)               -boiler/heat exchanger (HX)
-return fan (RF)          -pump    (PU)               -pump
-cooling (CCV)            -cooling tower (CT)         -valves
-dampers  (DMP)           -valves  (VV)               -temp sensors
-temp sensors (TS)        -temp sensors               -pressure sensors
-pressure sensors (PS)    -pressure sensors
-humidity sensor (HS)
-airflow sensor (AS)
"""
#for object: Air Handler 1
ah1 = BObj("AH", name="Air Handler 1")
#nodes
sf1 = BNode("SF", ah1, name="Supply fan 1")
vfd1 = BNode("VFD", ah1, name="Variable Frequency Drive 1")
rf1 = BNode("RF", ah1, name="Return fan 1")
vfd2 = BNode("VFD", ah1, name="Variable Frequency Drive 2")
ccv1 = BNode("CCV", ah1, name="cooling valve 1")
dmp1 = BNode("DMP", ah1, name="Exhaust damper")
dmp2 = BNode("DMP", ah1, name="Outside Air Damper")
dmp3 = BNode("DMP", ah1, name="Return Air Damper")
ps1 = BNode("PS", ah1, name="Pressure Sensor 1")
ts1 = BNode("TS", ah1, name="Temperature Sensor 1")
hs1 = BNode("HS", ah1, name="Humidity Sensor 1")
as1 = BNode("AS", ah1, name="Airflow Sensor 1")

dmp3.add_attribute("percent open", "SDH.AH1A_RAD")
dmp2.add_attribute("percent open", "SDH.AH1A_OAD")
dmp1.add_attribute("percent open", "SDH.AH1A_EAD")
ccv1.add_attribute("Percent open", "SDH.AH1A_CCV")
vfd2.add_attribute("fan speed", "SDH.AH1A.SF_VFD:Input ref1")
vfd2.add_attribute("fan power", "SDH.AH1A.SF_VFD:POWER")
vfd1.add_attribute("fan speed", "SDH.AH1A.SF_VFD:Input ref1")
vfd1.add_attribute("fan power", "SDH.AH1A.SF_VFD:POWER")

#fix?
ah1.add_nodes([sf1,rf1,ccv1,dmp1,dmp2,dmp3,ps1,ts1,hs1,as1])

dmp2.add_child(ccv1)
dmp2.add_child(dmp3)
dmp3.add_child(dmp1)
dmp3.add_child(rf1)
ccv1.add_child(sf1)
rf1.add_child(vfd2)
sf1.add_child(vfd1)


#for object: chilled water loop
cwl1 = BObj("CWL", name="Chilled Water Loop 1")
#nodes
ch1 = BNode("CH",cwl1,name="Chiller 1")
pu1 = BNode("PU",cwl1,name="Chilled Water pump 1")
pu2 = BNode("PU",cwl1,name="Condenser Water pump 1")
ct1 = BNode("CT",cwl1,name="Cooling tower")

cwl1.add_nodes([ch1,pu1,pu2,ct1])

ct1.add_child(pu2)
pu2.add_child(ch1)
ch1.add_child(pu1)


#nodes for object: hot water loop
hwl1 = BObj("HWL", name="Hot water loop 1")
#nodes
hx1 = BNode("HX",hwl1,name= "Heat Exchanger 1")
pu1 = BNode("PU",hwl1,name= "Hot water pump 1")
vv1 = BNode("VV",hwl1,name= "Heating valve 1")

hwl1.add_nodes([hx1,pu1,vv1])

hx1.add_child(pu1)
pu1.add_child(vv1)

#for object: Air Handler 1
ah2 = BObj("AH", name="Air Handler 2")
#nodes
sf1 = BNode("SF",ah2,name= "Supply fan 2")
vfd1 = BNode("VFD",ah2,name= "Variable Frequency Drive 2")
rf1 = BNode("RF",ah2,name= "Return fan 2")
vfd2 = BNode("VFD",ah2,name= "Variable Frequency Drive 2")
ccv1 = BNode("CCV",ah2,name= "cooling valve 2")
dmp1 = BNode("DMP",ah2,name= "Exhaust damper")
dmp2 = BNode("DMP",ah2,name= "Outside Air Damper")
dmp3 = BNode("DMP",ah2,name= "Return Air Damper")
ps1 = BNode("PS",ah2,name= "Pressure Sensor 2")
ts1 = BNode("TS",ah2,name= "Temperature Sensor 2")
hs1 = BNode("HS",ah2,name= "Humidity Sensor 2")
as1 = BNode("AS",ah2,name= "Airflow Sensor 2")

dmp3.add_attribute("percent open", "SDH.AH1A_RAD")
dmp1.add_attribute("percent open", "SDH.AH1A_EAD")
ccv1.add_attribute("Percent open", "SDH.AH1A_CCV")
vfd1.add_attribute("fan speed", "SDH.AH1A.SF_VFD:Input ref2")
vfd1.add_attribute("fan power", "SDH.AH1A.SF_VFD:POWER")
vfd2.add_attribute("fan speed", "SDH.AH1A.SF_VFD:Input ref2")
vfd2.add_attribute("fan power", "SDH.AH1A.SF_VFD:POWER")
dmp2.add_attribute("percent open", "SDH.AH1A_OAD")

ah2.add_nodes([sf1,rf1,ccv1,dmp1,dmp2,dmp3,ps1,ts1,hs1,as1])

dmp2.add_child(ccv1)
dmp2.add_child(dmp3)
dmp3.add_child(dmp1)
dmp3.add_child(rf1)
ccv1.add_child(sf1)
sf1.add_child(vfd1)
rf1.add_child(vfd2)

hvac_rel = Relational("HVAC Relational",[hwl1,cwl1,ah1,ah2])

hwl1.add_child(ah1)
hwl1.add_child(ah2)
cwl1.add_child(ah1)
cwl1.add_child(ah2)
#set up object hierarchy

print "....done setting up!"
print "1:",hvac_rel.query("AH<PU")
print "2:",hvac_rel.query(str(hvac_rel._nk.nodes()[0].uid)+"<PU")
