from models import *

sdh = Building(name="Sutardja Dai Hall")
sdh.save()

f = Floor(shortname='floor1', name="Floor 1",  building=sdh)
f.save()

v = View(shortname='floorplan', image='img.png', floor=f)
v.mtx = [[1, 0, 0], [0, 1, 0]]
v.save()

a = Area(shortname='area1', name="Area 1", regions='MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)))', floor=f)
a.save()
