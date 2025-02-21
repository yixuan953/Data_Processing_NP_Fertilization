# This code is used to extract manure N input from .hc files and transform it into .nc files

import h5py
import xarray as xr
import numpy as np
import os
import glob

folder_path = '../../../1_Raw_data/Fertilizer/Fertilization/N_Fert'
output_path = 'N_Manure_Input_Original'
os.makedirs(output_path, exist_ok=True)

h5_files = glob.glob(os.path.join(folder_path, '*.h5'))

for h5_file_name in h5_files:
    print(f"Processing .h5 file: {h5_file_name}")

    # Open the .h5 file
    h5file = h5py.File(h5_file_name, 'r')
    data1 = h5file['MA_surface'][:] # Here the surface and deep manure input is dependent on whether tillage is applied
    data2 = h5file['MA_deep'][:] # Manure input is assumed as Ma_deep if tillage is applied
    
    #check coordinates
    print("data1 shape:", data1.shape)
    print("Expected shape: (60, 2160, 4320)")

    # if lat and lon is wrong, correct
    if data1.shape == (60, 4320, 2160):
        print("Fixing dimension order...")
        data1 = np.transpose(data1, (0, 2, 1))
        data2 = np.transpose(data2, (0, 2, 1))   
        
    # Coordinates
    coords = {
        'year': np.arange(1961, 2021),
        'lon': np.linspace(-180 + (0.083333 / 2), 180 - (0.083333 / 2), 4320, dtype=np.float64),
        'lat': np.linspace(90 - (0.083333 / 2), -90 + (0.083333 / 2), 2160, dtype=np.float64),
    }
    
    
    # Create Dataset
    dataset = xr.Dataset(
        {
            'N_manure_surface': (['year', 'lat', 'lon'], data1, {'units': 'kg N/ha harvest area'}),
            'N_manure_deep': (['year', 'lat', 'lon'], data2, {'units': 'kg N/ha harvest area'}),
        },
        coords=coords
    )
    
    dataset = dataset.assign_coords(lat=("lat", coords["lat"]), lon=("lon", coords["lon"]))

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