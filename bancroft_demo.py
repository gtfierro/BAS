from node import Relational
from generic_objects import *
from bacnet_devices import *
import networkx as nx
import gis
import node_types

hvac = Relational('hvac')
doe_ah_a_and_dh_1 = AHU(hvac, 'doe_ah_a_and_dh_1',{
	'OUT_AIR_DMP':BancroftAHUDMP('Outside Air Damper','BACnet point name'),
	'OUT_AIR_TMP_SEN':BancroftSEN('Outside Air Temp Sensor','/device240102/oat'),
	'MIX_AIR_TMP_SEN':BancroftSEN('Mixed Air Temp Sensor','/device240102/aha_mat'),
	'RET_FAN':BACnetFAN('Return Fan','BACnet point name'),
	'RET_AIR_FLW_SEN':BACnetSEN('Return Air Flow Sensor','BACnet point name'),
	'EXH_AIR_DMP':BACnetDMP('Exhaust Air Damper','BACnet point name'),
	'EXH_AIR_TMP_SEN':BancroftSEN('Exhaust Air Temp Sensor','/device240102/dh1_eat'),
	'RET_AIR_HUM_SEN':BancroftSEN('Return Air Humidity Sensor','/device240102/avg_spc_hum'),
	'RET_AIR_TMP_SEN':BancroftSEN('Return Air Temp Sensor','/device240102/aha_rat'),
	'RET_AIR_DMP':BACnetDMP('Return Air Damper','BACnet point name'),
	'RET_AIR_PRS_SEN':BancroftSEN('Return Air Pressure Sensor','/device240102/a_sys_bldg_press'),
	'COO_VLV':BACnetVLV('Cooling Valve','/device240102/aha_chwv'),
	'SUP_AIR_FAN':BancroftFAN('Supply Air Fan','/device240102/m373'),
	'SUP_AIR_FLW_SEN':BancroftSEN('Supply Air Flow Sensor','/device240102/sa_cfm'),
	'SUP_AIR_TMP_SEN':BancroftSEN('Supply Air Temp Sensor','/device240102/ag_spc_temp'),
	'SUP_AIR_PRS_SEN':BACnetSEN('Supply Air Pressure Sensor','BACnet point name'),
})
doe_ah_c = AHU(hvac, 'doe_ah_c',{
	'OUT_AIR_DMP':BancroftAHUDMP('Outside Air Damper','BACnet point name'),
	'OUT_AIR_TMP_SEN':BancroftSEN('Outside Air Temp Sensor','/device240104/oat'),
	'MIX_AIR_TMP_SEN':BancroftSEN('Mixed Air Temp Sensor','/device240104/aha_mat'),
	'RET_FAN':BACnetFAN('Return Fan','BACnet point name'),
	'RET_AIR_FLW_SEN':BACnetSEN('Return Air Flow Sensor','BACnet point name'),
	'EXH_AIR_DMP':BACnetDMP('Exhaust Air Damper','BACnet point name'),
	'EXH_AIR_TMP_SEN':BancroftSEN('Exhaust Air Temp Sensor','/device240104/dh1_eat'),
	'RET_AIR_HUM_SEN':BancroftSEN('Return Air Humidity Sensor','/device240104/avg_spc_hum'),
	'RET_AIR_TMP_SEN':BancroftSEN('Return Air Temp Sensor','/device240104/aha_rat'),
	'RET_AIR_DMP':BACnetDMP('Return Air Damper','BACnet point name'),
	'RET_AIR_PRS_SEN':BancroftSEN('Return Air Pressure Sensor','/device240104/a_sys_bldg_press'),
	'COO_VLV':BACnetVLV('Cooling Valve','/device240104/aha_chwv'),
	'SUP_AIR_FAN':BancroftFAN('Supply Air Fan','/device240104/m373'),
	'SUP_AIR_FLW_SEN':BancroftSEN('Supply Air Flow Sensor','/device240104/sa_cfm'),
	'SUP_AIR_TMP_SEN':BancroftSEN('Supply Air Temp Sensor','/device240104/ag_spc_temp'),
	'SUP_AIR_PRS_SEN':BACnetSEN('Supply Air Pressure Sensor','BACnet point name'),
})
#doe_ah_b1_ah_b2_rf_1 = AHU(hvac, 'doe_ah_b1_ah_b2_rf_1',{
#	'OUT_AIR_DMP':BancroftAHUDMP('Outside Air Damper','BACnet point name'),
#	'OUT_AIR_TMP_SEN':BancroftSEN('Outside Air Temp Sensor','/device240114/oat'),
#	'MIX_AIR_TMP_SEN':BancroftSEN('Mixed Air Temp Sensor','/device240114/aha_mat'),
#	'RET_FAN':BACnetFAN('Return Fan','BACnet point name'),
#	'RET_AIR_FLW_SEN':BACnetSEN('Return Air Flow Sensor','BACnet point name'),
#	'EXH_AIR_DMP':BACnetDMP('Exhaust Air Damper','BACnet point name'),
#	'EXH_AIR_TMP_SEN':BancroftSEN('Exhaust Air Temp Sensor','/device240114/dh1_eat'),
#	'RET_AIR_HUM_SEN':BancroftSEN('Return Air Humidity Sensor','/device240114/avg_spc_hum'),
#	'RET_AIR_TMP_SEN':BancroftSEN('Return Air Temp Sensor','/device240114/aha_rat'),
#	'RET_AIR_DMP':BACnetDMP('Return Air Damper','BACnet point name'),
#	'RET_AIR_PRS_SEN':BancroftSEN('Return Air Pressure Sensor','/device240114/a_sys_bldg_press'),
#	'COO_VLV':BACnetVLV('Cooling Valve','/device240114/aha_chwv'),
#	'SUP_AIR_FAN':BancroftFAN('Supply Air Fan','/device240114/m373'),
#	'SUP_AIR_FLW_SEN':BancroftSEN('Supply Air Flow Sensor','/device240114/sa_cfm'),
#	'SUP_AIR_TMP_SEN':BancroftSEN('Supply Air Temp Sensor','/device240114/ag_spc_temp'),
#	'SUP_AIR_PRS_SEN':BACnetSEN('Supply Air Pressure Sensor','BACnet point name'),
#})
doe_vav_b_4_03n = VAV(hvac, 'doe_vav_b_4_03n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240615/flow_tab_1')})
try:
  doe_vav_b_4_03n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-03'])
