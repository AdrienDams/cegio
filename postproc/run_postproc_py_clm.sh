#!/bin/sh

#SBATCH --partition=shared
#SBATCH --ntasks=1  
#SBATCH --time=48:00:00
#SBATCH --account=aa0049

# set up

export run_prefix="$run_name.clm2.h0"
export firstyear=$startyear

# directory files

export targetdir="$cegio/data/postproc/$run_name"
export datadir="$cegio/data/$run_name"
export progdir="$cegio/postproc"
export permdir=${targetdir}/processed/permafrost #  output files for perma 

# make necessary directories
mkdir -p ${targetdir} ${targetdir}/processed/season ${scratch_dir} ${permdir}

echo "make seasons"
${progdir}/make_season_mean_all.sh

echo "make snowdepth means"
${progdir}/make_annual_mean_snowdepth.sh

echo "make ground temperature"
${progdir}/make_magt.sh

echo "make permafrost extend"
${progdir}/make_permafrost_extend.sh

# look for 5 consicutives days of snow
# output: nomber of days when is snow free in the year
echo "make snow free day"

for ((year=$startyear;year<=$endyear;year++)); do
 echo "year" $year

 snowinfile=${scratch_dir}/${run_name}.swemerge.$year.nc
 snowoutfile=${permdir}/${run_name}.snowfreeday.5days.$year.nc
 cdo -select,name=H2OSNO ${datadir}/daily/${run_prefix}.$year* $snowinfile

 python3 ${progdir}/end_snow_melt.py $snowinfile $snowoutfile
done

# maximum of soils that thaw in a year
# compare to the hydrologic end of measurements
# compute maximum ground temperature, using a spline (similar to 1st order polynol) to make a curve in ground to look for 0 intercept
echo "make ALT"
for ((year=$startyear;year<=$endyear;year++)); do
 echo "year" $year
 #note: the infile is created in the process of making the permafrost extend
 altinfile=${permdir}/${run_name}.${year}.perma.timemax.shallow.nc
 altoutfile=${permdir}/${run_name}.active_layer_depth.$year.nc
	
 python3 ${progdir}/active_layer.py $altinfile $altoutfile
done

