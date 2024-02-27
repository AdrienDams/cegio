import numpy as np
import pandas as pd
from datetime import date
import os
from os.path import exists
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import sys
from scipy import stats

# OPEN CONTROL DATA (DATA-Import from CSV (12 months for every point))
all_result_ctrl = pd.DataFrame(np.array(
	pd.read_csv(os.environ['cegio'] + "/evaluation/stations/make_figures/extracted_csv/results.tmp." + os.environ['run_name_ctrl'] + ".csv",sep=',',header=None)),
						columns=['year','month','station_lon','station_lat',
								 'depth','measurement','simulation','altitude','station_id'])

## OPEN EXPERIMENT DATA (DATA-Import from CSV (12 months for every point))
all_result_exp = pd.DataFrame(np.array(
	pd.read_csv(os.environ['cegio'] + "/evaluation/stations/make_figures/extracted_csv/results.tmp." + os.environ['run_name_exp'] + ".csv",sep=',',header=None)),
						columns=['year','month','station_lon','station_lat',
								 'depth','measurement','simulation','altitude','station_id'])

## ADDITIONAL EXPERIMENT 2 DATA (DATA-Import from CSV (12 months for every point))
all_result_exp2 = pd.DataFrame(np.array(
	pd.read_csv(os.environ['cegio'] + "/evaluation/stations/make_figures/extracted_csv/results.tmp." + os.environ['run_name_exp2'] + ".csv",sep=',',header=None)),
						columns=['year','month','station_lon','station_lat',
								 'depth','measurement','simulation','altitude','station_id'])

# Make data lists
months  = all_result_ctrl['month'].astype(int)
depths  = all_result_ctrl['depth']
obs = all_result_ctrl['measurement']

simulations_ctrl = all_result_ctrl['simulation']
simulations_exp  = all_result_exp['simulation']
simulations_exp2 = all_result_exp2['simulation']

# Masked arrays with nan (-9999) values
invalid = -9999
valid_indexes_ctrl = (obs != invalid) & (simulations_ctrl != invalid) & (obs > -50)
valid_indexes_exp = (obs != invalid) & (simulations_exp != invalid) & (obs > -50)
valid_indexes_exp2 = (obs != invalid) & (simulations_exp2 != invalid) & (obs > -50)

# Define depths you want to extract and ranges
depths_to_extract = [20, 80, 160, 320]
depth_ranges = [(0, 40), (41, 120), (121, 200), (201, 440)]

# Create empty arrays to store the monthly averages and standard deviations
obs_avg = np.zeros((12, len(depth_ranges)))
obs_std = np.zeros((12, len(depth_ranges)))
ctrl_avg = np.zeros((12, len(depth_ranges)))
ctrl_std = np.zeros((12, len(depth_ranges)))
exp_avg = np.zeros((12, len(depth_ranges)))
exp_std = np.zeros((12, len(depth_ranges)))
exp2_avg = np.zeros((12, len(depth_ranges)))
exp2_std = np.zeros((12, len(depth_ranges)))