except:
  print 'could not link VAV doe_vav_b-4-03'
doe_vav_b_4_13n = VAV(hvac, 'doe_vav_b_4_13n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240520/flow_tab_1')})
try:
  doe_vav_b_4_13n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-13'])
except:
  print 'could not link VAV doe_vav_b-4-13'
doe_vav_b_4_18 = VAV(hvac, 'doe_vav_b_4_18', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240616/flow_tab_1')})
try:
  doe_vav_b_4_18.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-18'])
except:
  print 'could not link VAV doe_vav_b-4-18'
doe_vav_b_4_19 = VAV(hvac, 'doe_vav_b_4_19', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240601/flow_tab_1')})
try:
  doe_vav_b_4_19.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-19'])
except:
  print 'could not link VAV doe_vav_b-4-19'
doe_vav_b_4_14 = VAV(hvac, 'doe_vav_b_4_14', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240604/flow_tab_1')})
try:
  doe_vav_b_4_14.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-14'])
except:
  print 'could not link VAV doe_vav_b-4-14'
doe_vav_b_4_15 = VAV(hvac, 'doe_vav_b_4_15', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240513/flow_tab_1')})
try:
  doe_vav_b_4_15.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-15'])
except:
  print 'could not link VAV doe_vav_b-4-15'
doe_vav_b_4_16 = VAV(hvac, 'doe_vav_b_4_16', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240511/flow_tab_1')})
try:
  doe_vav_b_4_16.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-16'])
except:
  print 'could not link VAV doe_vav_b-4-16'
doe_vav_b_4_17 = VAV(hvac, 'doe_vav_b_4_17', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240602/flow_tab_1')})
try:
  doe_vav_b_4_17.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-17'])
except:
  print 'could not link VAV doe_vav_b-4-17'
doe_vav_b_4_10 = VAV(hvac, 'doe_vav_b_4_10', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240509/flow_tab_1')})
try:
  doe_vav_b_4_10.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-10'])
except:
  print 'could not link VAV doe_vav_b-4-10'
doe_vav_b_4_11 = VAV(hvac, 'doe_vav_b_4_11', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240515/flow_tab_1')})
try:
  doe_vav_b_4_11.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-11'])
except:
  print 'could not link VAV doe_vav_b-4-11'
doe_vav_b_4_12 = VAV(hvac, 'doe_vav_b_4_12', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240517/flow_tab_1')})
try:
  doe_vav_b_4_12.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-12'])
except:
  print 'could not link VAV doe_vav_b-4-12'
doe_vav_b_4_13 = VAV(hvac, 'doe_vav_b_4_13', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240519/flow_tab_1')})
try:
  doe_vav_b_4_13.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-13'])
except:
  print 'could not link VAV doe_vav_b-4-13'
doe_vav_b_2_01 = VAV(hvac, 'doe_vav_b_2_01', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240320/flow_tab_1')})
try:
  doe_vav_b_2_01.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_b-2-01'])
except:
  print 'could not link VAV doe_vav_b-2-01'
doe_vav_b_4_14n = VAV(hvac, 'doe_vav_b_4_14n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240605/flow_tab_1')})
try:
  doe_vav_b_4_14n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-14'])
except:
  print 'could not link VAV doe_vav_b-4-14'
doe_vav_b_4_02n = VAV(hvac, 'doe_vav_b_4_02n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240613/flow_tab_1')})
try:
  doe_vav_b_4_02n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-02'])
except:
  print 'could not link VAV doe_vav_b-4-02'
doe_vav_b_3_4n = VAV(hvac, 'doe_vav_b_3_4n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240408/flow_tab_1')})
try:
  doe_vav_b_3_4n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-4'])
except:
  print 'could not link VAV doe_vav_b-3-4'
doe_vav_b_4_20 = VAV(hvac, 'doe_vav_b_4_20', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240618/flow_tab_1')})
try:
  doe_vav_b_4_20.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-20'])
except:
  print 'could not link VAV doe_vav_b-4-20'
doe_vav_b_4_05n = VAV(hvac, 'doe_vav_b_4_05n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240609/flow_tab_1')})
try:
  doe_vav_b_4_05n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-05'])
except:
  print 'could not link VAV doe_vav_b-4-05'
doe_vav_b_3_8n = VAV(hvac, 'doe_vav_b_3_8n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240416/flow_tab_1')})
try:
  doe_vav_b_3_8n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-8'])
except:
  print 'could not link VAV doe_vav_b-3-8'
doe_vav_b_3_12n = VAV(hvac, 'doe_vav_b_3_12n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240424/flow_tab_1')})
try:
  doe_vav_b_3_12n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-12'])
