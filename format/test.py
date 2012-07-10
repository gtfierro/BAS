from node import Relational
from generic_objects import *
from bacnet_devices import *
import networkx as nx
import gis
import node_types

gis.NodeLink.objects.all().delete()
hvac = relational('hvac')
doe_ah_b1_ah_b2_rf_1 = AHU(hvac, 'doe_ah_b1_ah_b2_rf_1', {
'OUT_AIR_DMP' : BACnetDMP( 'AH-B Low Outside Airflow Level 2 Alarm','m567'),
'OUT_AIR_TMP_SEN' : BACnetSEN( 'Run Time','m574'),
'MIX_AIR_TMP_SEN' : BACnetSEN( 'Run Time','m574'),
'RET_FAN' : BACnetFAN( 'Eff run command','m431'),
'RET_AIR_FLW_SEN' : BACnetSEN( 'OA Flow Gain','n169'),
'EXH_AIR_DMP' : BACnetDMP( 'Ht Req','m588'),
'RET_AIR_HUM_SEN' : BACnetSEN( 'Ht Req','m588'),
'RET_AIR_TMP_SEN' : BACnetSEN( 'Run Time','m574'),
'RET_AIR_DMP' : BACnetDMP( 'Run Time','m574'),
'RET_AIR_PRS_SEN' : BACnetSEN( 'B1 Duct Sratic Pressure','b1_stat_press'),
'COO_VLV' : BACnetVLV( 'Cooling Duct SA Flow CFM','n048'),
'SUP_AIR_FAN' : BACnetFAN( 'RF-1 Fan Hand Alarm Level 4 Alarm','m944'),
'SUP_AIR_FLW_SEN' : BACnetSEN( 'B2 Supply Air Flow','b2_sa_cfm'),
'SUP_AIR_TMP_SEN' : BACnetSEN( 'Run Time','m574'),
'SUP_AIR_PRS_SEN' : BACnetSEN( 'B1 Duct Sratic Pressure','b1_stat_press'),
})
doe_ah_a_and_dh_1 = AHU(hvac, 'doe_ah_a_and_dh_1', {
'OUT_AIR_DMP' : BACnetDMP( 'Outside Airflow','oa_cfm'),
'OUT_AIR_TMP_SEN' : BACnetSEN( 'Outside Airflow','oa_cfm'),
'MIX_AIR_TMP_SEN' : BACnetSEN( 'Ht Req','m404'),
'RET_FAN' : BACnetFAN( 'DH-1 Fan Status','m501'),
'RET_AIR_FLW_SEN' : BACnetSEN( 'Flow Gain','m351'),
'EXH_AIR_DMP' : BACnetDMP( 'Zone Hum STP ADJ','m720'),
'RET_AIR_HUM_SEN' : BACnetSEN( 'Space Humidity Setpoint','avg_spc_hum'),
'RET_AIR_TMP_SEN' : BACnetSEN( 'Regular Occ Mode','m401'),
'RET_AIR_DMP' : BACnetDMP( 'Regular Occ Mode','m401'),
'RET_AIR_PRS_SEN' : BACnetSEN( 'Class A Building Pressure (inH2O)','m521'),
'COO_VLV' : BACnetVLV( 'digital','m422'),
'SUP_AIR_FAN' : BACnetFAN( 'AH-A fan in hand level 4 alarm','m533'),
'SUP_AIR_FLW_SEN' : BACnetSEN( 'Outside Airflow','oa_cfm'),
'SUP_AIR_TMP_SEN' : BACnetSEN( 'Space Temp Setpoint','avg_spc_temp'),
'SUP_AIR_PRS_SEN' : BACnetSEN( 'Class A Building Pressure (inH2O)','m521'),
})
doe_ah_c = AHU(hvac, 'doe_ah_c', {
'OUT_AIR_DMP' : BACnetDMP( 'Outside Air Flow','oa_sa_cfm'),
'OUT_AIR_TMP_SEN' : BACnetSEN( 'Outside Air Flow','oa_sa_cfm'),
'MIX_AIR_TMP_SEN' : BACnetSEN( 'Run Time','m313'),
'RET_FAN' : BACnetFAN( 'Run For','m305'),
'RET_AIR_FLW_SEN' : BACnetSEN( 'Supply Air Flow','sa_cfm'),
'EXH_AIR_DMP' : BACnetDMP( 'Ht Req','m908'),
'RET_AIR_HUM_SEN' : BACnetSEN( 'Ht Req','m908'),
'RET_AIR_TMP_SEN' : BACnetSEN( 'Run Time','m313'),
'RET_AIR_DMP' : BACnetDMP( 'Run Time','m313'),
'RET_AIR_PRS_SEN' : BACnetSEN( 'Duct Sratic Pressure','stat_press'),
'COO_VLV' : BACnetVLV( 'Clg Vlv Percent','clg_vlv'),
'SUP_AIR_FAN' : BACnetFAN( 'Supply Air Flow','sa_cfm'),
'SUP_AIR_FLW_SEN' : BACnetSEN( 'Outside Air Flow','oa_sa_cfm'),
'SUP_AIR_TMP_SEN' : BACnetSEN( 'Run Time','m313'),
'SUP_AIR_PRS_SEN' : BACnetSEN( 'Duct Sratic Pressure','stat_press'),
})
