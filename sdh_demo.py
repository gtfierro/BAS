from node import Relational
from generic_objects import *
from bacnet_devices import *
import networkx as nx
import sys
import gis
import node_types

# Lights
l = Relational('Lights')
# Floor 4
lightbank4_1 = LIG(l, 'Light Bank 1', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY12"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY11")
                        })
lightbank4_2 = LIG(l, 'Light Bank 2', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY10"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY09")
                        })
lightbank4_3 = LIG(l, 'Light Bank 3', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY08"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY07")
                        })
lightbank4_4 = LIG(l, 'Light Bank 4', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY04"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY03")
                      })

lightbank4_5 = LIG(l, 'Light Bank 5', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY06"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY05")
                        })
# Floor 5
lightbank5_1 = LIG(l, 'Light Bank 1', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY10"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY11")
                        })
lightbank5_2 = LIG(l, 'Light Bank 2', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY12"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY13")
                        })
lightbank5_3 = LIG(l, 'Light Bank 3', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY07"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY06")
                        })
lightbank5_4 = LIG(l, 'Light Bank 4', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY09"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY08")
                        })
lightbank5_5 = LIG(l, 'Light Bank 5', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY05"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY04")
                        })
lightbank5_6 = LIG(l, 'Light Bank 6', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY03"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY02")
                        })

# Floor 6
lightbank6_1 = LIG(l, 'Light Bank 1', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86010/RELAY03"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86010/RELAY02")
                      })

# Floor 7
lightbank7_1 = LIG(l, 'Light Bank 1', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86011/RELAY09"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86011/RELAY08")
                      })
lightbank7_2 = LIG(l, 'Light Bank 2', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86011/RELAY11"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86011/RELAY10")
                        })
lightbank7_3 = LIG(l, 'Light Bank 3', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86011/RELAY05"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86011/RELAY04")
                        })
lightbank7_4 = LIG(l, 'Light Bank 4', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86011/RELAY07"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86011/RELAY06")
                      })


if 'Sutardja Dai Hall' in gis.buildings:
    sdh_floor4 = gis.buildings['Sutardja Dai Hall']['Floor 4']
    lightbank4_1.add_area(sdh_floor4['Zone 1'])
    lightbank4_2.add_area(sdh_floor4['Zone 2'])
    lightbank4_3.add_area(sdh_floor4['Zone 3'])
    lightbank4_4.add_area(sdh_floor4['Zone 4'])
    lightbank4_5.add_area(sdh_floor4['Zone 5'])

    sdh_floor6 = gis.buildings['Sutardja Dai Hall']['Floor 6']
    lightbank6_1.add_area(sdh_floor6['Zone 1'])

    sdh_floor7 = gis.buildings['Sutardja Dai Hall']['Floor 7']
    lightbank7_1.add_area(sdh_floor7['Zone 1'])
    lightbank7_2.add_area(sdh_floor7['Zone 2'])
    lightbank7_3.add_area(sdh_floor7['Zone 3'])
    lightbank7_4.add_area(sdh_floor7['Zone 4'])

