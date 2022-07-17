#!/bin/sh
# (from A. Damseaux)

#SBATCH --partition=compute
#SBATCH --ntasks=1  
#SBATCH --time=08:00:00
#SBATCH --account=aa0049

folder=$cegio/evaluation/stations

# create stations_ctsm_indexes.txt
python $folder/find_closest.py

# create new netCDF for the run
rm $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_area_$run_name.nc
rm $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_$run_name.nc
cp $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_area.nc $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_area_$run_name.nc
cp $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station.nc $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_$run_name.nc

for year in $( seq $startyear $endyear ) ; do
 export year
 echo $year
 for month in {1..9}; do
  export month
  echo $month

  infile=$cegio/data/$run_name/monthly/$run_name.clm2.h0.$year-0$month.nc
  python $folder/ctsm_vs_stations.py $infile
  python $folder/splines_years.py $infile

 done
 for month in {10..12}; do
  export month
  echo $month

  infile=$cegio/data/$run_name/monthly/$run_name.clm2.h0.$year-$month.nc
  python $folder/ctsm_vs_stations.py $infile
  python $folder/splines_years.py $infile

 done
done



 
