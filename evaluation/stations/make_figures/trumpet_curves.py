# script to produce one trumpet curve graph from CTSM output and stations data

import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import os
from os import sys
from scipy.interpolate import interp1d

## Constant
abs_zero = 273.15

output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/trumpet/"
os.makedirs(output_dir, exist_ok=True)

## Data

# open netcdf
stationfile_dir   = os.environ['cegio'] + "/data/stations/orig_data/"
stationfile_magt = stationfile_dir + "arctic_stations.soiltemp.yearly.mean.nc"
stationfile_min  = stationfile_dir + "arctic_stations.soiltemp.yearly.min.nc"
stationfile_max  = stationfile_dir + "arctic_stations.soiltemp.yearly.max.nc"

ctsmfile_dir  = os.environ['cegio'] + "/data/postproc/" + os.environ['run_name'] + "/processed/permafrost/"
ctsmfile_magt = ctsmfile_dir + os.environ['run_name'] + "." + os.environ['startyear'] + "-" + os.environ['endyear'] + ".magt.nc"
ctsmfile_min  = ctsmfile_dir + os.environ['run_name'] + ".minAGT." + os.environ['startyear'] + "-" + os.environ['endyear'] + ".nc"
ctsmfile_max  = ctsmfile_dir + os.environ['run_name'] + ".maxAGT." + os.environ['startyear'] + "-" + os.environ['endyear'] + ".nc"

dstation_magt = nc.Dataset(stationfile_magt, 'r') # read only
dstation_min  = nc.Dataset(stationfile_min, 'r')
dstation_max  = nc.Dataset(stationfile_max, 'r')

dctsm_magt = nc.Dataset(ctsmfile_magt, 'r')
dctsm_min  = nc.Dataset(ctsmfile_min, 'r')
dctsm_max  = nc.Dataset(ctsmfile_max, 'r')

# define function to apply temperature range mask to array
def filter_array(arr):
    masked_arr = np.ma.masked_invalid(arr)
    mask = (masked_arr >= -50) & (masked_arr <= 50)
    return np.where(mask, masked_arr, np.nan)

# write variables stations
sta_depth = np.array(dstation_magt['depth'])
sta_magt  = filter_array(dstation_magt['value'][:,:,0,:])
sta_min   = filter_array(dstation_min['value'][:,:,0,:])
sta_max   = filter_array(dstation_max['value'][:,:,0,:])

# write variables ctsm outputs
ctsm_depth = np.array(dctsm_magt['levgrnd'])*100 # convert from m to cm
ctsm_magt  = filter_array(np.array(dctsm_magt['TSOI'])-abs_zero) # convert from Kelvin to Celsius
ctsm_min   = filter_array(np.array(dctsm_min['TSOI'])-abs_zero)
ctsm_max   = filter_array(np.array(dctsm_max['TSOI'])-abs_zero)

# select variables for plot
interp_points = 500
nsta  = int(sys.argv[1])
nctsm = int(sys.argv[2])
#nsta = 125
#nctsm = 33127
maxdepth = 20

## Period to be choosen (depending on station data)
period = np.ma.nonzero(np.nanmean(~np.isnan(sta_magt[1:,:,nsta]),axis=1)) # nsta to choose station
startyearind = period[0][0]
endyearind   = period[0][-1] + 1
startyear    = startyearind + 1980
endyear      = endyearind + 1980 - 1

## Stations compute, +1 because not first year

# mean
sta_magt_mean = np.nanmean(sta_magt[startyearind+1:endyearind+1,:,nsta],axis=0) 
sta_min_mean  = np.nanmean(sta_min[startyearind+1:endyearind+1,:,nsta],axis=0)
sta_max_mean  = np.nanmean(sta_max[startyearind+1:endyearind+1,:,nsta],axis=0)
# std
sta_magt_std = np.nanstd(sta_magt[startyearind+1:endyearind+1,:,nsta],axis=0)
sta_min_std  = np.nanstd(sta_min[startyearind+1:endyearind+1,:,nsta],axis=0)
sta_max_std  = np.nanstd(sta_max[startyearind+1:endyearind+1,:,nsta],axis=0)

## Model output compute, nctsm to choose grid point closest to station

# mean
ctsm_magt_mean = np.nanmean(ctsm_magt[startyearind:endyearind,:,nctsm],axis=0)
ctsm_min_mean  = np.nanmean(ctsm_min[startyearind:endyearind,:,nctsm],axis=0)
ctsm_max_mean  = np.nanmean(ctsm_max[startyearind:endyearind,:,nctsm],axis=0)
# std
ctsm_magt_std = np.nanstd(ctsm_magt[startyearind:endyearind,:,nctsm],axis=0)
ctsm_min_std  = np.nanstd(ctsm_min[startyearind:endyearind,:,nctsm],axis=0)
ctsm_max_std  = np.nanstd(ctsm_max[startyearind:endyearind,:,nctsm],axis=0)

## Graph

# choose axis model
ydepth_ctsm = ctsm_depth[0:maxdepth]

xmagt_ctsm = ctsm_magt_mean[0:maxdepth]
xmin_ctsm  = ctsm_min_mean[0:maxdepth]
xmax_ctsm  = ctsm_max_mean[0:maxdepth]

# choose axis station
ydepth_sta_m = sta_depth[sta_depth < ydepth_ctsm[-1]] # be sure to don't take a depth below model

xmagt_sta_m = sta_magt_mean[sta_depth < ydepth_ctsm[-1]]
xmin_sta_m  = sta_min_mean[sta_depth < ydepth_ctsm[-1]]
xmax_sta_m  = sta_max_mean[sta_depth < ydepth_ctsm[-1]]