##Air Handler 1
#hvac = Relational('HVAC')
#ah1 = AHU(hvac, 'Air Handler 1', {
#            'OUT_AIR_DMP': BACnetDMP('Outside Air Damper','BACnet point name', 'BACnet setpoint name'),
#            'OUT_AIR_TMP_SEN': BACnetSEN('Outside Air Temp Sensor','BACnet point name'),
#            'MIX_AIR_TMP_SEN': BACnetSEN('Mixed Air Temp Sensor','BACnet point name'),
#            'RET_FAN': BACnetFAN('Return Fan','BACnet point name'),
#            'EXH_AIR_DMP': BACnetDMP('Exhaust Air Damper','BACnet point name', 'BACnet setpoint name'),
#            'RET_AIR_HUM_SEN': BACnetSEN('Return Air Humidity Sensor','BACnet point name'),
#            'RET_AIR_TMP_SEN': BACnetSEN('Return Air Temp Sensor','BACnet point name'),
#            'RET_AIR_DMP': BACnetDMP('Return Air Damper','BACnet point name', 'BACnet setpoint name'),
#            'RET_AIR_PRS_SEN': BACnetSEN('Return Air Pressure Sensor','BACnet point name'),
#            'RET_AIR_FLW_SEN': BACnetSEN('Return Air Flow Sensor','BACnet point name'),
#            'COO_VLV': BACnetVLV('Cooling Valve','BACnet point name'),
#            'SUP_AIR_FAN': BACnetFAN('Supply Air Fan','BACnet point name'),
#            'SUP_AIR_FLW_SEN': BACnetSEN('Supply Air Flow Sensor','BACnet point name'),
#            'SUP_AIR_TMP_SEN': BACnetSEN('Supply Air Temp Sensor','BACnet point name'),
#            'SUP_AIR_PRS_SEN': BACnetSEN('Supply Air Pressure Sensor','BACnet point name'),
#          })
#ah1['OUT_AIR_DMP'].add_child(ah1['OUT_AIR_TMP_SEN'])
#ah1['OUT_AIR_TMP_SEN'].add_child(ah1['MIX_AIR_TMP_SEN'])
#ah1['MIX_AIR_TMP_SEN'].add_child(ah1['COO_VLV'])
#ah1['COO_VLV'].add_child(ah1['SUP_AIR_FAN'])
#ah1['SUP_AIR_FAN'].add_child(ah1['SUP_AIR_FLW_SEN'])
#ah1['SUP_AIR_FLW_SEN'].add_child(ah1['SUP_AIR_TMP_SEN'])
#ah1['SUP_AIR_TMP_SEN'].add_child(ah1['SUP_AIR_PRS_SEN'])
#ah1['RET_FAN'].add_child(ah1['EXH_AIR_DMP'])
#ah1['RET_AIR_PRS_SEN'].add_child(ah1['RET_FAN'])
#ah1['RET_AIR_FLW_SEN'].add_child(ah1['RET_FAN'])
#ah1['RET_AIR_HUM_SEN'].add_child(ah1['RET_FAN'])
#ah1['RET_AIR_TMP_SEN'].add_child(ah1['RET_FAN'])
#ah1['RET_AIR_DMP'].add_child(ah1['RET_AIR_TMP_SEN'])
#ah1['RET_FAN'].add_child(ah1['MIX_AIR_TMP_SEN'])
#
##Air Handler 2
#ah2 = AHU(hvac, 'Air Handler 2', {
#            'OUT_AIR_DMP': BACnetDMP('Outside Air Damper','BACnet point name', 'BACnet setpoint name'),
#            'OUT_AIR_TMP_SEN': BACnetSEN('Outside Air Temp Sensor','BACnet point name'),
#            'MIX_AIR_TMP_SEN': BACnetSEN('Mixed Air Temp Sensor','BACnet point name'),
#            'RET_FAN': BACnetFAN('Return Fan','BACnet point name'),
#            'EXH_AIR_DMP': BACnetDMP('Exhaust Air Damper','BACnet point name', 'BACnet setpoint name'),
#            'RET_AIR_HUM_SEN': BACnetSEN('Return Air Humidity Sensor','BACnet point name'),
#            'RET_AIR_TMP_SEN': BACnetSEN('Return Air Temp Sensor','BACnet point name'),
#            'RET_AIR_DMP': BACnetDMP('Return Air Damper','BACnet point name', 'BACnet setpoint name'),
#            'RET_AIR_PRS_SEN': BACnetSEN('Return Air Pressure Sensor','BACnet point name'),
#            'RET_AIR_FLW_SEN': BACnetSEN('Return Air Flow Sensor','BACnet point name'),
#            'COO_VLV': BACnetVLV('Cooling Valve','BACnet point name', 'BACnet setpoint name'),
#            'SUP_AIR_FAN': BACnetFAN('Supply Air Fan','BACnet point name'),
#            'SUP_AIR_FLW_SEN': BACnetSEN('Supply Air Flow Sensor','BACnet point name'),
#            'SUP_AIR_TMP_SEN': BACnetSEN('Supply Air Temp Sensor','BACnet point name'),
#            'SUP_AIR_PRS_SEN': BACnetSEN('Supply Air Pressure Sensor','BACnet point name'),
#          })
#ah2['OUT_AIR_DMP'].add_child(ah2['OUT_AIR_TMP_SEN'])
#ah2['OUT_AIR_TMP_SEN'].add_child(ah2['MIX_AIR_TMP_SEN'])
#ah2['MIX_AIR_TMP_SEN'].add_child(ah2['COO_VLV'])
#ah2['COO_VLV'].add_child(ah2['SUP_AIR_FAN'])
#ah2['SUP_AIR_FAN'].add_child(ah2['SUP_AIR_FLW_SEN'])
#ah2['SUP_AIR_FLW_SEN'].add_child(ah2['SUP_AIR_TMP_SEN'])
#ah2['SUP_AIR_TMP_SEN'].add_child(ah2['SUP_AIR_PRS_SEN'])
#ah2['RET_FAN'].add_child(ah2['EXH_AIR_DMP'])
#ah2['RET_AIR_PRS_SEN'].add_child(ah2['RET_FAN'])
#ah2['RET_AIR_FLW_SEN'].add_child(ah2['RET_FAN'])
#ah2['RET_AIR_HUM_SEN'].add_child(ah2['RET_FAN'])
#ah2['RET_AIR_TMP_SEN'].add_child(ah2['RET_FAN'])
#ah2['RET_AIR_DMP'].add_child(ah2['RET_AIR_TMP_SEN'])
#ah2['RET_FAN'].add_child(ah2['MIX_AIR_TMP_SEN'])
#
##Cold Water Loop 
#cwl = CWL(hvac, 'Cold Water Loop', {
#            'CON_WAT_COO_TOW': BACnetTOW('Condensed Water Cooling Tower','BACNet point name'),
#            'CON_WAT_SUP_TMP_SEN': BACnetSEN('Condensed Water Supply Temp Sensor','BACNet point name'),
#            'CON_WAT_PMP': BACnetPMP('Condensed Water Pump','BACNet point name'),
#            'CON_CHL_WAT_CHR': BACnetCHR('Condensed to Chilled Water Chiller','BACNet point name'),
#            'CON_WAT_RET_TMP_SEN': BACnetSEN('Condensed Water Return Temp Sensor','BACNet point name'),
#            'CHL_WAT_SUP_TMP_SEN': BACnetSEN('Chilled Water Supply Temp Sensor','BACNet point name'),
#            'CHL_WAT_RET_TMP_SEN':  BACnetSEN('Chilled Water Return Temp Sensor','BACNet point name'),
#            'CHL_WAT_PMP': BACnetPMP('Chilled Water Pump','BACNet point name'),
#            'CHL_WAT_PRS_DIF_SEN':  BACnetSEN('Chilled Water Pressure Difference Sensor','BACNet point name'),
#  })
#cwl['CON_WAT_COO_TOW'].add_child(cwl['CON_WAT_SUP_TMP_SEN'])
#cwl['CON_WAT_SUP_TMP_SEN'].add_child(cwl['CON_WAT_PMP'])
#cwl['CON_WAT_PMP'].add_child(cwl['CON_CHL_WAT_CHR'])
#cwl['CON_CHL_WAT_CHR'].add_child(cwl['CON_WAT_RET_TMP_SEN'])
#cwl['CON_WAT_RET_TMP_SEN'].add_child(cwl['CON_WAT_COO_TOW'])
#cwl['CON_CHL_WAT_CHR'].add_child(cwl['CHL_WAT_SUP_TMP_SEN'])
#cwl['CHL_WAT_RET_TMP_SEN'].add_child(cwl['CHL_WAT_PMP'])
#cwl['CHL_WAT_RET_TMP_SEN'].add_child(cwl['CHL_WAT_PRS_DIF_SEN'])
#cwl['CHL_WAT_PMP'].add_child(cwl['CON_CHL_WAT_CHR'])
#cwl['CHL_WAT_SUP_TMP_SEN'].add_child(ah1['COO_VLV'])
#cwl['CHL_WAT_SUP_TMP_SEN'].add_child(ah2['COO_VLV'])
#
##Hot Water Loop
#hwl = HWL(hvac, 'Hot Water Loop', {
#            'HX': BACnetHX('Heat Exchanger','BACNet point name'),
#            'HOT_WAT_RET_TMP_SEN': BACnetSEN('Hot Water Return Temp Sensor','BACNet point name'),
#            'HOT_WAT_PRS_DIF_SEN': BACnetSEN('Hot Water Pressure Difference Sensor','BACNet point name'),
#            'HOT_WAT_PMP': BACnetPMP('Hot Water Pump','BACNet point name'),
#            'HOT_WAT_SUP_TMP_SEN': BACnetSEN('Hot Water Supply Temp Sensor','BACNet point name'),
#  })
#hwl['HX'].add_child(hwl['HOT_WAT_PMP'])
#hwl['HOT_WAT_RET_TMP_SEN'].add_child(hwl['HX'])
#hwl['HOT_WAT_PRS_DIF_SEN'].add_child(hwl['HOT_WAT_RET_TMP_SEN'])
#hwl['HOT_WAT_PMP'].add_child(hwl['HOT_WAT_SUP_TMP_SEN'])
#
#def make_vav(floor, number, has_heat_cool=True, pxcm_number=11):
#    global hvac, hwl, cwl, ah1, ah2
#    path = '/SDH.PXCM-{:02}/SDH/S{:1}-{:02}/'.format(pxcm_number, floor, number)
#    children = {
#        'AIR_VOLUME':BACnetSEN('Air Volume', path + 'AIR_VOLUME'),
#        'CLG_LOOPOUT':BACnetSEN('cooling temperature control loop output value', path + 'CLG_LOOPOUT'),
#        'CTL_FLOW_MAX':BACnetSEN('CTL Flow Max', path + 'CTL_FLOW_MAX'),
#        'CTL_FLOW_MIN':BACnetSEN('CTL Flow Min', path + 'CTL_FLOW_MIN'),
#        'CTL_STPT':BACnetSEN('CTL Setpoint', path + 'CTL_STPT'),
#        'DMPR_POS':BACnetDMP('Damper', path + 'DMPR_POS', path + 'DMPR_COMD'),
#        'ROOM_TEMP':BACnetSEN('Room temperature', path + 'ROOM_TEMP'),
#        }
#    if has_heat_cool:
#        children.update({
#        'HEAT.COOL':BACnetSEN('heat.cool', path + 'HEAT.COOL'),
#        'HTG_LOOPOUT':BACnetSEN('HTG Loopout', path + 'HTG Loopout'),
#        'VLV_POS':BACnetVLV('VLV (valve)', path + 'VLV_POS', path + 'VLV_COMD'),
#        })
#    vav = VAV(hvac, 'VAV ' + str(number), children)
#    ah1.add_child(vav)
#    ah2.add_child(vav)
#    # ah1['SUP_AIR_FAN'].add_child(vav['EXH_AIR_FAN'])
#    # ah2['SUP_AIR_FAN'].add_child(vav['EXH_AIR_FAN'])
#    # hwl['HOT_WAT_SUP_TMP_SEN'].add_child(vav['EXH_AIR_FAN'])
#    # vav['EXH_AIR_FAN'].add_child(hwl['HOT_WAT_RET_TMP_SEN'])
#    # vav['EXH_AIR_FAN'].add_child(cwl['CHL_WAT_PRS_DIF_SEN'])
#
#    floor_name = 'Floor ' + str(floor)
#    area_name = 'VAV ' + str(number)
#    if 'Sutardja Dai Hall' in gis.buildings:
#        sdh = gis.buildings['Sutardja Dai Hall']
#        if floor_name in sdh and area_name in sdh[floor_name]:
#            vav.add_area(sdh[floor_name][area_name])
#        else:
#            print 'VAV', number, 'on floor', floor, 'has no GIS area'
#    else:
#        print 'VAV GIS table not found'
#
#    return vav
#
#for x in range(1, 21 + 1):
#    make_vav(4, x, (x != 10 and x != 14))
#
#node_types.verify_devices()
#node_types.verify_objects()
#
#
#def draw_all(filename='out.png'):
#  """
#  draw every graph connected and everything yeah
#  """
#  def _make_abbreviation(string):
#    s = string.split(" ")
#    return ''.join([word[0] for word in s])
#  import matplotlib.pyplot as plt
#  plt.clf()
#  this = sys.modules[__name__]
#  relationals = [getattr(this, i) for i in this.__dict__ if isinstance(getattr(this,i), Relational)]
#  biggraph = nx.DiGraph()
#  for r in relationals:
#    for n in r._nk.nodes():
#      biggraph.add_edges_from(n._nk.edges())
#  for n in biggraph.nodes():
#    if n.external_parents:
#      for p in n.external_parents:
#        biggraph.add_edges_from(p._nk.edges())
#    if n.external_childs:
#      for c in n.external_childs:
#        biggraph.add_edges_from(c._nk.edges())
#  for n in biggraph.nodes():
#    if "." not in n.name:
#      n.name = n.name+"."+_make_abbreviation(n.container.name)
#  nx.draw_graphviz(biggraph,prog='neato',width=1,node_size=300,font_size=4,overlap='scalexy')
#  plt.savefig(filename)
