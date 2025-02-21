# This code is used to: Upscale the inorganic P fertilization input from 0.05 to 0.5 degree

import numpy as np
import os
import xarray as xr
import glob

# %% 1. Calculate the total amount of inorganic input for each pixel at 0.5 degree (harvest area * N fertilization rate)

# Output path:
P_inorg_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/P_Inorg_amount_05d'

# Input path
# Naming format of .nc file for the harvest area of each crop: CROPGRIDSv1.08_maize.nc
HA_005d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Fertilization/P_Fert/CropMask'
# Naming format of .nc file for the P2O5 input of each crop: NPKGRIDSv1.08_maize.nc
Inorg_005d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Fertilization/P_Fert/AppRate'

# Input the crop list:
crop_namelist = ['maize','rice','soybean','wheat']

for crop in crop_namelist:
    HA_005d = os.path.join(HA_005d_path, f"CROPGRIDSv1.08_{crop}.nc")
    Inorg_005d = os.path.join(Inorg_005d_path, f"NPKGRIDSv1.08_{crop}.nc")
    
    nc_HA = xr.open_dataset(HA_005d)    
    data_HA = nc_HA['harvarea'][:]
    data_HA = data_HA.where(data_HA >= 0, np.nan)
    
    nc_file = xr.open_dataset(Inorg_005d)    
    data_Inorg = nc_file['P2O5rate'][:]
    data_Inorg = data_Inorg.where(data_Inorg >= 0, np.nan)
    
    # Correct the coordinates with proper shapes
    lon = np.linspace(-180, 180, 7200)
    lat = np.linspace(90, -90, 3600)  
    
    data_Inorg.coords["lon"] = lon
    data_Inorg.coords["lat"] = lat

    data_HA.coords["lon"] = lon
    data_HA.coords["lat"] = lat    
    
    # Calculate the total amount of P2O5 inorganic input of the harvest area within a 0.05 degree pixel
    P2O5_amount = data_HA * data_Inorg 
        
    # Inorganic N amount
    a = xr.DataArray(
         P2O5_amount,
         dims=("lat", "lon"),
         coords={
             "lat": -lat,
             "lon": lon,        
                },
         name = "P2O5 input",
         attrs={
         "units": "kg P2O5"
                }
            )
    
    a_upscaled_no_nan = a.coarsen(lat=10, lon=10, boundary="trim").sum()
    a_upscaled = a_upscaled_no_nan.where(a_upscaled_no_nan != 0, np.nan)    
      
    output_P2O5_amount_05d = os.path.join(P_inorg_05d_path, f"P2O5_amount_{crop}.nc")
    
    a_upscaled.to_netcdf(output_P2O5_amount_05d)
    print(f"P2O5 input amount for {crop} has been saved")
    

# %%  2. Sum up the total harvest area to 0.5 degree resolution

HA_005d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Fertilization/P_Fert/CropMask'
HAcr_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/HAcr_05d'

nc_files = glob.glob(os.path.join(HA_005d_path, '*.nc'))

for nc_file_name in nc_files:
    
    nc_file = xr.open_dataset(nc_file_name)    
    data = nc_file['harvarea'][:]
    data = data.where(data >= 0, np.nan)
           
    # Create latitude and longitude arrays
    lat = np.linspace(90, -90, 3600)
    lon = np.linspace(-180, 180, 7200)
            
    # Create an xarray DataArray
    a = xr.DataArray(
         data,
         dims=("lat","lon"),
         coords={
             "lat": -lat,
             "lon": lon,
                },
            )
            
    upscaled_no_nan = a.coarsen(lat=10, lon=10, boundary="trim").sum()
    upscaled = upscaled_no_nan.where(upscaled_no_nan != 0, np.nan)
    
    file_name = os.path.basename(nc_file_name)
    output_nc_file = os.path.join(HAcr_05d_path, f"Upscaled05d_{file_name}")    
    upscaled.to_netcdf(output_nc_file)
    print(f"Saved upscaled data as {output_nc_file}")

# %% 3. Calculate the inorganic P fertilizer application rate 

P_inorg_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/P_Inorg_amount_05d'
HAcr_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/HAcr_05d'

# Output path for inorganic N fertilizers application rate at 0.5 degree
P_inorg_app_rate_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/P_Inorg_app_rate_05d'

crop_namelist = ['maize','rice','soybean','wheat']

for crop in crop_namelist:
    HAcr_05d = os.path.join(HAcr_05d_path, f"Upscaled05d_CROPGRIDSv1.08_{crop}.nc")
    Inorg_05d = os.path.join(P_inorg_05d_path, f"P2O5_amount_{crop}.nc")
    
    nc_HA = xr.open_dataset(HAcr_05d)    
    data_HA = nc_HA['harvarea'][:]
    
    nc_Inorg = xr.open_dataset(Inorg_05d)    
    data_Inorg = nc_Inorg['P2O5 input'][:]

    # Correct the coordinates with proper shapes
    lon = np.linspace(-180, 180, 720)  
    lat = np.linspace(90, -90, 360)  
    
    # Reassign the coordinates to the DataArrays
    data_HA.coords["lon"] = lon
    data_HA.coords["lat"] = lat
    
    data_Inorg.coords["lon"] = lon
    data_Inorg.coords["lat"] = lat

    
    # Calculate the total amount of P inorganic fertilizer input of the harvest area within a 0.5 degree pixel
    P_inorg_application_rate = 0.465 * data_Inorg / data_HA # Transforming P2O5 to P
        
    # Inorganic P fertilzer
    a = xr.DataArray(
         P_inorg_application_rate,
         dims=("lat", "lon"),
         coords={
             "lat": -lat,
             "lon": lon,
                },
         name = "Inorg_P_application_rate",
         attrs={
         "units": "kg P/ha harvest area"
                }
            )     
    output_P_inorg_app_rate_05d = os.path.join(P_inorg_app_rate_05d_path, f"P_inorg_app_rate_{crop}.nc")
    a.to_netcdf(output_P_inorg_app_rate_05d)
    print(f"P inorganic fertilizer application rate for {crop} has been calculated and saved")

