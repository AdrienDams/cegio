# (from A. Damseaux)
# print a linear plot between modelled (from CTSM output) and observed data (from station)

import numpy as np
import netCDF4 as nc
import matplotlib.pylab as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import TwoSlopeNorm
import os
from os import sys
from plotting_functions import *

output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/linear/"
os.makedirs(output_dir, exist_ok=True)

# open netcdf
stationfile = sys.argv[1]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/orig_data/old/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_ctsm_0906.nc"

dstation = nc.Dataset(stationfile, 'r') # read only

station_choosen = int(sys.argv[2])

# write variables stations
sta_var  = dstation['soiltemp']
ctsm_var = dstation['ctsm_soiltemp']

# extract station
sta_var  = sta_var[:,:,station_choosen]
ctsm_var = ctsm_var[:,:,station_choosen]

# remove depth below usuable
max_depth = 242
stepyear  = 5
sta_var   = sta_var[:,0:max_depth]
ctsm_var  = ctsm_var[:,0:max_depth]

# depth average
sta_var_davg  = np.average(sta_var, axis=1)
ctsm_var_davg = np.average(ctsm_var, axis=1)

# retrieve time index from year-month ctsm to station
startindex = np.min(np.nonzero(sta_var_davg.data))
endindex   = np.max(np.nonzero(sta_var_davg.data))

startperiod = 1979 + int(np.ceil(startindex/12))
endperiod   = 1979 + int(np.floor(endindex/12))

startindex_real = (startperiod - 1979) *12
endperiod_real  = (endperiod - 1979) *12

years  = range(startperiod,endperiod)
nyears = endperiod-startperiod

# select years
sta_var_ysel = sta_var_davg[startindex_real:endperiod_real]
ctsm_var_ysel = ctsm_var_davg[startindex_real:endperiod_real]

# running average
window=12
sta_var_ravg = np.mean(sta_var_ysel.reshape(-1, window), axis=1)
ctsm_var_ravg = np.mean(ctsm_var_ysel.reshape(-1, window), axis=1)

# difference
diff = ctsm_var_ravg-sta_var_ravg

## linear plot
fig, ax = plt.subplots(figsize=(12,4))

ax.plot(years, ctsm_var_ravg, color="#AD885F")
ax.plot(years, sta_var_ravg, color="black")

# color histogram
cm = plt.cm.RdYlBu_r
def my_ceil(a, precision=1):
    return np.true_divide(np.ceil(a * 10**precision), 10**precision)
cmap_top = my_ceil(np.max(np.absolute(diff)))
#rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
rescale = lambda y: (y - (-cmap_top)) / (cmap_top - -(cmap_top))
ax.bar(years, diff, color=cm(rescale(diff)))

# plot options
ymax = np.max([sta_var_ravg,ctsm_var_ravg,diff]) + 0.5
ymin = np.min([sta_var_ravg,ctsm_var_ravg,diff]) - 0.5
ax.set_ylim([ymin, ymax])
ax.axhline(y=0, color="k", linestyle="--")
ax.set_xlabel("year")
ax.set_ylabel("column soil temperature (in \N{DEGREE SIGN}C)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

# legend
ctsm_pos_lab = legend_positions(years, ctsm_var_ravg)
sta_pos_lab  = legend_positions(years, sta_var_ravg)
ax.text(ctsm_pos_lab[0],ctsm_pos_lab[1],s="ctsm ouput",color="#AD885F")
ax.text(sta_pos_lab[0],sta_pos_lab[1],s="station %s"%sys.argv[3],color="black")

# colorbar
sm = ScalarMappable(cmap=cm, norm=plt.Normalize(-cmap_top,cmap_top))
sm.set_array([])
cbar = plt.colorbar(sm, pad=0.1)
cbar.set_label('difference', rotation=270,labelpad=10)

plot_name = output_dir + "linear_station_%s"%sys.argv[3]
plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')

print("linear plot figure done!")

