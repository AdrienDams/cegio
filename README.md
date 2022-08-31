## Requirements
- Daily files from CTSM (minimum 3 years period)
- ESACCI and in-situ observation files (available by request at adamseau@awi.de)
- python3 (numpy, scipy, matplotlib, netCDF4, similaritymeasures libraries)
- cdo (minimum 2.0.3)
- nco (minimum 5.0.6)
- bash shell

## Install

```
export run_name=*casename*
export startyear=*yyyy*
export endyear=*yyyy*

export cegio=$PWD
export scratch_dir=*scratch_dir*
ln -s *data_directory* data/$run_name
```
## Post-processing

1. Extract desired variables
```
./postproc/extract_variable.sh
```

2. Compute monthly averages
```
./postproc/monthlyaverage.sh
```

3.. Run post-processing. This includes:
- Compute season averages `make_season_mean_all.sh`
- Compute snow depth averages `make_annual_mean_snowdepth.sh`
- Extract MAGT and make year averages `make_magt.sh`
- Compute permafrost extent `make_permafrost_extend.sh`
- Compute snow free day `end_snow_melt.py`
- Compute Active Layer Thickness (ALT) `active_layer.py`
```
./postproc/run_postproc_py_clm.sh
```
## Evaluations

1. Run model vs. ESACCI evaluation with 3 variables (sbatch strongly recommended)
- ALT
```
./evaluation/ESACCI/ESACCI_to_57_DOM02.ALT.sh
```
- Permafrost extent
```
./evaluation/ESACCI/ESACCI_to_57_DOM02.ALT.sh
```
- Ground temperature
```
./evaluation/ESACCI/ESACCI_to_57_DOM02.ALT.sh
```

2. Run model vs in-situ stations
```
./evaluation/stations/run_py.sh
```

## Mappings and plots

1. Create scatter plots and PCM area maps for every station
```
./evaluation/stations/make_figures/run_figures.sh
```

2. Create splines graph, linear plot and trumpet curves for specific station
```
./evaluation/stations/make_figures/run_figures_station.sh
```

3. Create maps for Model vs. ESACCI comparisons
```
./evaluation/ESACCI/make_figures/run_averages.sh
```
