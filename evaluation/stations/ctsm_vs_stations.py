# (from A. Damseaux)
# print a table with modelled (from CTSM output) and observed (from station) data for each station

# TODO list
# - make interplation closer point instead of the one below
# - use quality variable

import numpy as np
import netCDF4 as nc
import os
from os import sys

# open netcdf
stationfile = os.environ['cegio'] + "/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_" + os.environ['run_name'] + ".nc"
ctsmfile =  sys.argv[1]
#ctsmfile = "/work/aa0049/a271098/cegio/data/57_DOM02_032/monthly/57_DOM02_032.clm2.h0.2000-01.nc"

dstation = nc.Dataset(stationfile, 'a') # append
dctsm    = nc.Dataset(ctsmfile, 'r') # read only

# open index
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", delimiter=" ", dtype=int)

# write variables stations
sta_depth    = np.array(dstation['depth'])
sta_qua      = np.array(dstation['quality'])
sta_ctsm_var = dstation['ctsm_soiltemp']

# write variables ctsm outputs
ctsm_depth = np.array(dctsm['levgrnd'])*100 # convert from m to cm
ctsm_var   = np.array(dctsm['TSOI']) # change variable here

# write dimensions ctsm
depth_ctsm   = np.size(dctsm.dimensions['levgrnd'])

# retrieve time index from year-month ctsm to station
year  = int(os.environ['year'])
month = int(os.environ['month'])
date_index = ((year-1979)*12)+month-1

# creat output variable (only once)
#ctsm_var = dstation.createVariable('ctsm_soiltemp','f4',('time', 'depth', 'station'))

# depth levels which don't need interpolation
same_depth = np.zeros(depth_ctsm, dtype=int) # ctsm depth to stations depth
same_depth[0]=1
same_depth[1]=4
same_depth[2]=9
same_depth[3]=16
same_depth[4]=26
same_depth[5]=40
same_depth[6]=58
same_depth[7]=80
same_depth[8]=106
same_depth[10]=132
same_depth[12]=148

# depths which needs an interpolation
interp_depth = np.zeros(depth_ctsm, dtype=int) # ctsm depth to stations depth closest below
interp_depth[9]  = 125
interp_depth[11] = 139
interp_depth[13] = 150
interp_depth[14] = 153
interp_depth[15] = 157
interp_depth[16] = 161
interp_depth[17] = 165
interp_depth[18] = 170
interp_depth[19] = 173
interp_depth[20] = 176
interp_depth[21] = 183
interp_depth[22] = 195
interp_depth[23] = 214
interp_depth[24] = 240

# fill arrays
for i in range(len(index_table[:,0])):
 for j in range(depth_ctsm):
  if ( same_depth[j] != 0 ):  # only take depth which don't need interpolation
   # first 0 is time (sta) or useless dimension (ctsm), second is depth, third is
   sta_ctsm_var[date_index,same_depth[j],index_table[i,0]] = ctsm_var[0,j,index_table[i,1]]
  if ( interp_depth[j] != 0 ): # depth needing an interpolation
   # see here https://stackoverflow.com/a/55355684
   x = [ ctsm_var[0,j-1,index_table[i,1]], ctsm_var[0,j,index_table[i,1]] ]
   y = [ ctsm_depth[j-1], ctsm_depth[j] ]
   y_new = sta_depth[interp_depth[j]]
   x_new = np.interp(y_new, y, x)
   sta_ctsm_var[date_index,interp_depth[j],index_table[i,0]] = x_new

dstation.close()
