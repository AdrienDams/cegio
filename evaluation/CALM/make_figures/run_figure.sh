#!/bin/bash
#SBATCH --partition=shared
#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --account=aa0049

## Init
folder=$cegio/evaluation/CALM/make_figures
modelinput_dir="$cegio/data/postproc/$run_name/processed/permafrost"
modeloutput_dir="$cegio/data/CALM/$run_name/CTSM_regridded"
mkdir -p $modeloutput_dir
variable="ALT"

# Input
mkdir -p  $modelinput_dir/CALM_period
cp $modelinput_dir/$run_name.active_layer_depth.199?.nc $modelinput_dir/CALM_period
cp $modelinput_dir/$run_name.active_layer_depth.20??.nc $modelinput_dir/CALM_period
modelfiles="$modelinput_dir/CALM_period/$run_name.active_layer_depth.????.nc"
modelfile="$modelinput_dir/CALM_period/$run_name.active_layer_depth.period.nc"

# Output
modeloutput=$variable.$run_name.period.nc

## Period average
ncea -O $modelfiles $modelfile

## Regrid model
cdo -r setgrid,$descriptiongrid -selvar,$variable $modelfile $modeloutput_dir/grid_tmp.nc

# Remap model
cdo -r remapnn,$descriptionreg -selvar,$variable $modeloutput_dir/grid_tmp.nc $modeloutput_dir/remap_tmp.nc

# Crop model (not latitude above 90)
ncks -O -F -d lat,0.,90. $modeloutput_dir/remap_tmp.nc $modeloutput_dir/$modeloutput

# create figure
python $folder/map_ctsm_calm.py $modeloutput_dir/$modeloutput

# scatter
python $folder/scatter_ctsm_calm.py 
