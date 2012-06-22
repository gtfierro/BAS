from node import Relational
from classes import *
from bacnet_drivers import *
import gis

# Delete all NodeLink objects: we don't have persistent UUIDs so they need to be
# regenerated each time
gis.NodeLink.objects.all().delete()

#Lights
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

sdh_floor4 = gis.buildings['Sutardja Dai Hall']['Floor4']
lightbank1.areas.add(sdh_floor4['Zone1'])
lightbank2.areas.add(sdh_floor4['Zone2'])
lightbank3.areas.add(sdh_floor4['Zone3'])
lightbank4.areas.add(sdh_floor4['Zone4'])
lightbank5.areas.add(sdh_floor4['Zone5'])

#Air Handler 1
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
ah1['RET_FAN'].add_child(ah1['EXH_AIR_DMP'])
ah1['RET_AIR_PRS_SEN'].add_child(ah1['RET_FAN'])
ah1['RET_AIR_FLW_SEN'].add_child(ah1['RET_FAN'])
ah1['RET_AIR_HUM_SEN'].add_child(ah1['RET_FAN'])
ah1['RET_AIR_TMP_SEN'].add_child(ah1['RET_FAN'])
ah1['RET_AIR_DMP'].add_child(ah1['RET_AIR_TMP_SEN'])
ah1['RET_FAN'].add_child(ah1['MIX_AIR_TMP_SEN'])

#Air Handler 2
ah2 = AHU(hvac, 'Air Handler 2', {
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
ah2['OUT_AIR_DMP'].add_child(ah2['OUT_AIR_TMP_SEN'])
ah2['OUT_AIR_TMP_SEN'].add_child(ah2['MIX_AIR_TMP_SEN'])
ah2['MIX_AIR_TMP_SEN'].add_child(ah2['COO_VLV'])
ah2['COO_VLV'].add_child(ah2['SUP_AIR_FAN'])
ah2['SUP_AIR_FAN'].add_child(ah2['SUP_AIR_FLW_SEN'])
ah2['SUP_AIR_FLW_SEN'].add_child(ah2['SUP_AIR_TMP_SEN'])
ah2['SUP_AIR_TMP_SEN'].add_child(ah2['SUP_AIR_PRS_SEN'])
ah2['RET_FAN'].add_child(ah2['EXH_AIR_DMP'])
ah2['RET_AIR_PRS_SEN'].add_child(ah2['RET_FAN'])
ah2['RET_AIR_FLW_SEN'].add_child(ah2['RET_FAN'])
ah2['RET_AIR_HUM_SEN'].add_child(ah2['RET_FAN'])
ah2['RET_AIR_TMP_SEN'].add_child(ah2['RET_FAN'])
ah2['RET_AIR_DMP'].add_child(ah2['RET_AIR_TMP_SEN'])
ah2['RET_FAN'].add_child(ah2['MIX_AIR_TMP_SEN'])

#Cold Water Loop 
cwl = CWL(hvac, 'Cold Water Loop', {
            'CON_WAT_COO_TOW': BACnetTOW('Condensed Water Cooling Tower','BACNet point name'),
            'CON_WAT_SUP_TMP_SEN': BACnetSEN('Condensed Water Supply Temp Sensor','BACNet point name'),
            'CON_WAT_PMP': BACnetPMP('Condensed Water Pump','BACNet point name'),
            'CON_CHL_WAT_CHR': BACnetCHR('Condensed to Chilled Water Chiller','BACNet point name'),
            'CON_WAT_RET_TMP_SEN': BACnetSEN('Condensed Water Return Temp Sensor','BACNet point name'),
            'CHL_WAT_SUP_TMP_SEN': BACnetSEN('Chilled Water Supply Temp Sensor','BACNet point name'),
            'CHL_WAT_RET_TMP_SEN':  BACnetSEN('Chilled Water Return Temp Sensor','BACNet point name'),
            'CHL_WAT_PMP': BACnetPMP('Chilled Water Pump','BACNet point name'),
            'CHL_WAT_PRS_DIF_SEN':  BACnetSEN('Chilled Water Pressure Difference Sensor','BACNet point name'),
  })
cwl['CON_WAT_COO_TOW'].add_child(cwl['CON_WAT_SUP_TMP_SEN'])
cwl['CON_WAT_SUP_TMP_SEN'].add_child(cwl['CON_WAT_PMP'])
cwl['CON_WAT_PMP'].add_child(cwl['CON_CHL_WAT_CHR'])
cwl['CON_CHL_WAT_CHR'].add_child(cwl['CON_WAT_RET_TMP_SEN'])
cwl['CON_WAT_RET_TMP_SEN'].add_child(cwl['CON_WAT_COO_TOW'])
cwl['CON_CHL_WAT_CHR'].add_child(cwl['CHL_WAT_SUP_TMP_SEN'])
cwl['CHL_WAT_RET_TMP_SEN'].add_child(cwl['CHL_WAT_PMP'])
cwl['CHL_WAT_RET_TMP_SEN'].add_child(cwl['CHL_WAT_PRS_DIF_SEN'])
cwl['CHL_WAT_PMP'].add_child(cwl['CON_CHL_WAT_CHR'])
cwl['CHL_WAT_SUP_TMP_SEN'].add_child(ah1['COO_VLV'])
cwl['CHL_WAT_SUP_TMP_SEN'].add_child(ah2['COO_VLV'])

#cwl.add_child(ah1)
#cwl.add_child(ah2)

