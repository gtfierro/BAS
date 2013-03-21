from baslexer import BasLexer
import ply.yacc as yacc
from collections import deque
import itertools

from node import *
import gis
gis.NodeLink.objects.all().delete()
import sdh_demo as sdh

domain = [getattr(sdh, i) for i in sdh.__dict__ if isinstance(getattr(sdh,i), Relational)]

def flatten(l):
    return map(lambda x: x, list(itertools.chain(*l)))

def set_union(set1, set2):
    return set(set1).issubset(set(set2))

def isspatial(nodes):
    """
    returns True if [nodes] contains spatial objects
    """
    nodes = [nodes] if not isinstance(nodes,list) else nodes
    return all(map(lambda x: not isinstance(x, (Relational, Node)),nodes))

def filter_dup_uids(target):
    """
    Given a [target] list, returns a list where all components are unique by their uid
    """
    ret = []
    for item in target:
        if hasattr(item,'uid'):
            if item.uid not in map(lambda x: x.uid, ret):
                ret.append(item)
        else: #if it doesn't have a uid, then it's a spatial
            ret.append(item)
    return ret


def links_to_nodes(links):
    def _links_to_nodes( links):
        for r in domain:
            for node in r.nodes():
                if str(node.uid) in [link.uuid for link in links]:
                    yield node
    return Node.NodeList(_links_to_nodes(links))

def get_areas(gisobj):
    """
    returns a list of the areas for the given gisobj
    """
    areas = [gisobj] if not isinstance(gisobj,list) else gisobj
    flattened = []
    for place in areas:
        if isinstance(place, gis.Building):
            for floor in place.floors.all():
                flattened.extend(list(floor.areas.all()))
        elif isinstance(place, gis.Floor):
            flattened.extend(list(place.areas.all()))
        else:
            flattened.append(place)
    return flattened

def areas_to_nodes(areas):
    """
    For every item in [areas], we resolve it down to all areas inside it and
    then return the flat list of all nodes in those areas
    """
    areas = get_areas(areas)
    return links_to_nodes(list(itertools.chain.from_iterable(x.nodes.all() for x in areas)))

def nodes_to_areas(nodes):
    nodes = [nodes] if not isinstance(nodes,list) else nodes
    flattened = []
    for node in nodes:
      extension = node.areas.all()
      if extension:
        flattened.extend(extension)
    return list(set(flattened))

def allow_intersection(a1, a2):
    """
    double checks that the gis areas a1, a2 are on the same floor and building
    returns T/F
    """
    a1f = a1.floor
    a2f = a2.floor
    if a1f == a2f and a1f.building == a2f.building:
      return True
    return False

def expand_by_intersection(areas):
    """
    given an area or list of areas, returns the list of areas that intersect with those areas
    """
    areas = [areas] if not isinstance(areas, list) else areas
    res = []
    for a in areas:
      candidates = gis.Area.objects.filter(regions__overlaps=a.regions)
      res.extend([c for c in candidates if allow_intersection(c, a)])
    return False if res == areas else res

def resolve_spatial_nodes(querynodes, setnodes):
    query_is_spatial = isspatial(querynodes)
    set_is_spatial = isspatial(setnodes)
    if query_is_spatial and not set_is_spatial:
      setnodes = nodes_to_areas(setnodes)
      set_is_spatial = True
    elif not query_is_spatial and set_is_spatial:
      setnodes = areas_to_nodes(setnodes)
    if query_is_spatial and set_is_spatial:
      query_regions = set(get_areas(querynodes))
      set_regions = set(get_areas(setnodes))
      #return list(query_regions.intersection(set_regions)), None
      res = expand_by_intersection(list(set_regions))
      if res:
        return list(set(res)), None
      else:
        return False, None
    return querynodes, setnodes

def get_predecessors(qn):
    preds = qn.container.predecessors(qn)
    preds.extend(qn.container)
    return filter_dup_uids(preds)

def get_successors(qn):
    succs = qn.container.successors(qn)
    if isinstance(qn, Obj):
      succs.extend(qn.devices.values())
    return filter_dup_uids(succs)

def find_immediate(querynodes, setnodes, direction):
    immediates = []
    for qn in querynodes:
        if direction == "upstream":
          if set(setnodes).intersection(set(get_successors(qn))):
            immediates.append(qn)
        else:
          if set(setnodes).intersection(set(get_predecessors(qn))):
            immediates.append(qn)
    immediates = set(flatten(immediates))
    return filter_dup_uids(immediates)

