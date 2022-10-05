#!/bin/sh
# (from A. Damseaux)

#SBATCH --partition=shared
#SBATCH --ntasks=1  
#SBATCH --time=08:00:00
#SBATCH --account=aa0049

folder=$cegio/evaluation/CALM/
data_folder=$cegio/data/postproc/$run_name/processed/permafrost

# period average
ncecat $data_folder/$run_name.active_layer_depth.????.nc -O $data_folder/$run_name.active_layer_depth.period.nc

# create stations_ctsm_indexes.txt
python $folder/ctsm_vs_calm.py $data_folder/$run_name.active_layer_depth.period.nc
