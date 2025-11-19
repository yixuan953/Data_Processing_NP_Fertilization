# This code is used to 
# 1. Calculate the residue N fertilizer input
# 2. Downscale the file 

import h5py
import xarray as xr
import os
import glob
import numpy as np

# Path for all 
folder_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/Fertilization/N_all_fert_h5'
Crops = ["Maize", "Rice", "Wheat", "Soybean"]

output_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/N_Residue_app_rate_5arcm'

for crop in Crops:
    h5_file_name = os.path.join(folder_path, f"N_application_rate_{crop}_1961-2020.h5")
    print(f"Processing .h5 file: {h5_file_name}")
    # Open the .h5 file
    h5file = h5py.File(h5_file_name, 'r')

    # Calculate the Urea N input seperately  
    Residue1 = np.ma.filled(np.ma.masked_invalid(h5file['CR_surface'][:]), 0)
    Residue2 = np.ma.filled(np.ma.masked_invalid(h5file['CR_deep'][:]), 0)
    
    Residue_N_fert_no_nan = Residue1 + Residue2
    Residue_N_fert = np.where(Residue_N_fert_no_nan == 0, np.nan, Residue_N_fert_no_nan)
    print(f"Residue N input of {h5_file_name} have been summed up")

    #check coordinates
    print("Residue_N_fert shape:", Residue_N_fert.shape)
    print("Expected shape: (60, 2160, 4320)")

    # if lat and lon is wrong, correct
    if Residue_N_fert.shape == (60, 4320, 2160):
        print("Fixing dimension order...")
        Residue_N_fert = np.transpose(Residue_N_fert, (0, 2, 1))
        
    # Coordinates
    coords = {
        'year': np.arange(1961, 2021),
        'lon': np.linspace(-180 + (0.083333 / 2), 180 - (0.083333 / 2), 4320, dtype=np.float64),
        'lat': np.linspace(90 - (0.083333 / 2), -90 + (0.083333 / 2), 2160, dtype=np.float64),
    }
    
    # Create Dataset
    dataset = xr.Dataset(
        {
            'Residue_N_fert': (['year', 'lat', 'lon'], Residue_N_fert, {'units': 'kg N/ha harvest area'})
        },
        coords=coords
    )

    dataset = dataset.assign_coords(lat=("lat", coords["lat"]), lon=("lon", coords["lon"]))
    
    # Add global attributes
    dataset.attrs['description'] = "Annual Residue N fertilizer input (kg per ha harvest area)"
    
    # Create an xarray DataArray
    base_name = os.path.basename(h5_file_name)
    nc_file_name = base_name.replace('.h5', '.nc')
    nc_file = os.path.join(output_path, nc_file_name)

    dataset.to_netcdf(nc_file, format='NETCDF4', engine='netcdf4', encoding={
        'Residue_N_fert': {'zlib': True}
    })
        
    print(f"{h5_file_name} has been successfully tranformed to .nc")
    
    # Close the .h5 file
    h5file.close()