def search_relatives(node, target, direction):
    """
    [direction] is either "successors" or "predecessors"
    Given a [node], search all of its successors: Successors are all nodes reachable by a bfs from this node
    as well as the container of this node (if it exists) and all successors of that object and all nodes
    in those successors. As soon as we find a successor that is in [target], we return [node], but if we reach
    the end of the recursion, then we return None.

    How do we do this? We can get the immediate successors for a node using node.container._nk.successors(node)
    put these all onto a deque, followed by the container. We iterate through this generator, checking for membership in [target]. As we pop
    nodes off the deque, we add their immediate children to the deque.
    """
    #initialize whether we're looking for successors or predecessors
    relative_fxn = lambda x: getattr(x.container, direction)(x)
    #initialize already-visited lists
    already_visited = [node]
    #initialize queue
    queue = deque()
    #add first node to queue
    queue.appendleft(node)
    #add its Container if it isn't already a container
    if not isinstance(node, Container):
      queue.appendleft(node.container)
      already_visited.append(node.container)

    while queue: #loop until we reach the end of the queue
      #get next node off the top (FIFO)
      current = queue.pop()
      if current in target: #successful!
        return node
      #if this node is in a container we haven't visited yet, add
      #all of that container's nodes to our queue
      if isinstance(current, Container):
        if current not in already_visited:
          for n in current.nodes():
            if n not in already_visited:
              already_visited.append(n)
              queue.appendleft(n)
      #search the relatives of the current node according to relative_fxn
      #for each relative, if we haven't traversed it, add it to the queue
      for n in relative_fxn(current):
        if n not in already_visited:
          already_visited.append(n)
          queue.appendleft(n)
      #if current has an external container, add it to the queue
      if current.external_parents and direction == "predecessors":
        for p in current.external_parents:
          if p not in already_visited:
            already_visited.append(p)
            queue.appendleft(p)
      elif current.external_childs and direction == "successors":
        for c in current.external_childs:
          if c not in already_visited:
            already_visited.append(c)
            queue.appendleft(c)
      #finally, add the current's container to the queue
      if not isinstance(current.container, Relational):
        if current.container not in queue and current.container not in already_visited:
          already_visited.append(current.container)
          queue.appendleft(current.container)
    return None

class BasParser(object):
    basvars = dict()
    def build(self):
        return yacc.yacc(module=self)

    tokens = BasLexer.tokens

    # STATEMENT
    def p_statement_var(self, p):
        '''statement : VAR EQUALS query'''
        self.basvars[p[1]] = p[3]

    def p_statement_query(self, p):
        '''statement : query'''
        self.lastvalue = p[1]
        p[0] = p[1]

    # SET
    def p_set_query(self, p):
        '''set : LPAREN query RPAREN'''
        p[0] = self.lastvalue = p[2]

    def p_set_lastvalue(self, p):
        '''set : LASTVALUE'''
        p[0] = self.lastvalue

    def p_set_spatial(self, p):
        '''set : SPATIAL'''
        name_lookup = p[1][1:].strip()
        p[0] = self.lastvalue = gis.search(name_lookup)

    def p_set_name(self, p):
        '''set : NAME'''
        name_lookup = p[1][1:].strip()
        dom = p[0] if p[0] else domain
        res = []
        for r in dom:
            res.extend(r.search(lambda x: name_lookup in x.get_name()))
        p[0] = self.lastvalue = res

    def p_set_tag(self, p):
        '''set : TAG'''
        tag_lookup = p[1][1:].strip().replace(' ','_')
        res = []
        dom = p[0] if p[0] else domain
        for r in dom:
            if tag_lookup:
                res.extend(r.search(lambda x: set_union(tag_lookup.split('_'), x.tags)))
            else:
                res.extend(r.search(lambda x: True))

        p[0] = self.lastvalue = res

    def p_set_uuid(self, p):
        '''set : UUID'''
        uuid_lookup = p[1][1:].strip()
        res = []
        for r in domain:
            res.extend(r.search(lambda x: str(x.uid) == uuid_lookup))
        p[0] = self.lastvalue = res

    def p_set_var(self, p):
        '''set : VAR'''
        p[0] = self.basvars.get(p[1],[])

    # QUERY
    def p_query(self,p):
      '''query : set UPSTREAM query
               | set DOWNSTREAM query'''
      res = []
      if not isspatial(p[1]) and isspatial(p[3]):
        if p[2] == ">":
          _, target = resolve_spatial_nodes(p[1],p[3])
          p[0] = self.lastvalue = list(set(p[1]).intersection(set(target)))
          return
        else:
          _, target = resolve_spatial_nodes(p[1],p[3])
          p[0] = self.lastvalue = list(set(p[1]).intersection(set(target)))
          return

      domain,target = resolve_spatial_nodes(p[1],p[3])
      if not isspatial(domain) and not isspatial(target):
        if p[2] == ">": #upstream
          next_domain = [search_relatives(node, target,"successors") for node in domain]
        else:
          next_domain = [search_relatives(node, target,"predecessors") for node in domain]
        next_domain = filter(lambda x: x, next_domain)
        p[0] = self.lastvalue=filter_dup_uids(next_domain)
      elif not isspatial(domain) and isspatial(target): #nodes in an area
        domain_areas = nodes_to_areas(domain)
        domain,target = resolve_spatial_nodes(domain_areas, p[3])
        while not (domain and target):
          domain,target = resolve_spatial_nodes(domain_areas, p[3])
        p[0] = self.lastvalue = areas_to_nodes(domain)
      else:
        p[0] = self.lastvalue=domain

    def p_query_immediate(self, p):
        '''query : query UPSTREAMIMM set
                 | query DOWNSTREAMIMM set'''
        querynodes, setnodes = resolve_spatial_nodes(p[1],p[3])
        if p[2] == '>>':
            direction = 'upstream'
        else:
            direction = 'downstream'
        p[0] = self.lastvalue = find_immediate(querynodes, setnodes, direction)



    def p_query_set(self, p):
        '''query : set'''
        p[0] = self.last_value = p[1]


    def p_error(self, p):
        pass
