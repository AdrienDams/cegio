#!/bin/sh

#SBATCH --partition=shared
#SBATCH --ntasks=1  
#SBATCH --time=08:00:00
#SBATCH --account=aa0049

folder=$cegio/evaluation/stations
data_folder=$cegio/data/stations
mkdir -p $data_folder/$run_name

# create stations_ctsm_indexes.txt
python $folder/find_closest.py

# create new netCDF for the run
output_tmp="stations-vs-ctsm.1979-2020.tmp.$run_name.nc"
output_pcm="stations-vs-ctsm.1979-2020.pcm.$run_name.nc"
rm -f $data_folder/$run_name/$output_tmp
rm -f $data_folder/$run_name/$output_pcm
cp $data_folder/orig_data/arctic_stations.soiltemp.monthly.1979-2020.tmp.nc $data_folder/$run_name/$output_tmp
cp $data_folder/orig_data/arctic_stations.soiltemp.monthly.1979-2020.pcm.nc $data_folder/$run_name/$output_pcm

if [ $endyear -gt 2020 ]; then
 endyear=2020
fi

for year in $( seq $startyear $endyear ) ; do
 export year
 echo $year
 for month in {1..9}; do
  export month
  echo $month

  infile=$cegio/data/$run_name/monthly/$run_name.clm2.h0.$year-0$month.nc
  python $folder/ctsm_vs_stations.py $infile $data_folder/$run_name/$output_tmp
  python $folder/splines_years.py $infile $data_folder/$run_name/$output_pcm

 done
 for month in {10..12}; do
  export month
  echo $month

  infile=$cegio/data/$run_name/monthly/$run_name.clm2.h0.$year-$month.nc
  python $folder/ctsm_vs_stations.py $infile $data_folder/$run_name/$output_tmp
  python $folder/splines_years.py $infile $data_folder/$run_name/$output_pcm

 done
done
