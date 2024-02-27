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

variable = "SOILWAT"

# output
output_dir = os.environ['senstu'] + "/figures/map_diff/" + variable + "/"
os.makedirs(output_dir, exist_ok=True)

# open files and extract variables

# Soil ice
file_a1 = os.environ['senstu'] + "/data/" + os.environ['run_name_a'] + "/climatology/remap/remap." \
		+ os.environ['run_name_a'] + ".SOILICE." + os.environ['month'] + ".nc"
file_b1 = os.environ['senstu'] + "/data/" + os.environ['run_name_b'] + "/climatology/remap/remap." \
		+ os.environ['run_name_b'] + ".SOILICE." + os.environ['month'] + ".nc"
dfile_a1 = nc.Dataset(file_a1, 'r') # read only
dfile_b1 = nc.Dataset(file_b1, 'r') # read only
file_a1 = dfile_a1.variables["SOILICE"][0,:,:] # remove useless dimension
file_b1 = dfile_b1.variables["SOILICE"][0,:,:] # remove useless dimension

# Soil liq
file_a2 = os.environ['senstu'] + "/data/" + os.environ['run_name_a'] + "/climatology/remap/remap." \
		+ os.environ['run_name_a'] + ".SOILLIQ." + os.environ['month'] + ".nc"
file_b2 = os.environ['senstu'] + "/data/" + os.environ['run_name_b'] + "/climatology/remap/remap." \
		+ os.environ['run_name_b'] + ".SOILLIQ." + os.environ['month'] + ".nc"
dfile_a2 = nc.Dataset(file_a2, 'r') # read only
dfile_b2 = nc.Dataset(file_b2, 'r') # read only
file_a2 = dfile_a2.variables["SOILLIQ"][0,:,:] # remove useless dimension
file_b2 = dfile_b2.variables["SOILLIQ"][0,:,:] # remove useless dimension

file_a = file_a1 + file_a2
file_b = file_b1 + file_b2

lon = dfile_a1.variables['lon']
lat = dfile_a1.variables['lat']

# make diff
diff = file_a-file_b

## Mapping diff
fig = plt.figure(figsize=[10, 10], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())

# set colorbar limits
vmax = np.ceil(np.percentile(np.abs(diff.compressed()), 90))

# shade variables
filled = ax.pcolormesh(lon, lat, diff, cmap='RdBu_r', norm=TwoSlopeNorm(vcenter=0., vmax=vmax, vmin=-vmax),
                        transform=ccrs.PlateCarree(), shading='auto')
# extent map
ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

ax.set_title(os.environ['run_name_a'] + " - " + os.environ['run_name_b'], fontsize=16)

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
cbar = fig.colorbar(filled, extend='both', fraction=0.05)
cbar.set_label("1m-column soil liquid + ice water difference in kg/m2", rotation=-90, labelpad=13, fontsize=16)

plot_name = output_dir + variable + "." + os.environ['month'] + ".diff." + os.environ['run_name_a'] + "-" + os.environ['run_name_b']
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()
