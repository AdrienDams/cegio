#!/bin/sh
# (from A. Damseaux)

echo "Enter year (only for splines graph):" 

read year

echo "Enter month (only for splines graph):" 

read month

echo "Enter station ID:"

read search

# splines graph
python $cegio/evaluation/stations/make_figures/splines_graph.py $year $month $search

# linear plot
input_linear=$data_folder/stations-vs-ctsm.1979-2020.tmp.$run_name.nc
python $cegio/evaluation/stations/make_figures/linear_plot_station.py $input_linear $search

# trumpet curves
python $cegio/evaluation/stations/make_figures/trumpet_curves.py $search 
