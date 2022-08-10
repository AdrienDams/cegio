#!/bin/bash

echo "Enter station ID:"

read search

linesearch="$(grep -n $search $cegio/data/stations/station_list_AllArctic2020.txt | cut -f1 -d:)" 

sedresult="$(sed -n ${linesearch}p $cegio/evaluation/stations/stations_ctsm_indexes.txt)"

if [ "$sedresult" == " " ]; then
 echo "Error! Station out of domain"
else
 station_id="${sedresult%%,*}"
 ctsm_id="${sedresult##*, }"
 #echo $station_id
 #echo $ctsm_id

 python $cegio/evaluation/trumpet/trumpet_curves.py $station_id $ctsm_id $search
fi
