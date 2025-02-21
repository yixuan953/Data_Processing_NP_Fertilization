# This code is used to 
# 1. Calculate the inorganic N fertilizer input
# 2. Downscale the file 

import h5py
import xarray as xr
import os
import glob
import numpy as np

# Path for all 
folder_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Fertilization/N_Fert'
h5_files = glob.glob(os.path.join(folder_path, '*.h5'))
output_path = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_inorganic'

for h5_file_name in h5_files:
    print(f"Processing .h5 file: {h5_file_name}")
    # Open the .h5 file
    h5file = h5py.File(os.path.join(folder_path, h5_file_name), 'r')

    # Calculate the Urea N input seperately  
    urea1 = h5file['Urea_deep'][:] 
    urea2 = h5file['Urea_surface'][:]
    urea1 = np.ma.masked_invalid(urea1)
    urea2 = np.ma.masked_invalid(urea2)
    urea1_no_nan = np.ma.filled(urea1, 0)
    urea2_no_nan = np.ma.filled(urea2, 0)
    
    Urea_N_fert = None
    Urea_N_fert = np.zeros_like(urea1_no_nan, dtype=np.float32)
    Urea_N_fert_no_nan = urea1_no_nan + urea2_no_nan
    Urea_N_fert = np.where(Urea_N_fert_no_nan == 0, np.nan, Urea_N_fert_no_nan)
    print(f"Urea N input of {h5_file_name} have been summed up")

    Inorganic_N_fert_no_nan = None
    Inorganic_N_fert_no_nan = np.zeros_like(Urea_N_fert, dtype=np.float32)
    
    # Sum up all the N input of all of the inorganic fertilizer input   
    variables = ['AA_deep', 'AA_surface', 'AN_deep', 'AN_surface',
                 'AP_deep', 'AP_surface', 'AS_deep', 'AS_surface', 
                 'CAN_deep', 'CAN_surface', 'NK_deep', 'NK_surface', 
                 'NPK_deep', 'NPK_surface', 'NS_deep', 'NS_surface', 
                 'ONP_deep', 'ONP_surface', 'ONS_deep', 'ONS_surface']   
    
    for variable_name in variables:
        data = h5file[variable_name][:]
        data = np.ma.masked_invalid(data)
        data_no_nan = np.ma.filled(data, 0)
        Inorganic_N_fert_no_nan += data_no_nan

    Inorganic_N_fert = np.where(Inorganic_N_fert_no_nan == 0, np.nan, Inorganic_N_fert_no_nan)
    print(f"Inorganic fertilizer N input of {h5_file_name} have been summed up")   
        
    # Coordinates
    coords = {
        'year': np.arange(1961, 2021),  # Years 1961-2020
        'lon': np.linspace(-180, 180, 4320),  # Longitude
        'lat': np.linspace(90, -90, 2160),   # Latitude
    }
    
    # Create Dataset
    dataset = xr.Dataset(
        {
            'Inorganic_N_fert': (['year', 'lon', 'lat'], Inorganic_N_fert, {'units': 'kg N/ha harvest area'}),
            'Urea_N_fert': (['year', 'lon', 'lat'], Urea_N_fert, {'units': 'kg N/ha harvest area'}),
        },
        coords=coords
    )
    
    # Add global attributes
    dataset.attrs['description'] = "Annual inorganic N fertilizer input (kg per ha harvest area)"
    
    # Create an xarray DataArray
    base_name = os.path.basename(h5_file_name)
    nc_file_name = base_name.replace('.h5', '.nc')
    nc_file = os.path.join(output_path, nc_file_name)

    dataset.to_netcdf(nc_file, format='NETCDF4', engine='netcdf4', encoding={
        'Inorganic_N_fert': {'zlib': True},
        'Urea_N_fert': {'zlib': True}
    })
        
    print(f"{h5_file_name} has been successfully tranformed to .nc")
    
        # Close the .h5 file
    h5file.close()