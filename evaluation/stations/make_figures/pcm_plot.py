import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import cartopy
import cartopy.crs as ccrs
import os
import sys

# open files
stationfile = sys.argv[1]
#stationfile = "/work/aa0049/a271098/cegio/data/stations/57_DOM02_040/stations-vs-ctsm.1979-2020.pcm.57_DOM02_040.nc"
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/pcm/"
os.makedirs(output_dir, exist_ok=True)

dstation = nc.Dataset(stationfile, 'r') # read only

pcm = dstation['pcm']
lon = dstation['lon']
lon = lon[lon.mask == False]
lat = dstation['lat']

nstations = np.size(lon)
nseasons  = 4
nmonths   = 12

# period
startperiod = 1980 
endperiod   = 2020
startindex = ((startperiod-1979)*nmonths)
endindex   = ((endperiod-1979)*nmonths)

label_seasons = ['DJF', 'MAM', 'JJA', 'SON', 'period']

# looping over every seasons + period
for i in range(nseasons+1):
 i1 = (i*3)-1 # first month
 i2 = (i*3)   # second month
 i3 = (i*3)+1 # third month
#
 if(i<nseasons):
  # season average
  pcm_season  = (np.average(pcm[i1+startindex:i1+endindex:nmonths,:],axis=0) + \
					np.average(pcm[i2+startindex:i2+endindex:nmonths,:],axis=0) + \
						np.average(pcm[i3+startindex:i3+endindex:nmonths,:],axis=0))/3
#
  # take only stations with values
  pcm_true = np.array(pcm_season[pcm_season.mask == False])
  lon_true = lon[pcm_season.mask == False]
  lat_true = lat[pcm_season.mask == False]
#
 else: # period average
  pcm_period = np.average(pcm[startindex:endindex+nmonths,:],axis=0)
#
  pcm_true = np.array(pcm_period[pcm_period.mask == False])
  lon_true = lon[pcm_period.mask == False]
  lat_true = lat[pcm_period.mask == False]) 
#
 ## Mapping
 fig, ax = plt.subplots(1,1,figsize=(8,8),  subplot_kw={'projection': ccrs.NorthPolarStereo()})

 # display points
 sp = ax.scatter(lon_true,
				lat_true,
				c=pcm_true,
				cmap="Reds_r",
            	s=pcm_true*10,
				edgecolor='black',
				linewidth=0.1,
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

 # legend
 cbar = fig.colorbar(sp, ax=ax, spacing='proportional', shrink=0.7)
 cbar.set_label("PCM area (in C/m)", rotation=-90, labelpad=13)

 plot_name = output_dir + "pcm_" + label_seasons[i]
 plt.savefig(plot_name+'.pdf', format='pdf', bbox_inches='tight')

 print("pcm plot month " + label_seasons[i] + ": done!")
