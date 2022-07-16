#!/bin/bash

casenum=57_DOM02_004

daily_folder=/work/aa0049/a271098/archive/${casenum}/lnd/hist/daily
scratch_folder=/scratch/a/a271098/CTSM_scratch/${casenum}
d=1980-01-01 # start date (change test job name)
enddate=2020-01-01

while [ "$d" != $enddate ]; do
 if test -f "$daily_folder/${casenum}.clm2.h0.$d.ext.nc"; then # if file exists
  d=$(date -I -d "$d + 1 day")  # incremenet date
 else
  echo $d
  if test -f "$scratch_folder/${casenum}.clm2.h0.$d-00000.nc"; then # if file exists
   echo "File here"
  fi
  d=$(date -I -d "$d + 1 day")  # incremenet date
 fi

done
