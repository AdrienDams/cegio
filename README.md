![cegio_diagram](https://user-images.githubusercontent.com/24732655/216118980-9d2e0f97-a540-448f-ac96-3f972270891b.png)

## Requirements
- Daily files from CTSM (minimum 3 years period)
- ESACCI and in-situ observation files (available by request at adamseau@awi.de)
- python3 (numpy, pandas, scipy, matplotlib, seaborn, netCDF4, similaritymeasures, cartopy libraries)
- cdo (minimum 2.0.3)
- nco (minimum 5.0.6)
- bash shell
- sbatch

## Install
Replace `* *` with your own options

```
export run_name=*casename*
export startyear=*yyyy*
export endyear=*yyyy*

export descriptiongrid=*descriptiongridname*
export descriptionreg=*descriptiongridname*

export cegio=$PWD
export scratch_dir=*scratch_dir*
ln -s *data_directory* data/$run_name
```

`descriptiongrid` and `descriptionreg` are descriptions of the grid and domain you are using. Those tags are needed for the mappinng in *Mappings and plots* 3. and 4.

## Post-processing

1. Extract desired variables
```
sbatch ./postproc/extract_variable.sh
```

2. Compute monthly averages
```
sbatch ./postproc/monthlyaverage.sh
```

3. Run post-processing. This includes:
- Extract MAGT and make year averages `make_magt.sh`
- Compute permafrost extent `make_permafrost_extend.sh`
- Compute Active Layer Thickness (ALT) `active_layer.py`
```
sbatch ./postproc/run_postproc_py_clm.sh
```
## Evaluations

1. Run CTSM vs in-situ stations
```
sbatch ./evaluation/stations/run_py.sh
```

2. Run CTSM vs CALM stations
```
sbatch ./evaluation/CALM/run_py.sh
```

3. Run CTSM vs. ESACCI evaluation of 3 variables (TSOI, ALT and PFR)

```
./evaluation/ESACCI/run_ESACCI_to_57_DOM02.sh
```

## Mappings and plots

1. Create scatter plots and PCM area maps for every station
```
sbatch ./evaluation/stations/make_figures/run_figures.sh
```

2. Create splines graph, linear plot and trumpet curves for specific station
```
./evaluation/stations/make_figures/run_figures_station.sh
```

3. Create maps for CTSM vs. CALM
```
sbatch ./evaluation/CALM/make_figures/run_figure.sh
```

4. Create maps for CTSM vs. ESACCI comparisons
```
sbatch ./evaluation/ESACCI/make_figures/run_averages.sh
```
