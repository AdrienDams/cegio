# (from A. Damseaux)
# print only one spline graph

import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import similaritymeasures
import os
from os import sys
from scipy.interpolate import interp1d

# USER SETTINGS
year  = sys.argv[1]
month = sys.argv[2]
nstation = int(sys.argv[3])
nctsm    = int(sys.argv[4])
#year = "2000"
#month = "1"
#nstation = 12
#nctsm = 237592

# constant
abs_zero = 273.15

# open netcdf
stationfile = os.environ['cegio'] + "/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station.nc"
ctsmfile = os.environ['cegio'] + "/data/" + os.environ['run_name'] + "/monthly/" + os.environ['run_name'] + ".clm2.h0." + year + "-0" + month + ".nc"

dstation = nc.Dataset(stationfile, 'r') # read only
dctsm    = nc.Dataset(ctsmfile, 'r') # read only

# write variables stations
sta_depth = np.array(dstation['depth'])
sta_qua   = np.array(dstation['quality'])
sta_var   = np.array(dstation['soiltemp'])

# write variables ctsm outputs
ctsm_depth = np.array(dctsm['levgrnd'])*100 # convert from m to cm
ctsm_var   = np.array(dctsm['TSOI'])-abs_zero # convert from Kelvin to Celsius

# write dimensions ctsm
depth_ctsm   = np.size(dctsm.dimensions['levgrnd'])

# retrieve time index from year-month ctsm to station
date_index = ((int(year)-1979)*12)+int(month)-1 #verify the -1

# choose x and y
interp_points = 500
x1 = sta_var[date_index,:,:,nstation][:,0]
xf1 = x1[x1 > -abs_zero]
y1 = sta_depth
yf1 = y1[x1 > -abs_zero]
xf1 = xf1[yf1 < ctsm_depth[-1]] # be sure to don't take a depth below model
yf1 = yf1[yf1 < ctsm_depth[-1]] # be sure to don't take a depth below model

# interpolation top and bottom
top_interp = np.interp(yf1[0],ctsm_depth,ctsm_var[0,:,nctsm])
bot_interp = np.interp(yf1[-1],ctsm_depth,ctsm_var[0,:,nctsm])

# choose x and y 2
x2 = ctsm_var[0,:,nctsm] 											# choose only the station we want
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

# make plot
f = plt.figure()
ax = f.add_subplot(111)

plt.plot (x_smooth1, -y_new1, label="station")
plt.plot (x_smooth2, -y_new2, label="ctsm")
plt.scatter (xf1, -yf1)
plt.scatter (xf2, -yf2)

# area
plt.fill(np.append(x_smooth1, x_smooth2[::-1]), np.append(-y_new1, -y_new2[::-1]), 'red', alpha = 0.2)
plt.text(0.5, 0.5, "area: %s\N{DEGREE SIGN}C m"%round(pcm,2),horizontalalignment='center',\
          verticalalignment='center', transform = ax.transAxes,\
          bbox={'facecolor':'white','alpha':1,'edgecolor':'black','pad':1})
plt.title("station %s"%sys.argv[5] + " year %s"%year + " month %s"%month)

# plot options
plt.xlabel('soil temperature (in \N{DEGREE SIGN}C)')
plt.ylabel('depth (in cm)')

plt.legend()
plt.show()
