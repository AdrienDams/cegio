#!/bin/bash

outdir=${targetdir}"/processed/permafrost"
datadir=${datadir}"/daily"

cd ${outdir}

# make annual ground temperature

postendyear=$(( $endyear + 1 )) # take the next year of the last year
d=${startyear}-01-01 		# start date 
enddate=${postendyear}-01-01

while [ "$d" != $enddate ]; do
 
 # extract soil temp    
 ncks -v TSOI ${datadir}/${run_prefix}.${d}.ext.nc -O ${outdir}/${run_name}.${d}.soiltemp_ext.nc

 # annual average
 if [ ${d:5:10} == "12-31" ] ; then # if last date of the year
  ncea -A ${outdir}/${run_name}.${d:0:4}-??-??.soiltemp_ext.nc -o ${outdir}/${run_name}.${d:0:4}.magt.nc

  # remove all files after year average
  if [ -f ${outdir}/${run_name}.${d:0:4}.magt.nc ] ; then
   rm -f ${outdir}/${run_name}.${d:0:4}-??-??.soiltemp_ext.nc
  fi

  echo ${d:0:4}" year done"
 fi

 # incremenet date
 d=$(date -I -d "$d + 1 day")
 if [ ${d:5:10} == "02-29" ]; then # this day is not compute by CTSM
  d=$(date -I -d "$d + 1 day")
 fi
done 

# concatenate every years
ncrcat ${outdir}/${run_name}.????.magt.nc -O ${outdir}/${run_name}.${startyear}-${endyear}.magt.nc

# select all top layers
cdo selindexbox,1,240860,1,20 ${outdir}/${run_name}.${startyear}-${endyear}.magt.nc ${outdir}/${run_name}.${startyear}-${endyear}.magt.shallow.nc

# station file
datadir=${cegio}"/data/stations/orig_data"

cdo seldate,1979-07-01,2020-06-30 ${datadir}/arctic_stations.soiltemp.daily.1979-2020.nc ${datadir}/arctic_stations.soiltemp.july_start.nc
cdo yearmean ${datadir}/arctic_stations.soiltemp.july_start.nc ${datadir}/arctic_stations.soiltemp.yearly.mean.nc
cdo yearmax ${datadir}/arctic_stations.soiltemp.july_start.nc ${datadir}/arctic_stations.soiltemp.yearly.max.nc
cdo yearmin ${datadir}/arctic_stations.soiltemp.july_start.nc ${datadir}/arctic_stations.soiltemp.yearly.min.nc
