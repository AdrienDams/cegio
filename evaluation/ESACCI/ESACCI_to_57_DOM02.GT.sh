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
variable="TSOI"
depth="5m"
depthctsm=17 #9 for 1m, 12 for 2m, 17 for 5m

## Description file
descriptiongrid="/work/aa0049/a271098/output/description/description_ICON_arctic2_57_DOM02_unstructured.txt_new_cdo"
descriptionreg="/work/aa0049/a271098/output/description/description_ICON_arctic2_57_DOM02_reg.txt_new_cdo"
weightfile="/work/aa0049/a271098/output/evaluation/ESACCI/ESAto57.weights.con.nc"

for year in {1997..2019}; do
 echo $year
 # Input
 modelfiles="$modelinput_dir/$run_name.clm2.h0.$year-*.nc"
 modelfile="$modelinput_dir/$run_name.TSOI.$depth.$year.nc"
 obsfile="$obsinput_dir/ESACCI-*-$year-fv03.0.nc"

 # Output
 modeloutput=$variable.$depth.$run_name.$year.nc
 obsoutput=$variable.$depth.ESACCI.on.$run_name.$year.nc

 ## Model input yearly average
 ncra -O -F -d levgrnd,$depthctsm -v TSOI $modelfiles $modelfile

 ## Regrid model
 cdo -r setgrid,$descriptiongrid -selvar,$variable $modelfile $scratch_dir/grid_tmp.GT.nc # any file

 # Remap model
 cdo -r remapnn,$descriptionreg -selvar,$variable $scratch_dir/grid_tmp.GT.nc $scratch_dir/remap_tmp.GT.nc

 # Crop model (not latitude above 90)
 ncks -O -F -d lat,0.,90. $scratch_dir/remap_tmp.GT.nc $modeloutput_dir/$modeloutput

 # Remap obs
 #cdo -r -remap,$modeloutput_dir/$modeloutput,$weightfile $obsfile $obsoutput_dir/$obsoutput
 cdo -r -remapcon,$modeloutput_dir/$modeloutput -selvar,T$depth $obsfile $obsoutput_dir/$obsoutput

done
