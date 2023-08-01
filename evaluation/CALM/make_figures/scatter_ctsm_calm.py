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
calm_west, ctsm_west = calm_alt[west].flatten(), ctsm_alt[west].flatten()
calm_east, ctsm_east = calm_alt[east].flatten(), ctsm_alt[east].flatten()

# calculate slopes and intercepts, removing missing values
r_value_west, p_value_west = stats.pearsonr(calm_west[~np.isnan(calm_west) & ~np.isnan(ctsm_west)], ctsm_west[~np.isnan(calm_west) & ~np.isnan(ctsm_west)])
r_value_east, p_value_east = stats.pearsonr(calm_east[~np.isnan(calm_east) & ~np.isnan(ctsm_east)], ctsm_east[~np.isnan(calm_east) & ~np.isnan(ctsm_east)])

# create scatter plot with two different colors
fig, ax = plt.subplots()
fig.set_figheight(8)
fig.set_figwidth(8)

sns.regplot(calm_west, ctsm_west, label='Western Arctic', scatter_kws={'s':3,'alpha':0.5}, line_kws={'label':"Linear Reg"})
sns.regplot(calm_east, ctsm_east, label='Eastern Arctic', scatter_kws={'s':3,'alpha':0.5}, line_kws={'label':"Linear Reg"})

# Labeling
ax.set_xlabel(r' Observed ALT in m')
ax.set_ylabel(r' Modeled ALT in m')

# add x=y line
min_val = 0
max_val = max(np.max(calm_alt[~np.isnan(calm_alt)].flatten()), np.max(ctsm_alt[~np.isnan(ctsm_alt)].flatten()))
plt.plot([min_val, max_val], [min_val, max_val], linestyle='--', linewidth=1, color='gray', alpha=0.8)

# graph options
ax.set_xlim([0, 3])
ax.set_ylim([0, 8])

# Legend
ax.legend(loc = 'best', ncol=1)
leg = ax.get_legend()
L_labels = leg.get_texts()
L_labels[1].set_text(r'$R^2:{0:.2f}$'.format(r_value_west))
L_labels[3].set_text(r'$R^2:{0:.2f}$'.format(r_value_east))


# save output
plot_name = output_dir + "scatter_ctsm_calm"
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight')
plt.close()

print("calm scatter: done!")
