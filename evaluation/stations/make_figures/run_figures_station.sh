#!/bin/sh

#echo "Enter year (only for splines graph):" 

#read year

#echo "Enter month (only for splines graph):" 

#read month

echo "Enter station ID:"

read search

linesearch="$(grep -n $search $cegio/data/stations/station_list_AllArctic2022.txt | cut -f1 -d:)" 

sedresult="$(sed -n ${linesearch}p $cegio/evaluation/stations/stations_ctsm_indexes.txt)"

data_folder=$cegio/data/stations/$run_name

if [ "$sedresult" == " " ]; then
 echo "Error! Station out of domain"
else
 station_id="${sedresult%% *}"
 ctsm_id="${sedresult##* }"

 echo "station $search, $station_id, $ctsm_id "

 # splines graph
 #python $cegio/evaluation/stations/make_figures/splines_graph.py $year $month $station_id $ctsm_id $search

 # linear plot
 input_linear=$data_folder/stations-vs-ctsm.1979-2020.tmp.$run_name.nc
 python $cegio/evaluation/stations/make_figures/linear_plot_station.py $input_linear $station_id $search

 # trumpet curves
 python $cegio/evaluation/stations/make_figures/trumpet_curves.py $station_id $ctsm_id $search
fi
