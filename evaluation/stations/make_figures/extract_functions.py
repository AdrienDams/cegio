# Import Packages
import numpy as np
import pandas as pd
import os
from os.path import exists
import netCDF4 as nc

def Date_transformer(abs_list,relative):

    result=[]

    for i in range(int(len(abs_list)/12)):

        for j in range(12):

            result.append(relative+i)


    return result

# Loop through the data 
def Extract_Depths(data_obs,data_sim,date_list,data_depth,data_lon,data_lat,data_qua):

    list_all=[]

    for i in range(len(data_depth)):
        
        depth=data_depth[i]
        
        for j in range(len(data_lon)):
            
            station=[data_lon[j],data_lat[j]]
           
            for z in range(0,len(date_list),12):
                
                date_start=date_list[z]

                index=z
                checker1=True
                checker2=True

                # Fills help_list until the next year starts, or there is an unfilled value
                # Then the loop breaks. In the later case the months of that year get discarded
                # and date_start==date_list[index]
                help_list=[]
                while (index<z+12) and (checker1==True and checker2==True):

                    measurement=data_obs[j][i][index]
                    simulation=data_sim[j][i][index]
                    # minimum x records for every month
                    # double check already made in ctsm_vs_stations.py
                    if (data_qua[j][i][index] >= 20):
                        if (measurement < 1000 and simulation < 1000) : # why 1000?
                            help_list.append(
                                [int(date_start),
                                 round(station[0],3),
                                 round(station[1],3),
                                 round(depth,3),
                                 round(measurement,3),
                                 round(simulation,3)])
                        
                    checker1=bool(measurement < 1000)
                    checker2=bool(simulation  < 1000)

                
                    index=index+1 
                    
                if len(help_list)==12:  # if 12 values in a year
                    for item in help_list:
                        
                        list_all.append(item)

    

    all_result=pd.DataFrame(np.array(list_all),columns=['year','station_lon','station_lat','depth','measurement','simulation'])
    all_result.to_csv("results.tmp." + os.environ['run_name'] + ".csv",header=False,index=False)

    return all_result
             
## Extract files
stationtmpfile = sys.argv[1]
#stationtmpfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_004/stations-vs-ctsm.1979-2020.tmp.57_DOM02_004.nc"
datasettmp = nc.datasettmp(stationtmpfile)

# Load variables
data_obs   = datasettmp.variables['soiltemp'][:].T
time       = data_obs.shape[-1]
data_time  = datasettmp.variables['time'][:]
data_sim   = datasettmp.variables['ctsm_soiltemp'][:].T
data_depth = datasettmp.variables['depth'][:]
data_lon   = datasettmp.variables['lon'][:]
data_lat   = datasettmp.variables['lat'][:]
data_qua   = datasettmp.variables['quality'][:].T

datasettmp.close()

# Assign dates (YYYY) to time data
date_list = Date_transformer(data_time,1979)
# --------------------------------------------------------------------------

# --------------------- Extract data from NETCDF datasets ------------------
# We check whether we have data from every month of a year for every grid point,
# for all years. If this is not the case, this specific the data from that year
# gets discarded. This creates a results.csv file.
if exists("results.tmp." + os.environ['run_name'] + ".csv") == False:
	master = Extract_Depths(data_obs,data_sim,date_list,data_depth,data_lon,data_lat,data_qua)
	print("Data extracted!")
# --------------------------------------------------------------------------              
