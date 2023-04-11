# print a scatter plot between CTSM and CALM stations

import numpy as np
import pandas
from scipy import stats
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import seaborn as sns
sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": "-"})
import os
import sys

# open csv
calmfile = os.environ['cegio'] + "/evaluation/CALM/CALM_Summary_table_simplified.csv"
ctsmfile = os.environ['cegio'] + "/evaluation/CALM/ctsm_to_calm_" + os.environ['run_name'] + ".csv"
calm_table = np.array(pandas.read_csv(calmfile, encoding="ISO-8859-1"))
ctsm_table = np.array(pandas.read_csv(ctsmfile, encoding="ISO-8859-1",header=None))

# output
output_dir = os.environ['cegio'] + "/figures/" + os.environ['run_name'] + "/CALM/"
os.makedirs(output_dir, exist_ok=True)

# extract variables
calm_lon = calm_table[:,2].astype('float64')
calm_lat = calm_table[:,1].astype('float64')
ctsm_alt = ctsm_table.astype('float64')/100

calm_alt_outperiod = calm_table[:,3:].astype('float64')/100

# limit calm to ctsm data (TDL: need to create an external function)
startyear = int(os.environ['startyear'])
endyear   = int(os.environ['endyear'])
if startyear > 1990: startyearind=startyear-1990
else: startyearind=0

if endyear < 2021: endyearind=-(2021-endyear)
else: endyearind=None # end (-1 not working)

calm_alt = calm_alt_outperiod[:,startyearind:endyearind]

# difference (not used yet)
diff = np.zeros(np.shape(ctsm_alt))
for i in range(np.shape(ctsm_alt)[0]):
	for j in range(np.shape(ctsm_alt)[1]):
		if(ctsm_alt[i,j]>0):
			diff[i,j] = ctsm_alt[i,j]-calm_alt[i,j]
		else:
			diff[i,j] = None

# make two sides
west = calm_lon<0
east = calm_lon>0

# stats
#slope, intercept, r_value, p_value, std_err = stats.linregress(calm_alt,ctsm_alt)

# scatter plot
fig, (ax1, ax2) = plt.subplots(1, 2)

sns.regplot(x = calm_alt[np.where(west)].flatten(),
			y = ctsm_alt[np.where(west)].flatten(),
			scatter_kws={'s':2}, ax=ax1)

sns.regplot(x = calm_alt[np.where(east)].flatten(),
			y = ctsm_alt[np.where(east)].flatten(),
			scatter_kws={'s':2}, ax=ax2)

# title
ax1.title.set_text('Western Arctic')
ax2.title.set_text('Eastern Arctic')

# labeling
ax1.set_xlabel(r' ALT from CALM in m')
ax1.set_ylabel(r' ALT from CTSM in m ')
ax2.set_xlabel(r' ALT from CALM in m')
ax2.set_ylabel(r' ALT from CTSM in m ')

# axis options
ax1.set_aspect('equal', adjustable='box')
ax2.set_aspect('equal', adjustable='box')

# save output
plot_name = output_dir + "scatter_ctsm_calm"
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight')
plt.close()

print("calm scatter: done!")
