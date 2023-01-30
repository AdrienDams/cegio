#!/bin/bash
# Batch system directives
#SBATCH  --nodes=1
#SBATCH  --account=aa0049           
#SBATCH  --partition=shared 
#SBATCH  --time=48:00:00

directory=$cegio/data/$run_name

mkdir -p $directory/monthly

for year in $( seq $startyear $endyear ) ; do
 echo "year $year"
 for i in {1..9}; do
  ncea $directory/daily/${run_name}.clm2.h0.${year}-0${i}-??.ext.nc -O $directory/monthly/${run_name}.clm2.h0.${year}-0${i}.nc
 done
 for i in {10..12}; do
  ncea $directory/daily/${run_name}.clm2.h0.${year}-${i}-??.ext.nc -O $directory/monthly/${run_name}.clm2.h0.${year}-${i}.nc
 done
done
