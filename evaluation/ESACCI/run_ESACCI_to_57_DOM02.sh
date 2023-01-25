#!/bin/bash

# Bash file to regrid (1) a nc and (2) a 57_DOM02 to a same regular lat lon grid

export modeloutput_dir="$cegio/data/ESACCI/$run_name/CTSM_regridded"
export obsoutput_dir="$cegio/data/ESACCI/$run_name/ESACCI_regridded"
export scratch_ESA="$scratch_dir/ESACCI"
mkdir -p $modeloutput_dir
mkdir -p $obsoutput_dir
mkdir -p $scratch_ESA
mkdir -p $scratch_ESA/tmp

## Compute years
startyear_esa=1997
endyear_esa=2019
if [ $startyear -gt $startyear_esa ]
then
    startyear_esa=$startyear
fi
if [ $endyear -lt $endyear_esa ]
then
    endyear_esa=$endyear
fi
export startyear_esa
export endyear_esa

sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.ALT.sh
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.PFR.sh

export depth=1m
export toplayer=8
export botlayer=9
export inttop=0.23
export intbot=0.77
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.GT.sh
export depth=5m
export toplayer=16
export botlayer=17
export inttop=0.08
export intbot=0.92
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.GT.sh
export depth=10m
export toplayer=21
export botlayer=22
export inttop=0.96
export intbot=0.04
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.GT.sh
