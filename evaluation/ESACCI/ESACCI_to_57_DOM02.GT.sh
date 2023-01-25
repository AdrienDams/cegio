#!/bin/bash
#SBATCH --partition=shared
#SBATCH --ntasks=1
#SBATCH --time=8:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=60G

## Init
modelinput_dir="$cegio/data/$run_name/monthly"
modeloutput_dir="$cegio/data/ESACCI/$run_name/CTSM_regridded"
obsinput_dir="$cegio/data/ESACCI/orig_data"
obsoutput_dir="$cegio/data/ESACCI/$run_name/ESACCI_regridded"
variable="TSOI"
variable_esa="GTD"

echo $depth

# Move files for year average model and obs
for year in $( seq $startyear_esa $endyear_esa ) ; do
	ncra -O -d levgrnd,$toplayer -v $variable $modelinput_dir/$run_name.clm2.h0.$year-*.nc $scratch_ESA/tmp/$run_name.$variable.$depth.$year.top.nc
	ncra -O -d levgrnd,$botlayer -v $variable $modelinput_dir/$run_name.clm2.h0.$year-*.nc $scratch_ESA/tmp/$run_name.$variable.$depth.$year.bot.nc
	ln -sf $obsinput_dir/ESACCI-*$variable_esa*-$year-fv03.0.nc $scratch_ESA/tmp/ESACCI.$variable_esa.$year.nc
done

# Gather model
ncecat -O $scratch_ESA/tmp/$run_name.$variable.$depth.*top.nc $scratch_ESA/$run_name.$variable.$depth.period.top.nc
ncecat -O $scratch_ESA/tmp/$run_name.$variable.$depth.*bot.nc $scratch_ESA/$run_name.$variable.$depth.period.bot.nc

# Extract variable model
ncks -O -v $variable $scratch_ESA/$run_name.$variable.$depth.period.top.nc $scratch_ESA/$run_name.$variable.extracted.top.nc
ncks -O -v $variable $scratch_ESA/$run_name.$variable.$depth.period.bot.nc $scratch_ESA/$run_name.$variable.extracted.bot.nc

# Period average model and obs
ncra -O $scratch_ESA/$run_name.$variable.extracted.top.nc $scratch_ESA/$run_name.$variable.time_average.top.nc
ncra -O $scratch_ESA/$run_name.$variable.extracted.bot.nc $scratch_ESA/$run_name.$variable.time_average.bot.nc
ncra -O $scratch_ESA/tmp/ESACCI.$variable_esa.*.nc $scratch_ESA/ESACCI.$variable.$depth.$run_name.period.nc

# Linear interpolation model
ncflint -O -w $inttop,$intbot $scratch_ESA/$run_name.$variable.time_average.top.nc $scratch_ESA/$run_name.$variable.time_average.bot.nc $scratch_ESA/$run_name.$variable.time_average.nc

# Regrid model
cdo -r setgrid,$descriptiongrid -selvar,$variable $scratch_ESA/$run_name.$variable.time_average.nc $scratch_ESA/$run_name.grid_tmp.$variable.$depth.nc

# Remap model
cdo -r remapnn,$descriptionreg -selvar,$variable $scratch_ESA/$run_name.grid_tmp.$variable.$depth.nc $scratch_ESA/$run_name.remap_tmp.$variable.$depth.nc

# Crop model (not latitude above 90)
ncks -O -F -d lat,0.,90. $scratch_ESA/$run_name.remap_tmp.$variable.$depth.nc $modeloutput_dir/$run_name.$variable.$depth.period.nc

# Remap obs
cdo -r -remapcon,$modeloutput_dir/$run_name.$variable.$depth.period.nc -selvar,T$depth $scratch_ESA/ESACCI.$variable.$depth.$run_name.period.nc $scratch_ESA/final_tmp.$variable.$run_name.$depth.nc

# Rename and move obs
cdo chname,T$depth,$variable $scratch_ESA/final_tmp.$variable.$run_name.$depth.nc $obsoutput_dir/$run_name.$variable.$depth.period.nc
