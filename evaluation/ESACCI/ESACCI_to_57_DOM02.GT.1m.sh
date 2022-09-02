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

depth=1m
echo $depth

for year in {1997..2019}; do # years available from ESACCI
 echo $year
 # Input
 modelfiles="$modelinput_dir/$run_name.clm2.h0.$year-*.nc"
 modelfile="$run_name.TSOI.$depth.$year.nc"
 obsfile="$obsinput_dir/ESACCI-*GTD*-$year-fv03.0.nc"

 # Output
 modeloutput=$variable.$depth.$run_name.$year.nc
 obsoutput=$variable.$depth.$run_name.$year.nc

 # Model input yearly average
 ncra -O -F -d levgrnd,8 -v $variable $modelfiles $scratch_ESA/$modelfile.top
 ncra -O -F -d levgrnd,9 -v $variable $modelfiles $scratch_ESA/$modelfile.bottom

 # Linear interpolation (value calculated by hand)
 ncflint -w 0.23,0.77 $scratch_ESA/$modelfile.top $scratch_ESA/$modelfile.bottom $scratch_ESA/$modelfile

 # Regrid model
 cdo -r setgrid,$descriptiongrid -selvar,$variable $scratch_ESA/$modelfile.int $scratch_ESA/grid_tmp.GT.nc # any file

 # Remap model
 cdo -r remapnn,$descriptionreg -selvar,$variable $scratch_ESA/grid_tmp.GT.nc $scratch_ESA/remap_tmp.GT.nc

 # Crop model (not latitude above 90)
 ncks -O -F -d lat,0.,90. $scratch_ESA/remap_tmp.GT.nc $scratch_ESA/crop_tmp.GT.nc

 # Remap obs
 cdo -r -remapcon,$scratch_ESA/crop_tmp.GT.nc -selvar,T$depth $obsfile $scratch_ESA/final_tmp.GT.nc

 # Rename and move
 cdo chname,T$depth,TSOI $scratch_ESA/final_tmp.GT.nc $obsoutput_dir/$obsoutput

done
