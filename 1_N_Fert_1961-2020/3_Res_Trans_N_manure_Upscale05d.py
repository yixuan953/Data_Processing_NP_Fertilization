# This code is used to:
# 1. Read the harvest area for each crop and save to .nc file
# 2. Sum up the total harvest area to 0.5 degree resolution
# 3. Calculate the total amount of manure input for each pixel at 5arc minute (harvest area * N fertilization rate)
# 4. Sum up the total manure input to 0.5 degree resolution
# 5. Divide the N manure input amount at 0.5 degree resolution by harvest area at each pixel

import h5py
from netCDF4 import Dataset
import numpy as np
import os
import glob
import xarray as xr

# %% 1. Read the harvest area for each crop (.h5 to .nc)

HA_h5_file = '../../../1_Raw_data/Fertilizer/Fertilization/Harvested_area_1961-2020.h5'
HA_output_path = 'HA_5arcm'

os.makedirs(HA_output_path, exist_ok=True)

# Open the HDF5 file
with h5py.File(HA_h5_file, 'r') as h5file:

# Loop through each key in the HDF5 file
    for key in h5file.keys():
        data = h5file[key][:]

        #check coordinates
        print(f"Processing key: {key}, Original shape: {data.shape}")
        print("Expected shape: (60, 2160, 4320)")

        # if lat and lon is wrong, correct
        if data.shape == (60, 4320, 2160):
            print("Fixing dimension order...")
            data = np.transpose(data, (0, 2, 1))
        
        # Create a new NetCDF file for this dataset
        output_filename = f"{key}.nc"
        if key.lower() == "sunflower":
            output_filename = "Sunflower.nc"

        output_nc_file = os.path.join(HA_output_path, output_filename)
        
        with Dataset(output_nc_file, 'w', format='NETCDF4') as ncfile:
                      
            ncfile.createDimension('year', data.shape[0])
            ncfile.createDimension('lat', data.shape[1])
            ncfile.createDimension('lon', data.shape[2])

            ncfile.createVariable('year', 'f4', ('year',))[:] = np.arange(1961, 2021)
            ncfile.createVariable('lat', 'f4', ('lat',))[:] = np.linspace(90 - 0.041667, -90 + 0.041667, data.shape[1])
            ncfile.createVariable('lon', 'f4', ('lon',))[:] = np.linspace(-180 + 0.041667, 180 - 0.041667, data.shape[2])

            var = ncfile.createVariable('HA', data.dtype, ('year', 'lat', 'lon'))
            var[:, :, :] = data            
        
        print(f"Saved key '{key}' to {output_nc_file}") # Here the key 'sunflower' need to be manually changed to 'Sunflower' to match the name in fertilizer files

# %%  2. Sum up the total harvest area to 0.5 degree resolution

HA_5arcm_path = 'HA_5arcm'

HA_05d_path = 'HA_05d'
os.makedirs(HA_05d_path, exist_ok=True)

nc_files = glob.glob(os.path.join(HA_5arcm_path, '*.nc'))

for nc_file_name in nc_files:
    
    nc_file = xr.open_dataset(nc_file_name)    
    data = nc_file['HA'][:]   
           
    # Create latitude and longitude arrays
    lat = np.linspace(90 - (0.083333 / 2), -90 + (0.083333 / 2), 2160, dtype=np.float64)
    lon = np.linspace(-180 + (0.083333 / 2), 180 - (0.083333 / 2), 4320, dtype=np.float64)
            
    # Create an xarray DataArray
    a = xr.DataArray(
         data,
         dims=("year", "lat", "lon"),
         coords={
             "year": np.arange(1961, 2021),
             "lat": lat,
             "lon": lon,
                },
            )
            
    upscaled_no_nan = a.coarsen(lat=6, lon=6, boundary="trim").sum()
    upscaled = upscaled_no_nan.where(upscaled_no_nan != 0, np.nan)
    
    file_name = os.path.basename(nc_file_name)
    output_nc_file = os.path.join(HA_05d_path, f"{file_name}")    
    upscaled.to_netcdf(output_nc_file)
    print(f"Saved upscaled data for {output_nc_file}")


# %% 3. Calculate the total amount of manure input for each pixel at 0.5 degree resolution (harvest area * N fertilization rate)

# Output path:
N_manure_5arcm_path = 'N_Manure_amount_5arcm'
N_manure_05d_path = 'N_Manure_amount_05d'

os.makedirs(N_manure_5arcm_path, exist_ok=True)
os.makedirs(N_manure_05d_path, exist_ok=True)

# Naming format of .nc file for the harvest area of each crop: Barley.nc
HA_5arcm_path = 'HA_5arcm'
# Naming format of .nc file for the manure input of each crop: N_application_rate_Barley_1961-2020.nc
Manure_5arcm_path = 'N_Manure_Input_Original'

crop_namelist = ['Barley', 'Cassava', 'Cotton', 'Fruits', 'Groundnut', 'Maize', 'Millet', 'Oilpalm', 'Others crops', 'Potato', 'Rapeseed', 'Rice', 'Rye', 'Sorghum', 'Soybean', 'Sugarbeet', 'Sugarcane', 'Sweetpotato', 'Vegetables', 'Wheat', 'Sunflower']

