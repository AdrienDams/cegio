# print a heatmap between modelled (from CTSM output) and observed (from station) data for all station

import numpy as np
import netCDF4 as nc
import seaborn as sns; sns.set_theme()
import matplotlib.pylab as plt
import matplotlib.ticker as ticker
plt.style.use("seaborn")
import os
from os import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 

# open netcdf
stationfile = sys.argv[1]
dstation 	= nc.Dataset(stationfile, 'r') # read only

# output
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/heatmap/"
os.makedirs(output_dir, exist_ok=True)

# open index
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", delimiter=" ", dtype=int)

# write variables stations
sta_lon   = np.array(dstation['lon'])
sta_lat   = np.array(dstation['lat'])
sta_depth = np.array(dstation['depth'])
sta_var_data   = dstation['soiltemp']
ctsm_var_data  = dstation['ctsm_soiltemp']

# remove depth below usuable (before 242)
max_depth = 153
sta_depth = sta_depth[0:max_depth]
sta_var_nomask   = sta_var_data[:,0:max_depth,:]
ctsm_var_nomask  = ctsm_var_data[:,0:max_depth,:]

# don't include points with no ctsm temperature
sta_var  = np.ma.masked_array(sta_var_nomask, mask=ctsm_var_nomask.mask)
ctsm_var = ctsm_var_nomask

# retrieve time index from year-month ctsm to station
startperiod = int(os.environ['startyear']) 
endperiod   = int(os.environ['endyear'])
nyears = endperiod-startperiod
startindex = ((startperiod-1979)*12)
endindex   = ((endperiod-1979)*12)

# station selection
region_label = ['Alaska','Canadian_Archipelago','European_Russia','Western_Siberia', \
					'Central_Siberia', 'Eastern_Siberia']
regions = {1: [-180, -140], 2: [-140, 0], 3: [0, 50], 4: [50, 80], 5: [80, 125], 6: [125, 180]}
region_ind = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

for i, longitude in enumerate(sta_lon):
    for r, bounds in regions.items():
        if bounds[0] <= longitude < bounds[1]:
            region_ind[r].append(i)
            break

# depth rebinning
depth_classes=8
classes_size = int(sta_depth[-1]/depth_classes)
sta_var_rebin  = np.full((np.shape(sta_var)[0],depth_classes,np.shape(sta_var)[2]),np.nan)
ctsm_var_rebin = np.full((np.shape(ctsm_var)[0],depth_classes,np.shape(sta_var)[2]),np.nan)

for d in range(depth_classes):
	first_index = int(np.argwhere(sta_depth==(d)*classes_size))
	last_index  = int(np.argwhere(sta_depth==(d+1)*classes_size))
	sta_var_rebin[:,d,:]  = np.nanmean(sta_var[:,first_index:last_index,:],axis=1)	
	ctsm_var_rebin[:,d,:] = np.nanmean(ctsm_var[:,first_index:last_index,:],axis=1)			

# month period average
sta_var_months  = np.full((12,depth_classes,np.shape(sta_var)[2]),np.nan)
ctsm_var_months = np.full((12,depth_classes,np.shape(sta_var)[2]),np.nan)
for m in range(12):
	sta_var_months[m,:,:]  = np.nanmean(sta_var_rebin[m+startindex:m+endindex:12,:,:],axis=0) # start:stop:step
	ctsm_var_months[m,:,:] = np.nanmean(ctsm_var_rebin[m+startindex:m+endindex:12,:,:],axis=0)

for region in range(1,7):
	# station average and RMSE
	sta_var_mean  = np.full((12,depth_classes),np.nan)
	ctsm_var_mean = np.full((12,depth_classes),np.nan)
	rmse = np.full((12,depth_classes),np.nan)
	for m in range(12):
		for d in range(depth_classes):
			if(np.count_nonzero(~np.isnan(sta_var_months[m,d,region_ind[region]]))>=5):
				sta_var_mean[m,d]  = np.nanmean(sta_var_months[m,d,region_ind[region]])
				ctsm_var_mean[m,d] = np.nanmean(ctsm_var_months[m,d,region_ind[region]])
				rmse[m,d] = np.sqrt(np.nanmean( \
								np.square(ctsm_var_months[m,d,region_ind[region]]-sta_var_months[m,d,region_ind[region]])))

	# difference
	diff = ctsm_var_mean-sta_var_mean

	# heatmap options
	months_letter = ["J","F","M","A","M","J","J","A","S","O","N","D"]
	palette = sns.diverging_palette(240, 10, n=depth_classes, as_cmap=True)
	palette_seq = sns.light_palette("seagreen", as_cmap=True)
	top_depth_list = np.linspace(classes_size,int(sta_depth[-1]),depth_classes)

	### heatmap
	f,(ax1,ax2,ax3,ax4) = plt.subplots(4,1, figsize=(5,13))

	## plot 1
	sns.heatmap(np.transpose(np.round(sta_var_mean,1)), cmap=palette, center=0,
		robust=True, linewidths=0.1, linecolor="k",square=True, 
		yticklabels = top_depth_list, ax=ax1,
		annot=True, annot_kws={'size': 6})

	# plot options
	ax1.set(xticklabels=[]) 
	ax1.set(xlabel=None)
	ax1.set(ylabel="depth (in cm)")
	ax1.set_title("station soil temperature (in C)")
	ax1.set_yticklabels(ax1.get_yticklabels(), fontsize=6, position=(0.02,0))

	## plot 2
	sns.heatmap(np.transpose(np.round(ctsm_var_mean,1)), cmap=palette, center=0,
		robust=True, linewidths=0.1, linecolor="k",square=True,
		yticklabels = top_depth_list, ax=ax2,
		annot=True, annot_kws={'size': 6})

	# plot options
	ax2.set(xticklabels=[]) 
	ax2.set(xlabel=None)
	ax2.set(ylabel="depth (in cm)")
	ax2.set_title("ctsm soil temperature (in C)")
	ax2.set_yticklabels(ax2.get_yticklabels(), fontsize=6, position=(0.02,0))

	## plot 3
	sns.heatmap(np.transpose(np.round(diff,1)), cmap=palette, center=0,
		robust=True, linewidths=0.1, linecolor="k",square=True,
		xticklabels = months_letter, yticklabels = top_depth_list, ax=ax3,
		annot=True, annot_kws={'size': 6})

	# plot options
	ax3.set(xticklabels=[])
	ax3.set(xlabel=None)
	ax3.set(ylabel="depth (in cm)")
	ax3.set_title("ctsm-stations soil temperature (in C)")
	ax3.set_yticklabels(ax3.get_yticklabels(), fontsize=6, position=(0.02,0))

	## plot 4
	sns.heatmap(np.transpose(np.round(rmse,1)), cmap=palette_seq,
		robust=True, linewidths=0.1, linecolor="k",square=True,
		xticklabels = months_letter, yticklabels = top_depth_list, ax=ax4,
		annot=True, annot_kws={'size': 6})

	# plot options
	ax4.set(xlabel="month", ylabel="depth (in cm)")
	ax4.set_title("RMSE ctsm-stations")
	ax4.set_yticklabels(ax4.get_yticklabels(), fontsize=6, position=(0.02,0))

	output_name = "heatmap_" +  region_label[region-1]
	plt.suptitle(region_label[region-1])
	plt.subplots_adjust(top=0.95)

	plot_name = output_dir + output_name
	plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
	plt.close()

	print(output_name + ": done!")
