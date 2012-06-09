from node import *
from bacnet_classes import *


## COMMENT: why specify the type as a string here?
x = Relational('Everything')
ah1 = BacNetAH('AH', x, 'Air Handler 1')

sf1 = BacNetFAN("SF", ah1, name="Supply fan 1")
sf1.set_attribute("fan speed", "SDH.AH1A.SF_VFD:Input ref1")
sf1.set_attribute("fan power", "SDH.AH1A.SF_VFD:POWER")

rf1 = BacNetFAN("RF", ah1, name="Return fan 1")
rf1.set_attribute("fan speed", "SDH.AH1A.SF_VFD:Input ref1")
rf1.set_attribute("fan power", "SDH.AH1A.SF_VFD:POWER")

ccv1 = BacNetCCV("CCV", ah1, name="cooling valve 1")
dmp1 = BacNetDMP("DMP", ah1, name="Exhaust damper")
dmp2 = BacNetDMP("DMP", ah1, name="Outside Air Damper")
dmp3 = BacNetDMP("DMP", ah1, name="Return Air Damper")
ps1 = BacNetSEN("PS", ah1, name="Pressure Sensor 1")
ts1 = BacNetSEN("TS", ah1, name="Temperature Sensor 1")
hs1 = BacNetSEN("HS", ah1, name="Humidity Sensor 1")
as1 = BacNetSEN("AS", ah1, name="Airflow Sensor 1")

ah1.add_nodes([sf1,rf1,ccv1,dmp1,dmp2,dmp3,ps1,ts1,hs1,as1])

dmp2.add_child(ccv1)
dmp2.add_child(dmp3)
dmp3.add_child(dmp1)
dmp3.add_child(rf1)
ccv1.add_child(sf1)
