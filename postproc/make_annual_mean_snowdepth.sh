#!/bin/sh
# (from H. Matthes, modified for irregular grid by A. Damseaux)

outdir=${targetdir}"/processed/permafrost"
datadir=${datadir}"/daily"

cd ${outdir}

year=$startyear

while [ $year -le $endyear ]; do
 echo $year 

 ncea -v H2OSNO ${datadir}/${run_prefix}.${year}-??-??.ext.nc -O ${outdir}/${run_name}.annual_mean_snow_water_equivalent.${year}.nc
 ncea -v SNOW_DEPTH ${datadir}/${run_prefix}.${year}-??-??.ext.nc -O ${outdir}/${run_name}.annual_mean_snow_depth.${year}.nc 
  
 year=$(( $year + 1 ))

done

ncrcat ${outdir}/${run_prefix}.annual_mean_snow_water_equivalent.????.nc -O ${outdir}/${run_name}.annual_mean_snow_water_equivalent.${startyear}-${endyear}.nc
ncrcat ${outdir}/${run_prefix}.annual_mean_snow_depth.????.nc -O ${outdir}/${run_name}.annual_mean_snow_depth.${startyear}-${endyear}.nc
