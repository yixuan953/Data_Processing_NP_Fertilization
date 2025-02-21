## This code is used to transform PNratio.tif to PNratio.nc:
## 1) Resampling the .tif file to lon [-179.75 179.75], lat [89.75, -89.75]
## 2) Replace no-data values with NaN
## 3) Store the data in the format of .nc file

import rasterio
import netCDF4 as nc
import numpy as np
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin

# Input TIFF file and output NetCDF file
input_tiff = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Fertilization/PNratio.tif'
output_nc = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Fertilization/PNratio.nc'

# Define the target grid
lon_start, lon_end, lon_step = -179.75, 180, 0.5
lat_start, lat_end, lat_step = -89.75, 90, 0.5

lons = np.arange(lon_start, lon_end, lon_step)
lats = np.arange(lat_start, lat_end, lat_step)
transform = from_origin(lon_start - lon_step / 2, lat_end + lat_step / 2, lon_step, lat_step)

# Define the target shape
height = len(lats)
width = len(lons)
target_shape = (height, width)

# Resample the TIFF to the target grid
with rasterio.open(input_tiff) as src:
    source_data = src.read(1)
    source_nodata = src.nodata
    source_transform = src.transform
    source_crs = src.crs

    # Prepare target array
    target_data = np.full(target_shape, source_nodata, dtype=source_data.dtype)

    # Reproject to the target grid
    reproject(
        source=source_data,
        destination=target_data,
        src_transform=source_transform,
        src_crs=source_crs,
        dst_transform=transform,
        dst_crs=source_crs,  # Assuming source and target use EPSG:4326
        resampling=Resampling.nearest,
    )

# Replace no-data values with NaN
target_data = np.where(target_data == source_nodata, np.nan, target_data)

# Save the resampled data to a NetCDF file
with nc.Dataset(output_nc, 'w', format='NETCDF4') as ds:
    # Create dimensions
    ds.createDimension('latitude', len(lats))
    ds.createDimension('longitude', len(lons))

# Create variables
    latitudes = ds.createVariable('latitude', np.float32, ('latitude',))
    longitudes = ds.createVariable('longitude', np.float32, ('longitude',))
    variable = ds.createVariable('data', np.float32, ('latitude', 'longitude'), fill_value=np.nan)

    # Assign metadata
    ds.description = "NetCDF representation of raster data resampled to a regular grid"
    ds.source = "Converted from GeoTIFF using Python"
    ds.crs = "EPSG:4326"  # CRS metadata

    latitudes.units = "degrees_north"
    longitudes.units = "degrees_east"
    variable.units = "Unknown"  # Replace with actual unit if known
    variable.long_name = "Raster Data"

    # Write data
    latitudes[:] = -lats
    longitudes[:] = lons
    variable[:, :] = target_data

print(f"NetCDF file created: {output_nc}")