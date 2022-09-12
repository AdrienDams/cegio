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
export startyear_esa=2001
export endyear_esa=2019

sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.ALT.sh
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.PFR.sh

export depth=1m
export toplayer=8
export botlayer=9
export inttop=0.23
export intbot=0.77
sbatch $cegio/evaluation/ESACCI/ESACCI_to_57_DOM02.GT.sh
export depth=2m
export toplayer=11
export botlayer=12
export inttop=0.21
export intbot=0.79
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
