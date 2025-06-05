# H2_prod_sim
Hydrogen production simulation tool for the comparison of the H2 production configurations

This repository contains supplementary data to the paper:

R. Travaglini, L.S.F. Frowijn, A. Bianchini, Z. Lukszo, K. Bruninx:  
Offshore or onshore hydrogen production? A critical analysis on costs and operational considerations for the Dutch North Sea*, Applied Energy, 2025

The Python code used in this study is organized into three folders, each representing one of the hydrogen production configurations analyzed in the article. 

## Methodology

The methodology followed and the assumptions made to derive the results are described in detail in the article cited above.

## Usage

Each configuration folder contains a `main.py` script, which orchestrates the simulation by using modules from its subfolders. The simulation pipeline includes:

1. Wind Farm Simulation Tool (`NorthSea_timedependent` in folder `WindFarm`):  
   Enables time-dependent simulations based on the selected wind source.

2. Hydrogen Simulation Tool (`H2_simulation_nogrid` in folder `System Operation`):  
   Calculates transmission losses and the potential for hydrogen production thanks to the electrolyzer models in folder `Electrolyzer`.

3. Economic Model (`LCOH_calculator` in folder `Economics`):  
   Estimates the Levelized Cost of Hydrogen (LCOH) based on technical and financial outputs.

In the current code, data is used from the dataset of the paper. The databases can be found in the paper and the corresponding appendices.

## Citation

If you use this repository or its scripts in your work, please cite using the CITATION.cff as well as the paper:

R. Travaglini, L.S.F. Frowijn, A. Bianchini, Z. Lukszo, K. Bruninx:  
Offshore or onshore hydrogen production? A critical analysis on costs and operational considerations for the Dutch North Sea*, Applied Energy, 2025


## Licence

Creative Commons licenses
