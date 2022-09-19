import numpy as np
import pandas
import netCDF4 as nc
from scipy.spatial import distance
import os
import sys

# open files
ctsmfile = sys.argv[1]
#ctsmfile = "/work/aa0049/a271098/cegio/data/postproc/57_DOM02_004/processed/permafrost/57_DOM02_004.active_layer_depth.period.nc"
latlonf  = os.environ['cegio'] + "/data/" + os.environ['run_name'] + "/monthly/" + os.environ['run_name'] + ".clm2.h0.2000-12.nc"
calmfile = os.environ['cegio'] + "/evaluation/CALM/CALM_Summary_table_simplified.csv"
variable = "ALT"

dctsm   = nc.Dataset(ctsmfile, 'r') # read only
dlatlon = nc.Dataset(latlonf, 'r') # read only
calm_table = np.array(pandas.read_csv(calmfile, encoding="ISO-8859-1"))

# write variables ctsm outputs
ctsm_lon   = dlatlon['lon']
ctsm_lat   = dlatlon['lat']
ctsm_var   = dctsm['ALT'][10:,:] # only take 1990-2021
ctsm_coord = np.transpose([ctsm_lat, ctsm_lon])

# write variables calm
calm_lon     = calm_table[:,2]
calm_lon_360 = np.mod(calm_lon,360) # convert form -180 - 180 to 0 - 360
calm_lat     = calm_table[:,1]

# write dimensions calm
ncalm = np.size(calm_lon)

# create text file column
ctsm_to_calm = np.zeros([np.shape(calm_table)[0],np.shape(ctsm_var)[0]])

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
	if(nctsm != None):
		ctsm_to_calm[i,:] = ctsm_var[:,nctsm].data
	else:
		ctsm_to_calm[i,:] = None

np.savetxt(os.environ['cegio'] + "/evaluation/CALM/ctsm_to_calm_" + os.environ['run_name'] + ".csv", np.round(ctsm_to_calm*100), delimiter = ",", fmt="%s")






