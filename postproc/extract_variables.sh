#!/bin/bash

## ~~~~~~~~~~~~~~~~~~~~~~~~~ start user input ~~~~~~~~~~~~~~~~~~~~~~~~~
#SBATCH --partition=compute  # Specify partition name
#SBATCH --ntasks=1           # Specify max. number of tasks to be invoked
#SBATCH --time=08:00:00      # Set a limit on the total run time
#SBATCH --account=aa0049     # Charge resources on this project account
## ~~~~~~~~~~~~~~~~~~~~~~~~~ end user input ~~~~~~~~~~~~~~~~~~~~~~~~~

source_folder=$cegio/data/$run_name
daily_folder=$source_folder/daily
variables="SNOW_DEPTH,TSOI,TSA,SOILICE,SOILLIQ,H2OSNO,H2OSOI,FH2OSFC,FPSN,FSDS,FSA,FSH,FSNO,FSR,SNOW_PERSISTENCE,TLAI,lat,lon"
d=$startyear-01-01 #start date
nextyear=$(( $endyear + 1 ))
enddate=$nextyear-01-01

while [ "$d" != $enddate ]; do
 echo $d
 
 # extraction
 ncks -O -v $variables ${source_folder}/${run_name}.clm2.h0.$d-00000.nc $daily_folder/${run_name}.clm2.h0.$d.ext.nc

 # incremenet date
 d=$(date -I -d "$d + 1 day")
done
