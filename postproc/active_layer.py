# Active layer calculation (from F. Peyrusse, modified for irregular grid by A. Damseaux)

import numpy as np
import xarray as xr
from scipy import stats
from scipy import interpolate
import matplotlib.pyplot as plt
from os import sys

# alt outfile
outfile    = sys.argv[2]

# max st file
maxtfile   = sys.argv[1]
maxtfile   = "/work/aa0049/a271098/cegio/data/postproc/57_DOM02_001/processed/permafrost/57_DOM02_001.1980.perma.timemax.shallow.nc"
dsoilt     = xr.open_dataset(maxtfile, mask_and_scale=False)
soilt      = dsoilt['TSOI']

# This script is using a irregular grid, for 2D grid see Fabien's version
reso 	   = dsoilt['lndgrid'].shape[0] # resolution
soillev    = dsoilt['levgrnd']

misvals    = soilt.missing_value
misvalo    = -999.99

a_layer_d  = np.full([reso], misvalo, dtype=float)

#----- Functions
def find_profile_type(a):	
# Determine the kind of active layer found in the soil temperature profile a
#
 # Convert from K to C
 a = a - 273.15
#	
 # Count number of temperature sign changes (0 is considered frozen/negative)
 b = a[1:] # take the vectors with shifted index
 c = a[:-1]
 # if normal vector and shifted vector have different sign, there is a change of temperature
 sign_changes = ( ((b > 0.0) & (c <= 0.0)) | ((b <= 0.0) & (c > 0.0)) ).sum()
#	
 if sign_changes == 0: # if no sign changes, no active layer
  if a[0] > 0.0: 	# U
   return "thawed"
  else:	      		# F
   return "frozen" 
#
 elif sign_changes == 1 or sign_changes == 2:
  if a[0] > 0.0: 	# UF, UFU
   return "ALT"
  else:	      		# FU, FUF
   return "invalid"	# thalik?
#
 else:                 	# UFUF..., FUFU...
  return "invalid"	# other thalik or bottom?


def compute_alt(i, a, lev, misvalo):	
#Active layer calculation of soil profile a of type UF or UFU by interpolation.
#	
 # Convert from K to C
 a = a - 273.15
#
 # Find size of frozen block F
 size_F = (a <= 0.0).sum()
#
 # Get data points from all U layers, plus n_layers in F (at most max_layers_F)
 max_layers_F = 15
 n_layers_F = min(size_F, max_layers_F)
 last_layer_to_fit = ( (a <= 0.0).cumsum() < n_layers_F ).argmin()  # ??
#
 soil_temp = a[:last_layer_to_fit + 1] # limit the number of layers
 lev = lev[:last_layer_to_fit + 1]
	
 # Interpolation
 if (last_layer_to_fit <= 3): # why?
  a_layer_d = misvalo
		
 else:
  fsoil = interpolate.UnivariateSpline(lev, soil_temp)

  # Find root (zeros of the spine)
  roots_soil = fsoil.roots()
		
  if ( roots_soil.size > 0 ):
   a_layer_d = roots_soil[0]
  else:
   a_layer_d = misvalo


 return a_layer_d
	
	

# fill arrays
for i in range(reso):
 soil_profile = soilt.values[0,:,i] # take all depth of one grid point
			
 if ( any(soil_profile == misvals) ):
  pass
	
 else:
  soil_type  = find_profile_type(soil_profile) # is the grid point considered an ALT?

  if soil_type == "ALT":
   a_layer_d[i] = compute_alt(i, soil_profile, soillev, misvalo)
  
  elif soil_type == "frozen":
   a_layer_d[i] = 0.0 # why give frozen ground, a value of 0?

	
# produce output
da_alt = xr.DataArray(a_layer_d)
da_alt.name = 'ALT'

da_alt.to_netcdf(outfile, encoding={'ALT': {'dtype': 'float', '_FillValue': misvalo}})