except:
  print 'could not link VAV doe_vav_b-3-12'
doe_vav_b_4_11n = VAV(hvac, 'doe_vav_b_4_11n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240516/flow_tab_1')})
try:
  doe_vav_b_4_11n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-11'])
except:
  print 'could not link VAV doe_vav_b-4-11'
doe_vav_b_5_02n = VAV(hvac, 'doe_vav_b_5_02n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240622/flow_tab_1')})
try:
  doe_vav_b_5_02n.add_area(gis.buildings['Bancroft Library']['5th_floor']['doe_vav_b-5-02'])
except:
  print 'could not link VAV doe_vav_b-5-02'
doe_vav_b_3_01n = VAV(hvac, 'doe_vav_b_3_01n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240402/flow_tab_1')})
try:
  doe_vav_b_3_01n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-01'])
except:
  print 'could not link VAV doe_vav_b-3-01'
doe_vav_b_4_04n = VAV(hvac, 'doe_vav_b_4_04n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240611/flow_tab_1')})
try:
  doe_vav_b_4_04n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-04'])
except:
  print 'could not link VAV doe_vav_b-4-04'
doe_vav_b_3_9n = VAV(hvac, 'doe_vav_b_3_9n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240418/flow_tab_1')})
try:
  doe_vav_b_3_9n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-9'])
except:
  print 'could not link VAV doe_vav_b-3-9'
doe_vav_b_4_12n = VAV(hvac, 'doe_vav_b_4_12n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240518/flow_tab_1')})
try:
  doe_vav_b_4_12n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-12'])
except:
  print 'could not link VAV doe_vav_b-4-12'
doe_vav_b_3_3n = VAV(hvac, 'doe_vav_b_3_3n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240406/flow_tab_1')})
try:
  doe_vav_b_3_3n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-3'])
except:
  print 'could not link VAV doe_vav_b-3-3'
