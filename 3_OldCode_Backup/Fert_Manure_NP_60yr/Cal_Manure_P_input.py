# This code is used to: Calculate P manure input based on N manure input and PN ratio

import xarray as xr
import os
import numpy as np

# Read the PN ratio
PNraito_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/PNratio.nc'
PNratio_data = xr.open_dataset(PNraito_path)
PNratio = PNratio_data['PNratio'].values
# Expand dimensions and repeat along 'time' using NumPy
PNratio_transposed = PNratio.T 
PNratio_broadcasted = np.expand_dims(PNratio_transposed, axis=0)  # Add time dimension
PNratio_broadcasted = np.repeat(PNratio_broadcasted, 60, axis=0)  # Repeat along time dimension
PNratio_data.close()

PNratio_broadcasted_array = xr.DataArray(
    PNratio_broadcasted,
    dims=("year", "lon", "lat"),
    coords={
        "year": np.arange(1961, 2021),
        "lon": np.linspace(-180, 180, 720),
        "lat": np.linspace(90, -90, 360),
    },
    name="PNratio",
)

# Path for all the manure N input .nc file
folder_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_Manure_app_rate_05d'
crop_namelist = ['Barley', 'Cassava', 'Cotton', 'Fruits', 'Groundnut', 'Maize', 'Millet', 'Oilpalm', 'Others crops', 'Potato', 'Rapeseed', 'Rice', 'Rye', 'Sorghum', 'Soybean', 'Sugarbeet', 'Sugarcane', 'Sweetpotato', 'Vegetables', 'Wheat', 'Sunflower']

# Output paths
P_Manure_app_rate_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/P_Manure_app_rate_05d'
Manure_NP_app_rate_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/Manure_NP_Input_05d'                         
                     
for crop in crop_namelist:
    nc_file_name = os.path.join(folder_path, f"N_manure_app_rate_{crop}_1961-2020.nc") 
    nc_file = xr.open_dataset(nc_file_name)
    
    N_manure = nc_file['Manure_N_application_rate'][:]
        
    # Correct the coordinates with proper shapes
    years = np.arange(1961, 2021)  # 60 years
    lon = np.linspace(-180, 180, 720)
    lat = np.linspace(90, -90, 360)
        
    P_manure = N_manure * PNratio_broadcasted_array
    
    # Create an xarray for P manure
    a = xr.DataArray(
         P_manure,
         dims=("year", "lon", "lat"),
         coords={
             "year": years,
             "lon": lon,
             "lat": lat,
                },
         name = "Manure_P_application_rate",
         attrs={
         "units": "kg/ha harvest area"
                }
            )   
        
    output_P_manure_app_rate_05d = os.path.join(P_Manure_app_rate_05d_path, f"P_manure_app_rate_{crop}_1961-2020.nc")
    a.to_netcdf(output_P_manure_app_rate_05d)
    print(f"P manure of {crop} has been calculated and saved") 
