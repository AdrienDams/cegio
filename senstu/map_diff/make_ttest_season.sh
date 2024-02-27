#!/bin/sh

export run_name_a="57_DOM02_051" 
export run_name_b="57_DOM02_001" # control run
input_dir_a=$senstu/data/$run_name_a/monthly
input_dir_b=$senstu/data/$run_name_b/monthly
remap_dir_a=$senstu/data/$run_name_a/climatology/remap
remap_dir_b=$senstu/data/$run_name_b/climatology/remap
output_dir=$scratch_dir/ttest

export variable="TSOI"
export levelname="levgrnd"
export depth=9

season="SON"

# Calculate yearly mean
for year in {1980..2021}; do
	echo $year
	ncea -O -F -d $levelname,$depth -v $variable $input_dir_a/$run_name_a.clm2.h0.$year-{09,10,11}.nc $output_dir/$run_name_a.$year.nc
	ncea -O -F -d $levelname,$depth -v $variable $input_dir_b/$run_name_b.clm2.h0.$year-{09,10,11}.nc $output_dir/$run_name_b.$year.nc
done

# Calculate variance
cdo -r -O ensvar $output_dir/$run_name_a.????.nc $output_dir/$run_name_a.$variable.$season.var.nc
cdo -r -O ensvar $output_dir/$run_name_b.????.nc $output_dir/$run_name_b.$variable.$season.var.nc

# Regrid model
cdo -r setgrid,$descriptiongrid -selvar,$variable $output_dir/$run_name_a.$variable.$season.var.nc $output_dir/grid.$run_name_a.$variable.$season.var.nc
cdo -r setgrid,$descriptiongrid -selvar,$variable $output_dir/$run_name_b.$variable.$season.var.nc $output_dir/grid.$run_name_b.$variable.$season.var.nc
# Remap model
cdo -r remapnn,$descriptionreg -selvar,$variable $output_dir/grid.$run_name_a.$variable.$season.var.nc $output_dir/remap.$run_name_a.$variable.$season.var.nc
cdo -r remapnn,$descriptionreg -selvar,$variable $output_dir/grid.$run_name_b.$variable.$season.var.nc $output_dir/remap.$run_name_b.$variable.$season.var.nc
# Crop model (not latitude above 90)
ncks -O -F -d lat,0.,90. $output_dir/remap.$run_name_a.$variable.$season.var.nc $output_dir/crop.$run_name_a.$variable.$season.var.nc
ncks -O -F -d lat,0.,90. $output_dir/remap.$run_name_b.$variable.$season.var.nc $output_dir/crop.$run_name_b.$variable.$season.var.nc

mean_a=$remap_dir_a/remap.$run_name_a.TSOI.$season.nc
mean_b=$remap_dir_b/remap.$run_name_b.TSOI.$season.nc

var_a=$output_dir/crop.$run_name_a.$variable.$season.var.nc
var_b=$output_dir/crop.$run_name_b.$variable.$season.var.nc

s_p=$output_dir/remap.TSOI.$season.sp.nc

t=$output_dir/remap.TSOI.$season.t.nc

# 6.41 is sqrt of 42, 0.71 is 1/sqrt of 2
cdo mulc,6.41 -mulc,0.71 -sqrt -add $var_a $var_b $s_p

cdo divc,0.22 -div -sub $mean_a $mean_b $s_p $t

cdo studentt,82 -selvar,$variable $t $output_dir/remap.TSOI.$season.studentt.nc

