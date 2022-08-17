# (from A. Damseaux)
# print a linear plot between modelled (from CTSM output) and observed data (from station)

import numpy as np
import netCDF4 as nc
import matplotlib.pylab as plt
from matplotlib.cm import ScalarMappable
import os
from os import sys
from plotting_functions import *

output_dir = os.environ['cegio'] + "/figures/linear/"
os.makedirs(output_dir, exist_ok=True)

# open netcdf
stationfile = sys.argv[1]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_004/stations-vs-ctsm.1979-2019.tmp.57_DOM02_004.nc"

dstation = nc.Dataset(stationfile, 'r') # read only

# write variables stations
sta_var   = dstation['soiltemp']
ctsm_var  = dstation['ctsm_soiltemp']
sta_var   = sta_var[:,:,0,:] # remove useless dimension

# remove depth below usuable
max_depth = 242
stepyear  = 5
sta_var   = sta_var[:,0:max_depth,:]
ctsm_var  = ctsm_var[:,0:max_depth,:]

# retrieve time index from year-month ctsm to station
startperiod = 1979 
endperiod   = 2020
years  = range(startperiod,endperiod)
nyears = endperiod-startperiod

# depth average
sta_var_davg  = np.average(sta_var, axis=1)
ctsm_var_davg = np.average(ctsm_var, axis=1)

# station average
sta_var_savg  = np.average(sta_var_davg, axis=1)
ctsm_var_savg = np.average(ctsm_var_davg, axis=1)

# running average
window=12
sta_var_ravg = np.average(sta_var_savg.reshape(-1, window), axis=1)
ctsm_var_ravg = np.average(ctsm_var_savg.reshape(-1, window), axis=1)

# difference
diff = ctsm_var_ravg-sta_var_ravg

## linear plot
fig, ax = plt.subplots(figsize=(12,4))

ax.plot(years, ctsm_var_ravg, label="ctsm", color="#AD885F")
ax.plot(years, sta_var_ravg, label="stations", color="black")

# color histogram
cm = plt.cm.RdYlBu_r
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
ax.bar(years, diff, color=cm(rescale(diff)))

# plot options
ax.axhline(y=0, color="k", linestyle="--")
ax.set_xlabel("year")
ax.set_ylabel("column soil temperature (in C)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

# legend
ctsm_pos_lab = legend_positions(years, ctsm_var_ravg)
sta_pos_lab  = legend_positions(years, sta_var_ravg)
ax.text(ctsm_pos_lab[0],ctsm_pos_lab[1],s="ctsm ouput",color="#AD885F")
ax.text(sta_pos_lab[0],sta_pos_lab[1],s="stations",color="black")

# colorbar
sm = ScalarMappable(cmap=cm, norm=plt.Normalize(np.min(diff),np.max(diff)))
sm.set_array([])
cbar = plt.colorbar(sm, pad=0.1)
cbar.set_label('difference', rotation=270,labelpad=10)

plot_name = output_dir + "linear_period"
plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')

