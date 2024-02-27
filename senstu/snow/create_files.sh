#!/bin/sh

# need to run /work/aa0049/a271098/cegio/postproc/create_winter.sh before

modelinput_dir=$cegio/data/$run_name/monthly
modeloutput_dir=$cegio/data/$run_name/monthly/snow_depth/
variable=SNOW_DEPTH

mkdir -p $modeloutput_dir

for i in {01..12}; do
	echo $i
	# Extract data
	ncea -O -v $variable $modelinput_dir/$run_name.clm2.h0.*-$i.nc $modeloutput_dir/$variable.$i.nc
	# Regrid model
	cdo -r setgrid,$descriptiongrid -selvar,$variable $modeloutput_dir/$variable.$i.nc $modeloutput_dir/grid.$variable.tmp.$i.nc
	# Remap model
	cdo -r remapnn,$descriptionreg -selvar,$variable $modeloutput_dir/grid.$variable.tmp.$i.nc $modeloutput_dir/remap.$variable.tmp.$i.nc
	# Crop model (not latitude above 90)
	ncks -O -F -d lat,0.,90. $modeloutput_dir/remap.$variable.tmp.$i.nc $modeloutput_dir/$variable.remap.period.$i.nc
done

# winter
variable=TSA
# Regrid model
cdo -r setgrid,$descriptiongrid -selvar,$variable $modelinput_dir/winter_avg.nc $modelinput_dir/grid.$variable.tmp.nc
# Remap model
cdo -r remapnn,$descriptionreg -selvar,$variable $modelinput_dir/grid.$variable.tmp.nc $modelinput_dir/remap.$variable.tmp.nc
# Crop model (not latitude above 90)
ncks -O -F -d lat,0.,90. $modelinput_dir/remap.$variable.tmp.nc $modelinput_dir/$variable.remap.winter_avg.nc

# winter
variable=TSOI
# Extract good dimension for 1m
#ncks -O -F -d levgrnd,8 $modelinput_dir/winter_avg.nc $modelinput_dir/winter_avg.1d.nc # 8 for CLM45 9 for CLM5
# Extract good dimension for 20cm
# CLM45
ncks -O -F -d levgrnd,5 $modelinput_dir/winter_avg.nc $modelinput_dir/winter_avg.1d.nc
# CLM5
#ncks -O -F -d levgrnd,4 $modelinput_dir/winter_avg.nc $modelinput_dir/winter_avg.1d.top.nc # 16 cm 
#ncks -O -F -d levgrnd,5 $modelinput_dir/winter_avg.nc $modelinput_dir/winter_avg.1d.bot.nc # 26 cm
#ncflint -O -w 0.6,0.4 $modelinput_dir/winter_avg.1d.top.nc $modelinput_dir/winter_avg.1d.bot.nc $modelinput_dir/winter_avg.1d.nc
# Regrid model
cdo -r setgrid,$descriptiongrid -selvar,$variable $modelinput_dir/winter_avg.1d.nc $modelinput_dir/grid.$variable.tmp.nc
# Remap model
cdo -r remapnn,$descriptionreg -selvar,$variable $modelinput_dir/grid.$variable.tmp.nc $modelinput_dir/remap.$variable.tmp.nc
# Crop model (not latitude above 90)
ncks -O -F -d lat,0.,90. $modelinput_dir/remap.$variable.tmp.nc $modelinput_dir/$variable.remap.winter_avg.nc

rm $modelinput_dir/grid* $modeloutput_dir/grid*
rm $modelinput_dir/remap* $modeloutput_dir/remap*
