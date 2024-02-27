#!/bin/bash

# What user need to change
export run_name_a="57_DOM02_051"
export run_name_b="57_DOM02_001" # control run

export month="period"
export variable="ALT"

export legendtitle="ALT difference in m" 

file_a=$cegio/data/ESACCI/$run_name_a/CTSM_regridded/$run_name_a.ALT.period.nc
file_b=$cegio/data/ESACCI/$run_name_b/CTSM_regridded/$run_name_b.ALT.period.nc

python $senstu/map_diff/map_diff.py $file_a $file_b
