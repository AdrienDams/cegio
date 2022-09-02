#!/bin/sh
# (from H. Matthes, modified for irregular grid by A. Damseaux)
# produce season output

wrkdir=${targetdir}"/processed/season"
datadir=${datadir}"/monthly"

cd ${wrkdir}

rm -f ${run_name}.${year}.spring.nc ${run_name}.${year}.summer.nc ${run_name}.${year}.autumn.nc ${run_name}.${year}.winter.nc

year=$startyear

while [ $year -le $endyear ]; do
 echo $year
 preyear=$(( $year -1 )) # variable to take previous year

 cdo -O ensavg ${datadir}/${run_prefix}.${year}-03.nc ${datadir}/${run_prefix}.${year}-04.nc ${datadir}/${run_prefix}.${year}-05.nc ${run_name}.${year}.spring.nc
 cdo -O ensavg ${datadir}/${run_prefix}.${year}-06.nc ${datadir}/${run_prefix}.${year}-07.nc ${datadir}/${run_prefix}.${year}-08.nc ${run_name}.${year}.summer.nc
 cdo -O ensavg ${datadir}/${run_prefix}.${year}-09.nc ${datadir}/${run_prefix}.${year}-10.nc ${datadir}/${run_prefix}.${year}-11.nc ${run_name}.${year}.autumn.nc
 if [ $year -eq $firstyear ]; then # can't take previous here of the first year
  cdo -O ensavg ${datadir}/${run_prefix}.${year}-01.nc ${datadir}/${run_prefix}.${year}-02.nc ${run_name}.${year}.winter.nc
 else
  cdo -O ensavg ${datadir}/${run_prefix}.${year}-01.nc ${datadir}/${run_prefix}.${year}-02.nc ${datadir}/${run_prefix}.${preyear}-12.nc ${run_name}.${year}.winter.nc
 fi

 year=$(( $year + 1 ))

done

ncecat ${run_name}.????.spring.nc -O ${run_name}.${startyear}-${endyear}.spring.nc
ncecat ${run_name}.????.summer.nc -O ${run_name}.${startyear}-${endyear}.summer.nc
ncecat ${run_name}.????.autumn.nc -O ${run_name}.${startyear}-${endyear}.autumn.nc
ncecat ${run_name}.????.winter.nc -O ${run_name}.${startyear}-${endyear}.winter.nc

ncrcat ${run_name}.????.spring.nc -O ${run_name}.${startyear}-${endyear}.spring.nc1
ncrcat ${run_name}.????.summer.nc -O ${run_name}.${startyear}-${endyear}.summer.nc1
ncrcat ${run_name}.????.autumn.nc -O ${run_name}.${startyear}-${endyear}.autumn.nc1
ncrcat ${run_name}.????.winter.nc -O ${run_name}.${startyear}-${endyear}.winter.nc1
