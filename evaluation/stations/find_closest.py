# from A. Damseaux
# print a table with modelled (from CTSM output) and observed (from station) data for each station

import numpy as np
import xarray as xr
from scipy.spatial import distance
import os

# open netcdf
stationfile = os.environ['cegio'] + "/data/stations/orig_data/AllArctic_SoilTemperature_monthly_quality_1979-2019_station.nc"
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

# special stations
sta_special = []

# mask grid points special station (here for glacier)
gla_limit = 50.0
ctsm_lon_gla = np.where(pct_glacier > gla_limit, ctsm_lon,-9999)
ctsm_lat_gla = np.where(pct_glacier > gla_limit, ctsm_lat,-9999)
ctsm_var_gla = np.where(pct_glacier > gla_limit, ctsm_var,-9999)
ctsm_coord_gla = np.transpose([ctsm_lat_gla, ctsm_lon_gla])

# write dimensions stations
nstations = np.size(dstation['station'])

def closest_node(node, nodes, orig_index, var):
    closest_index = distance.cdist([node], nodes).argmin()
    # only print if distance between (1) lat_ctsm and lat_stat and (2) lon_ctsm and lon_stat is < 0.5 degree
    if ( (np.round(nodes[closest_index,0]) == np.round(node[0])) & (np.round(nodes[closest_index,1]) == np.round(node[1])) ):
     if ( var[0,:,closest_index].max() < 400 ): # exclude nodata values in TSOI (be sure that at least one value is below 400)
      return orig_index, closest_index
      #return closest_index

# go through all stations
for i in range(nstations):
 sta_coord    = (sta_lat[i], sta_lon_360[i])
 if( i == any(sta_special)): # special stations
  print(closest_node(sta_coord, ctsm_coord_gla, i, ctsm_var_gla))
 else:
  print(closest_node(sta_coord, ctsm_coord, i, ctsm_var))
 #print(i)
 #print(np.array(sta_coord))
 #print(closest_node(sta_coord, ctsm_coord, i, ctsm_var))
 #print(ctsm_coord[closest_node(sta_coord, ctsm_coord, i, ctsm_var),0], ctsm_coord[closest_node(sta_coord, ctsm_coord, i, ctsm_var),1])
