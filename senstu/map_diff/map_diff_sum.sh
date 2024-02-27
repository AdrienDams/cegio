#!/bin/bash

export run_name_a="57_DOM02_005" # default run
export run_name_b="57_DOM02_001"

echo "Map climatology monthly averages"
for i in {01..12}; do
	export month=$i
	echo $month

	python $senstu/map_diff/map_diff_sum.py
done

echo "Map climatology season averages"
for season in DJF MAM JJA SON; do
	export month=$season
	echo $season
	
	python $senstu/map_diff/map_diff_sum.py
done

echo "Map climatology year average"
export month="period"

# Calculate map difference
python $senstu/map_diff/map_diff_sum.py
