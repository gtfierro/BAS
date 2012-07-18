from node import Relational
from generic_objects import *
from bacnet_devices import *
import networkx as nx
import gis
import node_types

hvac = Relational('hvac')
doe_vav_b_4_03n = VAV(hvac, 'doe_vav_b_4_03n', {})
try:
  doe_vav_b_4_03n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-03'])
except:
  pass
doe_vav_b_4_13n = VAV(hvac, 'doe_vav_b_4_13n', {})
try:
  doe_vav_b_4_13n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-13'])
except:
  pass
doe_vav_b_4_18 = VAV(hvac, 'doe_vav_b_4_18', {})
try:
  doe_vav_b_4_18.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-18'])
except:
  pass
doe_vav_b_4_19 = VAV(hvac, 'doe_vav_b_4_19', {})
try:
  doe_vav_b_4_19.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-19'])
except:
  pass
doe_vav_b_4_14 = VAV(hvac, 'doe_vav_b_4_14', {})
try:
  doe_vav_b_4_14.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-14'])
except:
  pass
doe_vav_b_4_15 = VAV(hvac, 'doe_vav_b_4_15', {})
try:
  doe_vav_b_4_15.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-15'])
except:
  pass
doe_vav_b_4_16 = VAV(hvac, 'doe_vav_b_4_16', {})
try:
  doe_vav_b_4_16.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-16'])
except:
  pass
doe_vav_b_4_17 = VAV(hvac, 'doe_vav_b_4_17', {})
try:
  doe_vav_b_4_17.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-17'])
except:
  pass
doe_vav_b_4_10 = VAV(hvac, 'doe_vav_b_4_10', {})
try:
  doe_vav_b_4_10.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-10'])
except:
  pass
doe_vav_b_4_11 = VAV(hvac, 'doe_vav_b_4_11', {})
try:
  doe_vav_b_4_11.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-11'])
except:
  pass
doe_vav_b_4_12 = VAV(hvac, 'doe_vav_b_4_12', {})
try:
  doe_vav_b_4_12.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-12'])
except:
  pass
doe_vav_b_4_13 = VAV(hvac, 'doe_vav_b_4_13', {})
try:
  doe_vav_b_4_13.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-13'])
except:
  pass
doe_vav_b_2_01 = VAV(hvac, 'doe_vav_b_2_01', {})
try:
  doe_vav_b_2_01.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_b-2-01'])
except:
  pass
doe_vav_b_4_14n = VAV(hvac, 'doe_vav_b_4_14n', {})
try:
  doe_vav_b_4_14n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-14'])
except:
  pass
doe_vav_b_4_02n = VAV(hvac, 'doe_vav_b_4_02n', {})
try:
  doe_vav_b_4_02n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-02'])
except:
  pass
doe_vav_b_3_4n = VAV(hvac, 'doe_vav_b_3_4n', {})
try:
  doe_vav_b_3_4n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-4'])
except:
  pass
doe_vav_b_4_20 = VAV(hvac, 'doe_vav_b_4_20', {})
try:
  doe_vav_b_4_20.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-20'])
except:
  pass
doe_vav_b_4_05n = VAV(hvac, 'doe_vav_b_4_05n', {})
try:
  doe_vav_b_4_05n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-05'])
except:
  pass
doe_vav_b_3_8n = VAV(hvac, 'doe_vav_b_3_8n', {})
try:
  doe_vav_b_3_8n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-8'])
except:
  pass
doe_vav_b_3_12n = VAV(hvac, 'doe_vav_b_3_12n', {})
try:
  doe_vav_b_3_12n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-12'])
except:
  pass
doe_vav_b_4_11n = VAV(hvac, 'doe_vav_b_4_11n', {})
try:
  doe_vav_b_4_11n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-11'])
except:
  pass
doe_vav_b_5_02n = VAV(hvac, 'doe_vav_b_5_02n', {})
try:
  doe_vav_b_5_02n.areas.add(gis.buildings['Bancroft Library']['5th_floor']['#doe_vav_b-5-02'])
except:
  pass
doe_vav_b_3_01n = VAV(hvac, 'doe_vav_b_3_01n', {})
try:
  doe_vav_b_3_01n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-01'])
except:
  pass
doe_vav_b_4_04n = VAV(hvac, 'doe_vav_b_4_04n', {})
try:
  doe_vav_b_4_04n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-04'])
except:
  pass
doe_vav_b_3_9n = VAV(hvac, 'doe_vav_b_3_9n', {})
try:
  doe_vav_b_3_9n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-9'])
except:
  pass
doe_vav_b_4_12n = VAV(hvac, 'doe_vav_b_4_12n', {})
try:
  doe_vav_b_4_12n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-12'])
except:
  pass
