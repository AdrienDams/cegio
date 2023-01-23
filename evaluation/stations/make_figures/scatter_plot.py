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
                                 'depth','measurement','simulation'])

# Make data lists
year   = all_result['year'].astype(int)
months = all_result['month'].astype(int)
depth  = all_result['depth']
station_lon = all_result['station_lon']
station_lat = all_result['station_lat']
measurement = all_result['measurement']
simulation  = all_result['simulation']

# Masked arrays with nan (-9999) values
invalid = -9999
valid_indices = (measurement != invalid) & (simulation != invalid)

nmonths = 12

#  PLOT 1: Months 

# Plot pre-options
color_months = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                '#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
label_months = ['January','February','March','April','May','June',
            	'July','August','September','October','November','December']

# Initialize plot 
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(11)

r_value = np.zeros(nmonths)

for i in range(nmonths):
	r_value[i], p_value = stats.pearsonr(measurement[i:-1:nmonths][valid_indices],simulation[i:-1:nmonths][valid_indices])
#
	sns.regplot(x = measurement[i:-1:nmonths][valid_indices],
				y = simulation[i:-1:nmonths][valid_indices],
				color = color_months[i],
				label = label_months[i],
				scatter_kws={'s':3,'alpha':0.3},
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

#  PLOT 2, 3, 4: Depths, Regions, Decades

# Plot pre-options
depth_bins   = [0,40,80,120,185,320,np.max(depth)]
depths_color = ['#fdd0a2','#fdae6b','#fd8d3c','#f16913','#d94801','#8c2d04']
depths_label = ['0-40cm','40-80cm','80-120cm','120-185cm', '185-320cm',
            	'+320cm']

spatial_bins  = [-180,-140,0,50,80,125,180]
spatial_color = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33']
spatial_label = ['Alaska','Canadian Archipelago','European Russia','Western Siberia', \
					'Central Siberia', 'Eastern Siberia']

startyear = int(os.environ['startyear'])
endyear   = int(os.environ['endyear'])
if(endyear>np.max(year)): endyear = np.max(year)

decades   = range(startyear, endyear,10)
if decades[-1] != endyear:
	temporal_bins = np.append(decades,endyear)
else:
	temporal_bins = decades 

temporal_color_all = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00'] # 4 decades max (I add one just in case)
temporal_color = temporal_color_all[0:np.size(temporal_bins)-1]
temporal_label = [str(temporal_bins[i]) + '-' + str(temporal_bins[i+1]) for i in range(len(temporal_bins)-1)]

# create lists comprehension for looping
bins = [depth_bins, spatial_bins, temporal_bins]
colors = [depths_color, spatial_color, temporal_color]
labels = [depths_label, spatial_label, temporal_label]
key_variables = [depth, station_lon, year]
key_variables_name = ["depths", "spatial", "temporal"]

# Initialize plot
for variable_type in [0, 1, 2]:
	# Reorder data, get indices of elements in station_lon sorted in ascending order
	sort_indices = np.argsort(key_variables[variable_type])

	# Sort the arrays using the sort indices
	year_srt 		= np.array(year)[sort_indices]
	depth_srt 		= np.array(depth)[sort_indices]
	station_lon_srt = np.array(station_lon)[sort_indices]
	station_lat_srt = np.array(station_lat)[sort_indices]
	measurement_srt = np.array(measurement)[sort_indices]
	simulation_srt	= np.array(simulation)[sort_indices]

	key_variables_srt = [depth_srt, station_lon_srt, year_srt] # update list (TO-DO: need better approach)

	for month in range(nmonths):
		fig, ax = plt.subplots()
		fig.set_figheight(10)
		fig.set_figwidth(11)
		r_value = np.zeros(np.size(bins[variable_type])-1)

		for i in range(np.size(bins[variable_type])-1): # don't take first one to get n bins
			if variable_type == 1:
				# Calculate the absolute difference between the target longitude and each element in the station_lon array
				diff1 = np.abs(key_variables_srt[variable_type]-bins[variable_type][i])
				diff2 = np.abs(key_variables_srt[variable_type]-bins[variable_type][i+1])
				# Find the index of the minimum difference (i.e. the closest longitude)
				ind_bin1 = np.argmin(diff1)
				ind_bin2 = np.argmin(diff2)
			else:
				ind_bin1 = np.where(key_variables_srt[variable_type]==bins[variable_type][i])[0][0]
				ind_bin2 = np.where(key_variables_srt[variable_type]==bins[variable_type][i+1])[0][0]

			valid_indices = (measurement_srt[ind_bin1:ind_bin2:nmonths+month] != invalid) \
							 & (simulation_srt[ind_bin1:ind_bin2:nmonths+month] != invalid) # update invalid mask
			
			r_value[i], p_value = stats.pearsonr(measurement_srt[ind_bin1:ind_bin2:nmonths+month][valid_indices],
				simulation_srt[ind_bin1:ind_bin2:nmonths+month][valid_indices])
			
			sns.regplot(x = measurement_srt[ind_bin1:ind_bin2:nmonths+month][valid_indices],
						y = simulation_srt[ind_bin1:ind_bin2:nmonths+month][valid_indices],
						color = colors[variable_type][i],
						label = labels[variable_type][i],
						scatter_kws={'s':3,'alpha':0.3},
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
		for i in range(np.size(bins[variable_type])-1):
			L_labels[(2*i)+1].set_text(r'$R^2:{0:.2f}$'.format(r_value[i]))

		# Save fig
		plot_name = output_dir + "scatter_" + str(key_variables_name[variable_type]) + ".month" + str(month+1)
		plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')
		plt.close()

		print(str(key_variables_name[variable_type]) + " scatter plot month" + str(month+1) + ": done!")
