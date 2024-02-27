#!/bin/bash

# Define input directories and output directory
input_dir=$senstu/data/$run_name/monthly
output_dir=$senstu/data/$run_name/climatology

mkdir -p $output_dir
mkdir -p $output_dir/remap

echo $run_name

# Loop through months and calculate period average
for month in {01..12}; do
	echo $month

	# Make climatology averages and extract variable
	if [ "$dimension" = "2D" ]; then
		ncea -O -v $variable $input_dir/*.{1980..2021}-$month.nc $output_dir/$run_name.$variable.$month.nc
	fi
	# Select variable for 3D
	if [ "$dimension" = "3D" ]; then
		if [ "$depthavg" = "yes" ]; then
		    if [ "$sum" = "yes" ]; then
 		    	ncea -O -F -v $variable $input_dir/*.{1980..2021}-$month.nc $output_dir/$run_name.$variable.$month.tmp.nc
				ncks -O -F -d $levelname,$topdepth,$depth $output_dir/$run_name.$variable.$month.tmp.nc $output_dir/$run_name.$variable.$month.depthtmp.nc
        		ncwa -O -F -a $levelname -v $variable -y sum $output_dir/$run_name.$variable.$month.depthtmp.nc $output_dir/$run_name.$variable.$month.nc
   			else
     			ncea -O -F -v $variable $input_dir/*.{1980..2021}-$month.nc $output_dir/$run_name.$variable.$month.tmp.nc
       			ncwa -O -F -a $levelname -d $levelname,$topdepth,$depth -v $variable $output_dir/$run_name.$variable.$month.tmp.nc $output_dir/$run_name.$variable.$month.nc
    		fi
		fi
		if [ "$depthavg" = "no" ]; then
			ncea -O -F -d $levelname,$depth -v $variable $input_dir/*.{1980..2021}-$month.nc $output_dir/$run_name.$variable.$month.nc
		fi
	fi
	
	# Regrid model
	cdo -r setgrid,$descriptiongrid -selvar,$variable $output_dir/$run_name.$variable.$month.nc $output_dir/remap/grid.$run_name.$variable.$month.tmp.nc
	# Remap model
	cdo -r remapnn,$descriptionreg -selvar,$variable $output_dir/remap/grid.$run_name.$variable.$month.tmp.nc $output_dir/remap/remap.$run_name.$variable.$month.tmp.nc
	# Crop model (not latitude above 90)
	ncks -O -F -d lat,0.,90. $output_dir/remap/remap.$run_name.$variable.$month.tmp.nc $output_dir/remap/remap.$run_name.$variable.$month.nc

	# Remove temporay files
	rm -f $output_dir/*tmp.nc
	rm -f $output_dir/remap/*tmp.nc
done

# Make seasons averages
echo "DJF"
ncea -O $output_dir/remap/remap.$run_name.$variable.12.nc $output_dir/remap/remap.$run_name.$variable.01.nc $output_dir/remap/remap.$run_name.$variable.02.nc $output_dir/remap/remap.$run_name.$variable.DJF.nc
echo "MAM"
ncea -O $output_dir/remap/remap.$run_name.$variable.03.nc $output_dir/remap/remap.$run_name.$variable.04.nc $output_dir/remap/remap.$run_name.$variable.05.nc $output_dir/remap/remap.$run_name.$variable.MAM.nc
echo "JJA"
ncea -O $output_dir/remap/remap.$run_name.$variable.06.nc $output_dir/remap/remap.$run_name.$variable.07.nc $output_dir/remap/remap.$run_name.$variable.08.nc $output_dir/remap/remap.$run_name.$variable.JJA.nc
echo "SOM"
ncea -O $output_dir/remap/remap.$run_name.$variable.09.nc $output_dir/remap/remap.$run_name.$variable.10.nc $output_dir/remap/remap.$run_name.$variable.11.nc $output_dir/remap/remap.$run_name.$variable.SON.nc

# Make year average
echo "year average"
ncea -O $output_dir/remap/remap.$run_name.$variable.??.nc $output_dir/remap/remap.$run_name.$variable.period.nc
