#!/bin/bash
#SBATCH --partition=shared
#SBATCH --ntasks=1
#SBATCH --time=8:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=60G

## Init
modelinput_dir="$cegio/data/postproc/$run_name/processed/permafrost"
modeloutput_dir="$cegio/data/ESACCI/$run_name/CTSM_regridded"
obsinput_dir="$cegio/data/ESACCI/orig_data"
obsoutput_dir="$cegio/data/ESACCI/$run_name/ESACCI_regridded"
variable="PFR"
maskvariable="TSOI"

# Move files for period average model and obs
for year in $( seq $startyear_esa $endyear_esa ) ; do
	ln -sf $modelinput_dir/$run_name.permafrost_extend.${year}.shallow.nc $scratch_ESA/tmp/$run_name.$variable.$year.nc
	ln -sf $obsinput_dir/ESACCI-*${variable}*-$year-fv03.0.nc $scratch_ESA/tmp/ESACCI.$variable.$year.nc
done

# Gather model
ncecat -O $scratch_ESA/tmp/$run_name.$variable.*.nc $scratch_ESA/$run_name.$variable.period.nc

# Extract variable model
ncks -O -v $maskvariable $scratch_ESA/$run_name.$variable.period.nc $scratch_ESA/$run_name.$variable.extracted.nc

# Period average model and obs
ncra -O $scratch_ESA/$run_name.$variable.extracted.nc $modelinput_dir/$run_name.$variable.time_average.nc
ncra -O $scratch_ESA/tmp/ESACCI.$variable.*.nc $obsinput_dir/ESACCI.$variable.$run_name.period.nc

## Regrid model
cdo -r setgrid,$descriptiongrid -selvar,$maskvariable $modelinput_dir/$run_name.$variable.time_average.nc $scratch_ESA/$run_name.grid.$variable.tmp.nc

# Remap model
cdo -r remapnn,$descriptionreg -selvar,$maskvariable $scratch_ESA/$run_name.grid.$variable.tmp.nc $scratch_ESA/$run_name.remap.$variable.tmp.nc

# Crop model (not latitude above 90)
ncks -O -F -d lat,0.,90. $scratch_ESA/$run_name.remap.$variable.tmp.nc $modeloutput_dir/$run_name.$variable.period.nc

# Remap obs
cdo -r -remapcon,$modeloutput_dir/$run_name.$variable.period.nc $obsinput_dir/ESACCI.$variable.$run_name.period.nc $obsoutput_dir/$run_name.$variable.period.nc
