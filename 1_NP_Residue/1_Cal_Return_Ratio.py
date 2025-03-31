# This code is used to: Calculate the global cereal residue return ratio based on the data of Smerald et al.(2023) (https://www.nature.com/articles/s41597-023-02587-0)

import os
import pandas as pd
import xarray as xr
import numpy as np

input_file = "/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/Fertilization/Cereal_Res_Return_Ratio/crop_residue_usage_mean.nc"
output_dir = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/NP_Fert_Res"

ds_res = xr.open_dataset(input_file)

year = ds_res["time"].values
lat = ds_res["lat"].values
lon = ds_res["lon"].values

left_on_field = ds_res["left_on_field"][:]

residue_production = ds_res["residue_production"][:]
return_ratio = (left_on_field/residue_production)

# Create an xarray DataArray
a = xr.DataArray(
    return_ratio,
    dims=("year", "lat", "lon"),
    coords={
        "year": year,
        "lat": lat,
        "lon": lon,
        },
    attrs={
        "long_name": "Return ratio of cereals",
        "units": "-", 
        "description": "Return ratio is calculated by dividing residue_production amount by left_on_field amount (Smerald et al., 2023)"
        },
)
ds = xr.Dataset({"Return_Ratio": a})

output_ncfile = os.path.join(output_dir, f"Return_ratio_05d.nc")
ds.to_netcdf(output_ncfile)