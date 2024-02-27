import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.colors as colors
from matplotlib.colors import TwoSlopeNorm
import cartopy
import cartopy.crs as ccrs
import os
import sys

folder = os.environ['cegio'] + "/data/" + os.environ['run_name'] + "/monthly/"
output_dir = os.environ['senstu'] + "/figures/winter_offset/"
os.makedirs(output_dir, exist_ok=True)

# open files and extract variables

tsafile = folder + "TSA.remap.winter_avg.nc"
tsoifile = folder + "TSOI.remap.winter_avg.nc"
dtsa = nc.Dataset(tsafile, 'r') # read only
dtsoi = nc.Dataset(tsoifile, 'r') # read only

tsa = dtsa.variables["TSA"][0,:,:] # remove useless dimension
tsoi = dtsoi.variables["TSOI"][0,:,:] # remove useless dimension
lon = dtsa.variables['lon']
lat = dtsa.variables['lat']

# make diff
w_offset = tsoi-tsa

# Load glacier mask data
mask_file = os.environ['senstu'] + "/map_diff/mask_glacier.nc"
dfile_mask = nc.Dataset(mask_file, 'r')
glacier_mask = dfile_mask.variables['PCT_GLACIER'][:]

# Create masked diff variable
masked_w_offset = np.ma.masked_where(glacier_mask > 0, w_offset)

## Mapping diff
sbounds = np.linspace(10,35,11)
fig = plt.figure(figsize=[8, 8], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())

# shade variables
filled = ax.pcolormesh(lon, lat, masked_w_offset, cmap='YlOrRd',
                        transform=ccrs.PlateCarree(), shading='auto', norm=colors.BoundaryNorm(sbounds, 256))
# extent map
ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

# draw land and ocean
ax.add_feature(cartopy.feature.OCEAN)
ax.add_feature(cartopy.feature.LAND, facecolor="silver")
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
cbar = fig.colorbar(filled, boundaries=sbounds, extend='both')
cbar.set_label(r"Winter offset in C", rotation=-90, labelpad=13)

plot_name = output_dir + "winter_offset." + os.environ['run_name']
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()
