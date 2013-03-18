from flask import Flask
from flask import request
from flask import jsonify
import redis
import time
import random
import ast

from smap.archiver import client
c = client.SmapClient('http://ar1.openbms.org:8079')

rdb = redis.StrictRedis(host='localhost', port=6379, db=0)

app = Flask(__name__)

@app.route('/<path:point>',methods=['GET'])
def read_point(point):
    if not rdb.exists(point):
        res = c.query('select data before now limit 1 where uuid="{0}"'.format(point))
        if res:
            print 'from sMAP'
            rdb.set(point, res[0]['Readings'][0][1])
        else:
            print 'random'
            rdb.set(point, random.randint(0,3))
    return jsonify({'Readings': (time.time(),rdb.get(point)) })

@app.route('/<path:point>', methods=['PUT'])
def write_point(point):
    newstate = request.args.get('state')
    if rdb.exists(point):
        rdb.set(point, newstate)
    return jsonify({'Readings': (time.time(), rdb.get(point))})
 
if __name__=="__main__":
    app.run(debug=True,port=8080)
