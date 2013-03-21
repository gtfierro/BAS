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

def resolve_spatial_nodes(querynodes, setnodes):
    query_is_spatial = isspatial(querynodes)
    set_is_spatial = isspatial(setnodes)
    if query_is_spatial and not set_is_spatial:
      setnodes = nodes_to_areas(setnodes)
    elif not query_is_spatial and set_is_spatial:
      setnodes = areas_to_nodes(setnodes)
    return querynodes, setnodes

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
        print 'Name:', p[0]
        res = []
        for r in domain:
            res.extend(r.search(lambda x: name_lookup in x.get_name()))
        p[0] = self.lastvalue = res

    def p_set_tag(self, p):
        '''set : TAG'''
        tag_lookup = p[1][1:].strip().replace(' ','_')
        res = []
        for r in domain:
            if tag_lookup:
                res.extend(r.search(lambda x: set_union(tag_lookup.split('_'), x.tags)))
            else:
                res.extend(r.search(lambda x: True))

        p[0] = self.lastvalue = res

    def p_set_uuid(self, p):
        '''set : UUID'''
        uuid_lookup = p[1][1:].strip()
        res = []
        print 'start?', p[0]
        for r in domain:
            res.extend(r.search(lambda x: str(x.uid) == uuid_lookup))
        p[0] = self.lastvalue = res

    def p_set_var(self, p):
        '''set : VAR'''
        p[0] = self.basvars.get(p[1],[])

    # QUERY
    def p_query(self, p):
        '''query : query UPSTREAM set
                 | query DOWNSTREAM set'''
        querynodes, setnodes = resolve_spatial_nodes(p[1],p[3])
        print querynodes
        print setnodes
        if p[2] == ">": #query upstream of set
          pass
        else: #query downstream of set
          pass

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
