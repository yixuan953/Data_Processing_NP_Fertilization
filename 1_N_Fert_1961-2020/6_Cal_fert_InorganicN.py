#%% This code is used to 
# 1. Calculate the inorganic N fertilizer input
# 2. Downscale the file 

import h5py
import xarray as xr
import os
import glob
import numpy as np

# Path for all 
folder_path = '../../../1_Raw_data/Fertilizer/Fertilization/N_Fert'
h5_files = glob.glob(os.path.join(folder_path, '*.h5'))

output_path = 'N_inorganic'
os.makedirs(output_path, exist_ok=True)

#%%
for h5_file_name in h5_files:
    print(f"Processing .h5 file: {h5_file_name}")
    # Open the .h5 file
    h5file = h5py.File(h5_file_name, 'r')

    # Calculate the Urea N input seperately  
    urea1 = np.ma.filled(np.ma.masked_invalid(h5file['Urea_deep'][:]), 0)
    urea2 = np.ma.filled(np.ma.masked_invalid(h5file['Urea_surface'][:]), 0)
    
    Urea_N_fert_no_nan = urea1 + urea2
    Urea_N_fert = np.where(Urea_N_fert_no_nan == 0, np.nan, Urea_N_fert_no_nan)
    print(f"Urea N input of {h5_file_name} have been summed up")

    Inorganic_N_fert_no_nan = np.zeros_like(Urea_N_fert, dtype=np.float32)
    
    # Sum up all the N input of all of the inorganic fertilizer input   
    variables = ['AA_deep', 'AA_surface', 'AN_deep', 'AN_surface',
                 'AP_deep', 'AP_surface', 'AS_deep', 'AS_surface', 
                 'CAN_deep', 'CAN_surface', 'NK_deep', 'NK_surface', 
                 'NPK_deep', 'NPK_surface', 'NS_deep', 'NS_surface', 
                 'ONP_deep', 'ONP_surface', 'ONS_deep', 'ONS_surface']   
    
    for variable_name in variables:
        data = np.ma.filled(np.ma.masked_invalid(h5file[variable_name][:]), 0)
        Inorganic_N_fert_no_nan += data

    Inorganic_N_fert = np.where(Inorganic_N_fert_no_nan == 0, np.nan, Inorganic_N_fert_no_nan)
    print(f"Inorganic fertilizer N input of {h5_file_name} have been summed up")

    #check coordinates
    print("Inorganic_N_fert shape:", Inorganic_N_fert.shape)
    print("Expected shape: (60, 2160, 4320)")

    # if lat and lon is wrong, correct
    if Inorganic_N_fert.shape == (60, 4320, 2160):
        print("Fixing dimension order...")
        Inorganic_N_fert = np.transpose(Inorganic_N_fert, (0, 2, 1))
        Urea_N_fert = np.transpose(Urea_N_fert, (0, 2, 1))   
        
    # Coordinates
    coords = {
        'year': np.arange(1961, 2021),
        'lon': np.linspace(-180 + (0.083333 / 2), 180 - (0.083333 / 2), 4320, dtype=np.float64),
        'lat': np.linspace(90 - (0.083333 / 2), -90 + (0.083333 / 2), 2160, dtype=np.float64),
    }
    
    # Create Dataset
    dataset = xr.Dataset(
        {
            'Inorganic_N_fert': (['year', 'lat', 'lon'], Inorganic_N_fert, {'units': 'kg N/ha harvest area'}),
            'Urea_N_fert': (['year', 'lat', 'lon'], Urea_N_fert, {'units': 'kg N/ha harvest area'}),
        },
        coords=coords
    )

    dataset = dataset.assign_coords(lat=("lat", coords["lat"]), lon=("lon", coords["lon"]))

    
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
# %%