doe_vav_c_2_5 = VAV(hvac, 'doe_vav_c_2_5', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240305/flow_tab_1')})
try:
  doe_vav_c_2_5.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-5'])
except:
  print 'could not link VAV doe_vav_c-2-5'
doe_vav_c_2_4 = VAV(hvac, 'doe_vav_c_2_4', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240304/flow_tab_1')})
try:
  doe_vav_c_2_4.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-4'])
except:
  print 'could not link VAV doe_vav_c-2-4'
doe_vav_c_2_7 = VAV(hvac, 'doe_vav_c_2_7', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240307/flow_tab_1')})
try:
  doe_vav_c_2_7.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-7'])
except:
  print 'could not link VAV doe_vav_c-2-7'
doe_vav_c_2_6 = VAV(hvac, 'doe_vav_c_2_6', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240306/flow_tab_1')})
try:
  doe_vav_c_2_6.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-6'])
except:
  print 'could not link VAV doe_vav_c-2-6'
doe_vav_c_2_1 = VAV(hvac, 'doe_vav_c_2_1', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240301/flow_tab_1')})
try:
  doe_vav_c_2_1.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-1'])
except:
  print 'could not link VAV doe_vav_c-2-1'
doe_vav_c_2_3 = VAV(hvac, 'doe_vav_c_2_3', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240322/flow_tab_1')})
try:
  doe_vav_c_2_3.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-3'])
except:
  print 'could not link VAV doe_vav_c-2-3'
doe_vav_c_2_2 = VAV(hvac, 'doe_vav_c_2_2', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240302/flow_tab_1')})
try:
  doe_vav_c_2_2.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-2'])
except:
  print 'could not link VAV doe_vav_c-2-2'
doe_vav_b_2_01n = VAV(hvac, 'doe_vav_b_2_01n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240321/flow_tab_1')})
try:
  doe_vav_b_2_01n.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_b-2-01'])
except:
  print 'could not link VAV doe_vav_b-2-01'
doe_vav_c_2_9 = VAV(hvac, 'doe_vav_c_2_9', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240309/flow_tab_1')})
try:
  doe_vav_c_2_9.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-9'])
except:
  print 'could not link VAV doe_vav_c-2-9'
doe_vav_c_2_8 = VAV(hvac, 'doe_vav_c_2_8', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240308/flow_tab_1')})
try:
  doe_vav_c_2_8.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-8'])
except:
  print 'could not link VAV doe_vav_c-2-8'
doe_vav_b_3_15 = VAV(hvac, 'doe_vav_b_3_15', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240428/flow_tab_1')})
try:
  doe_vav_b_3_15.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-15'])
except:
  print 'could not link VAV doe_vav_b-3-15'
doe_vav_b_3_14 = VAV(hvac, 'doe_vav_b_3_14', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240427/flow_tab_1')})
try:
  doe_vav_b_3_14.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-14'])
except:
  print 'could not link VAV doe_vav_b-3-14'
doe_vav_b_3_11 = VAV(hvac, 'doe_vav_b_3_11', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240421/flow_tab_1')})
try:
  doe_vav_b_3_11.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-11'])
except:
  print 'could not link VAV doe_vav_b-3-11'
doe_vav_b_3_10 = VAV(hvac, 'doe_vav_b_3_10', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240419/flow_tab_1')})
try:
  doe_vav_b_3_10.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-10'])
except:
  print 'could not link VAV doe_vav_b-3-10'
doe_vav_b_3_13 = VAV(hvac, 'doe_vav_b_3_13', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240425/flow_tab_1')})
try:
  doe_vav_b_3_13.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-13'])
except:
  print 'could not link VAV doe_vav_b-3-13'
doe_vav_b_3_12 = VAV(hvac, 'doe_vav_b_3_12', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240423/flow_tab_1')})
try:
  doe_vav_b_3_12.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-12'])
except:
  print 'could not link VAV doe_vav_b-3-12'
doe_vav_c_1_6 = VAV(hvac, 'doe_vav_c_1_6', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240206/flow_tab_1')})
try:
  doe_vav_c_1_6.add_area(gis.buildings['Bancroft Library']['1st_floor']['doe_vav_c-1-6'])
except:
  print 'could not link VAV doe_vav_c-1-6'
doe_vav_c_1_4 = VAV(hvac, 'doe_vav_c_1_4', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240204/flow_tab_1')})
try:
  doe_vav_c_1_4.add_area(gis.buildings['Bancroft Library']['1st_floor']['doe_vav_c-1-4'])
except:
  print 'could not link VAV doe_vav_c-1-4'
doe_vav_c_1_5 = VAV(hvac, 'doe_vav_c_1_5', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240205/flow_tab_1')})
try:
  doe_vav_c_1_5.add_area(gis.buildings['Bancroft Library']['1st_floor']['doe_vav_c-1-5'])
except:
  print 'could not link VAV doe_vav_c-1-5'
doe_vav_c_1_2 = VAV(hvac, 'doe_vav_c_1_2', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240202/flow_tab_1')})
try:
  doe_vav_c_1_2.add_area(gis.buildings['Bancroft Library']['1st_floor']['doe_vav_c-1-2'])
except:
  print 'could not link VAV doe_vav_c-1-2'
doe_vav_c_1_3 = VAV(hvac, 'doe_vav_c_1_3', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240203/flow_tab_1')})
try:
  doe_vav_c_1_3.add_area(gis.buildings['Bancroft Library']['1st_floor']['doe_vav_c-1-3'])
except:
  print 'could not link VAV doe_vav_c-1-3'
doe_vav_c_1_1 = VAV(hvac, 'doe_vav_c_1_1', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240201/flow_tab_1')})
try:
  doe_vav_c_1_1.add_area(gis.buildings['Bancroft Library']['1st_floor']['doe_vav_c-1-1'])
except:
  print 'could not link VAV doe_vav_c-1-1'
doe_vav_c_2_11 = VAV(hvac, 'doe_vav_c_2_11', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240311/flow_tab_1')})
try:
  doe_vav_c_2_11.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-11'])
except:
  print 'could not link VAV doe_vav_c-2-11'
doe_vav_c_2_10 = VAV(hvac, 'doe_vav_c_2_10', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240310/flow_tab_1')})
try:
  doe_vav_c_2_10.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-10'])
except:
  print 'could not link VAV doe_vav_c-2-10'
doe_vav_c_2_13 = VAV(hvac, 'doe_vav_c_2_13', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240313/flow_tab_1')})
try:
  doe_vav_c_2_13.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-13'])
except:
  print 'could not link VAV doe_vav_c-2-13'
doe_vav_c_2_12 = VAV(hvac, 'doe_vav_c_2_12', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240312/flow_tab_1')})
try:
  doe_vav_c_2_12.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-12'])
except:
  print 'could not link VAV doe_vav_c-2-12'
doe_vav_c_2_15 = VAV(hvac, 'doe_vav_c_2_15', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240315/flow_tab_1')})
try:
  doe_vav_c_2_15.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-15'])
except:
  print 'could not link VAV doe_vav_c-2-15'
doe_vav_c_2_14 = VAV(hvac, 'doe_vav_c_2_14', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240314/flow_tab_1')})
try:
  doe_vav_c_2_14.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-14'])
except:
  print 'could not link VAV doe_vav_c-2-14'
doe_vav_c_2_17 = VAV(hvac, 'doe_vav_c_2_17', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240317/flow_tab_1')})
try:
  doe_vav_c_2_17.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-17'])
except:
  print 'could not link VAV doe_vav_c-2-17'
doe_vav_c_2_16 = VAV(hvac, 'doe_vav_c_2_16', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240316/flow_tab_1')})
try:
  doe_vav_c_2_16.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-16'])
except:
  print 'could not link VAV doe_vav_c-2-16'
doe_vav_c_2_19 = VAV(hvac, 'doe_vav_c_2_19', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240319/flow_tab_1')})
try:
  doe_vav_c_2_19.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-19'])
except:
  print 'could not link VAV doe_vav_c-2-19'
doe_vav_c_2_18 = VAV(hvac, 'doe_vav_c_2_18', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240318/flow_tab_1')})
try:
  doe_vav_c_2_18.add_area(gis.buildings['Bancroft Library']['2nd_floor']['doe_vav_c-2-18'])
except:
  print 'could not link VAV doe_vav_c-2-18'
doe_vav_b_4_07n = VAV(hvac, 'doe_vav_b_4_07n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240502/flow_tab_1')})
try:
  doe_vav_b_4_07n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-07'])
except:
  print 'could not link VAV doe_vav_b-4-07'
doe_vav_b_3_10n = VAV(hvac, 'doe_vav_b_3_10n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240420/flow_tab_1')})
try:
  doe_vav_b_3_10n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-10'])
except:
  print 'could not link VAV doe_vav_b-3-10'
doe_vav_b_4_17n = VAV(hvac, 'doe_vav_b_4_17n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240603/flow_tab_1')})
try:
  doe_vav_b_4_17n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-17'])
except:
  print 'could not link VAV doe_vav_b-4-17'
doe_vav_b_3_6n = VAV(hvac, 'doe_vav_b_3_6n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240412/flow_tab_1')})
try:
  doe_vav_b_3_6n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-6'])
except:
  print 'could not link VAV doe_vav_b-3-6'
doe_vav_b_3_02 = VAV(hvac, 'doe_vav_b_3_02', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240403/flow_tab_1')})
try:
  doe_vav_b_3_02.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-02'])
except:
  print 'could not link VAV doe_vav_b-3-02'
doe_vav_b_3_03 = VAV(hvac, 'doe_vav_b_3_03', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240405/flow_tab_1')})
try:
  doe_vav_b_3_03.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-03'])
except:
  print 'could not link VAV doe_vav_b-3-03'
doe_vav_b_3_01 = VAV(hvac, 'doe_vav_b_3_01', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240401/flow_tab_1')})
try:
  doe_vav_b_3_01.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-01'])
except:
  print 'could not link VAV doe_vav_b-3-01'
doe_vav_b_3_06 = VAV(hvac, 'doe_vav_b_3_06', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240411/flow_tab_1')})
try:
  doe_vav_b_3_06.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-06'])
except:
  print 'could not link VAV doe_vav_b-3-06'
doe_vav_b_3_07 = VAV(hvac, 'doe_vav_b_3_07', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240413/flow_tab_1')})
try:
  doe_vav_b_3_07.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-07'])
except:
  print 'could not link VAV doe_vav_b-3-07'
doe_vav_b_3_04 = VAV(hvac, 'doe_vav_b_3_04', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240407/flow_tab_1')})
try:
  doe_vav_b_3_04.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-04'])
except:
  print 'could not link VAV doe_vav_b-3-04'
doe_vav_b_3_05 = VAV(hvac, 'doe_vav_b_3_05', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240409/flow_tab_1')})
try:
  doe_vav_b_3_05.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-05'])
except:
  print 'could not link VAV doe_vav_b-3-05'
doe_vav_b_3_08 = VAV(hvac, 'doe_vav_b_3_08', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240415/flow_tab_1')})
try:
  doe_vav_b_3_08.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-08'])
except:
  print 'could not link VAV doe_vav_b-3-08'
doe_vav_b_3_09 = VAV(hvac, 'doe_vav_b_3_09', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240417/flow_tab_1')})
try:
  doe_vav_b_3_09.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-09'])
except:
  print 'could not link VAV doe_vav_b-3-09'
doe_vav_b_4_18n = VAV(hvac, 'doe_vav_b_4_18n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240617/flow_tab_1')})
try:
  doe_vav_b_4_18n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-18'])
except:
  print 'could not link VAV doe_vav_b-4-18'
doe_vav_b_4_06n = VAV(hvac, 'doe_vav_b_4_06n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240504/flow_tab_1')})
try:
  doe_vav_b_4_06n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-06'])
except:
  print 'could not link VAV doe_vav_b-4-06'
doe_vav_b_3_13n = VAV(hvac, 'doe_vav_b_3_13n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240426/flow_tab_1')})
try:
  doe_vav_b_3_13n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-13'])
except:
  print 'could not link VAV doe_vav_b-3-13'
doe_vav_b_4_10n = VAV(hvac, 'doe_vav_b_4_10n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240510/flow_tab_1')})
try:
  doe_vav_b_4_10n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-10'])
except:
  print 'could not link VAV doe_vav_b-4-10'
doe_vav_b_3_7n = VAV(hvac, 'doe_vav_b_3_7n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240414/flow_tab_1')})
try:
  doe_vav_b_3_7n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-7'])
except:
  print 'could not link VAV doe_vav_b-3-7'
doe_vav_b_5_01n = VAV(hvac, 'doe_vav_b_5_01n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240620/flow_tab_1')})
try:
  doe_vav_b_5_01n.add_area(gis.buildings['Bancroft Library']['5th_floor']['doe_vav_b-5-01'])
except:
  print 'could not link VAV doe_vav_b-5-01'
doe_vav_b_3_2n = VAV(hvac, 'doe_vav_b_3_2n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240404/flow_tab_1')})
try:
  doe_vav_b_3_2n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-2'])
except:
  print 'could not link VAV doe_vav_b-3-2'
doe_vav_c_0_3 = VAV(hvac, 'doe_vav_c_0_3', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240702/flow_tab_1')})
try:
  doe_vav_c_0_3.add_area(gis.buildings['Bancroft Library']['basement']['doe_vav_c-0-3'])
except:
  print 'could not link VAV doe_vav_c-0-3'
doe_vav_b_4_16n = VAV(hvac, 'doe_vav_b_4_16n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240512/flow_tab_1')})
try:
  doe_vav_b_4_16n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-16'])
except:
  print 'could not link VAV doe_vav_b-4-16'
doe_vav_b_4_06 = VAV(hvac, 'doe_vav_b_4_06', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240503/flow_tab_1')})
try:
  doe_vav_b_4_06.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-06'])
except:
  print 'could not link VAV doe_vav_b-4-06'
doe_vav_c_0_1 = VAV(hvac, 'doe_vav_c_0_1', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240703/flow_tab_1')})
try:
  doe_vav_c_0_1.add_area(gis.buildings['Bancroft Library']['basement']['doe_vav_c-0-1'])
except:
  print 'could not link VAV doe_vav_c-0-1'
doe_vav_b_4_09n = VAV(hvac, 'doe_vav_b_4_09n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240508/flow_tab_1')})
try:
  doe_vav_b_4_09n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-09'])
except:
  print 'could not link VAV doe_vav_b-4-09'
doe_vav_b_4_15n = VAV(hvac, 'doe_vav_b_4_15n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240514/flow_tab_1')})
try:
  doe_vav_b_4_15n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-15'])
except:
  print 'could not link VAV doe_vav_b-4-15'
doe_vav_c_0_5 = VAV(hvac, 'doe_vav_c_0_5', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240705/flow_tab_1')})
try:
  doe_vav_c_0_5.add_area(gis.buildings['Bancroft Library']['basement']['doe_vav_c-0-5'])
except:
  print 'could not link VAV doe_vav_c-0-5'
doe_vav_b_4_01n = VAV(hvac, 'doe_vav_b_4_01n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240607/flow_tab_1')})
try:
  doe_vav_b_4_01n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-01'])
except:
  print 'could not link VAV doe_vav_b-4-01'
doe_vav_b_4_08n = VAV(hvac, 'doe_vav_b_4_08n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240506/flow_tab_1')})
try:
  doe_vav_b_4_08n.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-08'])
except:
  print 'could not link VAV doe_vav_b-4-08'
doe_vav_b_3_11n = VAV(hvac, 'doe_vav_b_3_11n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240422/flow_tab_1')})
try:
  doe_vav_b_3_11n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-11'])
except:
  print 'could not link VAV doe_vav_b-3-11'
doe_vav_b_5_01 = VAV(hvac, 'doe_vav_b_5_01', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240619/flow_tab_1')})
try:
  doe_vav_b_5_01.add_area(gis.buildings['Bancroft Library']['5th_floor']['doe_vav_b-5-01'])
except:
  print 'could not link VAV doe_vav_b-5-01'
doe_vav_b_5_02 = VAV(hvac, 'doe_vav_b_5_02', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240621/flow_tab_1')})
try:
  doe_vav_b_5_02.add_area(gis.buildings['Bancroft Library']['5th_floor']['doe_vav_b-5-02'])
except:
  print 'could not link VAV doe_vav_b-5-02'
doe_vav_b_3_5n = VAV(hvac, 'doe_vav_b_3_5n', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240410/flow_tab_1')})
try:
  doe_vav_b_3_5n.add_area(gis.buildings['Bancroft Library']['3rd_floor']['doe_vav_b-3-5'])
except:
  print 'could not link VAV doe_vav_b-3-5'
doe_vav_b_4_09 = VAV(hvac, 'doe_vav_b_4_09', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240507/flow_tab_1')})
try:
  doe_vav_b_4_09.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-09'])
except:
  print 'could not link VAV doe_vav_b-4-09'
doe_vav_b_4_08 = VAV(hvac, 'doe_vav_b_4_08', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240505/flow_tab_1')})
try:
  doe_vav_b_4_08.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-08'])
except:
  print 'could not link VAV doe_vav_b-4-08'
doe_vav_b_4_07 = VAV(hvac, 'doe_vav_b_4_07', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240501/flow_tab_1')})
try:
  doe_vav_b_4_07.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-07'])
except:
  print 'could not link VAV doe_vav_b-4-07'
doe_vav_c_0_2 = VAV(hvac, 'doe_vav_c_0_2', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240701/flow_tab_1')})
try:
  doe_vav_c_0_2.add_area(gis.buildings['Bancroft Library']['basement']['doe_vav_c-0-2'])
except:
  print 'could not link VAV doe_vav_c-0-2'
doe_vav_b_4_05 = VAV(hvac, 'doe_vav_b_4_05', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240608/flow_tab_1')})
try:
  doe_vav_b_4_05.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-05'])
except:
  print 'could not link VAV doe_vav_b-4-05'
doe_vav_b_4_04 = VAV(hvac, 'doe_vav_b_4_04', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240610/flow_tab_1')})
try:
  doe_vav_b_4_04.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-04'])
except:
  print 'could not link VAV doe_vav_b-4-04'
doe_vav_b_4_03 = VAV(hvac, 'doe_vav_b_4_03', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240614/flow_tab_1')})
try:
  doe_vav_b_4_03.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-03'])
except:
  print 'could not link VAV doe_vav_b-4-03'
doe_vav_b_4_02 = VAV(hvac, 'doe_vav_b_4_02', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240612/flow_tab_1')})
try:
  doe_vav_b_4_02.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-02'])
except:
  print 'could not link VAV doe_vav_b-4-02'
doe_vav_b_4_01 = VAV(hvac, 'doe_vav_b_4_01', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240606/flow_tab_1')})
try:
  doe_vav_b_4_01.add_area(gis.buildings['Bancroft Library']['4th_floor']['doe_vav_b-4-01'])
except:
  print 'could not link VAV doe_vav_b-4-01'
doe_vav_c_0_4 = VAV(hvac, 'doe_vav_c_0_4', {'EXH_AIR_DMP':BancroftVAVDMP('Exhaust Air Damper','/device240704/flow_tab_1')})
try:
  doe_vav_c_0_4.add_area(gis.buildings['Bancroft Library']['basement']['doe_vav_c-0-4'])
except:
  print 'could not link VAV doe_vav_c-0-4'
doe_ah_c.add_child(doe_vav_c_2_5)
doe_ah_c.add_child(doe_vav_c_2_4)
doe_ah_c.add_child(doe_vav_c_2_7)
doe_ah_c.add_child(doe_vav_c_2_6)
doe_ah_c.add_child(doe_vav_c_2_1)
doe_ah_c.add_child(doe_vav_c_2_3)
doe_ah_c.add_child(doe_vav_c_2_2)
doe_ah_c.add_child(doe_vav_c_2_9)
doe_ah_c.add_child(doe_vav_c_2_8)
doe_ah_c.add_child(doe_vav_c_1_6)
doe_ah_c.add_child(doe_vav_c_1_4)
doe_ah_c.add_child(doe_vav_c_1_5)
doe_ah_c.add_child(doe_vav_c_1_2)
doe_ah_c.add_child(doe_vav_c_1_3)
doe_ah_c.add_child(doe_vav_c_1_1)
doe_ah_c.add_child(doe_vav_c_2_11)
doe_ah_c.add_child(doe_vav_c_2_10)
doe_ah_c.add_child(doe_vav_c_2_13)
doe_ah_c.add_child(doe_vav_c_2_12)
doe_ah_c.add_child(doe_vav_c_2_15)
doe_ah_c.add_child(doe_vav_c_2_14)
doe_ah_c.add_child(doe_vav_c_2_17)
doe_ah_c.add_child(doe_vav_c_2_16)
doe_ah_c.add_child(doe_vav_c_2_19)
doe_ah_c.add_child(doe_vav_c_2_18)
doe_ah_c.add_child(doe_vav_c_0_3)
doe_ah_c.add_child(doe_vav_c_0_1)
doe_ah_c.add_child(doe_vav_c_0_5)
doe_ah_c.add_child(doe_vav_c_0_2)
doe_ah_c.add_child(doe_vav_c_0_4)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_03n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_13n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_18)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_19)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_14)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_15)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_16)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_17)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_10)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_11)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_12)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_13)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_2_01)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_14n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_02n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_4n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_20)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_05n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_8n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_12n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_11n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_5_02n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_01n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_04n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_9n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_12n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_3n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_2_01n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_15)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_14)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_11)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_10)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_13)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_12)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_07n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_10n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_17n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_6n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_02)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_03)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_01)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_06)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_07)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_04)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_05)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_08)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_09)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_18n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_06n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_13n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_10n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_7n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_5_01n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_2n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_16n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_06)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_09n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_15n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_01n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_08n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_11n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_5_01)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_5_02)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_3_5n)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_09)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_08)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_07)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_05)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_04)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_03)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_02)
#doe_ah_b1_ah_b2_rf_1.add_child(doe_vav_b_4_01)
