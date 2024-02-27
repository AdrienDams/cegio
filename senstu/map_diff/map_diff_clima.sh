#!/bin/bash

# What user need to change
export run_name_a="57_DOM02_051" 
export run_name_b="57_DOM02_001" # control run
#(need to change period on make_climatology.sh line 18, 24, 28, 33)
export variable="TSOI"

export dimension="3D"
export levelname="levgrnd" # levsoi or levgrnd
export depth_a=9
export depth_b=9
export depthavg="no" # yes or no
export sum="no" # yes or no
export topdepth_a=1 # if depthavg is yes
export topdepth_b=1 # if depthavg is yes

# 1m-column soil liquid + ice water difference in kg/m2
# snow depth difference in m soil temperature difference at 1m (in °C) Temperature at 2m (in °C)
# 1m-column volumetric soil water difference (in mm3/mm3)
# soil temperature difference at 1m (in °C)
# snow cover fraction difference (in %)
# snow water equivalent difference (in mm)
export legendtitle="soil temperature difference at 1m (in °C)" 

echo "Make climatology averages"
export run_name=$run_name_a
export depth=$depth_a
export topdepth=$topdepth_a
#$senstu/map_diff/make_climatology.sh
export run_name=$run_name_b
export depth=$depth_b
export topdepth=$topdepth_b
#$senstu/map_diff/make_climatology.sh

echo "Map climatology monthly averages"
for i in {01..12}; do
	export month=$i
	echo $month

	file_a=$senstu/data/$run_name_a/climatology/remap/remap.$run_name_a.$variable.$month.nc
	file_b=$senstu/data/$run_name_b/climatology/remap/remap.$run_name_b.$variable.$month.nc

	#python $senstu/map_diff/map_diff.py $file_a $file_b
done

echo "Map climatology season averages"
for season in DJF MAM JJA SON; do
	export month=$season
	echo $season
	
	file_a=$senstu/data/$run_name_a/climatology/remap/remap.$run_name_a.$variable.$season.nc
	file_b=$senstu/data/$run_name_b/climatology/remap/remap.$run_name_b.$variable.$season.nc
	
	# Calculate map difference
	python $senstu/map_diff/map_diff.py $file_a $file_b
done

echo "Map climatology year average"
export month="period"

file_a=$senstu/data/$run_name_a/climatology/remap/remap.$run_name_a.$variable.period.nc
file_b=$senstu/data/$run_name_b/climatology/remap/remap.$run_name_b.$variable.period.nc

# Calculate map difference
#python $senstu/map_diff/map_diff.py $file_a $file_b
