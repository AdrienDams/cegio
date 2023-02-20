# print a table with modelled (from CTSM output) and observed (from station) data for each station

import numpy as np
import xarray as xr
from scipy.spatial import distance
import os

# open netcdf
stationfile_tsoi = os.environ['cegio'] + "/data/stations/orig_data/arctic_stations.soiltemp.monthly.1979-2020.nc"
stationfile_tsa = os.environ['cegio'] + "/data/stations/orig_data/arctic_stations.t2m.monthly.1950-2020.nc"
ctsmfile = os.environ['cegio'] + "/data/" + os.environ['run_name'] + "/monthly/" + os.environ['run_name'] + ".clm2.h0.2000-12.nc"
glacierfile = os.environ['cegio'] + "/data/surfdata_map/surfdata_57_DOM02_hist_16pfts_Irrig_CMIP6_simyr2000_c220822.nc"

dstation_tsoi = xr.open_dataset(stationfile_tsoi, mask_and_scale=False)
dstation_tsa = xr.open_dataset(stationfile_tsa, mask_and_scale=False)
dctsm = xr.open_dataset(ctsmfile, mask_and_scale=False)
gfile = xr.open_dataset(glacierfile, mask_and_scale=False)

# write variables stations
sta_lon_tsoi = dstation_tsoi['lon']
sta_lon_tsoi_360 = np.mod(sta_lon_tsoi, 360) # convert from -180 - 180 to 0 - 360
sta_lat_tsoi = dstation_tsoi['lat']
sta_lon_tsa = dstation_tsa['lon'] # to change
sta_lon_tsa_360 = np.mod(sta_lon_tsa, 360) # convert from -180 - 180 to 0 - 360
sta_lat_tsa = dstation_tsa['lat'] # to change

# write variables ctsm outputs
ctsm_lon = dctsm['lon']
ctsm_lat = dctsm['lat']
ctsm_var_tsoi = dctsm['TSOI']
ctsm_var_tsa = dctsm['TSA']
ctsm_var_tsa = np.expand_dims(ctsm_var_tsa, axis=1) # add empty dimension to match tsoi
ctsm_coord = np.transpose([ctsm_lat, ctsm_lon])

# write variable for glacier
pct_glacier = np.array(gfile['PCT_GLACIER'])
gla_limit = 50.0

# write dimensions stations
nstations_tsoi = np.size(dstation_tsoi['station'])
nstations_tsa = np.size(dstation_tsa['station'])

# create text file column
txt_file_tsoi = []
txt_file_tsa = []

def closest_node(node, nodes, orig_index, var):
    closest_index = distance.cdist([node], nodes).argmin()
    # only print if distance between (1) lat_ctsm and lat_stat and (2) lon_ctsm and lon_stat is < 0.5 degree
    if ( (np.round(nodes[closest_index,0]) == np.round(node[0])) & (np.round(nodes[closest_index,1]) == np.round(node[1])) ):
     if ( var[0,:,closest_index].max() < 400 ): # exclude nodata values in TSOI (be sure that at least one value is below 400)
      if ( pct_glacier[i] < gla_limit ): # exclude points on glacier
       return orig_index, closest_index
      else:
       return "", ""
     else:
      return "", ""
    else:
     return "", ""

# go through all tsoi temperature stations
for i in range(nstations_tsoi):
 sta_coord = (sta_lat_tsoi[i], sta_lon_tsoi_360[i])
 txt_file_tsoi.append(closest_node(sta_coord, ctsm_coord, i, ctsm_var_tsoi))

np.savetxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", txt_file_tsoi, fmt="%s")

# go through all tsa temperature stations
for i in range(nstations_tsa):
 sta_coord = (sta_lat_tsa[i], sta_lon_tsa_360[i])
 txt_file_tsa.append(closest_node(sta_coord, ctsm_coord, i, ctsm_var_tsa))

np.savetxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.t2m.txt", txt_file_tsa, fmt="%s")
