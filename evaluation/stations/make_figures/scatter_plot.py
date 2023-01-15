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

output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/scatter/"
os.makedirs(output_dir, exist_ok=True)

# DATA-Import from CSV (12 months for every point)
all_result = pd.DataFrame(np.array(
    pd.read_csv("/work/aa0049/a271098/cegio/evaluation/stations/make_figures/results.tmp." + os.environ['run_name'] + ".csv",sep=',',header=None)),
                        columns=['year','station_lon','station_lat',
                                 'depth','measurement','simulation'])

# Make data lists
year  = all_result['year'].astype(int)
depth = all_result['depth']
station_lon = np.round(all_result['station_lon'],2)
station_lat = np.round(all_result['station_lat'],2)
measurement = np.round(all_result['measurement'],2)
simulation  = np.round(all_result['simulation'],2)
nmonths=12

#  PLOT 1: Months 

# Plot pre-options
color_months = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                '#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
label_months = ['January','February','March','April','May','June',
            	'July','August','September','October','November','December']

# Initialize plot 
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
				scatter_kws={'s':5,'alpha':0.6},
				line_kws={'label':"Linear Reg"})

# Plot post-options

# Grid on
ax.set_xlim(-40,30)
ax.set_ylim(-40,30)
plt.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)

# Labeling
ax.set_xlabel(r' Observation in °C',fontsize=14)
ax.set_ylabel(r' Simulation in °C ',fontsize=14)

# Legend
ax.legend(loc = 2, bbox_to_anchor = (1,1))
leg = ax.get_legend()
L_labels = leg.get_texts()
for i in range(nmonths):
	L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

# Save fig
plot_name = output_dir + "scatter_months"
plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')
plt.close()

print("months scatter plot: done!")

#  PLOT 2: Depths

# Plot pre-options
depth_bins   = [0,40,80,120,185,320,np.max(depth)]
color_depths = ['#fdd0a2','#fdae6b','#fd8d3c','#f16913','#d94801','#8c2d04']
label_depths = ['0-40cm','40-80cm','80-120cm','120-185cm', '185-320cm',
            	'+320cm']

# Initialize plot
for month in range(nmonths):
	fig, ax = plt.subplots()
	fig.set_figheight(10)
	fig.set_figwidth(15)
	r_value = np.zeros(np.size(depth_bins)-1)

	for i in range(np.size(depth_bins)-1): # don't take first one to get 6 bins
		ind_bin1 = np.where(depth==depth_bins[i])[0][0]
		ind_bin2 = np.where(depth==depth_bins[i+1])[0][0]
		
		slope, intercept, r_value[i], p_value, std_err = \
			stats.linregress(measurement[ind_bin1:ind_bin2:nmonths+month],simulation[ind_bin1:ind_bin2:nmonths+month])
		
		sns.regplot(x = measurement[ind_bin1:ind_bin2:nmonths+month],
					y = simulation[ind_bin1:ind_bin2:nmonths+month],
					color = color_depths[i],
					label = label_depths[i],
					scatter_kws={'s':5,'alpha':0.6},
					line_kws={'label':"Linear Reg"})

	# Plot post-options

	# Grid on
	ax.set_xlim(-40,30)
	ax.set_ylim(-40,30)
	plt.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)

	# Labeling
	ax.set_title(str(label_months[month]),fontsize=14)
	ax.set_xlabel(r' Observation in °C',fontsize=14)
	ax.set_ylabel(r' Simulation in °C ',fontsize=14)

	# Legend
	ax.legend(loc = 2, bbox_to_anchor = (1,1))
	leg = ax.get_legend()
	L_labels = leg.get_texts()
	for i in range(np.size(depth_bins)-1):
		L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

	# Save fig
	plot_name = output_dir + "scatter_depths.month" + str(month+1)
	plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')
	plt.close()

	print("depths scatter plot month" + str(month+1) + ": done!")

#  PLOT 3: Regions

# Reorder data, get indices of elements in station_lon sorted in ascending order
sort_indices = np.argsort(station_lon)

# Sort the arrays using the sort indices
year_lonsrt 		= np.array(year)[sort_indices]
depth_lonsrt 		= np.array(depth)[sort_indices]
station_lon_lonsrt 	= np.array(station_lon)[sort_indices]
station_lat_lonsrt 	= np.array(station_lat)[sort_indices]
measurement_lonsrt 	= np.array(measurement)[sort_indices]
simulation_lonsrt	= np.array(simulation)[sort_indices]


# Plot pre-options
spatial_bins  = [-180,-140,0,50,80,125,180]
color_spatial = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33']
label_spatial = ['Alaska','Canadian Archipelago','European Russia','Western Siberia', \
					'Central Siberia', 'Eastern Siberia']

