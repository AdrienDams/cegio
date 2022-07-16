# Snow melt (from F. Peyrusse, modified for irregular grid by A. Damseaux)

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from os import sys
from timeit import default_timer as timer

# sfd outfile
outfile  = sys.argv[2]

# yearly infile
snowfile = sys.argv[1]
dsnowwe  = xr.open_dataset(snowfile, mask_and_scale=False)
snowwe   = dsnowwe['H2OSNO']                       

# This script is using a irregular grid, for 2D grid see Fabien's version
reso = dsnowwe['lndgrid'].shape[0] # resolution

misvale  = snowwe.missing_value
misvalo  = -999

snow_melt= np.full([reso], misvalo, dtype=float)

# glacier mask
maskfile = '/work/aa0049/a271098/inputdata/lnd/clm2/surfdata_map/surfdata_57_DOM02_hist_78pfts_CMIP6_simyr2000_c220330.nc'
dmask    = xr.open_dataset(maskfile, mask_and_scale=False)
glac     = dmask['PCT_GLACIER'] # glaciers
#lsm      = dmask['PCT_GLACIER'] # sea


#----- Functions
def find_snow_melt(snowwe, shift, melt_min, snow_min, misvalo):	
#Determine the last day of snow melt from a yearly snow water equivalent profile.
 ndays = 365 
 consec_melt_min = 0

 # looking for a snow melt gradient 
 for tt in range(shift, ndays):	
  shift_snow_diff = snowwe[tt - shift] - snowwe[tt - 1]
  		
  if ( shift_snow_diff >  melt_min):
   consec_melt_min += 1
  else:
   consec_melt_min = 0
		
  if(consec_melt_min >= shift):
   start_melt = tt - shift

   for zz in range(start_melt, ndays):
    if( snowwe[zz] < snow_min ):
     return zz + 1
		
 # no gradient found, we're going for consecutive minimal snow amounts
 consec_snow_min = 0
	
 for tt in range(ndays):
  if( snowwe[tt] < 10*snow_min ): # 1e-3 like in the Fortran code
   consec_snow_min += 1
  else:
   consec_snow_min = 0

  if(consec_snow_min >= shift): 
   return tt - shift + 2

 return misvalo

			
# parameters
shift    = 5
melt_min = 15.0
snow_min = 0.0001

# fill arrays
for i in range(reso):
 # exclude points with high percentages of sea or glacier
 #if ( ( lsm[i] <=  0.5 ) or ( glac[i] >= 50 ) ):
 if ( glac[i] >= 50 ):
  snow_melt[i] = misvalo

 else:
  snowwe_val = snowwe.values[:,i]
  snow_melt[i] = find_snow_melt(snowwe_val, shift, melt_min, snow_min, misvalo)

# produce output
da_sm = xr.DataArray(snow_melt, dims=snowwe[0].dims)
da_sm.name = 'snow_melt'

da_sm.to_netcdf(outfile, encoding={'snow_melt': {'dtype': 'float', '_FillValue': misvalo}})


	


