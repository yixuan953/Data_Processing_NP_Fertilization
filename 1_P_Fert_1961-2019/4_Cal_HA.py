# This code is used to calculate the total harvest area at half degree and save as .nc format

import rasterio
import numpy as np
import glob
import os
import xarray as xr 

crop_types = ["Rice", "Soybean", "Wheat", "Maize"] # The dataset also contains other crop types (in total 13 major crop groups)
years = range(1961,2020) # Do not contains 2020

# Path of the original .tiff files
input_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/Fertilization/P_Inorganic_1961-2019/HA_P_Inorganic_1961-2019'
process_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/P_Fert_Inorg_1961-2019/HA_5arcmin'
output_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/P_Fert_Inorg_1961-2019/HA_05d'
tiff_files = glob.glob(os.path.join(input_path,'*.tiff'))
area_file = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/General/pixel_area_ha_5arcmin.tiff'
with rasterio.open(area_file) as src1:
    area_5arcmin = src1.read(1)  # Read first band
    meta = src1.meta  # Copy metadata


# # Get the meta, lon, and lat from one example data
with rasterio.open(tiff_files[0]) as src_examp:
    meta = src_examp.meta
    lon = np.linspace(src_examp.bounds.left, src_examp.bounds.right, src_examp.width)
    lat = np.linspace(src_examp.bounds.top, src_examp.bounds.bottom, src_examp.height)

# # Create an empty data array
data = np.empty((len(years), len(lat), len(lon)), dtype=np.float32)
area = np.empty((len(years), len(lat), len(lon)), dtype=np.float32)

# # Read the value from each .tiff file, and save thme in .nc format
for crop in crop_types:
    for year in years:
        f = os.path.join(input_path, f"{crop}_{year}.tiff")
        i = year-1961
        with rasterio.open(f) as src:
            data[i, :, :] = src.read(1)
            area[i, :, :] = data[i, :, :] * area_5arcmin

    ds = xr.Dataset(
        {"HA": (["year", "lat", "lon"], area)},
         coords={"year": years, "lat": lat, "lon": lon}
        )

    output_nc_5arcmin = os.path.join(process_path, f"{crop}_HA_1961-2019.nc")
    ds.to_netcdf(output_nc_5arcmin)  
    print(f"TIFF file has been transformed to {output_nc_5arcmin}")

# Data upscaling
# Create latitude and longitude arrays
lat = np.linspace(90 - (0.083333 / 2), -90 + (0.083333 / 2), 2160, dtype=np.float64)
lon = np.linspace(-180 + (0.083333 / 2), 180 - (0.083333 / 2), 4320, dtype=np.float64)

# Read the variables from each .nc file
for crop in crop_types:
    f = os.path.join(process_path, f"{crop}_HA_1961-2019.nc")
    nc_file_5arcmin = xr.open_dataset(f)
    data_HA = nc_file_5arcmin["HA"][:]

    b = xr.DataArray(
        data_HA,
        dims=("year", "lat", "lon"),
        coords={
            "year": np.arange(1961, 2020),
            "lat": lat,
            "lon": lon,
        },
        attrs={
            "long_name": f"Harvest Area",
            "units": "hectar",  # Replace with actual units
            "description": f"Upscaled from 5 arcmin to 0.5 degree",
        },
    )

    # Resample to 0.5-degree resolution (coarsen 6×6)
    HA_upscaled_no_nan = b.coarsen(lat=6, lon=6, boundary="trim").sum()
    HA_upscaled = HA_upscaled_no_nan.where(HA_upscaled_no_nan != 0, np.nan)

    # Add attributes
    HA_upscaled.attrs = b.attrs

    # Save new NetCDF file for P
    output_nc_file = os.path.join(output_path, f"{crop}_HA_05d_1961-2019.nc")
    HA_upscaled.to_netcdf(output_nc_file)
    print(f"Saved upscaled data for {output_nc_file}")