# compute a .csv file with CTSM interpolated on CALM stations

import numpy as np
import pandas
import netCDF4 as nc
from scipy.spatial import distance
import os
import sys

# open files
ctsmfile = sys.argv[1] # from startyear to endyear
#ctsmfile = "/work/aa0049/a271098/cegio/data/postproc/57_DOM02_001/processed/permafrost/57_DOM02_001.active_layer_depth.period.nc"
latlonf  = os.environ['cegio'] + "/data/" + os.environ['run_name'] + "/monthly/" + os.environ['run_name'] + ".clm2.h0.2000-12.nc"
calmfile = os.environ['cegio'] + "/evaluation/CALM/CALM_Summary_table_simplified.csv"
variable = "ALT"

dctsm   = nc.Dataset(ctsmfile, 'r') # read only
dlatlon = nc.Dataset(latlonf, 'r') # read only
calm_table = np.array(pandas.read_csv(calmfile, encoding="ISO-8859-1"))

# decide start period
startyear = int(os.environ['startyear'])
if ( startyear < 1990): startyearind=1990-startyear

# write variables ctsm outputs
ctsm_lon   = dlatlon['lon']
ctsm_lat   = dlatlon['lat']
ctsm_var   = dctsm['ALT'][startyearind:,:] # only take from 1990
ctsm_coord = np.transpose([ctsm_lat, ctsm_lon])

# write variables calm
calm_lon     = calm_table[:,2]
calm_lon_360 = np.mod(calm_lon,360) # convert form -180 - 180 to 0 - 360
calm_lat     = calm_table[:,1]

# write dimensions calm
ncalm = np.size(calm_lon)
nyear = np.shape(ctsm_var)[0]

# create text file column
ctsm_to_calm = np.zeros([ncalm,nyear])

def closest_node(node, nodes):
	closest_index = distance.cdist([node], nodes).argmin()
	# only print if distance between (1) lat_ctsm and lat_calm and (2) lon_ctsm and lon_calm is < 0.5 degree
	if ( (np.round(nodes[closest_index,0]) == np.round(node[0])) & (np.round(nodes[closest_index,1]) == np.round(node[1])) ):
		return closest_index
	else:
		return None

# go through all calm
for i in range(ncalm):
	calm_coord = (calm_lat[i], calm_lon_360[i])
	nctsm = closest_node(calm_coord, ctsm_coord)
	for j in range(nyear):
		if(nctsm != None and ctsm_var[j,nctsm] != None):
			ctsm_to_calm[i,j] = ctsm_var[j,nctsm]
		else:
			ctsm_to_calm[i,j] = None

np.savetxt(os.environ['cegio'] + "/evaluation/CALM/ctsm_to_calm_" + os.environ['run_name'] + ".csv", np.round(ctsm_to_calm*100), delimiter = ",", fmt="%s")






