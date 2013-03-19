from node import Relational
from generic_objects import *
from bacnet_devices import *
import networkx as nx
import sys
import gis
import node_types
import smap
from smap import archiver
from smap.archiver import client
c = client.SmapClient('http://ar1.openbms.org:8079')

# Lights
l = Relational('Lights')
# Floor 4
lightbank4_1 = LIG(l, 'Light Bank 1', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY12",'6c87b20e-454a-5343-8776-f7377aa105f1'),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY11",'b48ca62b-425c-54a5-8b9e-87784201eef2')
                        })
lightbank4_2 = LIG(l, 'Light Bank 2', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY10",'441afaab-1712-56a1-a55e-e405601edfc2'),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY09",'7bf7569c-4578-52ed-8a65-08e695206a08')
                        })
lightbank4_3 = LIG(l, 'Light Bank 3', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY08",'6841a6f5-0820-5e43-becb-453bffb2c990'),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY07",'12684335-8922-548b-bc10-a896b2a4e713')
                        })
lightbank4_4 = LIG(l, 'Light Bank 4', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY04","960db648-0d55-5cd8-abb7-f8243be52d7d"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY03","f4d8ce79-20e6-55e1-8dcc-7872dcf849a5")
                      })

lightbank4_5 = LIG(l, 'Light Bank 5', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86007/RELAY06","c11a58b4-c806-5296-b542-ba093d5ed71e"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86007/RELAY05","b5dcb3f4-7083-5988-b4a1-119efc7623a5")
                        })
# Floor 5
lightbank5_1 = LIG(l, 'Light Bank 1', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY10","07f8b407-ab1e-5b9e-b0f9-706df33836c2"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY11","6d17ed21-1d71-5872-9bcd-11325dbde034")
                        })
lightbank5_2 = LIG(l, 'Light Bank 2', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY12","caa7cd5a-1de7-5f19-aed2-7da21169c1cc"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY13","b957d4e1-52cb-5f82-8739-e07cc34fca20")
                        })
lightbank5_3 = LIG(l, 'Light Bank 3', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY07","7d489e43-dedf-5964-9b07-58231250950c"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY06","8f74e013-1fd3-55d4-8fc3-f62cb3034ccf")
                        })
lightbank5_4 = LIG(l, 'Light Bank 4', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY09","47cf2d95-e654-5012-8e0c-5a318a95bd72"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY08","73192153-d25b-502c-a46d-98b6dba06d32")
                        })
lightbank5_5 = LIG(l, 'Light Bank 5', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY05","08680d31-28cb-5092-890a-a1541c027c10"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY04","92fce355-f665-5cf3-9f68-dda7454e4cc2")
                        })
lightbank5_6 = LIG(l, 'Light Bank 6', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86008/RELAY03","b38284da-a9ed-5b40-a206-f3e4f3302f83"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86008/RELAY02","c528235b-d4d0-544f-86b3-2e24536cce0b")
                        })

# Floor 6
lightbank6_1 = LIG(l, 'Light Bank 1', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86010/RELAY03","2d9f2ffd-dd53-5e64-8ed6-eb57441f83b7"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86010/RELAY02","33ee9b3c-2891-579f-8106-137f5a281d6b")
                      })

# Floor 7
lightbank7_1 = LIG(l, 'Light Bank 1', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86011/RELAY09","070af478-b12b-53ea-b0b9-c7833870723b"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86011/RELAY08","80df2c64-36d2-58d5-bb80-16999eb94408")
                      })
lightbank7_2 = LIG(l, 'Light Bank 2', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86011/RELAY11","0deb8b0e-5d9c-5e47-abb2-3b33b2570687"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86011/RELAY10","68fe6fd7-611a-50cf-a020-aebb5f222618")
                        })
lightbank7_3 = LIG(l, 'Light Bank 3', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86011/RELAY05","bbb2b35a-4bba-504a-a904-ace590e86449"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86011/RELAY04","e25a1409-f2ac-585c-92d2-f712126d3321")
                        })
