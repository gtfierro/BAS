from node import Relational
from bacnet_classes import *

x = Relational('Everything')
ah1 = BacNetAH(x, 'Air Handler 1')

sf1 = BacNetFAN(ah1, name="Supply Fan 1")
rats = BacNetSEN(ah1, name='Return Air Temp Sensor')
raps = BacNetSEN(ah1, name='Return Air Pressure Sensor')
rahs = BacNetSEN(ah1, name='Return Air Humidity Sensor')
rafs = BacNetSEN(ah1, name='Return Air Flow Sensor')

rf1 = BacNetFAN(ah1, name="Return Fan 1")

ead = BacNetDMP(ah1, name="Exhaust Air Damper")
mats = BacNetSEN(ah1, name="Mixed Air Temp Sensor")
oats = BacNetSEN(ah1, name='Outside Air Temp Sensor')
dmp2 = BacNetDMP(ah1, name="Outside Air Damper")

ccv1 = BacNetCCV(ah1, name="Cooling Valve 1")

dmp3 = BacNetDMP(ah1, name="Return Air Damper")
sffs = BacNetSEN(ah1, name="Supply Fan Air Flow Sensor")
sats = BacNetSEN(ah1, name="Supply Air Temp Sensor")
saps1 = BacNetSEN(ah1, name="Supply Air Pressure Sensor 1")
saps2 = BacNetSEN(ah1, name="Supply Air Pressure Sensor 2")

ah1.add_nodes([sf1,rats,raps,rahs,rafs,rf1,ead,mats,oats,dmp2,ccv1,dmp3,sffs,sats,saps1,saps2])

rats.add_child(rf1)
raps.add_child(rf1)
rahs.add_child(rf1)
rafs.add_child(rf1)

rf1.add_child(ead)
rf1.add_child(mats)
oats.add_child(mats)
mats.add_child(ccv1)
ccv1.add_child(sf1)
sf1.add_child(sffs)
sffs.add_child(sats)
sats.add_child(saps1)
saps1.add_child(saps2)