doe_vav_b_3_3n = VAV(hvac, 'doe_vav_b_3_3n', {})
try:
  doe_vav_b_3_3n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-3'])
except:
  pass
doe_vav_c_2_5 = VAV(hvac, 'doe_vav_c_2_5', {})
try:
  doe_vav_c_2_5.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-5'])
except:
  pass
doe_vav_c_2_4 = VAV(hvac, 'doe_vav_c_2_4', {})
try:
  doe_vav_c_2_4.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-4'])
except:
  pass
doe_vav_c_2_7 = VAV(hvac, 'doe_vav_c_2_7', {})
try:
  doe_vav_c_2_7.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-7'])
except:
  pass
doe_vav_c_2_6 = VAV(hvac, 'doe_vav_c_2_6', {})
try:
  doe_vav_c_2_6.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-6'])
except:
  pass
doe_vav_c_2_1 = VAV(hvac, 'doe_vav_c_2_1', {})
try:
  doe_vav_c_2_1.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-1'])
except:
  pass
doe_vav_c_2_3 = VAV(hvac, 'doe_vav_c_2_3', {})
try:
  doe_vav_c_2_3.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-3'])
except:
  pass
doe_vav_c_2_2 = VAV(hvac, 'doe_vav_c_2_2', {})
try:
  doe_vav_c_2_2.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-2'])
except:
  pass
doe_vav_b_2_01n = VAV(hvac, 'doe_vav_b_2_01n', {})
try:
  doe_vav_b_2_01n.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_b-2-01'])
except:
  pass
doe_vav_c_2_9 = VAV(hvac, 'doe_vav_c_2_9', {})
try:
  doe_vav_c_2_9.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-9'])
except:
  pass
doe_vav_c_2_8 = VAV(hvac, 'doe_vav_c_2_8', {})
try:
  doe_vav_c_2_8.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-8'])
except:
  pass
doe_vav_b_3_15 = VAV(hvac, 'doe_vav_b_3_15', {})
try:
  doe_vav_b_3_15.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-15'])
except:
  pass
doe_vav_b_3_14 = VAV(hvac, 'doe_vav_b_3_14', {})
try:
  doe_vav_b_3_14.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-14'])
except:
  pass
doe_vav_b_3_11 = VAV(hvac, 'doe_vav_b_3_11', {})
try:
  doe_vav_b_3_11.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-11'])
except:
  pass
doe_vav_b_3_10 = VAV(hvac, 'doe_vav_b_3_10', {})
try:
  doe_vav_b_3_10.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-10'])
except:
  pass
doe_vav_b_3_13 = VAV(hvac, 'doe_vav_b_3_13', {})
try:
  doe_vav_b_3_13.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-13'])
except:
  pass
doe_vav_b_3_12 = VAV(hvac, 'doe_vav_b_3_12', {})
try:
  doe_vav_b_3_12.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-12'])
except:
  pass
doe_vav_c_1_6 = VAV(hvac, 'doe_vav_c_1_6', {})
try:
  doe_vav_c_1_6.areas.add(gis.buildings['Bancroft Library']['1st_floor']['#doe_vav_c-1-6'])
except:
  pass
doe_vav_c_1_4 = VAV(hvac, 'doe_vav_c_1_4', {})
try:
  doe_vav_c_1_4.areas.add(gis.buildings['Bancroft Library']['1st_floor']['#doe_vav_c-1-4'])
except:
  pass
doe_vav_c_1_5 = VAV(hvac, 'doe_vav_c_1_5', {})
try:
  doe_vav_c_1_5.areas.add(gis.buildings['Bancroft Library']['1st_floor']['#doe_vav_c-1-5'])
except:
  pass
doe_vav_c_1_2 = VAV(hvac, 'doe_vav_c_1_2', {})
try:
  doe_vav_c_1_2.areas.add(gis.buildings['Bancroft Library']['1st_floor']['#doe_vav_c-1-2'])
except:
  pass
doe_vav_c_1_3 = VAV(hvac, 'doe_vav_c_1_3', {})
try:
  doe_vav_c_1_3.areas.add(gis.buildings['Bancroft Library']['1st_floor']['#doe_vav_c-1-3'])
except:
  pass
doe_vav_c_1_1 = VAV(hvac, 'doe_vav_c_1_1', {})
try:
  doe_vav_c_1_1.areas.add(gis.buildings['Bancroft Library']['1st_floor']['#doe_vav_c-1-1'])
except:
  pass
doe_vav_c_2_11 = VAV(hvac, 'doe_vav_c_2_11', {})
try:
  doe_vav_c_2_11.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-11'])
except:
  pass
doe_vav_c_2_10 = VAV(hvac, 'doe_vav_c_2_10', {})
try:
  doe_vav_c_2_10.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-10'])
except:
  pass