# use only masked data station
xmagt_sta = xmagt_sta_m[np.ma.nonzero(xmagt_sta_m)]
xmin_sta  = xmin_sta_m[np.ma.nonzero(xmagt_sta_m)]
xmax_sta  = xmax_sta_m[np.ma.nonzero(xmagt_sta_m)]

ydepth_sta = ydepth_sta_m[np.ma.nonzero(xmagt_sta_m)]

# use only masked data std station
xmagt_sta_std = sta_magt_std[np.ma.nonzero(xmagt_sta_m)]
xmin_sta_std  = sta_min_std[np.ma.nonzero(xmagt_sta_m)]
xmax_sta_std  = sta_max_std[np.ma.nonzero(xmagt_sta_m)]

# plot area std (l = left, r = right)
magt_stdl = ctsm_magt_mean[0:maxdepth] - ctsm_magt_std[0:maxdepth]/2
magt_stdr = ctsm_magt_mean[0:maxdepth] + ctsm_magt_std[0:maxdepth]/2
min_stdl  = ctsm_min_mean[0:maxdepth] - ctsm_min_std[0:maxdepth]/2
min_stdr  = ctsm_min_mean[0:maxdepth] + ctsm_min_std[0:maxdepth]/2
max_stdl  = ctsm_max_mean[0:maxdepth] - ctsm_max_std[0:maxdepth]/2
max_stdr  = ctsm_max_mean[0:maxdepth] + ctsm_max_std[0:maxdepth]/2

# spline construction lines model
ydepth_lin_ctsm = np.linspace(ydepth_ctsm.min(), ydepth_ctsm.max(),interp_points)

f_magt_ctsm = interp1d(ydepth_ctsm, xmagt_ctsm, kind='quadratic')
f_min_ctsm  = interp1d(ydepth_ctsm, xmin_ctsm, kind='quadratic')
f_max_ctsm  = interp1d(ydepth_ctsm, xmax_ctsm, kind='quadratic')

xmagt_smooth_ctsm = f_magt_ctsm(ydepth_lin_ctsm)
xmin_smooth_ctsm  = f_min_ctsm(ydepth_lin_ctsm)
xmax_smooth_ctsm  = f_max_ctsm(ydepth_lin_ctsm)

# spline construction std

f_magt_stdl = interp1d(ydepth_ctsm, magt_stdl, kind='quadratic')
f_magt_stdr = interp1d(ydepth_ctsm, magt_stdr, kind='quadratic')
f_min_stdl  = interp1d(ydepth_ctsm, min_stdl, kind='quadratic')
f_min_stdr  = interp1d(ydepth_ctsm, min_stdr, kind='quadratic')
f_max_stdl  = interp1d(ydepth_ctsm, max_stdl, kind='quadratic')
f_max_stdr  = interp1d(ydepth_ctsm, max_stdr, kind='quadratic')

xmagt_stdl_smooth = f_magt_stdl(ydepth_lin_ctsm)
xmagt_stdr_smooth = f_magt_stdr(ydepth_lin_ctsm)
xmin_stdl_smooth  = f_min_stdl(ydepth_lin_ctsm)
xmin_stdr_smooth  = f_min_stdr(ydepth_lin_ctsm)
xmax_stdl_smooth  = f_max_stdl(ydepth_lin_ctsm)
xmax_stdr_smooth  = f_max_stdr(ydepth_lin_ctsm)

# make plot
fig = plt.figure()
ax  = fig.add_subplot(111)

plt.plot(xmagt_smooth_ctsm, -ydepth_lin_ctsm, color="dimgrey")
plt.plot(xmin_smooth_ctsm, -ydepth_lin_ctsm, color="lightseagreen")
plt.plot(xmax_smooth_ctsm, -ydepth_lin_ctsm, color="salmon")

# errorbar area model
plt.fill_betweenx(-ydepth_lin_ctsm, xmagt_stdl_smooth, xmagt_stdr_smooth, alpha=0.2, color="dimgrey")
plt.fill_betweenx(-ydepth_lin_ctsm, xmin_stdl_smooth, xmin_stdr_smooth, alpha=0.2, color="lightseagreen")
plt.fill_betweenx(-ydepth_lin_ctsm, xmax_stdl_smooth, xmax_stdr_smooth, alpha=0.2, color="salmon")

not_nan_idx = ~np.isnan(xmagt_sta)
# errorbar station
plt.errorbar(xmagt_sta[not_nan_idx], -ydepth_sta[not_nan_idx], xerr = xmagt_sta_std[not_nan_idx], color="black", linestyle='dashed', capsize=2, linewidth=1.5)
plt.errorbar(xmin_sta[not_nan_idx], -ydepth_sta[not_nan_idx], xerr = xmin_sta_std[not_nan_idx], color="teal", linestyle='dashed', capsize=2, linewidth=1.5)
plt.errorbar(xmax_sta[not_nan_idx], -ydepth_sta[not_nan_idx], xerr = xmax_sta_std[not_nan_idx], color="orangered", linestyle='dashed', capsize=2, linewidth=1.5)

# plot options
plt.xlabel('soil temperature (in \N{DEGREE SIGN}C)')
plt.ylabel('depth (in cm)')
plt.title('Sturm run vs %s'%sys.argv[3] +  ' station, period %s'%startyear + '-%s'%endyear)
plt.grid(True, color = "grey", linestyle = "-.", alpha=0.2)
plt.axvline(x=0, color="black", linestyle=":")

plot_name = output_dir + "trumpet_curves_%s"%sys.argv[3]
plt.savefig(plot_name+'.png', format='png', bbox_inches='tight', dpi=300)

print("trumpet curves figure done!")
