# print a table with modelled (from CTSM output) and observed (from station) data for each station

import numpy as np
import pandas
import netCDF4 as nc
import os
from os import sys

abs_zero = 273.15

# open netcdf
ctsmfile =  sys.argv[1]
stationfile = sys.argv[2]
#ctsmfile= "/work/aa0049/a271098/cegio/data/57_DOM02_001/monthly/57_DOM02_001.clm2.h0.1980-01.nc"
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_001/stations-vs-ctsm.1980-2020.t2m.2.57_DOM02_001.nc"

dctsm    = nc.Dataset(ctsmfile, 'r') # read only
dstation = nc.Dataset(stationfile, 'a') # append

# open index
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.t2m.txt", delimiter=" ", dtype=int)

# open altitude values
alt_file = os.environ['cegio'] + "/data/stations/station_list_AllArctic2022.t2m.txt"
sta_alt  = np.array(pandas.read_fwf(alt_file, delimiter="\s+", engine="python",header=None))[:,4]

ctsm_alt_file = os.environ['cegio'] + "/data/surfdata_map/57_DOM02_topo.nc"
dalt = nc.Dataset(ctsm_alt_file, 'r') # read only

# write variables stations
sta_ctsm_var = dstation['ctsm_temp2']

# write variables ctsm outputs
ctsm_var   = np.array(dctsm['TSA'])-abs_zero
ctsm_alt   = np.array(dalt['ATM_TOPO'])[0,:]

# retrieve time index from year-month ctsm to station
year  = int(os.environ['year'])
month = int(os.environ['month'])
date_index = ((year-1950)*12)+month-1

# altitude air temperature correction (not used now)
def air_correct(sta_alt, ctsm_alt):
	if isinstance(sta_alt, (int, float)):
		diff_alt = ctsm_alt - sta_alt
		return diff_alt / 100 * 0.6
	else:
		return 0

# fill arrays
for i in range(len(index_table[:,0])):
	sta_index  = index_table[i,0]
	ctsm_index = index_table[i,1]

	sta_ctsm_var[date_index,sta_index] = ctsm_var[0,ctsm_index] + air_correct(sta_alt[sta_index],ctsm_alt[ctsm_index])

dstation.close()
