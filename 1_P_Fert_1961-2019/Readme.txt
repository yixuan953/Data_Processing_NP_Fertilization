----------------------Code description---------------
The code of this folder is used to upscale global inorganic P input from 0.05 degree to 0.5 degree
1. Cal_P_InorgFert_Amount_5min.py: Calculate the inorganic fertilizer input amount (in both P and P2O5) at 5 arcmin (P2O5 "application rate" * the area of each pixel) and sum up to 0.5 degree
   The original input "Application rate" is actually the "Application amount/the area of 5arcmin-pixel grid" 
2. Form_Trans_tiff2nc: Transform the calculated fertilizer application amount (5 arcmin) to .nc files, with the format "Crop_Nutri_1961-2019.nc"
3. Res_Trans_P_Inorg_Fert: Sum up the amount at 0.5 degree and save it into .nc file
3. Cal_HA_5d.py: Sum up the harvest area for each crop and transform it into .nc file
4. Divide the input amount at 0.5 degree resolution by harvest area of each pixel [kg P/ha harvest area] & [kg P2O5/ha harvest area]
   For this dataset, the P application rate will be the same within a cournty

----------------------Original dataset---------------
[P2O5 application rate for each crop type] 
Unit: kg ha-1（the area of 5arcmin pixel）y-1
Naming format: 
    "Crop_Nutri_Year.tiff"
Temporal scale: 1961-2019 annual
Spatial scale: global, 5arcmin
Data format: .tiff
Data source: Coello, F., Decorte, T., Janssens, I. et al. Global Crop-Specific Fertilization Dataset from 1961–2019. Sci Data 12, 40 (2025). https://doi.org/10.1038/s41597-024-04215-x
Website for downloading: 

[Harvest area] 
Unit: ha
Naming format: 
    1 - 
Temporal scale: 1961 - 2019 Annual
Spatial scale: global, 5arcmin
Data format: 
Data source: Coello, F., Decorte, T., Janssens, I. et al. Global Crop-Specific Fertilization Dataset from 1961–2019. Sci Data 12, 40 (2025). https://doi.org/10.1038/s41597-024-04215-x
Website for downloading: 

----------------------Transformed data------------
[Inorganic P application rate] 
   1 - P_inorg_app_rate [kg P / ha harvest area]
   2 - P2O5_inorg_app_rate [kg P2O5 / ha harvest area]
Temporal scale: annual, 1961-2019
Spatial scale: Global, 0.5 degree
Data format: .nc