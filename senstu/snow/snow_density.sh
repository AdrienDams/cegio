modelinput_dir=$cegio/data
modeloutput_dir=$scratch_dir/snow_depth
export run_name_a="57_DOM02_051"
export run_name_b="57_DOM02_001" # control run

# Define the list of run names
run_names=($run_name_a $run_name_b)

# Loop through the run names
for run_name in "${run_names[@]}"; do
    # Loop through the years 1980 to 2021
    for year in {1980..2021}; do
        echo $year
        # Create snow_density
        ncap2 -s 'snow_density=H2OSNO/SNOW_DEPTH' -O -v "$modelinput_dir/$run_name/monthly/$run_name.clm2.h0.$year-01.nc" "$modeloutput_dir/tmp.$run_name.sd.$year-01.nc"

        # Regrid model
        cdo -r setgrid,"$descriptiongrid" -selvar,snow_density "$modeloutput_dir/tmp.$run_name.sd.$year-01.nc" "$modeloutput_dir/grid.$run_name.sd.$year-01.nc"

        # Remap model
        cdo -r remapnn,"$descriptionreg" -selvar,snow_density "$modeloutput_dir/grid.$run_name.sd.$year-01.nc" "$modeloutput_dir/remap.$run_name.sd.$year-01.nc"

        # Crop model (not latitude above 90)
        ncks -O -F -d lat,0.,90. "$modeloutput_dir/remap.$run_name.sd.$year-01.nc" "$modeloutput_dir/$run_name.sd.$year-01.nc"
    done
    
    # Combine monthly files for each year into a single file for January
    cdo -r mergetime "$modeloutput_dir/$run_name.sd.????-01.nc" "$modeloutput_dir/$run_name.sd.all_years-01.nc"

    # Calculate the period average for January across the years 1980 to 2021
    cdo -r ymonmean "$modeloutput_dir/$run_name.sd.all_years-01.nc" "$modeloutput_dir/$run_name.sd.period.01.nc"
done


#python snow_density.py
