#!/bin/bash
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --time=8:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=8G

modeloutput_dir="$cegio/data/ESACCI/$run_name/CTSM_regridded"
obsoutput_dir="$cegio/data/ESACCI/$run_name/ESACCI_regridded"
scratch_ESA="$scratch_dir/ESACCI"
mkdir -p $modeloutput_dir
mkdir -p $obsoutput_dir
mkdir -p $scratch_ESA
export startyear_esa=1997
export endyear_esa=2019

sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.ALT.sh
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.PFR.sh
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.GT.1m.sh
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.GT.2m.sh
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.GT.5m.sh
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.GT.10m.sh
