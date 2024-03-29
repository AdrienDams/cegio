# print map of CTSM, ESACCI interpolated on the CTSM grid and their difference of GT

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
ctsmfile = sys.argv[1]
esafile  = sys.argv[2]
output_name = sys.argv[3] + "_ESAvsCTSM_TSOI"
variable = "TSOI"


dctsm = nc.Dataset(ctsmfile, 'r') # read only
desa  = nc.Dataset(esafile, 'r') # read only

# output
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/ESACCI/" + variable + "/"
os.makedirs(output_dir, exist_ok=True)

# extract variables
ctsm_var = dctsm.variables[variable][0,0,:,:]-273.15 # remove useless dimension
esa_var  = desa.variables[variable][0,:,:]

lon = dctsm.variables['lon']
lat = dctsm.variables['lat']

# difference
diff_var_gla = ctsm_var[:,:] - esa_var[:,:]

# Load glacier mask data
mask_file = os.environ['cegio'] + "/mask_glacier.nc"
dfile_mask = nc.Dataset(mask_file, 'r')
glacier_mask = dfile_mask.variables['PCT_GLACIER'][:]

# Create masked diff variable
diff_var = np.ma.masked_where(glacier_mask > 0, diff_var_gla)

absolute_average = np.round(np.nanmean(np.abs(diff_var)),2)
rmse = np.round(np.sqrt(np.nanmean(np.square(diff_var))),2)

# calculate 

all_var = [ctsm_var, esa_var]

## Mapping averages
cmap_top = 15
ts_norm = colors.TwoSlopeNorm(vcenter=0, vmin=-cmap_top, vmax=cmap_top)

fig = plt.figure(figsize=[16, 8], constrained_layout=True)
nax = 0

for ax in ["ax1", "ax2"]:
 ax = fig.add_subplot(1, 2, nax+1, projection=ccrs.NorthPolarStereo())
 
 # shade variables
 filled = ax.pcolormesh(lon, lat, all_var[nax], cmap='RdBu_r',	
						norm=ts_norm, transform=ccrs.PlateCarree())
 
 # extent map
 ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())
 
 if nax == 0:
  ax.set_title("CTSM")
 else:
  ax.set_title("ESA-CCI")
 
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
 if nax==1:
  # colour bar made from ESA data
  cbar = fig.colorbar(filled, ax=ax, boundaries=np.linspace(-cmap_top,6,8), extend="both")
  cbar.set_label(r"soil temperature in °C", rotation=-90, labelpad=13)
 
 # next iteration
 nax = nax+1

plot_name = output_dir + output_name + ".averages"
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

## Mapping diff
cmap_top = 8
ts_norm = colors.TwoSlopeNorm(vcenter=0, vmin=-cmap_top, vmax=cmap_top)
fig = plt.figure(figsize=[8, 8], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())

# shade variables
filled = ax.pcolormesh(lon, lat, diff_var, cmap='RdBu_r',	
						norm=ts_norm, transform=ccrs.PlateCarree())

# extent map
ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

ax.set_title("CTSM - ESA-CCI (MAD = %s"%absolute_average + " , RMSE = %s"%rmse + ")")

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
cbar = fig.colorbar(filled, ax=ax, boundaries=np.linspace(-cmap_top,cmap_top,9), extend="both")
cbar.set_label(r"soil temperature in °C", rotation=-90, labelpad=13)

plot_name = output_dir + output_name + ".diff"
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

print("soiltemp average maps " + output_name + ": done!")
