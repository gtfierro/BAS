import json

def empty_floor(image="floor_plans/"):
    return {
        "views": {
            "floorplan": {
                "mtx": [
                    [
                        9.999999974752427078783512e-07, 
                        9.999999974752427078783512e-07, 
                        -122.258762000000004377398
                        ], 
                    [
                        0, 
                        -1.000000004580670065479353e-06, 
                        37.87483600000000194540917
                        ]
                    ], 
                "image": image
                }
            },
        "areas": {}
        }

def empty_area(type="none"):
    return {
        "regions": [
            [
                [
                    -122.2583280000000058862497, 
                     37.87485699999999866349754
                     ], 
                [
                    -122.2582940000000064628694, 
                     37.87477200000000010504664
                     ], 
                [
                    -122.2581289999999967221811, 
                     37.87480899999999905958248
                     ], 
                [
                    -122.2581619999999986703187, 
                     37.87489500000000219870344
                     ], 
                [
                    -122.2583280000000058862497, 
                     37.87485699999999866349754
                     ]
                ]
            ],
        "streams": [],
        "metadata": { "Type": type }
        }


class Building(object):
    def __init__(self, name, floors=None):
        if isinstance(floors, list):
            f = dict(zip(floors, [empty_floor() for _ in range(len(floors))]))
        elif isinstance(floors, dict):
            f = floors
        else:
            f = {}
        self.obj = {'name': name, 'floors':f}

    def add_floor(self, name):
        self.obj['floors'][name] = empty_floor()

    def add_area(self, floor, area, type='null'):
        assert floor in self.obj['floors'], "Invalid floor"
        self.obj['floors'][floor]['areas'][area] = empty_area(type)

    def dump(self, file):
        json.dump(self.obj, file)

    def dumps(self):
        json.dumps(self.obj)

    def register(self):
        import gis
        return gis.Building.from_dict(self.obj)

################################################################################

## Create a building with some floors
#b = Building('Test Building', ['Floor 1', 'Floor 2', 'Floor 3'])
#
## Add more floors programmatically
#b.add_floor('Floor 4')
#
## New lighting zone. (The third argument is type. 'lighting' is used for lighting zones,
##                   'hvac' for VAVs, and 'thermostat' for physical thermostat locations)
#b.add_area('Floor 1', 'Zone 1', 'lighting')
#
## New VAV area
#b.add_area('Floor 1', 'VAV 12', 'hvac')
#
## Write JSON to a file
### The final JSON file should then be copied to the data/ directory, and createdb.sh
### should be modified to load it into the database automatically
## b.dump(open('test.json', 'w'))
#
## Or the data can be written directly to the database
#b.register()
