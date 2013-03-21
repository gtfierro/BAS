from baslexer import BasLexer
from basparser import BasParser

lexer = BasLexer().build()
parser = BasParser().build()

cache = {}
def query(string):
    if string not in cache:
      cache[string] = parser.parse(string)
      if not cache[string]:
        cache[string] = 'none'
    elif cache[string] == 'none':
      cache[string] = parser.parse(string)
    return cache[string]

def get_uuid(u):
  res = []
  for r in basparser.domains:
    res.extend(r.search(lambda x: str(x.uid) == u))
  return res[0] if res else None

if __name__ == '__main__':
    import readline
    while True:
      try:
        q = raw_input("query> ")
      except EOFError:
        print
        break
      if not q:
        continue
      res = query(q)
      print res
