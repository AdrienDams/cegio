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

# open files
var_a_file = os.environ['scratch_dir'] + "/snow_depth/" + os.environ['run_name_a'] + ".sd.period.01.nc"
var_b_file = os.environ['scratch_dir'] + "/snow_depth/" + os.environ['run_name_b'] + ".sd.period.01.nc"
variable = "snow_density"

dvar_a = nc.Dataset(var_a_file, 'r') # read only
dvar_b  = nc.Dataset(var_b_file, 'r')

# output
output_dir = os.environ['senstu'] + "/figures/snow_density/"
os.makedirs(output_dir, exist_ok=True)

# extract variables
var_a = dvar_a.variables[variable][0,:,:] # remove useless dimension
var_b  = dvar_b.variables[variable][0,:,:]

lon = dvar_a.variables['lon']
lat = dvar_a.variables['lat']

# difference
diff_var = var_a[:,:] - var_b[:,:]

all_var = [var_a, var_b]

def setup_map(ax): #Set up common map features for a Cartopy subplot.
	ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())
	# draw land and ocean
	ax.add_feature(cartopy.feature.OCEAN)
	ax.add_feature(cartopy.feature.LAND, facecolor="silver")
	ax.coastlines(linewidth=0.5, color='black')
	# compute a circle in axes coordinates
	theta = np.linspace(0, 2 * np.pi, 100)
	center, radius = [0.5, 0.5], 0.5
	verts = np.vstack([np.sin(theta), np.cos(theta)]).T
	circle = mpath.Path(verts * radius + center)
	ax.set_boundary(circle, transform=ax.transAxes)
	# gridlines labels
	gl = ax.gridlines(draw_labels=True)

## Mapping averages
ts_norm = colors.Normalize(vmin=0, vmax=600)

fig, axes = plt.subplots(1, 2, figsize=[16, 8], constrained_layout=True, subplot_kw={'projection': ccrs.NorthPolarStereo()})

titles = ["CLM45", "CLM5"]

for i, ax in enumerate(axes):
	filled = ax.pcolormesh(lon, lat, all_var[i], cmap='Blues', norm=ts_norm, transform=ccrs.PlateCarree())
	ax.set_title(titles[i])
	setup_map(ax)
	if i == 1:
		cbar = fig.colorbar(filled, ax=ax, boundaries=np.linspace(0,600,7), extend="max")
		cbar.set_label(r"snow density in kg/m3", rotation=-90, labelpad=13)

plot_name = output_dir + os.environ['run_name_a'] + "-" + os.environ['run_name_b'] + ".averages"
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

## Mapping diff
cmap_top = 100
ts_norm = colors.TwoSlopeNorm(vcenter=0, vmin=-cmap_top, vmax=cmap_top)

fig, ax = plt.subplots(1, 1, figsize=[8, 8], constrained_layout=True, subplot_kw={'projection': ccrs.NorthPolarStereo()})

# shade variables
filled = ax.pcolormesh(lon, lat, diff_var, cmap='RdBu_r', norm=ts_norm, transform=ccrs.PlateCarree())

ax.set_title("CLM5 - CLM45")

setup_map(ax)

# legend
cbar = fig.colorbar(filled, ax=ax, boundaries=np.linspace(-cmap_top,cmap_top,9), extend="both")
cbar.set_label(r"snow density in kg/m3", rotation=-90, labelpad=13)

plot_name = output_dir + os.environ['run_name_a'] + "-" + os.environ['run_name_b'] + ".diff"
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()
