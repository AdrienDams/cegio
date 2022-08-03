# (from A. Damseaux)
# print a table with modelled (from CTSM output) and observed (from station) data for each station

import numpy as np
import netCDF4 as nc
import os
from os import sys

# open netcdf
ctsmfile =  sys.argv[1]
#ctsmfile = "/work/aa0049/a271098/cegio/data/57_DOM02_032/monthly/57_DOM02_032.clm2.h0.2000-01.nc"
stationfile = sys.argv[2]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_57_DOM02_032.nc"

dstation = nc.Dataset(stationfile, 'a') # append
dctsm    = nc.Dataset(ctsmfile, 'r') # read only

# open index
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", delimiter=" ", dtype=int)
#index_table = np.genfromtxt("stations_ctsm_indexes.txt", delimiter=" ", dtype=int)

# write variables stations
sta_depth    = np.array(dstation['depth'])
sta_qua      = np.array(dstation['quality'])
sta_ctsm_var = dstation['ctsm_soiltemp']

# creat output variable (not needed with current data)
#sta_ctsm_var = dstation.createVariable('ctsm_soiltemp','f4',('time', 'depth', 'station'))

# write variables ctsm outputs
ctsm_depth = np.round(np.array(dctsm['levgrnd'])*100,2) # convert from m to cm
ctsm_var   = np.array(dctsm['TSOI']) # change variable here

# write dimensions ctsm
depth_ctsm   = np.size(dctsm.dimensions['levgrnd'])

# retrieve time index from year-month ctsm to station
year  = int(os.environ['year'])
month = int(os.environ['month'])
date_index = ((year-1979)*12)+month-1
quality_minimum = 20.0 # minimum of days in a month to keep data

# fill arrays
for i in range(len(index_table[:,0])):
 for j in range(depth_ctsm):
  A = sta_qua[date_index,j,0,index_table[i,0]]
  if( A > quality_minimum):
   if ( np.in1d(ctsm_depth[0],sta_depth) == True ):  # only take depth which don't need interpolation
    sta_depth_idx = np.argmin(np.abs(ctsm_depth[0]-sta_depth))
    sta_ctsm_var[date_index,sta_depth_idx,index_table[i,0]] = ctsm_var[0,j,index_table[i,1]]
   else: # depth needing an interpolation
    sta_depth_idx = np.argmin(np.abs(ctsm_depth[0]-sta_depth))
    if ( sta_depth[sta_depth_idx] < ctsm_depth[j] ): # take previous ctsm depth for interp
     x = [ ctsm_var[0,j-1,index_table[i,1]], ctsm_var[0,j,index_table[i,1]] ]
     y = [ ctsm_depth[j-1], ctsm_depth[j] ]
    if ( sta_depth[sta_depth_idx] > ctsm_depth[j] ): # take next ctsm depth for interp
     x = [ ctsm_var[0,j,index_table[i,1]], ctsm_var[0,j+1,index_table[i,1]] ]
     y = [ ctsm_depth[j], ctsm_depth[j+1] ]
    y_new = sta_depth[sta_depth_idx]
    x_new = np.interp(y_new, y, x)
    sta_ctsm_var[date_index,sta_depth_idx,index_table[i,0]] = x_new

dstation.close()
