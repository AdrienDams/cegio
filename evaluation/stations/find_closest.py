# from A. Damseaux
# print a table with modelled (from CTSM output) and observed (from station) data for each station

import numpy as np
import xarray as xr
from scipy.spatial import distance
import os

# open netcdf
stationfile = os.environ['cegio'] + "/data/stations/orig_data/arctic_stations.soiltemp.monthly.1979-2019.nc"
ctsmfile    = os.environ['cegio'] + "/data/" + os.environ['run_name'] + "/monthly/" + os.environ['run_name'] + ".clm2.h0.2000-12.nc"
glacierfile = os.environ['cegio'] + "/data/surfdata_map/surfdata_57_DOM02_hist_78pfts_CMIP6_simyr2000_c220330.nc"

dstation = xr.open_dataset(stationfile, mask_and_scale=False)
dctsm    = xr.open_dataset(ctsmfile, mask_and_scale=False)
gfile    = xr.open_dataset(glacierfile, mask_and_scale=False)

# write variables stations
sta_lon     = dstation['lon']
sta_lon_360 = np.mod(sta_lon,360) # convert form -180 - 180 to 0 - 360
sta_lat     = dstation['lat']

# write variables ctsm outputs
ctsm_lon   = dctsm['lon']
ctsm_lat   = dctsm['lat']
ctsm_var   = dctsm['TSOI']
ctsm_coord = np.transpose([ctsm_lat, ctsm_lon])

# write variable for glacier
pct_glacier = np.array(gfile['PCT_GLACIER'])
gla_limit = 50.0

# write dimensions stations
nstations = np.size(dstation['station'])

# create text file column
txt_file = []

def closest_node(node, nodes, orig_index, var):
    closest_index = distance.cdist([node], nodes).argmin()
    # only print if distance between (1) lat_ctsm and lat_stat and (2) lon_ctsm and lon_stat is < 0.5 degree
    if ( (np.round(nodes[closest_index,0]) == np.round(node[0])) & (np.round(nodes[closest_index,1]) == np.round(node[1])) ):
     if ( var[0,:,closest_index].max() < 400 ): # exclude nodata values in TSOI (be sure that at least one value is below 400)
      if ( pct_glacier[i] < gla_limit ): 		# exclude points on glacier
       return orig_index, closest_index
      else:
       return "", ""
     else:
      return "", ""
    else:
     return "", ""

# go through all stations
for i in range(nstations):
 sta_coord = (sta_lat[i], sta_lon_360[i])
 txt_file.append(closest_node(sta_coord, ctsm_coord, i, ctsm_var))


np.savetxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", txt_file, fmt="%s")
