# This code is used to;
# 1) Calculate PN ratio based on N and P content in manure
# 2) Transform PN raito .tiff file into .nc file

import rasterio
import numpy as np
import netCDF4 as nc
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin
import os

# Load the TIFF files
Ncontent_tiff = '../../../1_Raw_data/Fertilizer/Fertilization/NManure_global_geotif/nmanure_global.tif'
Pcontent_tiff = '../../../1_Raw_data/Fertilizer/Fertilization/PManure_global_geotif/pmanure_global.tif'

# Input the output path
output_path = 'PNratio'
os.makedirs(output_path, exist_ok=True)

output_file = 'PNratio/PNratio.tif'
output_nc = 'PNratio/PNratio.nc'

with rasterio.open(Ncontent_tiff) as src1, rasterio.open(Pcontent_tiff) as src2:
    # Print the data information of P and N content in manure to ensure they have the same coordinates
    print("Metadata of Ncontent:", src1.meta)
    print("Metadata of Pcontent:", src2.meta)

    # Read data as arrays
    Ncontent = src1.read(1)
    Ncontent[Ncontent < 0.0001] = np.nan
    
    Pcontent = src2.read(1)
    Pcontent[Pcontent < 0.0001] = np.nan

    # Calculate the PN ratios
    PNratio = Pcontent/Ncontent

with rasterio.open(Ncontent_tiff) as src1:
    meta = src1.meta.copy()
    meta.update(dtype=rasterio.float32)

with rasterio.open(output_file, 'w', **meta) as dst:
    dst.write(PNratio.astype(rasterio.float32), 1)
    
print(f"Result saved to {output_file}")

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
with rasterio.open(output_file) as src:
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
target_data[target_data == 0] = np.nan

# Save the resampled data to a NetCDF file
with nc.Dataset(output_nc, 'w', format='NETCDF4') as ds:
    # Create dimensions
    ds.createDimension('latitude', len(lats))
    ds.createDimension('longitude', len(lons))

# Create variables
    latitudes = ds.createVariable('latitude', np.float32, ('latitude',))
    longitudes = ds.createVariable('longitude', np.float32, ('longitude',))
    variable = ds.createVariable('PNratio', np.float32, ('latitude', 'longitude'), fill_value=np.nan)

    # Assign metadata
    ds.description = "NetCDF representation of raster data resampled to a regular grid"
    ds.source = "Converted from GeoTIFF using Python"
    ds.crs = "EPSG:4326"  # CRS metadata

    latitudes.units = "degrees_north"
    longitudes.units = "degrees_east"
    variable.units = "-" 
    variable.long_name = "PNratio"

    # Write data
    latitudes[:] = -lats
    longitudes[:] = lons
    variable[:, :] = target_data

print(f"NetCDF file created: {output_nc}")