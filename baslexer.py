import ply.lex as lex

class BasLexer(object):
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    tokens = [
        'NAME', 'UUID', 'VAR', 'TAG', 'SPATIAL',
        'UPSTREAM', 'DOWNSTREAM', 'EQUALS', 'LASTVALUE',
        'LPAREN', 'RPAREN',
        'UPSTREAMIMM', 'DOWNSTREAMIMM'
        ]

    t_UPSTREAM    = r'>'
    t_DOWNSTREAM  = r'<'
    t_UPSTREAMIMM    = r'>>'
    t_DOWNSTREAMIMM  = r'<<'
    t_LPAREN      = r'\('
    t_RPAREN      = r'\)'
    #t_LBRACK      = r'\['
    #t_RBRACK      = r'\]'
    t_EQUALS      = r'='
    t_ignore      = ' \t'

    def t_NAME(self,t):
        r'\$[^!][\w\-\:\_\s]+'
        t.value = t.value.strip()
        return t

    def t_TAG(self,t):
        r'(\.|\#|\&)([^!]?[A-Z_ ]+)?[ ]?'
        t.value = t.value.strip()
        return t

    def t_SPATIAL(self,t):
        r'!\#?([\w\-\:\_\s]+)?'
        t.value = t.value.strip()
        return t

    def t_UUID(self,t):
        r'(\%|\^)[^!]?[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}[ ]?'
        t.value = t.value.strip()
        return t

    def t_VAR(self,t):
        r'\@[^!]?[a-zA-Z_][a-zA-Z0-9_]*[ ]?'
        t.value = t.value.strip()
        return t

    def t_LASTVALUE(self,t):
        r'\b\_\b'
        t.value = t.value.strip()
        return t

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
