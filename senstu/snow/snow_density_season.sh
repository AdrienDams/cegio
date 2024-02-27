#!/bin/bash
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --time=08:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=60G


modelinput_dir=$cegio/data
modeloutput_dir=$scratch_dir/snow_depth
export run_name_a="57_DOM02_051"
export run_name_b="57_DOM02_001" # control run

# Define the list of run names
run_names=($run_name_a $run_name_b)

# Define months for each season
declare -A seasons=( ["Winter"]="12 01 02" ["Spring"]="02 03 04" ["Summer"]="06 07 08" ["Autumn"]="09 10 11" )

for season in "${!seasons[@]}"; do
    for run_name in "${run_names[@]}"; do
        echo $season
        month_list=${seasons[$season]}
        
        # Initialize variable to store merged files
        merged_files=""

        # Concatenate file names for the specific season across all years
        for year in {1980..2021}; do
            for month in $month_list; do
                for day in {01..31}; do
                    file="$modelinput_dir/$run_name/daily/$run_name.clm2.h0.$year-$month-$day.ext.nc"
                    if [ -f "$file" ]; then
                        merged_files+=" $file"
                    fi
                done
            done
        done
        
        # Merge files for the specific season across all years
        cdo -O -r mergetime $merged_files "$modeloutput_dir/$run_name.$season.all_years.nc"

        # Calculate snow_density for the season
        cdo -O -r expr,'snow_density=H2OSNO/SNOW_DEPTH' "$modeloutput_dir/$run_name.$season.all_years.nc" "$modeloutput_dir/$run_name.$season.all_years.sd.nc"

        cdo -O -r ymonmean "$modeloutput_dir/$run_name.$season.all_years.sd.nc" "$modeloutput_dir/$run_name.$season.paverage.sd.nc"
        cdo -O -r timmean "$modeloutput_dir/$run_name.$season.paverage.sd.nc" "$modeloutput_dir/$run_name.$season.average.sd.nc"

        # Regrid the model for the season
        cdo -O -r setgrid,"$descriptiongrid" -selvar,snow_density "$modeloutput_dir/$run_name.$season.average.sd.nc" "$modeloutput_dir/$run_name.$season.grid.sd.nc"

        # Remap the model for the season
        cdo -O -r remapnn,"$descriptionreg" -selvar,snow_density "$modeloutput_dir/$run_name.$season.grid.sd.nc" "$modeloutput_dir/$run_name.$season.remap.sd.nc"

        # Crop the model for the season (latitude below 90)
        ncks -O -F -d lat,0.,90. "$modeloutput_dir/$run_name.$season.remap.sd.nc" "$modeloutput_dir/$run_name.sd.period.$season.nc"
    done

    python snow_density_season.py $season
done