# Initialize plot
for month in range(nmonths):
	fig, ax = plt.subplots()
	fig.set_figheight(10)
	fig.set_figwidth(15)
	r_value = np.zeros(np.size(spatial_bins)-1)

	for i in range(np.size(spatial_bins)-1): # don't take first one to get 6 bins
		# Calculate the absolute difference between the target longitude and each element in the station_lon array
		diff1 = np.abs(station_lon_lonsrt-spatial_bins[i])
		diff2 = np.abs(station_lon_lonsrt-spatial_bins[i+1])
		# Find the index of the minimum difference (i.e. the closest longitude)
		ind_bin1 = np.argmin(diff1)
		ind_bin2 = np.argmin(diff2)
		
		slope, intercept, r_value[i], p_value, std_err = \
			stats.linregress(measurement[ind_bin1:ind_bin2:nmonths+month],simulation[ind_bin1:ind_bin2:nmonths+month])
		
		sns.regplot(x = measurement[ind_bin1:ind_bin2:nmonths+month],
					y = simulation[ind_bin1:ind_bin2:nmonths+month],
					color = color_spatial[i],
					label = label_spatial[i],
					scatter_kws={'s':5,'alpha':0.6},
					line_kws={'label':"Linear Reg"})

	# Plot post-options

	# Grid on
	ax.set_xlim(-40,30)
	ax.set_ylim(-40,30)
	plt.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)

	# Labeling
	ax.set_title(str(label_months[month]),fontsize=14)
	ax.set_xlabel(r' Observation in °C',fontsize=14)
	ax.set_ylabel(r' Simulation in °C ',fontsize=14)

	# Legend
	ax.legend(loc = 2, bbox_to_anchor = (1,1))
	leg = ax.get_legend()
	L_labels = leg.get_texts()
	for i in range(np.size(spatial_bins)-1):
		L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

	# Save fig
	plot_name = output_dir + "scatter_spatial.month" + str(month+1)
	plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')
	plt.close()

	print("spatial scatter plot month" + str(month+1) + ": done!")

#  PLOT 4: Decades

# Reorder data, get indices of elements in year sorted in ascending order
sort_indices = np.argsort(year)

# Sort the arrays using the sort indices
year_timsrt 		= np.array(year)[sort_indices]
depth_timsrt 		= np.array(depth)[sort_indices]
station_lon_timsrt 	= np.array(station_lon)[sort_indices]
station_lat_timsrt 	= np.array(station_lat)[sort_indices]
measurement_timsrt 	= np.array(measurement)[sort_indices]
simulation_timsrt	= np.array(simulation)[sort_indices]

# Plot pre-options
decades = range(np.min(year_timsrt), np.max(year_timsrt),10)
if decades[-1] != np.max(year_timsrt):
	temporal_bins = np.append(decades,np.max(year_timsrt))
else:
	temporal_bins = decades 

all_color_temporal = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33']
color_temporal = all_color_temporal[0:np.size(temporal_bins)-1]
label_temporal = ['1980-1990','1990-2000','2000-2010','2010-2020']

# Initialize plot
for month in range(nmonths):
	fig, ax = plt.subplots()
	fig.set_figheight(10)
	fig.set_figwidth(15)
	r_value = np.zeros(np.size(temporal_bins)-1)

	for i in range(np.size(temporal_bins)-1): # don't take first one to get 6 bins
		ind_bin1 = np.where(year_timsrt==temporal_bins[i])[0][0]
		ind_bin2 = np.where(year_timsrt==temporal_bins[i+1])[0][0]
		
		slope, intercept, r_value[i], p_value, std_err = \
			stats.linregress(measurement[ind_bin1:ind_bin2:nmonths+month],simulation[ind_bin1:ind_bin2:nmonths+month])
		
		sns.regplot(x = measurement[ind_bin1:ind_bin2:nmonths+month],
					y = simulation[ind_bin1:ind_bin2:nmonths+month],
					color = color_temporal[i],
					label = label_temporal[i],
					scatter_kws={'s':5,'alpha':0.6},
					line_kws={'label':"Linear Reg"})

	# Plot post-options

	# Grid on
	ax.set_xlim(-40,30)
	ax.set_ylim(-40,30)
	plt.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)

	# Labeling
	ax.set_title(str(label_months[month]),fontsize=14)
	ax.set_xlabel(r' Observation in °C',fontsize=14)
	ax.set_ylabel(r' Simulation in °C ',fontsize=14)

	# Legend
	ax.legend(loc = 2, bbox_to_anchor = (1,1))
	leg = ax.get_legend()
	L_labels = leg.get_texts()
	for i in range(np.size(temporal_bins)-1):
		L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

	# Save fig
	plot_name = output_dir + "scatter_temporal.month" + str(month+1)
	plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')
	plt.close()

	print("temporal scatter plot month" + str(month+1) + ": done!")

