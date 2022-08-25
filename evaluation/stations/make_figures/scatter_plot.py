import netCDF4 as nc
import numpy as np
import pandas as pd
from datetime import date
import os
from os.path import exists
import matplotlib.pyplot as plt
import sys
import seaborn as sns
sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": "-"})
from scipy import stats
from extract_functions import *

# ----------------------------- Open data ---------------------------------
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/scatter/"
os.makedirs(output_dir, exist_ok=True)

# Load file
stationfile = sys.argv[1]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_004/stations-vs-ctsm.1979-2019.tmp.57_DOM02_004.nc"
dataset = nc.Dataset(stationfile)

# Load variables
data_obs   = dataset.variables['soiltemp'][:].T
time       = data_obs.shape[-1]
data_time  = dataset.variables['time'][:]
data_sim   = dataset.variables['ctsm_soiltemp'][:].T
data_depth = dataset.variables['depth'][:]
data_lon   = dataset.variables['lon'][:]
data_lat   = dataset.variables['lat'][:]
nmonths    = 12

dataset.close()

# Assign dates (YYYY) to time data
date_list = Date_transformer(data_time,1979)
# --------------------------------------------------------------------------

# --------------------- Extract data from NETCDF Datasets ------------------
# We check whether we have data from every month of a year for every grid point,
# for all years. If this is not the case, this specific the data from that year
# gets discarded. This creates a results.csv file.
if exists("results.csv") == False:
	master = Extract_Depths(data_obs,data_sim,date_list,data_depth,data_lon,data_lat)
	print("Data extracted!")
# --------------------------------------------------------------------------

# -------------------------- DATA-Import from CSV --------------------------
# 12 months for every point
all_result = pd.DataFrame(np.array(
    pd.read_csv('results.csv',sep=',',header=None)),
                        columns=['year','station_lon','station_lat',
                                 'depth','measurement','simulation'])
# --------------------------------------------------------------------------

# ----------------------------- Make data lists ----------------------------
year  = all_result['year'].astype(int)
depth = all_result['depth']
station_lon = np.round(all_result['station_lon'],2)
station_lat = np.round(all_result['station_lat'],2)
measurement = np.round(all_result['measurement'],2)
simulation  = np.round(all_result['simulation'],2)
# --------------------------------------------------------------------------

# ---------------------------- PLOT 1: MONTHS ------------------------------

# ---------------------------- Plot pre-options ----------------------------
# plot colors
color_months = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                '#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
label_months = ['January','February','March','April','May','June',
            	'July','August','September','October','November','December']

# ----------------------------- Initialize plot ---------------------------- 
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)
r_value = np.zeros(nmonths)

for i in range(nmonths):
	slope, intercept, r_value[i], p_value, std_err = stats.linregress(measurement[i:-1:nmonths],simulation[i:-1:nmonths])

	sns.regplot(x = measurement[i:-1:nmonths],
				y = simulation[i:-1:nmonths],
				color = color_months[i],
				label = label_months[i],
				scatter_kws={'s':7},
				line_kws={'label':"Linear Reg"})
# --------------------------------------------------------------------------

# ---------------------------- Plot post-options ---------------------------
# Grid on
ax.set_xlim(-40,30)
ax.set_ylim(-40,30)
plt.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)
# --------------------------------------------------------------------------

# --------------------------------- Labeling -------------------------------
ax.set_xlabel(r' Observation in °C',fontsize=14)
ax.set_ylabel(r' Simulation in °C ',fontsize=14)
# --------------------------------------------------------------------------

# --------------------------------- Legend ---------------------------------
ax.legend(loc = 2, bbox_to_anchor = (1,1))
leg = ax.get_legend()
L_labels = leg.get_texts()
for i in range(nmonths):
	L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

# --------------------------------- Save fig -------------------------------
plot_name = output_dir + "scatter_months"
plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')
plt.close()

print("months scatter plot: done!")

# ---------------------------- PLOT 2: DEPTHS ------------------------------

# ---------------------------- Plot pre-options ----------------------------
depth_bins   = [0,40,80,120,160,200,320,np.max(depth)]
color_depths = ['#ffffd4','#fee391','#fec44f','#fe9929','#ec7014','#cc4c02',
                '#8c2d04']
label_depths = ['0-40cm','40-80cm','80-120cm','120-160cm','160-200cm','200-320cm',
            	'+320cm']

# ----------------------------- Initialize plot ----------------------------
for month in range(nmonths):
	fig, ax = plt.subplots()
	fig.set_figheight(10)
	fig.set_figwidth(15)
	r_value = np.zeros(np.size(depth_bins)-1)

	for i in range(np.size(depth_bins)-1): 								# don't take first one to get 7 bins
		ind_bin1 = np.where(depth==depth_bins[i])[0][0]
		ind_bin2 = np.where(depth==depth_bins[i+1])[0][0]
		
		slope, intercept, r_value[i], p_value, std_err = \
			stats.linregress(measurement[ind_bin1:ind_bin2:nmonths+month],simulation[ind_bin1:ind_bin2:nmonths+month])
		
		sns.regplot(x = measurement[ind_bin1:ind_bin2:nmonths+month],
					y = simulation[ind_bin1:ind_bin2:nmonths+month],
					color = color_depths[i],
					label = label_depths[i],
					scatter_kws={'s':7},
					line_kws={'label':"Linear Reg"})
	# --------------------------------------------------------------------------

	# ---------------------------- Plot post-options ---------------------------
	# Grid on
	ax.set_xlim(-40,30)
	ax.set_ylim(-40,30)
	plt.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)
	# --------------------------------------------------------------------------

	# --------------------------------- Labeling -------------------------------
	ax.set_title(str(label_months[month]),fontsize=14)
	ax.set_xlabel(r' Observation in °C',fontsize=14)
	ax.set_ylabel(r' Simulation in °C ',fontsize=14)
	# --------------------------------------------------------------------------

	# --------------------------------- Legend ---------------------------------
	ax.legend(loc = 2, bbox_to_anchor = (1,1))
	leg = ax.get_legend()
	L_labels = leg.get_texts()
	for i in range(np.size(depth_bins)-1):
		L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

	# --------------------------------- Save fig -------------------------------
	plot_name = output_dir + "scatter_depths.month" + str(month+1)
	plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')
	plt.close()

	print("depths scatter plot month" + str(month+1) + ": done!")















