import requests
import json

def read_point(point, root='http://127.0.0.1:8080/data/WattStopper'):
    r = requests.get(root + point)
    if not r:
        raise Exception, 'Request for data failed'
    time, reading = json.loads(r.text)['Readings'][-1]
    return reading

def write_point(point, value, type=None, root='http://127.0.0.1:8080/data/WattStopper'):
    if type:
        write_multiple_points({point: {'type': type, 'value': value}})
    else:
        write_multiple_points({point: {'value': value}})

def write_multiple_points(data, root='http://127.0.0.1:8080/data/WattStopper'):
    requests.post(root+'/write', json.dumps(data), headers={'content-type': 'application/json'})