for crop in crop_namelist:
    HA_5arcm = os.path.join(HA_5arcm_path, f"{crop}.nc")
    Manure_5arcm = os.path.join(Manure_5arcm_path, f"N_application_rate_{crop}_1961-2020.nc")
    
    nc_HA = xr.open_dataset(HA_5arcm)    
    data_HA = nc_HA['HA'][:].transpose("year", "lat", "lon") # read and correct shape to year, lat, lon if needed
    
    nc_file = xr.open_dataset(Manure_5arcm)    
    data_Manure = nc_file['N_manure_Total'][:].transpose("year", "lat", "lon") # read and correct shape to year, lat, lon if needed
    
    # Correct the coordinates with proper shapes
    years = np.arange(1961, 2021)  # 60 years
    lon = np.linspace(-180 + (0.083333 / 2), 180 - (0.083333 / 2), 4320)  # 4320 longitudes
    lat = np.linspace(90 - (0.083333 / 2), -90 + (0.083333 / 2), 2160)  # 2160 latitudes
    
    
    # Reassign the coordinates to the DataArrays
    data_HA.coords["year"] = years
    data_HA.coords["lon"] = lon
    data_HA.coords["lat"] = lat
    
    data_Manure.coords["year"] = years
    data_Manure.coords["lon"] = lon
    data_Manure.coords["lat"] = lat
    
    # Calculate the total amount of N manure input of the harvest area within a 5 arc minute pixel
    N_manure_amount = data_HA * data_Manure  
        
    # Create an xarray DataArray
    b = xr.DataArray(
         N_manure_amount,
         dims=("year", "lat", "lon"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "N_manure_amount",
         attrs={
         "units": "kg"
                }
            )

# 4. Sum up the total N manure input amount at the 0.5 degree resolution
    upscaled_no_nan = b.coarsen(lat=6, lon=6, boundary="trim").sum()
    upscaled = upscaled_no_nan.where(upscaled_no_nan != 0, np.nan)    
      
    output_N_manure_amount_5arcm = os.path.join(N_manure_5arcm_path, f"N_manure_input_amount_{crop}_1961-2020.nc") 
    output_N_manure_amount_05d = os.path.join(N_manure_05d_path, f"N_manure_input_amount_{crop}_1961-2020.nc")
    
    b.to_netcdf(output_N_manure_amount_5arcm)
    upscaled.to_netcdf(output_N_manure_amount_05d)
    print(f"Total N manure input amount for {crop} has been saved")
    
# %% 5. Divide the N manure input amount at 0.5 degree resolution by harvest area at each pixel

# Input path for N manure input amount at 0.5 degree
N_manure_05d_path = 'N_Manure_amount_05d'
# Input path for total harvest area at 0.5 degree
HA_05d_path = 'HA_05d'

# Output path for N manure application rate at 0.5 degree
N_Manure_app_rate_05d_path = 'N_Manure_app_rate_05d'
os.makedirs(N_Manure_app_rate_05d_path, exist_ok=True)

crop_namelist = ['Barley', 'Cassava', 'Cotton', 'Fruits', 'Groundnut', 'Maize', 'Millet', 'Oilpalm', 'Others crops', 'Potato', 'Rapeseed', 'Rice', 'Rye', 'Sorghum', 'Soybean', 'Sugarbeet', 'Sugarcane', 'Sweetpotato', 'Vegetables', 'Wheat', 'Sunflower']

for crop in crop_namelist:
    HA_05d = os.path.join(HA_05d_path, f"{crop}.nc")
    Manure_05d = os.path.join(N_manure_05d_path, f"N_manure_input_amount_{crop}_1961-2020.nc")
    
    nc_HA = xr.open_dataset(HA_05d)    
    data_HA = nc_HA['HA'][:].transpose("year", "lat", "lon") # read and correct shape to year, lat, lon if needed
    
    nc_file = xr.open_dataset(Manure_05d)    
    data_Manure = nc_file['N_manure_amount'][:].transpose("year", "lat", "lon") # read and correct shape to year, lat, lon if needed
    
    # Correct the coordinates with proper shapes
    years = np.arange(1961, 2021)  # 60 years
    lon = np.linspace(-180 + (0.5 / 2), 180 - (0.5 / 2), 720)  
    lat = np.linspace(90 - (0.5 / 2), -90 + (0.5 / 2), 360)  
    
    
    # Reassign the coordinates to the DataArrays
    data_HA.coords["year"] = years
    data_HA.coords["lon"] = lon
    data_HA.coords["lat"] = lat
    
    data_Manure.coords["year"] = years
    data_Manure.coords["lon"] = lon
    data_Manure.coords["lat"] = lat
    
    # Calculate the total amount of N manure input of the harvest area within a 5 arc minute pixel
    N_manure_application_rate = data_Manure / data_HA
    
    # Create an xarray DataArray
    c = xr.DataArray(
         N_manure_application_rate,
         dims=("year", "lat", "lon"),
         coords={
             "year": np.arange(1961, 2021),
             "lon": lon,
             "lat": lat,
                },
         name = "Manure_N_application_rate",
         attrs={
         "units": "kg/ha harvest area"
                }
            )   
        
    output_N_manure_app_rate_05d = os.path.join(N_Manure_app_rate_05d_path, f"N_manure_app_rate_{crop}_1961-2020.nc")
    c.to_netcdf(output_N_manure_app_rate_05d)
    print(f"N manure application rate for {crop} has been calculated and saved")