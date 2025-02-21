# This code is used to: Upscale the inorganic N fertilization input from 5 arc min to 0.5 degree

import numpy as np
import os
import xarray as xr

# %% 1. Calculate the total amount of inorganic input for each pixel at 0.5 degree resolution (harvest area * N fertilization rate)

# Output path:
N_inorg_5arcm_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_Inorg_amount_5arcm'
N_inorg_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_Inorg_amount_05d'

# Naming format of .nc file for the harvest area of each crop: Barley.nc
HA_5arcm_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/HA_5arcm'
# Naming format of .nc file for the N input of each crop: N_application_rate_Barley_1961-2020.nc
Inorg_5arcm_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_Inorganic_Original'

crop_namelist = ['Barley', 'Cassava', 'Cotton', 'Fruits', 'Groundnut', 'Maize', 'Millet', 'Oilpalm', 'Others crops', 'Potato', 'Rapeseed', 'Rice', 'Rye', 'Sorghum', 'Soybean', 'Sugarbeet', 'Sugarcane', 'Sweetpotato', 'Vegetables', 'Wheat', 'Sunflower']

for crop in crop_namelist:
    HA_5arcm = os.path.join(HA_5arcm_path, f"{crop}.nc")
    Inorg_5arcm = os.path.join(Inorg_5arcm_path, f"N_application_rate_{crop}_1961-2020.nc")
    
    nc_HA = xr.open_dataset(HA_5arcm)    
    data_HA = nc_HA['HA'][:]
    
    nc_file = xr.open_dataset(Inorg_5arcm)    
    data_Urea = nc_file['Urea_N_fert'][:]
    data_Inorg = nc_file['Inorganic_N_fert'][:]
    
    # Correct the coordinates with proper shapes
    years = np.arange(1961, 2021)  # 60 years
    lon = np.linspace(-180, 180, 4320)  # 4320 longitudes
    lat = np.linspace(90, -90, 2160)  # 2160 latitudes
    
    # Reassign the coordinates to the DataArrays
    data_Urea.coords["year"] = years
    data_Urea.coords["lon"] = lon
    data_Urea.coords["lat"] = lat
    
    data_Inorg.coords["year"] = years
    data_Inorg.coords["lon"] = lon
    data_Inorg.coords["lat"] = lat

    data_HA.coords["year"] = years
    data_HA.coords["lon"] = lon
    data_HA.coords["lat"] = lat    

    data_Total_Inorg = data_Urea + data_Inorg
    
    # Calculate the total amount of N inorganic input of the harvest area within a 5 arc minute pixel
    Urea_N_amount = data_HA * data_Urea
    Inorg_N_amount = data_HA * data_Inorg 
    Total_Inorg_N_amount = data_HA * data_Total_Inorg 
        
    # Urea N amount
    a = xr.DataArray(
         Urea_N_amount,
         dims=("year", "lon", "lat"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Urea_N_amount",
         attrs={
         "units": "kg"
                }
            )
    a_upscaled_no_nan = a.coarsen(lat=6, lon=6, boundary="trim").sum()
    a_upscaled = a_upscaled_no_nan.where(a_upscaled_no_nan != 0, np.nan)    
      
    output_N_Urea_amount_5arcm = os.path.join(N_inorg_5arcm_path, f"N_Urea_amount_{crop}_1961-2020.nc") 
    output_N_Urea_amount_05d = os.path.join(N_inorg_05d_path, f"N_Urea_amount_{crop}_1961-2020.nc")
    
    a.to_netcdf(output_N_Urea_amount_5arcm)
    a_upscaled.to_netcdf(output_N_Urea_amount_05d)
    print(f"Urea N input amount for {crop} has been saved")
    
    # Inorganic N amount
    b = xr.DataArray(
         Inorg_N_amount,
         dims=("year", "lon", "lat"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Inorg_N_amount",
         attrs={
         "units": "kg"
                }
            )
    b_upscaled_no_nan = b.coarsen(lat=6, lon=6, boundary="trim").sum()
    b_upscaled = b_upscaled_no_nan.where(b_upscaled_no_nan != 0, np.nan)    
      
    output_N_Inorg_amount_5arcm = os.path.join(N_inorg_5arcm_path, f"N_Inorg_amount_{crop}_1961-2020.nc") 
    output_N_Inorg_amount_05d = os.path.join(N_inorg_05d_path, f"N_Inorg_amount_{crop}_1961-2020.nc")
    
    b.to_netcdf(output_N_Inorg_amount_5arcm)
    b_upscaled.to_netcdf(output_N_Inorg_amount_05d)
    print(f"Inorganic N input amount for {crop} has been saved")
    
    # Total inorganic N amount
    c = xr.DataArray(
         Total_Inorg_N_amount,
         dims=("year", "lon", "lat"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Total inorganic N amount",
         attrs={
         "units": "kg"
                }
            )
    c_upscaled_no_nan = c.coarsen(lat=6, lon=6, boundary="trim").sum()
    c_upscaled = c_upscaled_no_nan.where(c_upscaled_no_nan != 0, np.nan)    
      
    output_N_Total_Inorg_amount_5arcm = os.path.join(N_inorg_5arcm_path, f"N_Total_Inorg_amount_{crop}_1961-2020.nc") 
    output_N_Total_Inorg_amount_05d = os.path.join(N_inorg_05d_path, f"N_Total_Inorg_amount_{crop}_1961-2020.nc")
    
    c.to_netcdf(output_N_Total_Inorg_amount_5arcm)
    c_upscaled.to_netcdf(output_N_Total_Inorg_amount_05d)
    print(f"Total inorganic N input amount for {crop} has been saved")
    
# %% 2. Calculate the N inorganic fertilizer application rate 

N_inorg_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_Inorg_amount_05d'
HA_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/HA_05d'

# Output path for inorganic N fertilizers application rate at 0.5 degree
N_inorg_app_rate_05d_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_Inorg_app_rate_05d'

crop_namelist = ['Barley', 'Cassava', 'Cotton', 'Fruits', 'Groundnut', 'Maize', 'Millet', 'Oilpalm', 'Others crops', 'Potato', 'Rapeseed', 'Rice', 'Rye', 'Sorghum', 'Soybean', 'Sugarbeet', 'Sugarcane', 'Sweetpotato', 'Vegetables', 'Wheat', 'Sunflower']

for crop in crop_namelist:
    HA_05d = os.path.join(HA_05d_path, f"{crop}.nc")
    Urea_05d = os.path.join(N_inorg_05d_path, f"N_Urea_amount_{crop}_1961-2020.nc")
    Inorg_05d = os.path.join(N_inorg_05d_path, f"N_Inorg_amount_{crop}_1961-2020.nc")
    Total_Inorg_05d = os.path.join(N_inorg_05d_path, f"N_Total_Inorg_amount_{crop}_1961-2020.nc")
    
    nc_HA = xr.open_dataset(HA_05d)    
    data_HA = nc_HA['HA'][:]
    
    nc_Urea = xr.open_dataset(Urea_05d)    
    data_Urea = nc_Urea['Urea_N_amount'][:]

    nc_Inorg = xr.open_dataset(Inorg_05d)    
    data_Inorg = nc_Inorg['Inorg_N_amount'][:]

    nc_Total_Inorg = xr.open_dataset(Total_Inorg_05d)    
    data_Total_Inorg = nc_Total_Inorg['Total inorganic N amount'][:]

    # Correct the coordinates with proper shapes
    years = np.arange(1961, 2021)  # 60 years
    lon = np.linspace(-180, 180, 720)  
    lat = np.linspace(90, -90, 360)  
    
    # Reassign the coordinates to the DataArrays
    data_HA.coords["year"] = years
    data_HA.coords["lon"] = lon
    data_HA.coords["lat"] = lat
    
    data_Urea.coords["year"] = years
    data_Urea.coords["lon"] = lon
    data_Urea.coords["lat"] = lat

    data_Inorg.coords["year"] = years
    data_Inorg.coords["lon"] = lon
    data_Inorg.coords["lat"] = lat

    data_Total_Inorg.coords["year"] = years
    data_Total_Inorg.coords["lon"] = lon
    data_Total_Inorg.coords["lat"] = lat
    
    # Calculate the total amount of N inorganic fertilizer input of the harvest area within a 5 arc minute pixel
    N_urea_application_rate = data_Urea / data_HA
    N_inorg_application_rate = data_Inorg / data_HA
    N_total_inorg_application_rate = data_Total_Inorg / data_HA
    
    # Urea N
    a = xr.DataArray(
         N_urea_application_rate,
         dims=("year", "lon", "lat"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Urea_N_application_rate",
         attrs={
         "units": "kg N/ha harvest area"
                }
            )     
    output_N_urea_app_rate_05d = os.path.join(N_inorg_05d_path, f"N_urea_app_rate_{crop}_1961-2020.nc")
    a.to_netcdf(output_N_urea_app_rate_05d)
    print(f"N urea application rate for {crop} has been calculated and saved")
    
    # Inorganic fertilzer
    b = xr.DataArray(
         N_inorg_application_rate,
         dims=("year", "lon", "lat"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Inorg_N_application_rate",
         attrs={
         "units": "kg N/ha harvest area"
                }
            )     
    output_N_inorg_app_rate_05d = os.path.join(N_inorg_05d_path, f"N_inorg_app_rate_{crop}_1961-2020.nc")
    b.to_netcdf(output_N_inorg_app_rate_05d)
    print(f"N inorganic fertilizer application rate for {crop} has been calculated and saved")
    
    # Total inorganic fertilizer
    c = xr.DataArray(
         N_total_inorg_application_rate,
         dims=("year", "lon", "lat"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Total_inorg_N_application_rate",
         attrs={
         "units": "kg N/ha harvest area"
                }
            )     
    output_N_total_inorg_app_rate_05d = os.path.join(N_inorg_05d_path, f"N_total_inorg_app_rate_{crop}_1961-2020.nc")
    c.to_netcdf(output_N_total_inorg_app_rate_05d)
    print(f"N total inorganic fertilizer application rate for {crop} has been calculated and saved")