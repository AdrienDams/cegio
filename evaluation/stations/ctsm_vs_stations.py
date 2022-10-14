# (from A. Damseaux)
# print a table with modelled (from CTSM output) and observed (from station) data for each station

import numpy as np
import pandas
import netCDF4 as nc
import os
from os import sys

abs_zero = 273.15

# open netcdf
ctsmfile =  sys.argv[1]
#ctsmfile= "/work/aa0049/a271098/cegio/data/57_DOM02_040/monthly/57_DOM02_040.clm2.h0.1980-01.nc"
stationfile = sys.argv[2]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_040/stations-vs-ctsm.1979-2020.tmp.57_DOM02_040.nc"

dctsm    = nc.Dataset(ctsmfile, 'r') # read only
dstation = nc.Dataset(stationfile, 'a') # append

# open index
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", delimiter=" ", dtype=int)

# open altitude values
alt_file = os.environ['cegio'] + "/data/stations/station_list_AllArctic2022.txt"
sta_alt  = np.array(pandas.read_fwf(alt_file, delimiter="\s+", engine="python",header=None))[:,4]

ctsm_alt_file = os.environ['cegio'] + "/data/surfdata_map/57_DOM02_topo.nc"
dalt = nc.Dataset(ctsm_alt_file, 'r') # read only

# write variables stations
sta_depth    = np.array(dstation['depth'])
sta_qua      = np.array(dstation['quality'])
sta_ctsm_var = dstation['ctsm_soiltemp']

# write variables ctsm outputs
ctsm_depth = np.round(np.array(dctsm['levgrnd'])*100,2) # convert from m to cm
ctsm_var   = np.array(dctsm['TSOI'])-abs_zero # change variable here
ctsm_alt   = np.array(dalt['ATM_TOPO'])[0,:]

# retrieve time index from year-month ctsm to station
year  = int(os.environ['year'])
month = int(os.environ['month'])
date_index = ((year-1979)*12)+month-1
qua_min = 20.0 # minimum of days in a month to keep data

# altitude air temperature correction (not used now)
def air_correct(sta_alt,ctsm_alt):
 diff_alt = ctsm_alt-sta_alt
 return diff_alt/100*0.6

# fill arrays
for i in range(len(index_table[:,0])):
 sta_index  = index_table[i,0]
 ctsm_index = index_table[i,1]

 for j in range(len(sta_depth)):
  qua_check = sta_qua[date_index,j,sta_index]

  if( (qua_check > qua_min) &  (qua_check < 32) ):
   ctsm_depth_idx = np.argmin(np.abs(sta_depth[j]-ctsm_depth)) # take ctsm depth index closest to sta index

   if ( np.in1d(sta_depth[j],ctsm_depth) == True or sta_depth[j]==0):
   # same depth or first depth, only take depth which don't need interpolation
    sta_ctsm_var[date_index,j,sta_index] = ctsm_var[0,ctsm_depth_idx,ctsm_index]
    #+air_correct(sta_alt[sta_index],ctsm_alt[ctsm_index])

   else: # depth needing an interpolation
    if ( sta_depth[j] > np.max(ctsm_depth) ): # if station depth below max ctsm, continue
     continue

    elif ( sta_depth[j] < ctsm_depth[ctsm_depth_idx] ): # take previous ctsm depth for interp
     x = [ ctsm_var[0,ctsm_depth_idx-1,ctsm_index], ctsm_var[0,ctsm_depth_idx,ctsm_index] ]
     y = [ ctsm_depth[ctsm_depth_idx-1], ctsm_depth[ctsm_depth_idx] ]

    elif ( sta_depth[j] > ctsm_depth[ctsm_depth_idx] ): # take next ctsm depth for interp
     x = [ ctsm_var[0,ctsm_depth_idx,ctsm_index], ctsm_var[0,ctsm_depth_idx+1,ctsm_index] ]
     y = [ ctsm_depth[ctsm_depth_idx], ctsm_depth[ctsm_depth_idx+1] ]

    y_new = sta_depth[j]
    x_new = np.round(np.interp(y_new, y, x),4)
    sta_ctsm_var[date_index,j,sta_index] = x_new#+air_correct(sta_alt[sta_index],ctsm_alt[ctsm_index])

dstation.close()
