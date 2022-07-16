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
scratch_dir="/scratch/a/a271098/ESACCI"
variable="PFR"
maskvariable="TSOI"

## Description file
descriptiongrid="/work/aa0049/a271098/output/description/description_ICON_arctic2_57_DOM02_unstructured.txt_new_cdo"
descriptionreg="/work/aa0049/a271098/output/description/description_ICON_arctic2_57_DOM02_reg.txt_new_cdo"
weightfile="/work/aa0049/a271098/output/evaluation/ESACCI/ESAto57.weights.con.nc"

for year in {1997..2019}; do
 echo $year
 # Input
 modelfile="$modelinput_dir/$run_name.permafrost_extend.${year}.nc"
 obsfile="$obsinput_dir/ESACCI-*-${year}-fv03.0.nc"

 # Output
 modeloutput=$variable.$run_name.$year.nc
 obsoutput=$variable.ESACCI.on.$run_name.$year.nc

 ## Take top layer
 ncks -O -F -d levgrnd,1 -selvar,$maskvariable $modelfile $scratch_dir/top_tmp.PFR.nc

 ## Regrid model
 cdo -r setgrid,$descriptiongrid -selvar,$maskvariable $scratch_dir/top_tmp.PFR.nc $scratch_dir/grid_tmp.PFR.nc # any file

 # Remap model
 cdo -r remapnn,$descriptionreg -selvar,$maskvariable $scratch_dir/grid_tmp.PFR.nc $scratch_dir/remap_tmp.PFR.nc

 # Crop model (not latitude above 90)
 ncks -O -F -d lat,0.,90. $scratch_dir/remap_tmp.PFR.nc $modeloutput_dir/$modeloutput

 # Remap obs
 #cdo -r -remap,$modeloutput_dir/$modeloutput,$weightfile $obsfile $obsoutput_dir/$obsoutput
 cdo -r -remapcon,$modeloutput_dir/$modeloutput $obsfile $obsoutput_dir/$obsoutput

done
