#!/bin/sh
# (from A. Damseaux)

#SBATCH --partition=compute
#SBATCH --ntasks=1  
#SBATCH --time=08:00:00
#SBATCH --account=aa0049

folder=$cegio/evaluation/stations
data_folder=$cegio/data/stations/orig_data

# create stations_ctsm_indexes.txt
python $folder/find_closest.py

# create new netCDF for the run
output_tmp="$data_folder/stations-vs-ctsm.1979-2019.tmp.$run_name.nc"
output_pcm="$data_folder/stations-vs-ctsm.1979-2019.pcm.$run_name.nc"
rm -f $data_folder/$output_tmp
rm -f $data_folder/$output_pcm
cp $data_folder/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station.nc $output_tmp
cp $data_folder/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_area.nc $output_pcm

for year in $( seq $startyear $endyear ) ; do
 export year
 echo $year
 for month in {1..9}; do
  export month
  echo $month

  infile=$cegio/data/$run_name/monthly/$run_name.clm2.h0.$year-0$month.nc
  python $folder/ctsm_vs_stations.py $infile $output_tmp
  python $folder/splines_years.py $infile $output_pcm

 done
 for month in {10..12}; do
  export month
  echo $month

  infile=$cegio/data/$run_name/monthly/$run_name.clm2.h0.$year-$month.nc
  python $folder/ctsm_vs_stations.py $infile $output_tmp
  python $folder/splines_years.py $infile $output_pcm

 done
done



 
