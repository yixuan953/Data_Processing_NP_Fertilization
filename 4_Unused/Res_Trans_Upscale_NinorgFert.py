# This code is used to:
# 1) Upscale the inorganic N fertilizer input into 0.5 degree
# 2) Sum up the total inorganic N fertilizer input (Urea + Others)

import glob
import os
import numpy as np
import xarray as xr

folder_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_inorganic'
output_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_inorganic_05d'
nc_files = glob.glob(os.path.join(folder_path, '*.nc'))

# As we would like to transform the original data size (60, 4320, 2160) to (60, 720, 360)
scale_factor = 6  

for nc_file_name in nc_files:
    print(f"Processing {nc_file_name}")
    
    ds = xr.open_dataset(nc_file_name)
    # Extract the variables
    Urea_N_fert = ds['Urea_N_fert'].values 
    Inorganic_N_fert = ds['Inorganic_N_fert'].values
    ds.close()
    
    # Reshape data to group blocks of 6x6
    Urea_N_fert_reshaped = Urea_N_fert.reshape(
        (Urea_N_fert.shape[0],
         Urea_N_fert.shape[1] // scale_factor,
         scale_factor, 
         Urea_N_fert.shape[2] // scale_factor, 
         scale_factor)
    )
    Urea_N_upscaled = np.nanmean(Urea_N_fert_reshaped, axis=(2, 4))
    
    Inorganic_N_fert_reshaped = Inorganic_N_fert.reshape(
        (Inorganic_N_fert.shape[0], 
         Inorganic_N_fert.shape[1] // scale_factor, 
         scale_factor, 
         Inorganic_N_fert.shape[2] // scale_factor, 
         scale_factor)
    )
    Inorganic_N_upscaled = np.nanmean(Inorganic_N_fert_reshaped, axis=(2, 4))
    
    # Define the new latitude and longitude
    years = np.arange(1961, 2021)  # Years 1961-2020
    lon_new = np.linspace(-180, 180, 720, endpoint=False)
    lat_new = np.linspace(90, -90, 360, endpoint=False)  

    # Write the upscaled data into a new .nc file
    new_nc_file_name = os.path.join(output_path, nc_file_name)
    ds_new = xr.Dataset()
    ds_new['year'] = ('year', years)
    ds_new['lon'] = ('lon', lon_new)
    ds_new['lat'] = ('lat', lat_new)
    ds_new['Urea_N_fert'] = (('year', 'lon', 'lat'), Urea_N_fert_reshaped)
    ds_new['Inorganic_N_fert'] = (('year', 'lon', 'lat'), Inorganic_N_fert_reshaped)
    ds_new['Total_inorganic_N_fert'] = (('year', 'lon', 'lat'), Urea_N_fert_reshaped + Inorganic_N_fert_reshaped)
        
    # Add units attributes
    ds_new['lon'].attrs['units'] = 'degrees_east'
    ds_new['lat'].attrs['units'] = 'degrees_north'
    ds_new['Urea_N_fert'].attrs['units'] = 'Kg N/ha harvest area'
    ds_new['Inorganic_N_fert'].attrs['units'] = 'Kg N/ha harvest area'
    ds_new['Total_inorganic_N_fert'].attrs['units'] = 'Kg N/ha harvest area'
    
    # Save to a new netcdf file
    ds_new.to_netcdf(new_nc_file_name)
    ds_new.close()
    print(f"Upscaled data saved to {new_nc_file_name}")     