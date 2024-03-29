import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.colors as colors
import cartopy
import cartopy.crs as ccrs
import os
import sys

# open files
stationfile = sys.argv[1]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_001/stations-vs-ctsm.1979-2020.pcm.57_DOM02_001.nc"
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/pcm/"
os.makedirs(output_dir, exist_ok=True)

dstation = nc.Dataset(stationfile, 'r') # read only

pcm = dstation['pcm']
lon = dstation['lon']
lat = dstation['lat']

nstations = np.size(lon)
nmonths   = 12

# period
startperiod = int(os.environ['startyear'])
endperiod   = int(os.environ['endyear'])
nyears = endperiod-startperiod
startindex = ((startperiod-1979)*nmonths)
endindex   = ((endperiod-1979)*nmonths)

# looping over every month + period
for i in range(nmonths+1):
	if(i<nmonths):
		# month period average
		pcm_month  = np.average(pcm[i+startindex:i+endindex:nmonths,:],axis=0)
		# take only stations with values
		pcm_true = np.array(np.round(pcm_month[pcm_month.mask == False],2))
		lon_true = np.array(lon[pcm_month.mask == False])
		lat_true = np.array(lat[pcm_month.mask == False])
	else: # year average
		pcm_period = np.average(pcm[startindex:endindex,:],axis=0)
		pcm_true = np.array(np.round(pcm_period[pcm_period.mask == False],2))
		lon_true = np.array(lon[pcm_period.mask == False])
		lat_true = np.array(lat[pcm_period.mask == False])

	# sort big points first
	#sort_indices = np.argsort(pcm_true)
	#pcm_true 	= np.array(pcm_true)[sort_indices]
	#lon_true 	= np.array(lon_true)[sort_indices]
	#lat_true 	= np.array(lat_true)[sort_indices]

    ## Mapping
    # colormap
	scmap_top = 8
	s_bounds_lin = np.linspace(-scmap_top,scmap_top,9)
	s_bounds_geo = [-8., -4., -2., -1.,  0.,  1.,  2.,  4.,  8.]

	fig, ax = plt.subplots(1,1,figsize=(8,8),  subplot_kw={'projection': ccrs.NorthPolarStereo()})

	# display points
	sp = ax.scatter(lon_true,
				lat_true,
				c=pcm_true,
				cmap="RdBu_r",
				#s=np.absolute(pcm_true)*10,
				edgecolor='black',
				linewidth=0.1,
				norm=colors.BoundaryNorm(boundaries=s_bounds_geo, ncolors=256, extend='both'),
				transform=ccrs.PlateCarree())

	# extent map
	ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

	# draw land and ocean
	ax.add_feature(cartopy.feature.OCEAN)
	ax.add_feature(cartopy.feature.LAND)
	ax.coastlines(linewidth=0.5, color='black')

	# compute a circle in axes coordinates
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)

	# gridlines labels
	gl = ax.gridlines(draw_labels=True)

	# legend point
	#handles, labels = sp.legend_elements(prop="sizes", alpha=0.6, num=4)     
	#labels = ["8", "16", "24"]     
	#legend = ax.legend(handles, labels, loc="lower right", frameon=False)
	#plt.legend(*sp.legend_elements("sizes", alpha=0.6, num=4), loc="lower right", frameon=False)

	# legend
	cbar = fig.colorbar(sp, ax=ax, shrink=0.7)
	cbar.set_label(r'Temperature PCM (in °C)', rotation=-90, labelpad=13)

	plot_name = output_dir + "pcm_month" + str(i+1)
	plt.savefig(plot_name+'.png', format='png', bbox_inches='tight', dpi=300)

	print("pcm plot month " + str(i+1) + ": done!")
