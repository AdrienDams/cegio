#!/usr/bin/env python3
# from A. Damseaux
# print a table with modelled (from CTSM output) and observed (from station) data for each station

import numpy as np
import xarray as xr
from scipy.spatial import distance
import os

# open netcdf
stationfile = os.environ['cegio'] + "/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station.nc"
dstation = xr.open_dataset(stationfile, mask_and_scale=False)

# open indexes
index_table = np.loadtxt("stations_ctsm_indexes.txt", delimiter=",", unpack=False).astype(int)

# write variables stations
sta_qua   = np.array(dstation['quality'])
sta_depth = np.array(dstation['depth'])

# write dimensions stations
tstations = np.size(dstation['time'])
nstations = np.size(dstation['station'])
dstations = np.size(dstation['depth'])

depth_kept = []
depth_kept_index = []

# functions
def to_days(timedelta):
	x = np.timedelta64(timedelta, 'ns')
	days = x.astype('timedelta64[D]')
	return days.astype(int)

# go through all stations
for i in range(nstations):
 for j in range(dstations):
  for k in range(tstations):
   if( to_days(sta_qua[k,j,0,i]) > 20 ):
    if not sta_depth[j] in depth_kept :
     depth_kept.append(sta_depth[j])
     depth_kept_index.append(j)

#np.savetxt('depth_kept.txt',np.column_stack([depth_kept_index,depth_kept]),delimiter=",", fmt="%s")
