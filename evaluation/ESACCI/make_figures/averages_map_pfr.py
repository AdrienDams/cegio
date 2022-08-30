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
#ctsmfile = "/work/aa0049/a271098/cegio/data/ESACCI/57_DOM02_004/CTSM_regridded/PFR.57_DOM02_004.1997.nc"
#esafile  = "/work/aa0049/a271098/cegio/data/ESACCI/57_DOM02_004/ESACCI_regridded/PFR.ESACCI.on.57_DOM02_004.1998.nc"
#output_name = "1997"
variable = "PFR"


dctsm = nc.Dataset(ctsmfile, 'r') # read only
desa  = nc.Dataset(esafile, 'r') # read only

# output
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/ESACCI/" + variable + "/"
os.makedirs(output_dir, exist_ok=True)

# extract variables
ctsm_var = dctsm.variables['TSOI'][0,:,:]-273.15 # remove useless dimension
esa_var  = desa.variables[variable][0,:,:]

lon = dctsm.variables['lon']
lat = dctsm.variables['lat']

# masking
thre_cont  = 90
thre_dcont = 50
esa_continuous  = np.where(esa_var>thre_cont, 1, np.nan)
esa_dcontinuous = np.where((esa_var<thre_cont) & (esa_var>thre_dcont), 1, np.nan)
esa_free		= np.where(esa_var<thre_dcont, 1, np.nan)
ctsm_continuous = np.where(ctsm_var<0, 1, np.nan)
ctsm_free 		= np.where(ctsm_var>0, 1, np.nan)

# multi-masking
contcont = np.where((esa_continuous == 1) & (ctsm_continuous == 1),1,np.nan)
contfree = np.where((esa_continuous == 1) & (ctsm_free == 1),1,np.nan)
freecont = np.where((esa_free == 1) & (ctsm_continuous == 1),1,np.nan)
disccont = np.where((esa_dcontinuous == 1) & (ctsm_continuous == 1),1,np.nan)
discfree = np.where((esa_dcontinuous == 1) & (ctsm_free == 1),1,np.nan)

## Mapping averages
darkgreen  = colors.ListedColormap(['#1a9641'])
lightgreen = colors.ListedColormap(['#a6d96a'])
darkred    = colors.ListedColormap(['#d7191c'])
yellow     = colors.ListedColormap(['#ffffbf'])
fig = plt.figure(figsize=[5, 5], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())

# shade variables
filled1 = ax.pcolormesh(lon, lat, contcont, cmap=darkgreen, transform=ccrs.PlateCarree())
filled2 = ax.pcolormesh(lon, lat, contfree, cmap=darkred, transform=ccrs.PlateCarree())
filled3 = ax.pcolormesh(lon, lat, freecont, cmap=darkred, transform=ccrs.PlateCarree())
filled4 = ax.pcolormesh(lon, lat, disccont, cmap=lightgreen, transform=ccrs.PlateCarree())
filled5 = ax.pcolormesh(lon, lat, discfree, cmap=yellow, transform=ccrs.PlateCarree())

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

plt.show()

plot_name = output_dir + output_name + ".diff"
plt.savefig(plot_name +'.pdf', format='pdf', bbox_inches='tight')
plt.close()

print("permafrost map: done!")
