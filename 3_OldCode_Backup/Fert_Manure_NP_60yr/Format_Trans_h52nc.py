# This code is used to extract manure N input from .hc files and transform it into .nc files

import h5py
import xarray as xr
import numpy as np
import os
import glob

folder_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Fertilization'
output_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Fertilization/Processed_data/N_Manure_Input_Original'
h5_files = glob.glob(os.path.join(folder_path, '*.h5'))

for h5_file_name in h5_files:
    print(f"Processing .h5 file: {h5_file_name}")

    # Open the .h5 file
    h5file = h5py.File(os.path.join(folder_path, h5_file_name), 'r')
    data1 = h5file['MA_surface'][:] # Here the surface and deep manure input is dependent on whether tillage is applied
    data2 = h5file['MA_deep'][:] # Manure input is assumed as Ma_deep if tillage is applied
    
    # Coordinates
    coords = {
        'year': np.arange(1961, 2021),  # Years 1961-2020
        'lon': np.linspace(-180, 180, 4320),  # Longitude
        'lat': np.linspace(90, -90, 2160),   # Latitude
    }
    
    # Create Dataset
    dataset = xr.Dataset(
        {
            'N_manure_surface': (['year', 'lon', 'lat'], data1, {'units': 'kg N/ha harvest area'}),
            'N_manure_deep': (['year', 'lon', 'lat'], data2, {'units': 'kg N/ha harvest area'}),
        },
        coords=coords
    )
    
    # Add global attributes
    dataset.attrs['description'] = "Annual N manure input (kg per ha harvest area)"
    
    # Create an xarray DataArray
    base_name = os.path.basename(h5_file_name)
    nc_file_name = base_name.replace('.h5', '.nc')
    nc_file = os.path.join(output_path, nc_file_name)

    dataset.to_netcdf(nc_file, format='NETCDF4', engine='netcdf4', encoding={
        'N_manure_surface': {'zlib': True},
        'N_manure_deep': {'zlib': True}
    })
        
    print(f"Renamed {h5_file_name} to {nc_file_name}")
    
    # Close the .h5 file
    h5file.close()