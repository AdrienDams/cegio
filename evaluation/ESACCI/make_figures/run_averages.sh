#!/bin/sh
#SBATCH --partition=shared
#SBATCH --ntasks=1  
#SBATCH --time=48:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=10G

folder=$cegio/evaluation/ESACCI/make_figures
data_folder=$cegio/data/ESACCI/$run_name
declare -a depthlist=("1m" "5m" "10m") # ("1m" "2m" "5m" "10m")

## Soiltemp 
# loop over depth
for i in {0..2}; do
 depth=${depthlist[i]}
 echo $depth

 # period average
 input_ctsm=$data_folder/CTSM_regridded/$run_name.TSOI.$depth.period.nc
 input_esa=$data_folder/ESACCI_regridded/$run_name.TSOI.$depth.period.nc

 python $folder/averages_map_soiltemp.py $input_ctsm $input_esa $depth

done
echo "TSOI done"

## ALT

# period average
input_ctsm=$data_folder/CTSM_regridded/$run_name.ALT.period.nc
input_esa=$data_folder/ESACCI_regridded/$run_name.ALT.period.nc

python $folder/averages_map_alt.py $input_ctsm $input_esa period

echo "ALT done"

## PFR

# period average
input_ctsm=$data_folder/CTSM_regridded/$run_name.PFR.period.nc
input_esa=$data_folder/ESACCI_regridded/$run_name.PFR.period.nc

input_ctsm_orig=$cegio/data/postproc/$run_name/processed/permafrost/$run_name.PFR.time_average.nc
input_esa_orig=$cegio/data/ESACCI/orig_data/ESACCI.PFR.$run_name.period.nc

python $folder/averages_map_pfr.py $input_ctsm $input_esa period $input_ctsm_orig $input_esa_orig

echo "PFR done"
 
