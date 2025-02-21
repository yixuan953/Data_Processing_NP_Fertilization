import os
import glob
import rasterio
import numpy as np
import xarray as xr

nutri_types = ["P2O5", "N"] # The others could be "K2O"
crop_types = ["Rice", "Soybean", "Wheat", "Maize"] # The dataset also contains other crop types (in total 13 major crop groups)
years = range(1961,2020) # Do not contains 2020

# Path of the original .tiff files
input_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/Fertilization/NPK_1960-2019/Cropland_Maps'
process_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Fertilization/Org_NPK_MainCrop'
tiff_files = glob.glob(os.path.join(input_path,'*.tiff'))

# Get the meta, lon, and lat from one example data
with rasterio.open(tiff_files[0]) as src_examp:
    meta = src_examp.meta
    lon = np.linspace(src_examp.bounds.left, src_examp.bounds.right, src_examp.width)
    lat = np.linspace(src_examp.bounds.top, src_examp.bounds.bottom, src_examp.height)

# Create an empty data array
data = np.empty((len(years), len(lat), len(lon)), dtype=np.float32)

# Read the value from each .tiff file, and save thme in .nc format
for crop in crop_types:
    for nutri in nutri_types:
        for year in years:
            f = os.path.join(input_path, f"{crop}_{nutri}_{year}.tiff")
            i = year-1961
            with rasterio.open(f) as src:
                arr = src.read(1)  # Convert to float
                arr[arr <= 0] = np.nan  # Replace 0 with NaN
                print("Mean:", np.nanmean(arr))
                data[i, :, :] = arr

        ds = xr.Dataset(
            {nutri: (["year", "lat", "lon"], data)},
            coords={"year": years, "lat": lat, "lon": lon}
        )

        output_nc = os.path.join(process_path, f"{crop}_{nutri}_1961-2019.nc")
        ds.to_netcdf(output_nc)    