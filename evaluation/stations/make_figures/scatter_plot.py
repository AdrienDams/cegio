# print a scatter plot between CTSM and station file

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
    pd.read_csv(os.environ['cegio'] + "/evaluation/stations/make_figures/extracted_csv/results.tmp." + os.environ['run_name'] + ".csv",sep=',',header=None)),
                        columns=['year','month','station_lon','station_lat',
                                 'depth','measurement','simulation','altitude','station_id'])

# Make data lists
years   = all_result['year'].astype(int)
months = all_result['month'].astype(int)
depths  = all_result['depth']
station_lons = all_result['station_lon']
station_lats = all_result['station_lat']
measurements = all_result['measurement']
simulations  = all_result['simulation']
altitudes    = all_result['altitude']
station_ids  = all_result['station_id']

# Masked arrays with nan (-9999) values
invalid = -9999
valid_indexes = (measurements != invalid) & (simulations != invalid) & (measurements > -50)

# Group arrays
arrays = [years, months, depths, station_lons, station_lats, measurements, simulations, altitudes, station_ids, valid_indexes]
year, month, depth, station_lon, station_lat, measurement, simulation, altitude, station_id, valid_index = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

#  PLOT 1: Regions

# Plot pre-options
region_bins  = [-180,-140,0,50,80,125,180]
nregions = np.size(region_bins)-1
indexes_reg = []
region_color = ['#1f78b4','#33a02c','#ff7f00','#6a3d9a','#ffff99','#b15928']
region_label = ['Alaska','Canadian_Archipelago','European_Russia','Western_Siberia', \
					'Central_Siberia', 'Eastern_Siberia']

# Initialize plot 
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(10)

r_value = np.zeros(nregions)

for region in range(nregions):
	# group longitude indexes of same region
	mask = np.logical_and(arrays[station_lon] >= region_bins[region], arrays[station_lon] < region_bins[region+1])
	indexes_reg.append(np.where(mask)[0])

	update_valid_ind = arrays[valid_index][indexes_reg[region]]
	x_var = arrays[measurement][indexes_reg[region]][update_valid_ind]
	y_var = arrays[simulation][indexes_reg[region]][update_valid_ind]

	r_value[region], p_value = stats.pearsonr(x_var,y_var)

	sns.regplot(x = x_var,
				y = y_var,
				color = region_color[region],
				label = region_label[region],
				scatter_kws={'s':2,'alpha':0.2},
				line_kws={'label':"Linear Reg"})

# Plot post-options
# Grid on
ax.set_xlim(-40,30)
ax.set_ylim(-40,30)
plt.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)

# Labeling
ax.set_xlabel(r' Observed soil temperature in °C',fontsize=14)
ax.set_ylabel(r' Modeled soil temperature in °C ',fontsize=14)

# Legend
ax.legend(loc = 'lower right', bbox_to_anchor=(1.0, 0.0), ncol=1)
leg = ax.get_legend()
L_labels = leg.get_texts()
for i in range(nregions):
	L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

# Save fig
plot_name = output_dir + "scatter_regions"
plt.savefig(plot_name+'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

print("Regions scatter plot: done!")

# PLOT 2: Altitudes

altitudes_bins  = [0,100,200,400,800,1000]
naltitudes = np.size(altitudes_bins)-1
indexes_alt = []
altitudes_color = ['#01665e','#5ab4ac','#f6e8c3','#d8b365','#8c510a']
altitudes_label = ['0-100m','100-200m','200-400m','400-800m','800m +']

# Initialize plot
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(10)

r_value = np.zeros(naltitudes)

for alt in range(len(altitudes_bins)-1):
	mask = np.logical_and(arrays[altitude] >= altitudes_bins[alt], arrays[altitude] < altitudes_bins[alt + 1])
	indexes_alt.append(np.where(mask)[0])

	update_valid_ind = arrays[valid_index][indexes_alt[alt]]
	x_var = arrays[measurement][indexes_alt[alt]][update_valid_ind]
	y_var = arrays[simulation][indexes_alt[alt]][update_valid_ind]

	r_value[alt], p_value = stats.pearsonr(x_var,y_var)

	sns.regplot(
		x=x_var,
		y=y_var,
		color=altitudes_color[alt],
		label=altitudes_label[alt],
		scatter_kws={'s': 2, 'alpha': 0.2},
		line_kws={'label': "Linear Reg"})

# Plot options for altitude ranges
ax.set_xlim(-40, 30)
ax.set_ylim(-40, 30)
ax.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)

