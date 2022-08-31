# (from A. Damseaux)
# compute pcm area for every station

import numpy as np
import netCDF4 as nc
import similaritymeasures
import os
from os import sys
from scipy.interpolate import interp1d

# constant
abs_zero = 273.15

# open netcdf
ctsmfile    = sys.argv[1]
stationfile = sys.argv[2]

dstation = nc.Dataset(stationfile, 'a') # append
dctsm    = nc.Dataset(ctsmfile, 'r') # read only

# open index
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", delimiter=" ", dtype=int)

# write variables stations
sta_depth = np.array(dstation['depth'])
sta_qua   = np.array(dstation['quality'])
sta_var   = np.array(dstation['soiltemp'])
pcm_area  = dstation['pcm_area']

# write variables ctsm outputs
ctsm_depth = np.array(dctsm['levgrnd'])*100 # convert from m to cm
ctsm_var   = np.array(dctsm['TSOI'])-abs_zero # convert from Kelvin to Celsius

# write dimensions ctsm
depth_ctsm   = np.size(dctsm.dimensions['levgrnd'])

# retrieve time index from year-month ctsm to station
year  = int(os.environ['year'])
month = int(os.environ['month'])
date_index = ((year-1979)*12)+month-1

# select depth for pcm
min_points = 4 # minimum of points in station to compute
interp_points = 500
quality_minimum = 20.0

for i in range(len(index_table[:,0])):
 # choose x and y
 x1 = sta_var[date_index,:,index_table[i,0]][:,0]
 xf1 = x1[x1 > -abs_zero] # remove null data
 if( np.size(xf1) >= min_points ): # run the rest if enough data
  # check if quality is good enough
  A = sta_qua[date_index,:,0,index_table[i,0]]
  if( A[A > 0].mean() > quality_minimum ):
   y1 = sta_depth
   yf1 = y1[x1 > -abs_zero] # remove null data
   xf1 = xf1[yf1 < ctsm_depth[-1]] # be sure to don't take a depth below model
   yf1 = yf1[yf1 < ctsm_depth[-1]] # be sure to don't take a depth below model

   # interpolation top and bottom
   top_interp = np.interp(yf1[0],ctsm_depth,ctsm_var[0,:,index_table[i,1]])
   bot_interp = np.interp(yf1[-1],ctsm_depth,ctsm_var[0,:,index_table[i,1]])

   # choose x and y 2
   x2 = ctsm_var[0,:,index_table[i,1]] 											# choose only the station we want
   xf2 = x2[np.where((ctsm_depth > yf1[0]) & (ctsm_depth < yf1[-1]))] 	# add temps between both interp station depth
   xf2 = np.append(top_interp, xf2) 									# add first station temp
   xf2 = np.append(xf2, bot_interp) 									# add last station temp
   yf2 = ctsm_depth[np.where((ctsm_depth > yf1[0]) & (ctsm_depth < yf1[-1]))] # add depths between both interp station depth
   yf2 = np.append(yf1[0], yf2)  										# add first station depth
   yf2 = np.append(yf2, yf1[-1]) 										# add last station depth 

   # spline construction
   y_new1 = np.linspace(yf1.min(), yf1.max(),interp_points)
   y_new2 = np.linspace(yf2.min(), yf2.max(),interp_points)
   f1 = interp1d(yf1, xf1, kind='quadratic')
   f2 = interp1d(yf2, xf2, kind='quadratic')
   x_smooth1 = f1(y_new1)
   x_smooth2 = f2(y_new2)

   # similiraty measures
   spline1 = np.zeros((interp_points,2))
   spline2 = np.zeros((interp_points,2))

   spline1[:,0] = x_smooth1
   spline2[:,0] = x_smooth2
   spline1[:,1] = y_new1
   spline2[:,1] = y_new2

   pcm = similaritymeasures.pcm(spline1, spline2)
   if( pcm > 500.0 ):
    print("Warning: PCM value very high")
    print(index_table[i,0],index_table[i,1],pcm)

   # fill value in table
   pcm_area[date_index,index_table[i,0]] = pcm

dstation.close()
