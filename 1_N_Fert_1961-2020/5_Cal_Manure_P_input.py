# This code is used to: Calculate P manure input based on N manure input and PN ratio

import xarray as xr
import os
import numpy as np

# Read the PN ratio
PNraito_path = 'PNratio/PNratio.nc'
PNratio_data = xr.open_dataset(PNraito_path)
PNratio = PNratio_data['PNratio'].values

print("PNratio shape:", PNratio.shape)

if PNratio.shape == (720, 360):
    print("Swapping lat and lon dimensions...")
    PNratio = PNratio.T

# Expand dimensions and repeat along 'time' using NumPy
PNratio_broadcasted = np.expand_dims(PNratio, axis=0)  # Add time dimension
PNratio_broadcasted = np.repeat(PNratio_broadcasted, 60, axis=0)  # Repeat along time dimension
PNratio_data.close()

PNratio_broadcasted_array = xr.DataArray(
    PNratio_broadcasted,
    dims=("year", "lat", "lon"),
    coords={
        "year": np.arange(1961, 2021),
        "lon": np.linspace(-180 + (0.5 / 2), 180 - (0.5 / 2), 720),
        "lat": np.linspace(90 - (0.5 / 2), -90 + (0.5 / 2), 360),
    },
    name="PNratio",
)

# Path for all the manure N input .nc file
folder_path = 'N_Manure_app_rate_05d'
crop_namelist = ['Barley', 'Cassava', 'Cotton', 'Fruits', 'Groundnut', 'Maize', 'Millet', 'Oilpalm', 'Others crops', 'Potato', 'Rapeseed', 'Rice', 'Rye', 'Sorghum', 'Soybean', 'Sugarbeet', 'Sugarcane', 'Sweetpotato', 'Vegetables', 'Wheat', 'Sunflower']

# Output paths
P_Manure_app_rate_05d_path = 'P_Manure_app_rate_05d'
#Manure_NP_app_rate_05d_path = 'Manure_NP_Input_05d'

os.makedirs(P_Manure_app_rate_05d_path, exist_ok=True)
#os.makedirs(Manure_NP_app_rate_05d_path, exist_ok=True)

                     
for crop in crop_namelist:
    nc_file_name = os.path.join(folder_path, f"N_manure_app_rate_{crop}_1961-2020.nc") 
    nc_file = xr.open_dataset(nc_file_name)
    
    N_manure = nc_file['Manure_N_application_rate'][:].transpose("year", "lat", "lon")  # read and if needed correct shape to year, lat, lon
        
    # Correct the coordinates with proper shapes
    years = np.arange(1961, 2021)  # 60 years
    lon = np.linspace(-180 + (0.5 / 2), 180 - (0.5 / 2), 720)  
    lat = np.linspace(90 - (0.5 / 2), -90 + (0.5 / 2), 360)
        
    P_manure = N_manure * PNratio_broadcasted_array
    
    # Create an xarray for P manure
    a = xr.DataArray(
         P_manure,
         dims=("year", "lat", "lon"),
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
