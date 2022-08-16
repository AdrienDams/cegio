# (from A. Damseaux)
# print a table with modelled (from CTSM output) and observed (from station) data for each station

import numpy as np
import netCDF4 as nc
import os
from os import sys

abs_zero = 273.15

# open netcdf
ctsmfile =  sys.argv[1]
#ctsmfile = "/work/aa0049/a271098/cegio/data/57_DOM02_004/monthly/57_DOM02_004.clm2.h0.2000-01.nc"
stationfile = sys.argv[2]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/orig_data/arctic_stations.soiltemp.monthly.1979-2019.nc"

dctsm    = nc.Dataset(ctsmfile, 'r') # read only
dstation = nc.Dataset(stationfile, 'a') # append

# open index
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", delimiter=" ", dtype=int)

# write variables stations
sta_depth    = np.array(dstation['depth'])
sta_qua      = np.array(dstation['quality'])
sta_ctsm_var = dstation['ctsm_soiltemp']

# creat output variable (not needed with current data)
#sta_ctsm_var = dstation.createVariable('ctsm_soiltemp','f4',('time', 'depth', 'station'))

# write variables ctsm outputs
ctsm_depth = np.round(np.array(dctsm['levgrnd'])*100,2) # convert from m to cm
ctsm_var   = np.array(dctsm['TSOI'])-abs_zero # change variable here

# retrieve time index from year-month ctsm to station
year  = int(os.environ['year'])
month = int(os.environ['month'])
date_index = ((year-1979)*12)+month-1
qua_min = 20.0 # minimum of days in a month to keep data

# fill arrays
for i in range(len(index_table[:,0])):
 for j in range(len(sta_depth)):
  qua_check = sta_qua[date_index,j,0,index_table[i,0]]
  if( qua_check > qua_min):
   ctsm_depth_idx = np.argmin(np.abs(sta_depth[j]-ctsm_depth)) # take ctsm depth index closest to sta index
   if ( np.in1d(sta_depth[j],ctsm_depth) == True ):  # same depth, only take depth which don't need interpolation
    sta_ctsm_var[date_index,j,index_table[i,0]] = ctsm_var[0,ctsm_depth_idx,index_table[i,1]]
   else: # depth needing an interpolation
    if ( sta_depth[j] < ctsm_depth[ctsm_depth_idx] ): # take previous ctsm depth for interp
     x = [ ctsm_var[0,ctsm_depth_idx-1,index_table[i,1]], ctsm_var[0,ctsm_depth_idx,index_table[i,1]] ]
     y = [ ctsm_depth[ctsm_depth_idx-1], ctsm_depth[ctsm_depth_idx] ]
    if ( sta_depth[j] > ctsm_depth[ctsm_depth_idx] ): # take next ctsm depth for interp
     x = [ ctsm_var[0,ctsm_depth_idx,index_table[i,1]], ctsm_var[0,ctsm_depth_idx+1,index_table[i,1]] ]
     y = [ ctsm_depth[ctsm_depth_idx], ctsm_depth[ctsm_depth_idx+1] ]
    y_new = sta_depth[j]
    x_new = np.round(np.interp(y_new, y, x),5)
    sta_ctsm_var[date_index,j,index_table[i,0]] = x_new

dstation.close()
