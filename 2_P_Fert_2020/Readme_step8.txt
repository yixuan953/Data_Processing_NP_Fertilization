----------------------Code description---------------
The code of this folder [Res_Trans_P_manure_Upscale05d.py] is used to upscale global inorganic P input from 0.05 degree to 0.5 degree
1. Calculate the total amount of P2O5 input [kg] for each pixel at 0.05 degree resolution (harvest area * P2O5 application rate) and sum up to 0.5 degree
2. Sum up the total harvest area at 0.5 degree resolution
3. Divide the P2O5 input amount at 0.5 degree resolution by harvest area at each pixel, and transform P2O5 to P application rate [kg P/ha harvest area]

----------------------Original dataset---------------
[P2O5 application rate for each crop type] 
Unit: kg ha-1（harvest area）y-1
Variables: 
    1 - P2O5rate: P2O5 input per ha harvest area
Temporal scale: ~2020 annual
Spatial scale: global, 0.05 degree
Data format: .nc
Data source: Nguyen, T.H., Tang, F.H.M., Conchedda, G. et al. NPKGRIDS: a global georeferenced dataset of N, P2O5, and K2O fertilizer application rates for 173 crops. Sci Data 11, 1179 (2024). https://doi.org/10.1038/s41597-024-04030-4
Website for downloading: https://doi.org/10.6084/m9.figshare.24616050

[Harvest area] 
Unit: ha
Variables: 
    1 - harvarea: P2O5 input per ha harvest area
Temporal scale: Annual
Spatial scale: global, 0.05 degree
Data format: .nc
Data source: Tang, F.H.M., Nguyen, T.H., Conchedda, G. et al. CROPGRIDS: a global geo-referenced dataset of 173 crops. Sci Data 11, 413 (2024). https://doi.org/10.1038/s41597-024-03247-7
Website for downloading: https://doi.org/10.6084/m9.figshare.22491997

----------------------Transformed data------------
[Inorganic P application rate] 
P_inorg_app_rate [kg P / ha harvest area]
Temporal scale: annual, ~2020
Spatial scale: Global, 0.5 degree
Data format: .nc