#!/bin/sh
# (from A. Damseaux)

#SBATCH --partition=compute
#SBATCH --ntasks=1  
#SBATCH --time=08:00:00
#SBATCH --account=aa0049

# create new netCDF for the run
cp -p $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_area.nc $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_area_$run_name.nc
cp -p $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station.nc $cegio/data/stations/orig_data/AllArctic_SoilTemperature_monthly_native_quality_1979-2019_station_$run_name.nc

for year in {$startyear..$endyear}; do
 echo $year
 for month in {1..9}; do
  echo $month

  infile=$cegio/data/$run_name/monthly/$run_name.clm2.h0.$year-0$month.nc
  python ctsm_vs_stations.py $infile
  python splines_years.py $infile

 done
 for month in {10..12}; do
  echo $month

  infile=$cegio/data/$run_name/monthly/$run_name.clm2.h0.$year-$month.nc
  python ctsm_vs_stations.py $infile
  python splines_years.py $infile

 done
done



 
