# print a map of difference between CTSM and CALM stations

import numpy as np
import pandas
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.colors as colors
import cartopy
import cartopy.crs as ccrs
import os
import sys

# open netcdf
ctsmfile = sys.argv[1]
#ctsmfile = "/work/aa0049/a271098/cegio/data/CALM/57_DOM02_004/CTSM_regridded/ALT.57_DOM02_004.period.nc"
variable = "ALT"
dctsm = nc.Dataset(ctsmfile, 'r') # read only

# open csv
calmfile = os.environ['cegio'] + "/evaluation/CALM/CALM_Summary_table_simplified.csv"
ctsmfile = os.environ['cegio'] + "/evaluation/CALM/ctsm_to_calm_" + os.environ['run_name'] + ".csv"
calm_table = np.array(pandas.read_csv(calmfile, encoding="ISO-8859-1"))
ctsm_table = np.array(pandas.read_csv(ctsmfile, encoding="ISO-8859-1",header=None))

# output
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/CALM/"
os.makedirs(output_dir, exist_ok=True)

# extract variables
back_alt = dctsm.variables[variable][:,:] 
ctsm_lon = dctsm.variables['lon']
ctsm_lat = dctsm.variables['lat']

calm_lon = calm_table[:,2].astype('float64')
calm_lat = calm_table[:,1].astype('float64')
ctsm_alt = ctsm_table.astype('float64')

calm_alt_outperiod = calm_table[:,3:].astype('float64')

# limit calm to ctsm data (TDL: need to create an external function)
startyear = int(os.environ['startyear'])
endyear   = int(os.environ['endyear'])
if startyear > 1990: startyearind=startyear-1990
else: startyearind=0

if endyear < 2021: endyearind=-(2021-endyear)
else: endyearind=None # end (-1 not working)

calm_alt = calm_alt_outperiod[:,startyearind:endyearind]

# difference
diff = np.zeros(np.shape(ctsm_alt))
for i in range(np.shape(ctsm_alt)[0]):
	for j in range(np.shape(ctsm_alt)[1]):
		if(ctsm_alt[i,j]>0):
			diff[i,j] = ctsm_alt[i,j]-calm_alt[i,j]
		else:
			diff[i,j] = None

diff_avg = np.nanmean(diff, axis=1)/100

## Mapping averages
fcmap_top = 6 # in m
f_bounds  = np.linspace(0,fcmap_top,fcmap_top+1)
scmap_top = 2
s_bounds  = np.linspace(-scmap_top,scmap_top,9)
fig = plt.figure(figsize=[10, 10], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())
 
# shade variable
filled = ax.pcolormesh(ctsm_lon, ctsm_lat, back_alt, cmap='BuGn',	
						norm=colors.BoundaryNorm(boundaries=f_bounds, ncolors=256, extend='max'),
						transform=ccrs.PlateCarree())

# scatter
scatter = ax.scatter(calm_lon[~np.isnan(diff_avg)], calm_lat[~np.isnan(diff_avg)], s=50, c=diff_avg[~np.isnan(diff_avg)], cmap='RdBu_r',
						norm=colors.BoundaryNorm(boundaries=s_bounds, ncolors=256, extend='both'),
						transform=ccrs.PlateCarree(), edgecolors='black', linewidths=0.5, zorder=1)
 
# extent map
ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())
 
# draw land and ocean
ax.add_feature(cartopy.feature.OCEAN)
ax.add_feature(cartopy.feature.LAND, facecolor="silver")
ax.coastlines(linewidth=0.6, color='black')
 
# compute a circle in axes coordinates
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)
 
# gridlines labels
gl = ax.gridlines(draw_labels=True)
 
# legend
cbar_filled = fig.colorbar(filled, ax=ax, boundaries=f_bounds, orientation='horizontal', fraction=0.05)
cbar_filled.set_label(r"CTSM acive soil layer thickness in m")
cbar_filled = fig.colorbar(scatter, ax=ax, boundaries=s_bounds, fraction=0.05)
cbar_filled.set_label(r"difference of ALT (CTSM - CALM) in m", rotation=-90, labelpad=13)

plot_name = output_dir + "map_ctsm_calm"
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight')
plt.close()

print("calm map: done!")