lightbank7_4 = LIG(l, 'Light Bank 4', {
                        'LO_REL' : BACnetREL( "Low Relay", "/WS86011/RELAY07","9c3b8e2a-b5cc-58fe-b408-264ad767daf9"),
                        'HI_REL' : BACnetREL( "High Relay", "/WS86011/RELAY06","2ceedbb3-571e-501a-a3b4-aaab6d79c30f")
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

#Air Handler 1
hvac = Relational('HVAC')
ah1 = AHU(hvac, 'Air Handler 1', {
            'OUT_AIR_DMP': BACnetDMP('Outside Air Damper','BACnet point name', 'BACnet setpoint name'),
            'OUT_AIR_TMP_SEN': BACnetSEN('Outside Air Temp Sensor','BACnet point name'),
            'MIX_AIR_TMP_SEN': BACnetSEN('Mixed Air Temp Sensor','BACnet point name'),
            'RET_FAN': BACnetFAN('Return Fan','BACnet point name'),
            'EXH_AIR_DMP': BACnetDMP('Exhaust Air Damper','BACnet point name', 'BACnet setpoint name'),
            'RET_AIR_HUM_SEN': BACnetSEN('Return Air Humidity Sensor','BACnet point name'),
            'RET_AIR_TMP_SEN': BACnetSEN('Return Air Temp Sensor','BACnet point name'),
            'RET_AIR_DMP': BACnetDMP('Return Air Damper','BACnet point name', 'BACnet setpoint name'),
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
def get_uuid(pointname, metadata):
    """
    Searches list of [metadata] for something resembling [pointname] and returns the uuid
    """
    for item in metadata:
        if pointname in item['Metadata']['PointName']:
            return item['uuid']
    return None

def make_vav(floor, number, has_heat_cool=True, pxcm_number=11):
    global hvac, hwl, cwl, ah1, ah2
    path = '/SDH.PXCM-{:02}/SDH/S{:1}-{:02}/'.format(pxcm_number, floor, number)
    pointsearch = 'SDH.S{:1}-{:02}%'.format(floor,number)
    metadata = c.query("select uuid, Metadata/PointName where Metadata/PointName like '{0}'".format(pointsearch))
    children = {
        'AIR_VOLUME':BACnetSEN('Air Volume', path + 'AIR_VOLUME', uid=get_uuid('AIR VOLUME',metadata)),
        'CLG_LOOPOUT':BACnetSEN('cooling temperature control loop output value', path + 'CLG_LOOPOUT', uid=get_uuid('CLG LOOPOUT',metadata)),
        'CTL_FLOW_MAX':BACnetSEN('CTL Flow Max', path + 'CTL_FLOW_MAX', uid=get_uuid('CTL FLOW MAX', metadata)),
        'CTL_FLOW_MIN':BACnetSEN('CTL Flow Min', path + 'CTL_FLOW_MIN', uid=get_uuid('CTL FLOW MIN', metadata)),
        'CTL_STPT':BACnetSEN('CTL Setpoint', path + 'CTL_STPT', uid=get_uuid('CTL STPT', metadata)),
        'DMPR_POS':BACnetDMP('Damper', path + 'DMPR_POS', path + 'DMPR_COMD', uid=get_uuid('DMPR POS', metadata)),
        'ROOM_TEMP':BACnetSEN('Room temperature', path + 'ROOM_TEMP', uid=get_uuid('ROOM TEMP', metadata)),
        }
    if has_heat_cool:
        children.update({
        'HEAT.COOL':BACnetSEN('heat.cool', path + 'HEAT.COOL', uid=get_uuid('HEAT COOL', metadata)),
        'HTG_LOOPOUT':BACnetSEN('HTG Loopout', path + 'HTG Loopout', uid=get_uuid('HTG LOOPOUT', metadata)),
        'VLV_POS':BACnetVLV('VLV (valve)', path + 'VLV_POS', path + 'VLV_COMD', uid=get_uuid('VLV POS', metadata)),
        })
    vav = VAV(hvac, 'VAV ' + str(number), children)
    ah1.add_child(vav)
    # ah1['SUP_AIR_FAN'].add_child(vav['EXH_AIR_FAN'])
    # ah2['SUP_AIR_FAN'].add_child(vav['EXH_AIR_FAN'])
    # hwl['HOT_WAT_SUP_TMP_SEN'].add_child(vav['EXH_AIR_FAN'])
    # vav['EXH_AIR_FAN'].add_child(hwl['HOT_WAT_RET_TMP_SEN'])
    # vav['EXH_AIR_FAN'].add_child(cwl['CHL_WAT_PRS_DIF_SEN'])

    floor_name = 'Floor ' + str(floor)
    area_name = 'VAV ' + str(number)
    if 'Sutardja Dai Hall' in gis.buildings:
        sdh = gis.buildings['Sutardja Dai Hall']
        #if '4' not in floor_name: return
        if floor_name in sdh and area_name in sdh[floor_name]:
            vav.add_area(sdh[floor_name][area_name])
        else:
            print 'VAV', number, 'on floor', floor, 'has no GIS area'
    else:
        print 'VAV GIS table not found'

    return vav

for x in range(1, 21 + 1):
    make_vav(4, x, (x != 10 and x != 14))

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
