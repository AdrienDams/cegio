#!/bin/bash

## ~~~~~~~~~~~~~~~~~~~~~~~~~ start user input ~~~~~~~~~~~~~~~~~~~~~~~~~

#SBATCH --job-name=slk_job   # Specify job name
#SBATCH --output=slk_job.o%j # name for standard output log file
#SBATCH --error=slk_job.e%j  # name for standard error output log file
#SBATCH --partition=compute  # Specify partition name
#SBATCH --ntasks=1           # Specify max. number of tasks to be invoked
#SBATCH --time=08:00:00      # Set a limit on the total run time
#SBATCH --account=aa0049     # Charge resources on this project account
#SBATCH --mem=6GB
## ~~~~~~~~~~~~~~~~~~~~~~~~~ end user input ~~~~~~~~~~~~~~~~~~~~~~~~~

casenum=57_DOM02_032
source_folder=/work/aa0049/a271098/archive/${casenum}/lnd/hist
daily_folder=/work/aa0049/a271098/archive/${casenum}/lnd/hist/daily
target_namespace=/arch/aa0049/$USER/CTSM/${casenum}/lnd/hist/daily
variables="SNOW_DEPTH,TSOI,TSA,SOILICE,SOILLIQ,H2OSNO,H2OSOI,FH2OSFC,FPSN,FSDS,FSA,FSH,FSNO,FSR,SNOW_PERSISTENCE,TLAI,lat,lon"
d=2000-01-01 #start date (change test job name)
enddate=2002-01-01

while [ "$d" != $enddate ]; do
 echo $d
 
 # extraction
 ncks -O -v $variables ${source_folder}/${casenum}.clm2.h0.$d-00000.nc $daily_folder/${casenum}.clm2.h0.$d.ext.nc

 # archiving and removing
 if test -f "$daily_folder/${casenum}.clm2.h0.$d.ext.nc"; then # if last day is done
  echo "doing 'slk archive -R ${source_folder}/${casenum}.clm2.h0.$d-00000.nc ${target_namespace}'"
  slk archive -R ${source_folder}/${casenum}.clm2.h0.$d-00000.nc ${target_namespace}

  # '$?' captures the exit code of the previous command
  if [ $? -ne 0 ]; then
   echo "an error occurred in slk archive call"
  else
   echo "archival successful"
   rm ${source_folder}/${casenum}.clm2.h0.$d-00000.nc
  fi
 fi

 # incremenet date
 d=$(date -I -d "$d + 1 day")
done

# slk list ${target_namespace} | cat
