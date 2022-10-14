#!/bin/sh
# (from A. Damseaux)

#SBATCH --partition=shared
#SBATCH --ntasks=1  
#SBATCH --time=48:00:00
#SBATCH --account=aa0049

folder=$cegio/evaluation/stations/make_figures
data_folder=$cegio/data/stations/$run_name

input_tmp=$data_folder/stations-vs-ctsm.1979-2020.tmp.$run_name.nc
input_pcm=$data_folder/stations-vs-ctsm.1979-2020.pcm.$run_name.nc

# extract data
python $folder/extract_functions.py $input_tmp

# heatmap
python $folder/heatmap.py $input_tmp

# pcm
python $folder/pcm_plot.py $input_pcm

# scatter plots
python $folder/scatter_plot.py



 
