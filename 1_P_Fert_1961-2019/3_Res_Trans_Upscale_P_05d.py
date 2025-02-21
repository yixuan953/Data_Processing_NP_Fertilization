# This code is used to:
# 1. Upscale the P2O5 input amount (kg) from 5arcmin to 0.5 degree
# 2. Calculate the P fertilizer input amount (kg) based on P2O5 input amount
# 3. Add variable descriptions to the .nc files

import os
import glob
import rasterio
import numpy as np
import xarray as xr

nutri_types = ["P2O5", "N"] # The others could be "K2O"
crop_types = ["Rice", "Soybean", "Wheat", "Maize"] # The dataset also contains other crop types (in total 13 major crop groups)

# Path of the original .nc files
input_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/P_Fert_Inorg_1961-2019/P_Inorg_Amount_5arcmin'

# Path of the output
output_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/P_Fert_Inorg_1961-2019/P_Inorg_Amount_05d'

# Create latitude and longitude arrays
lat = np.linspace(90 - (0.083333 / 2), -90 + (0.083333 / 2), 2160, dtype=np.float64)
lon = np.linspace(-180 + (0.083333 / 2), 180 - (0.083333 / 2), 4320, dtype=np.float64)

# Read the variables from each .nc file
for crop in crop_types:
    for nutri in nutri_types:
        f = os.path.join(input_path, f"{crop}_{nutri}_1961-2019.nc")
        nc_file_5arcmin = xr.open_dataset(f)
        data = nc_file_5arcmin[nutri][:]

        if nutri != "P2O5":
            # Create an xarray DataArray
            a = xr.DataArray(
                data,
                dims=("year", "lat", "lon"),
                coords={
                    "year": np.arange(1961, 2020),
                    "lat": lat,
                    "lon": lon,
                        },
                attrs={
                    "long_name": f"Summed up {nutri} input amount for {crop} at 0.5 degree",
                    "units": "kg",  # Replace with the actual units
                    "description": f"Upscaled {nutri} data for {crop} from 1961 to 2019",
                },
                )
        
            upscaled_no_nan = a.coarsen(lat=6, lon=6, boundary="trim").sum()
            upscaled = upscaled_no_nan.where(upscaled_no_nan != 0, np.nan)

            output_nc_file = os.path.join(output_path, f"{crop}_{nutri}_1961-2019.nc")    
            upscaled.to_netcdf(output_nc_file)
            print(f"Saved upscaled data for {output_nc_file}")
        
        else:
            data_P = data * 0.4346 # Convert from P2O5 to P

            # Create an xarray DataArray for P
            b = xr.DataArray(
                data_P,
                dims=("year", "lat", "lon"),
                coords={
                    "year": np.arange(1961, 2020),
                    "lat": lat,
                    "lon": lon,
                },
                attrs={
                    "long_name": f"Phosphorus (P) input for {crop}",
                    "units": "kg",  # Replace with actual units
                    "description": f"Converted from P2O5 input ({nutri}) using P2O5 × 0.4364",
                },
            )

            # Resample to 0.5-degree resolution (coarsen 6×6)
            P_upscaled_no_nan = b.coarsen(lat=6, lon=6, boundary="trim").sum()
            P_upscaled = P_upscaled_no_nan.where(P_upscaled_no_nan != 0, np.nan)

            # Add attributes
            P_upscaled.attrs = b.attrs

            # Save new NetCDF file for P
            output_nc_file = os.path.join(output_path, f"{crop}_P_1961-2019.nc")
            P_upscaled.to_netcdf(output_nc_file)
            print(f"Saved P input data to {output_nc_file}")

            # Create an xarray DataArray: same as N
            a = xr.DataArray(
                data,
                dims=("year", "lat", "lon"),
                coords={
                    "year": np.arange(1961, 2020),
                    "lat": lat,
                    "lon": lon,
                        },
                attrs={
                    "long_name": f"Summed up {nutri} input amount for {crop} at 0.5 degree",
                    "units": "kg",  # Replace with the actual units
                    "description": f"Upscaled {nutri} data for {crop} from 1961 to 2019",
                },
                )
        
            upscaled_no_nan = a.coarsen(lat=6, lon=6, boundary="trim").sum()
            upscaled = upscaled_no_nan.where(upscaled_no_nan != 0, np.nan)

            output_nc_file = os.path.join(output_path, f"{crop}_{nutri}_1961-2019.nc")    
            upscaled.to_netcdf(output_nc_file)
            print(f"Saved upscaled data for {output_nc_file}")