doe_vav_c_2_13 = VAV(hvac, 'doe_vav_c_2_13', {})
try:
  doe_vav_c_2_13.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-13'])
except:
  pass
doe_vav_c_2_12 = VAV(hvac, 'doe_vav_c_2_12', {})
try:
  doe_vav_c_2_12.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-12'])
except:
  pass
doe_vav_c_2_15 = VAV(hvac, 'doe_vav_c_2_15', {})
try:
  doe_vav_c_2_15.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-15'])
except:
  pass
doe_vav_c_2_14 = VAV(hvac, 'doe_vav_c_2_14', {})
try:
  doe_vav_c_2_14.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-14'])
except:
  pass
doe_vav_c_2_17 = VAV(hvac, 'doe_vav_c_2_17', {})
try:
  doe_vav_c_2_17.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-17'])
except:
  pass
doe_vav_c_2_16 = VAV(hvac, 'doe_vav_c_2_16', {})
try:
  doe_vav_c_2_16.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-16'])
except:
  pass
doe_vav_c_2_19 = VAV(hvac, 'doe_vav_c_2_19', {})
try:
  doe_vav_c_2_19.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-19'])
except:
  pass
doe_vav_c_2_18 = VAV(hvac, 'doe_vav_c_2_18', {})
try:
  doe_vav_c_2_18.areas.add(gis.buildings['Bancroft Library']['2nd_floor']['#doe_vav_c-2-18'])
except:
  pass
doe_vav_b_4_07n = VAV(hvac, 'doe_vav_b_4_07n', {})
try:
  doe_vav_b_4_07n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-07'])
except:
  pass
doe_vav_b_3_10n = VAV(hvac, 'doe_vav_b_3_10n', {})
try:
  doe_vav_b_3_10n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-10'])
except:
  pass
doe_vav_b_4_17n = VAV(hvac, 'doe_vav_b_4_17n', {})
try:
  doe_vav_b_4_17n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-17'])
except:
  pass
doe_vav_b_3_6n = VAV(hvac, 'doe_vav_b_3_6n', {})
try:
  doe_vav_b_3_6n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-6'])
except:
  pass
doe_vav_b_3_02 = VAV(hvac, 'doe_vav_b_3_02', {})
try:
  doe_vav_b_3_02.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-02'])
except:
  pass
doe_vav_b_3_03 = VAV(hvac, 'doe_vav_b_3_03', {})
try:
  doe_vav_b_3_03.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-03'])
except:
  pass
doe_vav_b_3_01 = VAV(hvac, 'doe_vav_b_3_01', {})
try:
  doe_vav_b_3_01.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-01'])
except:
  pass
doe_vav_b_3_06 = VAV(hvac, 'doe_vav_b_3_06', {})
try:
  doe_vav_b_3_06.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-06'])
except:
  pass
doe_vav_b_3_07 = VAV(hvac, 'doe_vav_b_3_07', {})
try:
  doe_vav_b_3_07.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-07'])
except:
  pass
doe_vav_b_3_04 = VAV(hvac, 'doe_vav_b_3_04', {})
try:
  doe_vav_b_3_04.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-04'])
except:
  pass
doe_vav_b_3_05 = VAV(hvac, 'doe_vav_b_3_05', {})
try:
  doe_vav_b_3_05.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-05'])
except:
  pass
doe_vav_b_3_08 = VAV(hvac, 'doe_vav_b_3_08', {})
try:
  doe_vav_b_3_08.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-08'])
except:
  pass
doe_vav_b_3_09 = VAV(hvac, 'doe_vav_b_3_09', {})
try:
  doe_vav_b_3_09.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-09'])
except:
  pass
doe_vav_b_4_18n = VAV(hvac, 'doe_vav_b_4_18n', {})
try:
  doe_vav_b_4_18n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-18'])
except:
  pass
doe_vav_b_4_06n = VAV(hvac, 'doe_vav_b_4_06n', {})
try:
  doe_vav_b_4_06n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-06'])
except:
  pass
doe_vav_b_3_13n = VAV(hvac, 'doe_vav_b_3_13n', {})
try:
  doe_vav_b_3_13n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-13'])
except:
  pass
doe_vav_b_4_10n = VAV(hvac, 'doe_vav_b_4_10n', {})
try:
  doe_vav_b_4_10n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-10'])
except:
  pass
doe_vav_b_3_7n = VAV(hvac, 'doe_vav_b_3_7n', {})
try:
  doe_vav_b_3_7n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-7'])
except:
  pass
doe_vav_b_5_01n = VAV(hvac, 'doe_vav_b_5_01n', {})
try:
  doe_vav_b_5_01n.areas.add(gis.buildings['Bancroft Library']['5th_floor']['#doe_vav_b-5-01'])
except:
  pass
doe_vav_b_3_2n = VAV(hvac, 'doe_vav_b_3_2n', {})
try:
  doe_vav_b_3_2n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-2'])
