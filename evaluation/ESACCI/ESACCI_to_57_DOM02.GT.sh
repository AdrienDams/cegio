#!/bin/bash
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --time=8:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=8G

# from A. Damseaux
# Bash file to regrid (1) any nc and (2) a 57_DOM02 to a same regular lat lon grid

## Init
modelinput_dir="$cegio/data/$run_name/monthly"
modeloutput_dir="$cegio/data/ESACCI/$run_name/CTSM_regridded"
obsinput_dir="$cegio/data/ESACCI/orig_data"
obsoutput_dir="$cegio/data/ESACCI/$run_name/ESACCI_regridded"
scratch_ESA="$scratch_dir/ESACCI"
variable="TSOI"

## Description file
descriptiongrid="/work/aa0049/a271098/output/description/description_ICON_arctic2_57_DOM02_unstructured.txt_new_cdo"
descriptionreg="/work/aa0049/a271098/output/description/description_ICON_arctic2_57_DOM02_reg.txt_new_cdo"

echo $depth

for year in $( seq $startyear_esa $endyear_esa ) ; do # years available from ESACCI
 echo $year
 # Input
 modelfiles="$modelinput_dir/$run_name.clm2.h0.$year-*.nc"
 modelfile="$run_name.TSOI.$depth.$year.nc"
 obsfile="$obsinput_dir/ESACCI-*GTD*-$year-fv03.0.nc"

 # Output
 modeloutput=$variable.$depth.$run_name.$year.nc
 obsoutput=$variable.$depth.$run_name.$year.nc

 # Model input yearly average
 echo $depth $toplayer $botlayer
 ncra -O -d levgrnd,$toplayer -v $variable $modelfiles $scratch_ESA/$modelfile.top
 ncra -O -d levgrnd,$botlayer -v $variable $modelfiles $scratch_ESA/$modelfile.bottom

 # Linear interpolation (value calculated by hand)
 ncflint -O -w $inttop,$intbot $scratch_ESA/$modelfile.top $scratch_ESA/$modelfile.bottom $scratch_ESA/$modelfile

 # Regrid model
 cdo -r setgrid,$descriptiongrid -selvar,$variable $scratch_ESA/$modelfile $scratch_ESA/grid_tmp.$variable.$depth.nc # any file

 # Remap model
 cdo -r remapnn,$descriptionreg -selvar,$variable $scratch_ESA/grid_tmp.$variable.$depth.nc $scratch_ESA/remap_tmp.$variable.$depth.nc

 # Crop model (not latitude above 90)
 ncks -O -F -d lat,0.,90. $scratch_ESA/remap_tmp.$variable.$depth.nc $modeloutput_dir/$modeloutput

 # Remap obs
 cdo -r -remapcon,$modeloutput_dir/$modeloutput -selvar,T$depth $obsfile $scratch_ESA/final_tmp.$variable.$depth.nc

 # Rename and move
 cdo chname,T$depth,TSOI $scratch_ESA/final_tmp.$variable.$depth.nc $obsoutput_dir/$obsoutput

done
