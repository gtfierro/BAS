from flask import Flask
from flask import request
from flask import jsonify
import redis
import time
import random
import ast

rdb = redis.StrictRedis(host='localhost', port=6379, db=0)

app = Flask(__name__)

@app.route('/<path:point>',methods=['GET'])
def read_point(point):
    if not rdb.exists(point):
        rdb.set(point, random.randint(0,3))
    return jsonify({'Readings': (time.time(),rdb.get(point)) })

@app.route('/<path:point>', methods=['POST','PUT'])
def write_point(point):
    data = ast.literal_eval(request.data)
    rdb.set(point, data['value'])
    return jsonify({point: rdb.get(point)})
 
if __name__=="__main__":
    app.run(debug=True,port=8080)