ax.set_xlabel(r'Observed soil temperature in °C', fontsize=14)
ax.set_ylabel(r'Modeled soil temperature in °C', fontsize=14)

ax.legend(loc='lower right', bbox_to_anchor=(1.0, 0.0), ncol=1)
leg = ax.get_legend()
L_labels = leg.get_texts()
for i in range(len(altitudes_bins) - 1):
    L_labels[(2 * i) + 1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

# Save fig
plot_name = output_dir + "scatter_altitudes"
plt.savefig(plot_name+'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

print("Altitudes scatter plot: done!")

#  PLOT 3, 4, 5: Each Region by Depths, Months, Decades

# Plot pre-options
depth_bins   = [0,40,80,120,185,320,np.max(depths)]
depths_color = ['#fdd0a2','#fdae6b','#fd8d3c','#f16913','#d94801','#8c2d04']
depths_label = ['0-40cm','40-80cm','80-120cm','120-185cm', '185-320cm',
            	'+320cm']

month_bins   = np.arange(1,14) # 12 + 0 numbering + upper limit
month_color = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                '#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
month_label = ['January','February','March','April','May','June',
            	'July','August','September','October','November','December']

startyear = int(os.environ['startyear'])
endyear   = int(os.environ['endyear'])
if(endyear > np.max(arrays[year])): endyear = np.max(arrays[year])

decades   = range(startyear, endyear,10)
if decades[-1] != endyear:
	decade_bins = np.append(decades,endyear)
else:
	decade_bins = decades 

decade_color_all = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00'] # 4 decades max (I add one just in case)
decade_color = decade_color_all[0:np.size(decade_bins)-1]
decade_label = [str(decade_bins[i]) + '-' + str(decade_bins[i+1]) for i in range(len(decade_bins)-1)]

# create lists comprehension for looping
bins = [depth_bins, month_bins, decade_bins]
colors = [depths_color, month_color, decade_color]
labels = [depths_label, month_label, decade_label]
key_variables = [depth, month, year]
key_variables_name = ["depths", "months", "decades"]

# Initialize plot
for region in range(nregions):
	# gather elements only from the region with previous masks
	reg_arrays = [array.values[indexes_reg[region].astype(int)] for array in arrays]

	for variable_type in range(np.size(key_variables)):
		fig, ax = plt.subplots()
		fig.set_figheight(10)
		fig.set_figwidth(10)

		bin_size = np.size(bins[variable_type])-1 # don't take first one to get n bins
		r_value = np.zeros(bin_size)

		for bin in range(bin_size):
			mask = np.logical_and(reg_arrays[key_variables[variable_type]] >= bins[variable_type][bin], 
									reg_arrays[key_variables[variable_type]] < bins[variable_type][bin+1])
			indexes_bin = np.where(mask)[0]
	
			update_valid_ind = reg_arrays[valid_index][indexes_bin]
			if np.size(update_valid_ind) == 0: continue

			x_var = reg_arrays[measurement][indexes_bin][update_valid_ind]
			y_var = reg_arrays[simulation][indexes_bin][update_valid_ind]
			
			r_value[bin], p_value = stats.pearsonr(x_var,y_var)
			
			sns.regplot(x = x_var,
						y = y_var,
						color = colors[variable_type][bin],
						label = labels[variable_type][bin],
						scatter_kws={'s':3,'alpha':0.3},
						line_kws={'label':"Linear Reg"})

		# Plot post-options
		# Grid on
		ax.set_xlim(-40,30)
		ax.set_ylim(-40,30)
		plt.plot([-40, 30], [-40, 30], color="gray", linestyle="--", linewidth=1)

		# Labeling
		ax.set_title(str(region_label[region]),fontsize=14)
		ax.set_xlabel(r' Observed soil temperature in °C',fontsize=14)
		ax.set_ylabel(r' Modeled soil temperature in °C ',fontsize=14)

		# Legend
		ax.legend(loc = 2, bbox_to_anchor = (1,1))
		leg = ax.get_legend()
		L_labels = leg.get_texts()
		if (np.size(L_labels)-2*bin_size != 0):
			print("Not enough data: pass graph " + str(region_label[region]) + " " + str(key_variables_name[variable_type]))
			continue

		for i in range(bin_size):
			L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

		# Save fig
		plot_name = output_dir + "scatter_" + str(region_label[region]) + "_" + str(key_variables_name[variable_type])
		plt.savefig(plot_name+'.png', format='png', bbox_inches='tight', dpi=300)
		plt.close()

		print(str(region_label[region]) + " " + str(key_variables_name[variable_type]) + " scatter plot: done!")
