import numpy as np
import os
import xarray as xr
import glob

# %% 1. Calculate the total amount of inorganic input for each pixel at 0.5 degree (harvest area * P fertilization rate)

# Output path for storing upscaled inorganic P fertilization data
P_inorg_05d_path = 'P_Inorg_amount_05d'
os.makedirs(P_inorg_05d_path, exist_ok=True)

# Input path for harvest area files (Crop Mask)
HA_005d_path = '../../../1_Raw_data/Fertilizer/Fertilization/P_Fert/CropMask'
# Input path for P2O5 input data
Inorg_005d_path = '../../../1_Raw_data/Fertilizer/Fertilization/P_Fert/AppRate'

# Define latitude and longitude arrays for 0.05-degree resolution
lat_005d = np.linspace(90 - (0.05 / 2), -90 + (0.05 / 2), 3600)
lon_005d = np.linspace(-180 + (0.05 / 2), 180 - (0.05 / 2), 7200)

# Define the crop list for processing
crop_namelist = ['maize', 'rice', 'soybean', 'wheat']

for crop in crop_namelist:
    # Define file paths
    HA_005d = os.path.join(HA_005d_path, f"CROPGRIDSv1.08_{crop}.nc")
    Inorg_005d = os.path.join(Inorg_005d_path, f"NPKGRIDSv1.08_{crop}.nc")
    
    # Open NetCDF files
    nc_HA = xr.open_dataset(HA_005d)    
    data_HA = nc_HA['harvarea'][:].where(nc_HA['harvarea'] >= 0, np.nan)
    
    nc_file = xr.open_dataset(Inorg_005d)    
    data_Inorg = nc_file['P2O5rate'][:].where(nc_file['P2O5rate'] >= 0, np.nan)
    
    # Ensure latitude direction is from 90 to -90
    if data_HA.lat[0] < data_HA.lat[-1]:
        data_HA = data_HA[::-1, :]
        data_Inorg = data_Inorg[::-1, :]

    # Assign correct latitude and longitude coordinates
    data_HA = data_HA.assign_coords(lat=lat_005d, lon=lon_005d)
    data_Inorg = data_Inorg.assign_coords(lat=lat_005d, lon=lon_005d)
    
    # Calculate the total amount of inorganic P2O5 input (kg per pixel)
    P2O5_amount = data_HA * data_Inorg 
    
    # Create xarray DataArray with appropriate dimensions and attributes
    a = xr.DataArray(
         P2O5_amount,
         dims=("lat", "lon"),
         coords={"lat": lat_005d, "lon": lon_005d},
         name="P2O5 input",
         attrs={"units": "kg P2O5"}
    )
    
    # Upscale from 0.05° to 0.5° resolution
    a_upscaled_no_nan = a.coarsen(lat=10, lon=10, boundary="trim").sum()
    a_upscaled = a_upscaled_no_nan.where(a_upscaled_no_nan != 0, np.nan)    

    # Ensure latitude remains from 90 to -90
    lat_05d = np.linspace(90 - (0.5 / 2), -90 + (0.5 / 2), 360)
    lon_05d = np.linspace(-180 + (0.5 / 2), 180 - (0.5 / 2), 720)
    a_upscaled = a_upscaled.assign_coords(lat=lat_05d, lon=lon_05d)
      
    # Save output NetCDF file
    output_P2O5_amount_05d = os.path.join(P_inorg_05d_path, f"P2O5_amount_{crop}.nc")
    a_upscaled.to_netcdf(output_P2O5_amount_05d)
    print(f"P2O5 input amount for {crop} has been saved")

# %% 2. Sum up the total harvest area to 0.5 degree resolution

# Output path for storing upscaled harvest area data
HAcr_05d_path = 'HAcr_05d'
os.makedirs(HAcr_05d_path, exist_ok=True)

nc_files = glob.glob(os.path.join(HA_005d_path, '*.nc'))

for nc_file_name in nc_files:
    # Open NetCDF file
    nc_file = xr.open_dataset(nc_file_name)    
    data = nc_file['harvarea'][:].where(nc_file['harvarea'] >= 0, np.nan)
    
    # Ensure latitude direction is from 90 to -90
    if data.lat[0] < data.lat[-1]:
        data = data[::-1, :]

    # Assign correct latitude and longitude coordinates
    data = data.assign_coords(lat=lat_005d, lon=lon_005d)

    # Upscale from 0.05° to 0.5° resolution
    upscaled_no_nan = data.coarsen(lat=10, lon=10, boundary="trim").sum()
    upscaled = upscaled_no_nan.where(upscaled_no_nan != 0, np.nan)
    upscaled = upscaled.assign_coords(lat=lat_05d, lon=lon_05d)

    # Save output NetCDF file
    file_name = os.path.basename(nc_file_name)
    output_nc_file = os.path.join(HAcr_05d_path, f"Upscaled05d_{file_name}")    
    upscaled.to_netcdf(output_nc_file)
    print(f"Saved upscaled data as {output_nc_file}")

# %% 3. Calculate the inorganic P fertilizer application rate

# Output path for storing inorganic P application rate data at 0.5-degree resolution
P_inorg_app_rate_05d_path = 'P_Inorg_app_rate_05d'
os.makedirs(P_inorg_app_rate_05d_path, exist_ok=True)

for crop in crop_namelist:
    HAcr_05d = os.path.join(HAcr_05d_path, f"Upscaled05d_CROPGRIDSv1.08_{crop}.nc")
    Inorg_05d = os.path.join(P_inorg_05d_path, f"P2O5_amount_{crop}.nc")
    
    # Open NetCDF files
    nc_HA = xr.open_dataset(HAcr_05d)    
    data_HA = nc_HA['harvarea'][:]
    
    nc_Inorg = xr.open_dataset(Inorg_05d)    
    data_Inorg = nc_Inorg['P2O5 input'][:]

    # Ensure latitude direction is from 90 to -90
    if data_HA.lat[0] < data_HA.lat[-1]:
        data_HA = data_HA[::-1, :]
        data_Inorg = data_Inorg[::-1, :] 

    # Assign correct latitude and longitude coordinates
    data_HA = data_HA.assign_coords(lat=lat_05d, lon=lon_05d)
    data_Inorg = data_Inorg.assign_coords(lat=lat_05d, lon=lon_05d)

    # Compute inorganic P application rate (kg P/ha)
    P_inorg_application_rate = (0.465 * data_Inorg) / data_HA.where(data_HA > 0)

    # Create xarray DataArray
    a = xr.DataArray(
        P_inorg_application_rate,
        dims=("lat", "lon"),
        coords={"lat": lat_05d, "lon": lon_05d},
        name="Inorg_P_application_rate",
        attrs={"units": "kg P/ha harvest area"}
    )

    # Save output NetCDF file
    output_P_inorg_app_rate_05d = os.path.join(P_inorg_app_rate_05d_path, f"P_inorg_app_rate_{crop}.nc")
    a.to_netcdf(output_P_inorg_app_rate_05d)
    print(f"P inorganic fertilizer application rate for {crop} has been calculated and saved")
