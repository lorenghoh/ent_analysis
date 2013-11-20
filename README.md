[ent_analysis](https://github.com/lorenghoh/ent_analysis "ent_analysis")
==========

## Entrainment analysis toolkit for SAM ##
The **entrainment analysis toolkit** is a package used to post-process output data generated by SAM ([System for Atmospheric Modelling](http://rossby.msrc.sunysb.edu/~marat/SAM.html)) with entrainment calculation implemented by Dawe and Austin (2011a). This package combines (parallelized and automated) SAM output conversion (```bin3D2nc```), cloudtracker and several different post-process scripts. 

 The raw ```.bin3D``` data from SAM is converted, and sorted to be used by  [*cloudtracker*](https://github.com/freedryk/cloudtracker). Then for each cloud parcel, the package creates a ```netCDF``` file containing all the relevant output data from SAM. Now with the individual cloud data collected by ```cloudtracker```, it is possible to apply reanalysis scripts (or *analysis modules*) to produce a more detailed picture of each cloud parcel -- these *modules* will modify output ```netCDF``` files and add additional statistical variables needed for the entrainment analysis. 

## Current status ##
Current version of ent_analysis package will not fully run yet. 

### In Progress ###
- [x] Automate data structure
- [x] Make config.cfg modifiable
- [x] ```time_parser```
- [ ] Automatically read dimensions from input files
- [ ] ```run_analysis.py``` refactoring
- [ ] Module integration 

### Next ###
- [ ] Complete (*automated*) test run using the standard ```BOMEX_25m_25m_25m``` output
- [ ] Output control

### Maybe ###
- [ ] Parallelize [*cloudtracker*](https://github.com/freedryk/cloudtracker) module 
- [ ] Calculate density perturbation in ```time_profiles```

### Done ###
- [x] Modify parallelization to be handled by the main script (```run_analysis.py```)
- [x] Modularize the main script (for pre-processing)
- [x] Add parallelization to ```conversion``` module
- [x] Add parallelization to ```generate_tracking``` module
- [x] Add parallelization to ```time_profiles``` module
- [x] Better written ```README.md```
- [x] Parallelize ```profiler``` scripts
- [x] Modify ```id_profiles``` module for parallelization
- [x] Add ```id_profiles``` module for automation (turned off by default)
- [x] Automatically generate profiles
- [x] Modify core_entrain
- [x] Modify condensed_entrain
- [x] Automate/parallelize entrainment profiles
- [x] ```convert.py``` with dynamic modules
- [x] Better module configuration
- [x] Complete Python module wrapper 

## Getting Started ##
 To run the entrainment analysis toolkit, the following Python modules **must** be installed (as needed for the [*cloudtracker*](https://github.com/freedryk/cloudtracker) module):

- numpy
- networkx
- netcdf4-python *or* pupynere

### Installation ###
Download ent_analysis package to SAM directory, or where the model output will be stored for better performance (*recommended* if the storage is limited). Ensure that the configuration file ```config.cfg``` is properly modified according to the system configuration. 

### Example ###
 To run entrainment analysis toolkit, simple run:```./run_analysis.py```

Or, use the MOAB script ```msub MOAB```