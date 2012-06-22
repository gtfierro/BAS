from node import Relational
from classes import *
from bacnet_drivers import *
import gis

# Delete all NodeLink objects: we don't have persistent UUIDs so they need to be
# regenerated each time
gis.NodeLink.objects.all().delete()

l = Relational('Lights')
lightbank1 = LIG(l, 'Light Bank 1', {
                      'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY11"),
                      'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY12")
                      })
lightbank2 = LIG(l, 'Light Bank 2', {
                      'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY09"),
                      'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY10")
                      })
lightbank3 = LIG(l, 'Light Bank 3', {
                      'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY07"),
                      'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY08")
                      })
lightbank4 = LIG(l, 'Light Bank 4', {
                      'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY03"),
                      'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY04")
                      })
lightbank5 = LIG(l, 'Light Bank 5', {
                      'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY05"),
                      'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY06")
                      })

sdh = gis.Building.objects.get(name='Sutardja Dai Hall')
lightbank1.areas.add(sdh['Floor4']['Zone1'])
lightbank2.areas.add(sdh['Floor4']['Zone2'])
lightbank3.areas.add(sdh['Floor4']['Zone3'])
lightbank4.areas.add(sdh['Floor4']['Zone4'])
lightbank5.areas.add(sdh['Floor4']['Zone5'])

hvac = Relational('HVAC')
ah1 = AHU(hvac, 'Air Handler 1', {
            'OUT_AIR_DMP': BACnetDMP('Outside Air Damper','BACnet point name'),
            'OUT_AIR_TMP_SEN': BACnetSEN('Outside Air Temp Sensor','BACnet point name'),
            'MIX_AIR_TMP_SEN': BACnetSEN('Mixed Air Temp Sensor','BACnet point name'),
            'RET_FAN': BACnetFAN('Return Fan','BACnet point name'),
            'EXH_AIR_DMP': BACnetDMP('Exhaust Air Damper','BACnet point name'),
            'RET_AIR_HUM_SEN': BACnetSEN('Return Air Humidity Sensor','BACnet point name'),
            'RET_AIR_TMP_SEN': BACnetSEN('Return Air Temp Sensor','BACnet point name'),
            'RET_AIR_DMP': BACnetDMP('Return Air Damper','BACnet point name'),
            'RET_AIR_PRS_SEN': BACnetSEN('Return Air Pressure Sensor','BACnet point name'),
            'RET_AIR_FLW_SEN': BACnetSEN('Return Air Flow Sensor','BACnet point name'),
            'COO_VLV': BACnetVLV('Cooling Valve','BACnet point name'),
            'SUP_AIR_FAN': BACnetFAN('Supply Air Fan','BACnet point name'),
            'SUP_AIR_FLW_SEN': BACnetSEN('Supply Air Flow Sensor','BACnet point name'),
            'SUP_AIR_TMP_SEN': BACnetSEN('Supply Air Temp Sensor','BACnet point name'),
            'SUP_AIR_PRS_SEN': BACnetSEN('Supply Air Pressure Sensor','BACnet point name'),
          })
ah1['OUT_AIR_DMP'].add_child(ah1['OUT_AIR_TMP_SEN'])
ah1['OUT_AIR_TMP_SEN'].add_child(ah1['MIX_AIR_TMP_SEN'])
ah1['MIX_AIR_TMP_SEN'].add_child(ah1['COO_VLV'])
ah1['COO_VLV'].add_child(ah1['SUP_AIR_FAN'])
ah1['SUP_AIR_FAN'].add_child(ah1['SUP_AIR_FLW_SEN'])
ah1['SUP_AIR_FLW_SEN'].add_child(ah1['SUP_AIR_TMP_SEN'])
ah1['SUP_AIR_TMP_SEN'].add_child(ah1['SUP_AIR_PRS_SEN'])
#rats.add_child(rf1)
#raps.add_child(rf1)
#rahs.add_child(rf1)
#rafs.add_child(rf1)
#
#rf1.add_child(ead)
#rf1.add_child(mats)
#oats.add_child(mats)
#mats.add_child(ccv1)
#ccv1.add_child(sf1)
#sf1.add_child(sffs)
#sffs.add_child(sats)
#sats.add_child(saps1)
#saps1.add_child(saps2)
#dmp3.add_child(rats)
#dmp2.add_child(oats)
#
#
#ah2 = BacNetAH(x, 'Air Handler 2')
#
#sf1 = BacNetFAN(ah1, name="Supply Fan 1")
#rats = BacNetSEN(ah1, name='Return Air Temp Sensor')
#raps = BacNetSEN(ah1, name='Return Air Pressure Sensor')
#rahs = BacNetSEN(ah1, name='Return Air Humidity Sensor')
#rafs = BacNetSEN(ah1, name='Return Air Flow Sensor')
#
#rf1 = BacNetFAN(ah1, name="Return Fan 1")
#
#ead = BacNetDMP(ah1, name="Exhaust Air Damper")
#mats = BacNetSEN(ah1, name="Mixed Air Temp Sensor")
#oats = BacNetSEN(ah1, name='Outside Air Temp Sensor')
#dmp2 = BacNetDMP(ah1, name="Outside Air Damper")
#
#ccv1 = BacNetCCV(ah1, name="Cooling Valve 1")
#
#dmp3 = BacNetDMP(ah1, name="Return Air Damper")
#sffs = BacNetSEN(ah1, name="Supply Fan Air Flow Sensor")
#sats = BacNetSEN(ah1, name="Supply Air Temp Sensor")
#saps1 = BacNetSEN(ah1, name="Supply Air Pressure Sensor 1")
#saps2 = BacNetSEN(ah1, name="Supply Air Pressure Sensor 2")
#
#ah2.add_nodes([sf1,rats,raps,rahs,rafs,rf1,ead,mats,oats,dmp2,ccv1,dmp3,sffs,sats,saps1,saps2])
#
#rats.add_child(rf1)
#raps.add_child(rf1)
#rahs.add_child(rf1)
#rafs.add_child(rf1)
#
#rf1.add_child(ead)
#rf1.add_child(mats)
#oats.add_child(mats)
#mats.add_child(ccv1)
#ccv1.add_child(sf1)
#sf1.add_child(sffs)
#sffs.add_child(sats)
#sats.add_child(saps1)
#saps1.add_child(saps2)
