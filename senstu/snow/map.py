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

variable = "SNOW_DEPTH"

# output
output_dir = os.environ['senstu'] + "/figures/snow/" + variable + "/"
os.makedirs(output_dir, exist_ok=True)

# open files and extract variables
file_a = "/work/aa0049/a271098/senstu/data/57_DOM02_005/climatology/remap/remap.57_DOM02_005.SNOW_DEPTH.JJA.nc"
dfile_a = nc.Dataset(file_a, 'r') # read only

var = dfile_a.variables[variable][0,:,:] # remove useless dimension
lon = dfile_a.variables['lon']
lat = dfile_a.variables['lat']

# Load glacier mask data
mask_file = os.environ['senstu'] + "/map_diff/mask_glacier.nc"
dfile_mask = nc.Dataset(mask_file, 'r')
glacier_mask = dfile_mask.variables['PCT_GLACIER'][:]

# Create masked variable
masked_var = np.ma.masked_where(glacier_mask > 0, var)

## Mapping
fig = plt.figure(figsize=[10, 10], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())

# shade variables
filled = ax.pcolormesh(lon, lat, masked_var, cmap='Blues', vmax = 0.2,
                       transform=ccrs.PlateCarree(), shading='auto')

# Set masked values to white
filled.set_facecolor('white')

# extent map
ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

ax.set_title(variable, fontsize=16)

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
cbar = fig.colorbar(filled, extend='max', fraction=0.05)
cbar.set_label("snow depth in m", rotation=-90, labelpad=13, fontsize=16)

plot_name = output_dir + variable
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight')
plt.close()