# Loop through each month
for month in range(1, 13):
	# Create boolean arrays to filter by month and valid depth
	month_bool = months == month
	
	# Initialize arrays to store filtered data for each depth range
	obs_month_depths = []
	simulations_ctrl_month_depths = []
	simulations_exp_month_depths = []
	simulations_exp2_month_depths = []
	
	# Filter by valid month and depth ranges
	for depth_range in depth_ranges:
		depth_min, depth_max = depth_range
		valid_depths_bool = (depths >= depth_min) & (depths < depth_max)
		
		obs_month_depth = obs[month_bool & valid_depths_bool & valid_indexes_ctrl]
		simulations_ctrl_month_depth = simulations_ctrl[month_bool & valid_depths_bool & valid_indexes_ctrl]
		simulations_exp_month_depth = simulations_exp[month_bool & valid_depths_bool & valid_indexes_exp]
		simulations_exp2_month_depth = simulations_exp2[month_bool & valid_depths_bool & valid_indexes_exp2]
		
		obs_month_depths.append(obs_month_depth)
		simulations_ctrl_month_depths.append(simulations_ctrl_month_depth)
		simulations_exp_month_depths.append(simulations_exp_month_depth)
		simulations_exp2_month_depths.append(simulations_exp2_month_depth)
	
	# Calculate monthly averages and standard deviations for each depth range
	for i in range(len(depth_ranges)):
		obs_avg[month-1, i] = np.mean(obs_month_depths[i])
		obs_std[month-1, i] = np.std(obs_month_depths[i])
		ctrl_avg[month-1, i] = np.mean(simulations_ctrl_month_depths[i])
		ctrl_std[month-1, i] = np.std(simulations_ctrl_month_depths[i])
		exp_avg[month-1, i] = np.mean(simulations_exp_month_depths[i])
		exp_std[month-1, i] = np.std(simulations_exp_month_depths[i])
		exp2_avg[month-1, i] = np.mean(simulations_exp2_month_depths[i])
		exp2_std[month-1, i] = np.std(simulations_exp2_month_depths[i])

# Shift the data by four months
shift = 8
obs_avg = np.roll(obs_avg, -shift, axis=0)
obs_std = np.roll(obs_std, -shift, axis=0)
ctrl_avg = np.roll(ctrl_avg, -shift, axis=0)
ctrl_std = np.roll(ctrl_std, -shift, axis=0)
exp_avg = np.roll(exp_avg, -shift, axis=0)
exp_std = np.roll(exp_std, -shift, axis=0)
exp2_avg = np.roll(exp2_avg, -shift, axis=0)
exp2_std = np.roll(exp2_std, -shift, axis=0)

# Define colors for each dataset
obs_color = 'black'
ctrl_color = 'blue'
exp_color = 'green'
exp2_color = 'red'

# Set up the figure and subplots
fig, axs = plt.subplots(len(depths_to_extract), 1, figsize=(8, 10), sharex=True)
plt.subplots_adjust(hspace=0, wspace=0)

# Loop through each depth
for i, depth in enumerate(depths_to_extract):
	# Plot the obs data
	axs[i].plot(range(1, 13), obs_avg[:, i], color=obs_color, label='Observations')
	
	# Plot the control data
	axs[i].plot(range(1, 13), ctrl_avg[:, i], color=ctrl_color, label='Control run')
	
	# Plot the experiment data
	axs[i].plot(range(1, 13), exp_avg[:, i], color=exp_color, label='Obu run')
	
	# Plot the experiment 2 data
	axs[i].plot(range(1, 13), exp2_avg[:, i], color=exp2_color, label='Sturm run')
	
	# Add axis labels and title for each subplot
	axs[i].text(0, 1, f'-{depth} cm', rotation=90, verticalalignment='center', fontsize=10)
	
	# Fix y-axis
	axs[i].set_ylim(-12, 12)
	axs[i].set_xlim(1,12)
	
	# Add y-ticks and tick options
	loc = plticker.MultipleLocator(base=4.0) # this locator puts ticks at regular intervals
	axs[i].yaxis.set_major_locator(loc)
	axs[i].tick_params(direction='in')
	
	# Add a legend to the first subplot
	if i == 0:
		axs[i].legend(loc='best')

# Add axis label
plt.xticks(range(1, 13), ("Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"))

fig.suptitle('Monthly soil temperature in °C', fontsize=12, y=0.9)

# output
output_dir = os.environ['senstu'] + "/figures/annual_cycle/"
os.makedirs(output_dir, exist_ok=True)
plot_name = output_dir + "annual_cycle." + os.environ['run_name_ctrl'] + "-" + os.environ['run_name_exp'] + "-" + os.environ['run_name_exp2']
plt.savefig(plot_name + '.png', format='png', bbox_inches='tight', dpi=300)
