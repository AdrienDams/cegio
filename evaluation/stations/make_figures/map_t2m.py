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
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_001/stations-vs-ctsm.1980-2020.t2m.57_DOM02_001.nc"
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/t2m/"
os.makedirs(output_dir, exist_ok=True)

dstation = nc.Dataset(stationfile, 'r') # read only

t2m_sta = dstation['temp2'][:]
t2m_ctsm = dstation['ctsm_temp2'][:]
diff = t2m_ctsm-t2m_sta
lon = dstation['lon']
lat = dstation['lat']

nstations = np.size(lon)
nmonths   = 12

# period
startperiod = int(os.environ['startyear'])
endperiod   = int(os.environ['endyear'])
nyears = endperiod-startperiod
startindex = ((startperiod-1950)*nmonths)
endindex   = ((endperiod-1950)*nmonths)

# looping over every month + period
for i in range(nmonths+1):
	if(i<nmonths):
		# month period average
		diff_month  = np.average(diff[i+startindex:i+endindex:nmonths,:],axis=0)
		# take only stations with values
		diff_true = np.array(np.round(diff_month[diff_month.mask == False],2))
		lon_true = np.array(lon[diff_month.mask == False])
		lat_true = np.array(lat[diff_month.mask == False])
	else: # year average
		diff_period = np.average(diff[startindex:endindex,:],axis=0)
		diff_true = np.array(np.round(diff_period[diff_period.mask == False],2))
		lon_true = np.array(lon[diff_period.mask == False])
		lat_true = np.array(lat[diff_period.mask == False])

    ## Mapping
    # colormap
	s_bounds = [-4., -3, -2., -1.,  0.,  1., 2., 3.,  4.]

	fig, ax = plt.subplots(1,1,figsize=(8,8),  subplot_kw={'projection': ccrs.NorthPolarStereo()})

	# display points
	sp = ax.scatter(lon_true,
				lat_true,
				s=8,
				c=diff_true,
				cmap="RdBu_r",
				norm=colors.BoundaryNorm(boundaries=s_bounds, ncolors=256, extend='both'),
				transform=ccrs.PlateCarree())

	# extent map
	ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

	# draw land and ocean
	ax.add_feature(cartopy.feature.OCEAN)
	ax.add_feature(cartopy.feature.LAND, facecolor='lightgray')
	ax.coastlines(linewidth=0.5, color='black')

	# compute a circle in axes coordinates
	theta = np.linspace(0, 2*np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)

	# gridlines labels
	gl = ax.gridlines(draw_labels=True)

	# legend
	cbar = fig.colorbar(sp, ax=ax, shrink=0.7, boundaries=s_bounds, extend='both')
	cbar.set_label(r'Temperature difference (in °C)', rotation=-90, labelpad=13)

	plot_name = output_dir + "diff_month" + str(i+1)
	plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')

	print("diff plot month " + str(i+1) + ": done!")