except:
  pass
doe_vav_c_0_3 = VAV(hvac, 'doe_vav_c_0_3', {})
try:
  doe_vav_c_0_3.areas.add(gis.buildings['Bancroft Library']['basement']['#doe_vav_c-0-3'])
except:
  pass
doe_vav_b_4_16n = VAV(hvac, 'doe_vav_b_4_16n', {})
try:
  doe_vav_b_4_16n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-16'])
except:
  pass
doe_vav_b_4_06 = VAV(hvac, 'doe_vav_b_4_06', {})
try:
  doe_vav_b_4_06.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-06'])
except:
  pass
doe_vav_c_0_1 = VAV(hvac, 'doe_vav_c_0_1', {})
try:
  doe_vav_c_0_1.areas.add(gis.buildings['Bancroft Library']['basement']['#doe_vav_c-0-1'])
except:
  pass
doe_vav_b_4_09n = VAV(hvac, 'doe_vav_b_4_09n', {})
try:
  doe_vav_b_4_09n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-09'])
except:
  pass
doe_vav_b_4_15n = VAV(hvac, 'doe_vav_b_4_15n', {})
try:
  doe_vav_b_4_15n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-15'])
except:
  pass
doe_vav_c_0_5 = VAV(hvac, 'doe_vav_c_0_5', {})
try:
  doe_vav_c_0_5.areas.add(gis.buildings['Bancroft Library']['basement']['#doe_vav_c-0-5'])
except:
  pass
doe_vav_b_4_01n = VAV(hvac, 'doe_vav_b_4_01n', {})
try:
  doe_vav_b_4_01n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-01'])
except:
  pass
doe_vav_b_4_08n = VAV(hvac, 'doe_vav_b_4_08n', {})
try:
  doe_vav_b_4_08n.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-08'])
except:
  pass
doe_vav_b_3_11n = VAV(hvac, 'doe_vav_b_3_11n', {})
try:
  doe_vav_b_3_11n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-11'])
except:
  pass
doe_vav_b_5_01 = VAV(hvac, 'doe_vav_b_5_01', {})
try:
  doe_vav_b_5_01.areas.add(gis.buildings['Bancroft Library']['5th_floor']['#doe_vav_b-5-01'])
except:
  pass
doe_vav_b_5_02 = VAV(hvac, 'doe_vav_b_5_02', {})
try:
  doe_vav_b_5_02.areas.add(gis.buildings['Bancroft Library']['5th_floor']['#doe_vav_b-5-02'])
except:
  pass
doe_vav_b_3_5n = VAV(hvac, 'doe_vav_b_3_5n', {})
try:
  doe_vav_b_3_5n.areas.add(gis.buildings['Bancroft Library']['3rd_floor']['#doe_vav_b-3-5'])
except:
  pass
doe_vav_b_4_09 = VAV(hvac, 'doe_vav_b_4_09', {})
try:
  doe_vav_b_4_09.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-09'])
except:
  pass
doe_vav_b_4_08 = VAV(hvac, 'doe_vav_b_4_08', {})
try:
  doe_vav_b_4_08.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-08'])
except:
  pass
doe_vav_b_4_07 = VAV(hvac, 'doe_vav_b_4_07', {})
try:
  doe_vav_b_4_07.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-07'])
except:
  pass
doe_vav_c_0_2 = VAV(hvac, 'doe_vav_c_0_2', {})
try:
  doe_vav_c_0_2.areas.add(gis.buildings['Bancroft Library']['basement']['#doe_vav_c-0-2'])
except:
  pass
doe_vav_b_4_05 = VAV(hvac, 'doe_vav_b_4_05', {})
try:
  doe_vav_b_4_05.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-05'])
except:
  pass
doe_vav_b_4_04 = VAV(hvac, 'doe_vav_b_4_04', {})
try:
  doe_vav_b_4_04.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-04'])
except:
  pass
doe_vav_b_4_03 = VAV(hvac, 'doe_vav_b_4_03', {})
try:
  doe_vav_b_4_03.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-03'])
except:
  pass
doe_vav_b_4_02 = VAV(hvac, 'doe_vav_b_4_02', {})
try:
  doe_vav_b_4_02.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-02'])
except:
  pass
doe_vav_b_4_01 = VAV(hvac, 'doe_vav_b_4_01', {})
try:
  doe_vav_b_4_01.areas.add(gis.buildings['Bancroft Library']['4th_floor']['#doe_vav_b-4-01'])
except:
  pass
doe_vav_c_0_4 = VAV(hvac, 'doe_vav_c_0_4', {})
try:
  doe_vav_c_0_4.areas.add(gis.buildings['Bancroft Library']['basement']['#doe_vav_c-0-4'])
except:
  pass
