#!/bin/sh
# (from A. Damseaux)

#SBATCH --partition=shared
#SBATCH --ntasks=1  
#SBATCH --time=08:00:00
#SBATCH --account=aa0049

folder=$cegio/evaluation/stations/make_figures
data_folder=$cegio/data/stations/$run_name

# extract data
python extract_functions.py

# heatmap
intput_heat=$data_folder/stations-vs-ctsm.1979-2020.tmp.$run_name.nc
python $folder/heatmap_global.py $intput_heat

# pcm area
input_pcm=$data_folder/stations-vs-ctsm.1979-2020.pcm.$run_name.nc
python $folder/pcm_plot.py $input_pcm

# scatter plots
input_tmp=$data_folder/stations-vs-ctsm.1979-2020.tmp.$run_name.nc
python $folder/scatter_plot.py $input_tmp



 
