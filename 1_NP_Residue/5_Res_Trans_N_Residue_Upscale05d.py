# This code is used to: Upscale the Residue N fertilization input from 5 arc min to 0.5 degree

import numpy as np
import os
import xarray as xr

# 1. Calculate the total amount of Residue input for each pixel at 5 arcmin (harvest area * N fertilization rate)

# Output path:
N_Residue_5arcm_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/N_Residue_amount_5arcm'
N_Residue_05d_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/N_Residue_amount_05d'

os.makedirs(N_Residue_5arcm_path, exist_ok=True)
os.makedirs(N_Residue_05d_path, exist_ok=True)

# Naming format of .nc file for the harvest area of each crop: Barley.nc
HA_5arcm_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/HA_5arcm'
# Naming format of .nc file for the N input of each crop: N_application_rate_Barley_1961-2020.nc
Residue_5arcm_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/N_Residue_app_rate_5arcm'

crop_namelist = ['Maize', 'Rice', 'Soybean', 'Wheat']

for crop in crop_namelist:
    HA_5arcm = os.path.join(HA_5arcm_path, f"{crop}.nc")
    Residue_5arcm = os.path.join(Residue_5arcm_path, f"N_application_rate_{crop}_1961-2020.nc")
    
    nc_HA = xr.open_dataset(HA_5arcm)    
    data_HA = nc_HA['HA'][:].transpose("year", "lat", "lon")  # read and if needed correct shape to year, lat, lon
    
    nc_file = xr.open_dataset(Residue_5arcm)    
    data_Residue = nc_file['Residue_N_fert'][:].transpose("year", "lat", "lon")  # read and if needed correct shape to year, lat, lon
    
    # Correct the coordinates with proper shapes
    years = np.arange(1961, 2021)  # 60 years
    lon = np.linspace(-180 + (0.083333 / 2), 180 - (0.083333 / 2), 4320)  # 4320 longitudes
    lat = np.linspace(90 - (0.083333 / 2), -90 + (0.083333 / 2), 2160)  # 2160 latitudes
    
    # Reassign the coordinates to the DataArrays    
    data_Residue.coords["year"] = years
    data_Residue.coords["lon"] = lon
    data_Residue.coords["lat"] = lat

    data_HA.coords["year"] = years
    data_HA.coords["lon"] = lon
    data_HA.coords["lat"] = lat

    # Calculate the total amount of N Residue input of the harvest area within a 5 arc minute pixel
    Residue_N_amount = data_HA * data_Residue 

    # Residue N amount
    b = xr.DataArray(
         Residue_N_amount,
         dims=("year", "lat", "lon"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Residue_N_amount",
         attrs={
         "units": "kg"
                }
            )
    b_upscaled_no_nan = b.coarsen(lat=6, lon=6, boundary="trim").sum()
    b_upscaled = b_upscaled_no_nan.where(b_upscaled_no_nan != 0, np.nan)    
      
    output_N_Residue_amount_5arcm = os.path.join(N_Residue_5arcm_path, f"N_Residue_amount_{crop}_1961-2020.nc") 
    output_N_Residue_amount_05d = os.path.join(N_Residue_05d_path, f"N_Residue_amount_{crop}_1961-2020.nc")
    
    b.to_netcdf(output_N_Residue_amount_5arcm)
    b_upscaled.to_netcdf(output_N_Residue_amount_05d)
    print(f"Residue N input amount for {crop} has been saved")
    
# 2. Calculate the N Residue fertilizer application rate 

# Naming format of .nc file for the harvest area of each crop: Barley.nc
HA_5arcm_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/HA_5arcm'
HA_05d_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/HA_05d'

crop_namelist = ['Maize', 'Rice', 'Soybean', 'Wheat']

# Output path for Residue N fertilizers application rate at 0.5 degree
N_Residue_app_rate_05d_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/N_Residue_app_rate_05d'
os.makedirs(N_Residue_app_rate_05d_path, exist_ok=True)

for crop in crop_namelist:
    HA_05d = os.path.join(HA_05d_path, f"{crop}.nc")
    Residue_05d = os.path.join(N_Residue_05d_path, f"N_Residue_amount_{crop}_1961-2020.nc")
    
    nc_HA = xr.open_dataset(HA_05d)    
    data_HA = nc_HA['HA'][:].transpose("year", "lat", "lon")  # read and if needed correct shape to year, lat, lon
    
    nc_Residue = xr.open_dataset(Residue_05d)    
    data_Residue = nc_Residue['Residue_N_amount'][:].transpose("year", "lat", "lon")  # read and if needed correct shape to year, lat, lon

    # Correct the coordinates with proper shapes
    years = np.arange(1961, 2021)  # 60 years
    lon = np.linspace(-180 + (0.5 / 2), 180 - (0.5 / 2), 720)  
    lat = np.linspace(90 - (0.5 / 2), -90 + (0.5 / 2), 360)  
    
    # Reassign the coordinates to the DataArrays
    data_HA.coords["year"] = years
    data_HA.coords["lon"] = lon
    data_HA.coords["lat"] = lat

    data_Residue.coords["year"] = years
    data_Residue.coords["lon"] = lon
    data_Residue.coords["lat"] = lat

    # Calculate the applicatio rate
    N_Residue_application_rate = data_Residue / data_HA
        
    # Residue fertilzer
    b = xr.DataArray(
         N_Residue_application_rate,
         dims=("year", "lat", "lon"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Residue_N_application_rate",
         attrs={
         "units": "kg N/ha harvest area"
                }
            )     
    output_N_Residue_app_rate_05d = os.path.join(N_Residue_app_rate_05d_path, f"N_Residue_app_rate_{crop}_1961-2020.nc")
    b.to_netcdf(output_N_Residue_app_rate_05d)
    print(f"N Residue fertilizer application rate for {crop} has been calculated and saved")