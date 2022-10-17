# (from A. Damseaux)
# print a heatmap between modelled (from CTSM output) and observed (from station) data for all station

import numpy as np
import netCDF4 as nc
import seaborn as sns; sns.set_theme()
import matplotlib.pylab as plt
plt.style.use("seaborn")
import os
from os import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 

# open netcdf
stationfile = sys.argv[1]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_040/stations-vs-ctsm.1979-2020.tmp.57_DOM02_040.nc"

dstation = nc.Dataset(stationfile, 'r') # read only

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
startperiod = 2000 
endperiod   = 2014
nyears = endperiod-startperiod
startindex = ((startperiod-1979)*12)
endindex   = ((endperiod-1979)*12)

# station selection
q1_sta_list = []
q2_sta_list = []
q3_sta_list = []
q4_sta_list = []
for i in range(np.size(sta_lon)):
	if i in index_table[:,0]:
		if(sta_lon[i]>=0) & (sta_lon[i]<90):
			q1_sta_list.append(i)
		if(sta_lon[i]>=90) & (sta_lon[i]<180):
			q2_sta_list.append(i)
		if(sta_lon[i]<0) & (sta_lon[i]>=-90):
			q3_sta_list.append(i)
		if(sta_lon[i]<-90) & (sta_lon[i]>=-180):
			q4_sta_list.append(i)

sta_list = [q1_sta_list,q2_sta_list,q3_sta_list,q4_sta_list]

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

for quarter in range(4):
	# station average
	sta_var_true  = np.full((12,depth_classes),np.nan)
	ctsm_var_true = np.full((12,depth_classes),np.nan)
	for m in range(12):
		for d in range(depth_classes):
			if(np.count_nonzero(~np.isnan(sta_var_months[m,d,sta_list[quarter]]))>=5):
				sta_var_true[m,d]  = np.nanmean(sta_var_months[m,d,sta_list[quarter]])
				ctsm_var_true[m,d] = np.nanmean(ctsm_var_months[m,d,sta_list[quarter]])

	# difference
	diff = ctsm_var_true-sta_var_true

	# heatmap options
	months_letter = ["J","F","M","A","M","J","J","A","S","O","N","D"]
	palette = sns.diverging_palette(240, 10, n=depth_classes, as_cmap=True)
	top_depth_list = np.linspace(classes_size,int(sta_depth[-1]),depth_classes)

	### heatmap
	f,(ax1,ax2,ax3) = plt.subplots(3,1, figsize=(5,10))

	## plot 1
	sns.heatmap(np.transpose(np.round(sta_var_true,1)), cmap=palette, center=0,
		robust=True, linewidths=0.1, linecolor="k",square=True, 
		yticklabels = top_depth_list, ax=ax1,
		annot=True, annot_kws={'size': 6})

	# plot options
	ax1.set(xticklabels=[]) 
	ax1.set(xlabel=None)
	ax1.set(ylabel="depth (in cm)")
	ax1.set_title("station soil temperature (in C)")

	## plot 2
	sns.heatmap(np.transpose(np.round(ctsm_var_true,1)), cmap=palette, center=0,
		robust=True, linewidths=0.1, linecolor="k",square=True,
		yticklabels = top_depth_list, ax=ax2,
		annot=True, annot_kws={'size': 6})

	# plot options
	ax2.set(xticklabels=[]) 
	ax2.set(xlabel=None)
	ax2.set(ylabel="depth (in cm)")
	ax2.set_title("ctsm soil temperature (in C)")

	## plot 3
	sns.heatmap(np.transpose(np.round(diff,1)), cmap=palette, center=0,
		robust=True, linewidths=0.1, linecolor="k",square=True,
		xticklabels = months_letter, yticklabels = top_depth_list, ax=ax3,
		annot=True, annot_kws={'size': 6})

	# plot options
	ax3.set(xlabel="month", ylabel="depth (in cm)")
	ax3.set_title("ctsm-stations soil temperature (in C)")

	output_name = "quarter" + str(quarter+1)
	plot_name = output_dir + output_name
	plt.savefig(plot_name +'.pdf', format='pdf', bbox_inches='tight')
	plt.close()

	print("heatmap quarter " + str(quarter+1) + ": done!")

