import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import cartopy
import cartopy.crs as ccrs
import os

# open files
stationfile = sys.argv[1]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_004/stations-vs-ctsm.1979-2019.pcm.57_DOM02_004.nc"
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/pcm/"
os.makedirs(output_dir, exist_ok=True)

dstation = nc.Dataset(stationfile, 'r') # read only

pcm = dstation['pcm_area']
lon = dstation['lon']
lat = dstation['lat']

nstations = np.size(lon)
nmonths   = 12

# period
startperiod = 1980 
endperiod   = 2019
nyears = endperiod-startperiod
startindex = ((startperiod-1979)*nmonths)
endindex   = ((endperiod-1979)*nmonths)

# looping over every month + period
for i in range(nmonths+1):

 if(i<nmonths):
  # month period average
  pcm_month  = np.average(pcm[i+startindex:i+endindex:nmonths,:],axis=0)

  # take only stations with values
  pcm_true = np.array(pcm_month[pcm_month.mask == False])
  lon_true = np.array(lon[pcm_month.mask == False])
  lat_true = np.array(lat[pcm_month.mask == False])

 else:
  pcm_period = np.average(pcm[startindex:endindex+nmonths,:],axis=0)

  pcm_true = np.array(pcm_period[pcm_period.mask == False])
  lon_true = np.array(lon[pcm_period.mask == False])
  lat_true = np.array(lat[pcm_period.mask == False])  

 ## Mapping
 fig, ax = plt.subplots(1,1,figsize=(8,8),  subplot_kw={'projection': ccrs.NorthPolarStereo()})

 # display points
 sp = ax.scatter(lon_true,
				lat_true,
				c=pcm_true,
				cmap="Reds_r",
            	s=pcm_true,
				edgecolor='black',
				linewidth=0.1,
            	transform=ccrs.PlateCarree())

 # extent map
 ax.set_extent([-180, 180, 90, 56], ccrs.PlateCarree())

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

 # legend
 cbar = fig.colorbar(sp, ax=ax, spacing='proportional', shrink=0.7)
 cbar.set_label("PCM area (in C/m)", rotation=-90, labelpad=13)

 plot_name = output_dir + "pcm_month" + str(i+1)
 plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')

 print("plot month " + str(i+1) + ": done!")
