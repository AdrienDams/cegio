# extract station data in a readable .csv format

import numpy as np
import pandas as pd
import os
from os.path import exists
import netCDF4 as nc
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
 
## Extract files
station_file = sys.argv[1]
dstation = nc.Dataset(station_file)

# Load variables
data_time	= dstation.variables['time'][:]
data_sta	= np.around(dstation.variables['soiltemp'][:].T,3)
data_ctsm	= np.around(dstation.variables['ctsm_soiltemp'][:].T,3)
data_depth	= np.around(dstation.variables['depth'][:],3)
data_lon	= np.around(dstation.variables['lon'][:],3)
data_lat	= np.around(dstation.variables['lat'][:],3)
data_qua	= dstation.variables['quality'][:].T

dstation.close()

# Assign dates (YYYY) and month (MM) to time data
years  = np.arange(1979, 2022)
months = np.arange(1, 13)

data_year  = np.repeat(years, 12)
data_month = np.tile(months, 2022-1979)

# Check if file exists
if exists(os.environ['cegio'] + "/evaluation/stations/make_figures/extracted_csv/results.tmp." + os.environ['run_name'] + ".csv") == False:
	print("Start data extraction")

	# Loop through the data 
	list_all=[]
	print("station", end=' ', flush=True)
	for i in range(len(data_lon)):
		print(i, end=' ', flush=True)
		for j in range(len(data_depth)):   
			for k in range(0,len(data_year),12): # reduce loop time by checking only every year
				if any(data_qua[i][j][k:k+12] >= 20): # only take value with more than 20 days of measurements
					# we want to print a list of 12 entries for each month of this year/station/depth (even nan values)

					for month in range(12):
						list_all.append(
						[int(data_year[k+month]),	int(data_month[k+month]),
						data_lon[i], data_lat[i],
						data_depth[j],
						data_sta[i][j][k+month], data_ctsm[i][j][k+month]])

	# Replace masked elements with NaN
	list_all = np.ma.filled(list_all, fill_value=np.nan)
	# Transform list into pd data frame
	all_result=pd.DataFrame(np.array(list_all),columns=['data_year','data_month','data_lon','data_lat','data_depth','data_sta','data_ctsm'])
	# Export to .csv file (na_rep is to replace empty elements by -9999)
	all_result.to_csv(os.environ['cegio'] + "/evaluation/stations/make_figures/extracted_csv/results.tmp." + os.environ['run_name'] + ".csv",header=False,index=False,na_rep=-9999)

	print("Data extracted!")
