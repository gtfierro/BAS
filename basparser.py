from baslexer import BasLexer
import ply.yacc as yacc
from collections import deque

from node import *
import gis
gis.NodeLink.objects.all().delete()
import sdh_demo as sdh

domain = [getattr(sdh, i) for i in sdh.__dict__ if isinstance(getattr(sdh,i), Relational)]

class BasParser(object):
    def build(self):
        return yacc.yacc(module=self)

    tokens = BasLexer.tokens

    # STATEMENT
    def p_statement_var(self, p):
        '''statement : VAR EQUALS query'''
        pass

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
        pass

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
        pass

    # QUERY
    def p_query_direction(self, p):
        '''query : query direction set'''
        pass

    def p_query_set(self, p):
        '''query : set'''
        p[0] = self.last_value = p[1]
        pass

    # DIRECTION
    def p_direction(self, p):
        '''direction : UPSTREAM
                     | DOWNSTREAM'''
        pass

    def p_error(self, p):
        pass
