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
output_name = sys.argv[3]
#ctsmfile = "/work/aa0049/a271098/cegio/data/ESACCI/57_DOM02_004/CTSM_regridded/ALT.57_DOM02_004.1997.nc"
#esafile  = "/work/aa0049/a271098/cegio/data/ESACCI/57_DOM02_004/ESACCI_regridded/ALT.ESACCI.on.57_DOM02_004.1997.nc"
#output_name = "1997"
variable = "ALT"

dctsm = nc.Dataset(ctsmfile, 'r') # read only
desa  = nc.Dataset(esafile, 'r') # read only

# output
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/ESACCI/" + variable + "/"
os.makedirs(output_dir, exist_ok=True)

# extract variables
ctsm_var = dctsm.variables[variable][:,:] 
esa_var  = desa.variables[variable][0,:,:] # remove useless dimension

# only take esa where ctsm exists
esa_var_test = np.ma.masked_array(esa_var, mask=ctsm_var.mask == False)

lon = dctsm.variables['lon']
lat = dctsm.variables['lat']

# difference
diff_var = ctsm_var[:,:] - esa_var[:,:]

all_var = [ctsm_var, esa_var]

## Mapping averages
cmap_top = 6
fig = plt.figure(figsize=[10, 5], constrained_layout=True)
nax = 0

for ax in ["ax1", "ax2"]:
 ax = fig.add_subplot(1, 2, nax+1, projection=ccrs.NorthPolarStereo())
 
 # shade variables
 filled = ax.pcolormesh(lon, lat, all_var[nax], cmap='BuGn',	
						norm=colors.TwoSlopeNorm(vcenter = cmap_top/2, vmin = 0, vmax = cmap_top),
						transform=ccrs.PlateCarree())
 
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
  cbar = fig.colorbar(filled, ax=ax, boundaries=np.linspace(0,cmap_top,cmap_top+1))
  cbar.set_label(r"acive soil layer thickness in m", rotation=-90, labelpad=13)
 
 # next iteration
 nax = nax+1

plot_name = output_dir + output_name + ".averages"
plt.savefig(plot_name +'.pdf', format='pdf', bbox_inches='tight')
plt.close()

## Mapping diff
cmap_top = 6
fig = plt.figure(figsize=[5, 5], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())

# shade variables
filled = ax.pcolormesh(lon, lat, diff_var, cmap='RdBu_r',	
						norm=colors.TwoSlopeNorm(vcenter = 0, vmin = -cmap_top, vmax = cmap_top),
						transform=ccrs.PlateCarree())

# extent map
ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

ax.set_title("difference")

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
cbar = fig.colorbar(filled, ax=ax, boundaries=np.linspace(-2,cmap_top,cmap_top+3))
cbar.set_label(r"acive soil layer thickness in m", rotation=-90, labelpad=13)

plot_name = output_dir + output_name + ".diff"
plt.savefig(plot_name +'.pdf', format='pdf', bbox_inches='tight')
plt.close()

print("alt average map " + output_name + ": done!")
