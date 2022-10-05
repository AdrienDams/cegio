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
calm_alt = calm_table[:,3:].astype('float64')/100
ctsm_alt = ctsm_table.astype('float64')/100

# difference
diff = np.zeros(np.shape(ctsm_alt))
for i in range(np.shape(ctsm_alt)[0]):
	for j in range(np.shape(ctsm_alt)[1]):
		if(ctsm_alt[i,j]>0):
			diff[i,j] = ctsm_alt[i,j]-calm_alt[i,j]
		else:
			diff[i,j] = None

# stats
#slope, intercept, r_value, p_value, std_err = stats.linregress(calm_alt,ctsm_alt)

# scatter plot
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(3)

sns.regplot(x = np.ma.masked_invalid(calm_alt[ctsm_alt>0]).flatten(),
			y = np.ma.masked_invalid(ctsm_alt[ctsm_alt>0]).flatten())

# labeling
ax.set_xlabel(r' ALT from CALM in m',fontsize=14)
ax.set_ylabel(r' ALT from CTSM in m ',fontsize=14)

#plot options
ax.set_xlim(0,3)
ax.set_ylim(0,8)

# save output
plot_name = output_dir + "scatter_ctsm_calm"
plt.savefig(plot_name +'.pdf', format='pdf', bbox_inches='tight')
plt.close()

print("calm scatter: done!")
