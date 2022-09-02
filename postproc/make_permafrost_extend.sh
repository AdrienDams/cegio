#!/bin/bash
# (from H. Matthes, modified for irregular grid by A. Damseaux)
# calculate minimum and maximum ground t
# compute permafrost

outdir=${targetdir}"/processed/permafrost"
datadir=${datadir}"/daily"

cd ${outdir}

postendyear=$(( $endyear + 1 )) # take the next year of the last year
d=${startyear}-01-01 		# start date 
enddate=${postendyear}-01-01

while [ "$d" != $enddate ]; do
 year=${d:0:4}

 # extract soil temperature
 ncks -v TSOI ${datadir}/${run_prefix}.${d}.ext.nc -O ${outdir}/${run_name}.${d}.soiltemp_ext.nc

 if [ ${d:5:10} == "12-31" ] ; then # if last date of the year
  echo "average year" $year
  # year average
  ncrcat ${outdir}/${run_name}.$year-*-*.soiltemp_ext.nc -O ${outdir}/${run_name}.$year.perma.nc

  # maximum and minimum over the time (one time value)
  cdo -O timselmax,365 ${outdir}/${run_name}.$year.perma.nc ${outdir}/${run_name}.$year.perma.timemax.nc
  cdo -O timselmin,365 ${outdir}/${run_name}.$year.perma.nc ${outdir}/${run_name}.$year.perma.timemin.nc

  # extract top layers (no bedrock)
  cdo selindexbox,1,240860,1,20 ${outdir}/${run_name}.$year.perma.timemax.nc ${outdir}/${run_name}.$year.perma.timemax.shallow.nc
  
  rm -f ${outdir}/${run_name}.$year-*-*.soiltemp_ext.nc
  rm -f ${outdir}/${run_name}.$year.perma.nc

  # calculate the vertmin of the maximum temp (minimum or maximum through all layers)
  cdo -O vertmin ${outdir}/${run_name}.$year.perma.timemax.nc ${outdir}/${run_name}.$year.perma.vertmin.nc
  cdo -O vertmin ${outdir}/${run_name}.$year.perma.timemax.shallow.nc ${outdir}/${run_name}.$year.perma.vertmin.shallow.nc
  
  # compute permafrost extent
  if [[ $year -gt ${startyear} ]]; then # don't take first year into consideration because permafrost is 2 years consecutive
    preyear=$(( $year - 1 )) # take previous year
    # concatenated two previous years
    ncrcat ${outdir}/${run_name}.$preyear.perma.vertmin.nc ${outdir}/${run_name}.$year.perma.vertmin.nc -O dummy.${year}.nc
    # add two previous years shallow
    ncrcat ${outdir}/${run_name}.$preyear.perma.vertmin.shallow.nc ${outdir}/${run_name}.$year.perma.vertmin.shallow.nc -O dummy.${year}.shallow.nc
    # take only the maximum of two previous year (if maximum is negative = permafrost)
    cdo -O timselmax,2 dummy.${year}.nc ${outdir}/${run_name}.permafrost_extend.${year}.nc
    cdo -O timselmax,2 dummy.${year}.shallow.nc ${outdir}/${run_name}.permafrost_extend.${year}.shallow.nc
    rm dummy.${year}.nc
    rm dummy.${year}.shallow.nc
  fi
 fi 
 d=$(date -I -d "$d + 1 day") # increment day
 if [ ${d:5:10} == "02-29" ]; then # this day is not compute by CTSM
  d=$(date -I -d "$d + 1 day")
 fi
done

# concatenate every year
ncrcat ${outdir}/${run_name}.*.perma.timemax.nc -O ${outdir}/${run_name}.maxAGT.${startyear}-${endyear}.nc
ncrcat ${outdir}/${run_name}.*.perma.timemin.nc -O ${outdir}/${run_name}.minAGT.${startyear}-${endyear}.nc
nextyear=$(( ${startyear} + 1 ))
ncrcat ${outdir}/${run_name}.permafrost_extend.*.nc -O ${outdir}/${run_name}.permafrost_extend.${nextyear}-${end_year}.nc
ncrcat ${outdir}/${run_name}.permafrost_extend.*.shallow.nc -O ${outdir}/${run_name}.permafrost_extend.${nextyear}-${end_year}.shallow.nc
