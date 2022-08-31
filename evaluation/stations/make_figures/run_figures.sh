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

# make regions
#input_tmp="stations-vs-ctsm.1979-2019.tmp"
#rm -f $data_folder/$input_tmp.q1.$run_name.nc
#rm -f $data_folder/$input_tmp.q2.$run_name.nc
#rm -f $data_folder/$input_tmp.q3.$run_name.nc
#rm -f $data_folder/$input_tmp.q4.$run_name.nc

#ncks -d lon,0.,90. $data_folder/$input_tmp.$run_name.nc -O $data_folder/$input_tmp.q1.$run_name.nc
#ncks -d lon,90.,180. $data_folder/$input_tmp.$run_name.nc -O $data_folder/$input_tmp.q2.$run_name.nc
#ncks -d lon,-90.,0. $data_folder/$input_tmp.$run_name.nc -O $data_folder/$input_tmp.q3.$run_name.nc
#ncks -d lon,-180.,-90. $data_folder/$input_tmp.$run_name.nc -O $data_folder/$input_tmp.q4.$run_name.nc

# heatmap
#python $folder/heatmap_global.py $data_folder/$input_tmp.$run_name.nc
#python $folder/heatmap_regional.py $data_folder/$input_tmp.q1.$run_name.nc $data_folder/$input_tmp.q2.$run_name.nc $data_folder/$input_tmp.q3.$run_name.nc $data_folder/$input_tmp.q4.$run_name.nc

# pcm area
input_pcm=$data_folder/stations-vs-ctsm.1979-2020.pcm.$run_name.nc
python $folder/pcm_plot.py $input_pcm

# scatter plots
input_tmp=$data_folder/stations-vs-ctsm.1979-2020.tmp.$run_name.nc
python $folder/scatter_plot.py $input_tmp



 
