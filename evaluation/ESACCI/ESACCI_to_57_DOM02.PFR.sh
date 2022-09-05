#!/bin/bash
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --time=8:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=8G

# from A. Damseaux
# Bash file to regrid (1) any nc and (2) a 57_DOM02 to a same regular lat lon grid
# Run this file sbatch 57_DOM02_to_grid.sh

## Init
modelinput_dir="$cegio/data/postproc/$run_name/processed/permafrost"
modeloutput_dir="$cegio/data/ESACCI/$run_name/CTSM_regridded"
obsinput_dir="$cegio/data/ESACCI/orig_data"
obsoutput_dir="$cegio/data/ESACCI/$run_name/ESACCI_regridded"
scratch_ESA="$scratch_dir/ESACCI"
variable="PFR"
maskvariable="TSOI"

## Description file
descriptiongrid="/work/aa0049/a271098/output/description/description_ICON_arctic2_57_DOM02_unstructured.txt_new_cdo"
descriptionreg="/work/aa0049/a271098/output/description/description_ICON_arctic2_57_DOM02_reg.txt_new_cdo"

for year in $( seq $startyear_esa $endyear_esa ) ; do # years available from ESACCI
 echo $year
 # Input
 modelfile="$modelinput_dir/$run_name.permafrost_extend.${year}.nc"
 obsfile="$obsinput_dir/ESACCI-*PFR*-$year-fv03.0.nc"

 # Output
 modeloutput=$variable.$run_name.$year.nc
 obsoutput=$variable.$run_name.$year.nc

 ## Take top layer
 ncks -O -F -d levgrnd,1 -selvar,$maskvariable $modelfile $scratch_ESA/top_tmp.PFR.nc

 ## Regrid model
 cdo -r setgrid,$descriptiongrid -selvar,$maskvariable $scratch_ESA/top_tmp.PFR.nc $scratch_ESA/grid_tmp.PFR.nc # any file

 # Remap model
 cdo -r remapnn,$descriptionreg -selvar,$maskvariable $scratch_ESA/grid_tmp.PFR.nc $scratch_ESA/remap_tmp.PFR.nc

 # Crop model (not latitude above 90)
 ncks -O -F -d lat,0.,90. $scratch_ESA/remap_tmp.PFR.nc $modeloutput_dir/$modeloutput

 # Remap obs
 cdo -r -remapcon,$modeloutput_dir/$modeloutput $obsfile $obsoutput_dir/$obsoutput

done
