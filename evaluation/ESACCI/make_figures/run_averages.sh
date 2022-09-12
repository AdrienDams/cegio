#!/bin/sh
# (from A. Damseaux)

#SBATCH --partition=shared
#SBATCH --ntasks=1  
#SBATCH --time=48:00:00
#SBATCH --account=aa0049

folder=$cegio/evaluation/ESACCI/make_figures
data_folder=$cegio/data/ESACCI/$run_name
declare -a depthlist=("1m" "2m" "5m" "10m")
export startyear_esa=1997
export endyear_esa=2019

## Soiltemp 
# loop over depth
# only take 1m because no significant difference between temperature depth compare to spread of location
for i in {0..0}; do
 depth=${depthlist[i]}
 echo $depth

 # loop over month
 for year in $( seq $startyear_esa $endyear_esa ) ; do
  input_ctsm=$data_folder/CTSM_regridded/TSOI.$depth.$run_name.$year.nc
  input_esa=$data_folder/ESACCI_regridded/TSOI.$depth.$run_name.$year.nc

  python $folder/averages_map_soiltemp.py $input_ctsm $input_esa $year.$depth
 done

 # period average
 input_ctsm_period=$data_folder/CTSM_regridded/TSOI.$depth.$run_name.period.nc
 input_esa_period=$data_folder/ESACCI_regridded/TSOI.$depth.$run_name.period.nc

 ncea -O $data_folder/CTSM_regridded/TSOI.$depth.$run_name.????.nc -O $input_ctsm_period
 ncea -O $data_folder/ESACCI_regridded/TSOI.$depth.$run_name.????.nc -O $input_esa_period

 python $folder/averages_map_soiltemp.py $input_ctsm_period $input_esa_period $depth

done
echo "TSOI done"

## ALT
# loop over month
for year in $( seq $startyear_esa $endyear_esa ) ; do
 input_ctsm=$data_folder/CTSM_regridded/ALT.$run_name.$year.nc
 input_esa=$data_folder/ESACCI_regridded/ALT.$run_name.$year.nc

 python $folder/averages_map_alt.py $input_ctsm $input_esa $year
done

# period average
input_ctsm_period=$data_folder/CTSM_regridded/ALT.$run_name.period.nc
input_esa_period=$data_folder/ESACCI_regridded/ALT.$run_name.period.nc

ncea -O $data_folder/CTSM_regridded/ALT.$run_name.????.nc -O $input_ctsm_period
ncea -O $data_folder/ESACCI_regridded/ALT.$run_name.????.nc -O $input_esa_period

python $folder/averages_map_alt.py $input_ctsm_period $input_esa_period period

echo "ALT done"

## PFR
# loop over month
for year in $( seq $startyear_esa $endyear_esa ) ; do
 input_ctsm=$data_folder/CTSM_regridded/PFR.$run_name.$year.nc
 input_esa=$data_folder/ESACCI_regridded/PFR.$run_name.$year.nc

 python $folder/averages_map_pfr.py $input_ctsm $input_esa $year
done

# period average
input_ctsm_period=$data_folder/CTSM_regridded/PFR.$run_name.period.nc
input_esa_period=$data_folder/ESACCI_regridded/PFR.$run_name.period.nc

ncea -O $data_folder/CTSM_regridded/PFR.$run_name.????.nc -O $input_ctsm_period
ncea -O $data_folder/ESACCI_regridded/PFR.$run_name.????.nc -O $input_esa_period

python $folder/averages_map_pfr.py $input_ctsm_period $input_esa_period period

echo "PFR done"
 
