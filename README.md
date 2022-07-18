## Requirements
- Daily files from CTSM (minimum 3 years period)
- python3 (numpy, scipy, matplotlib, netCDF4, similaritymeasures library)
- cdo (minimum 2.0.3)
- nco (minimum 5.0.6)
- bash shell

1. Install

```
export run_name=*casename*
export startyear=*yyyy*
export endyear=*yyyy*

export cegio=$PWD
export scratch_dir=*scratch_dir*
ln -s *data_directory* data/$run_name
```

2. Extract desired variables
```
./postproc/extract_variable.sh
```

3. Compute monthly averages
```
./postproc/monthlyaverage.sh
```

4. Run post-processing. This includes:
- Compute season averages `make_season_mean_all.sh`
- Compute snow depth averages `make_annual_mean_snowdepth.sh`
- Extract MAGT and make year averages `make_magt.sh`
- Compute permafrost extent `make_permafrost_extend.sh`
- Compute snow free day `end_snow_melt.py`
- Compute Active Layer Thickness (ALT) `active_layer.py`
```
./postproc/run_postproc_py_clm.sh
```

5. Run model vs. ESACCI evaluation with 3 variables
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

6. Run model vs in-situ stations
```
./evaluation/stations/run_py.sh
```
(`splines_graph.py` can create a graph for one station and one month of the spline - change settings in file)

7. Compute trumpet curve model vs in-situ stations
```
./evaluation/trumpet/run_trumpet.sh
```
