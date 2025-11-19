# This code is used to create the annual N, P residue input based on the global cereal crops' return ratio and residue N, P amount calculated by wofost
import os
import xarray as xr
import numpy as np


input_file1 = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/NP_Fert_Res/Return_ratio_05d.nc" # The global return ratio
output_dir = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/NP_Fert_Res"

StudyAreas = ["Yangtze"] # ["Rhine", "Yangtze", "LaPlata", "Indus"] 
crop_types = ["maize","mainrice","secondrice","soybean","winterwheat"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"] 

for StudyArea in StudyAreas:
    for crop in crop_types:
        input_file2 = f"/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/NP_Fert_Res/{StudyArea}_{crop}_Annual_his.nc"
        
        if not os.path.exists(input_file2):
            print(f"File not found: {input_file2}, skipping...")
            continue

        ds1 = xr.open_dataset(input_file1)
        ds2 = xr.open_dataset(input_file2)

        # Rename variable in ds1 for clarity
        ds1_subset = ds1.sel(lat=slice(ds2.lat.min(), ds2.lat.max()), lon=slice(ds2.lon.min(), ds2.lon.max()))

        # Find common years
        common_years = np.intersect1d(ds1_subset.year, ds2.year)

        # Select common years from both datasets
        ds1_common = ds1_subset.sel(year=common_years)
        ds2_common = ds2.sel(year=common_years)

        # Perform element-wise multiplication for N_Residue and P_Residue
        N_Res_Input = ds1_common["Return_Ratio"] * ds2_common["N_Residue"]
        P_Res_Input = ds1_common["Return_Ratio"] * ds2_common["P_Residue"]

        # Save results to a new NetCDF file

        result_ds = xr.Dataset(
            {
            "N_Res_Input": (["year", "lat", "lon"], N_Res_Input.data),
            "P_Res_Input": (["year", "lat", "lon"], P_Res_Input.data)
            }, 
            coords={"year": common_years, "lat": ds2.lat, "lon": ds2.lon}
        )

        result_ds['N_Res_Input'].attrs['units'] = 'kg/ha'
        result_ds['P_Res_Input'].attrs['units'] = 'kg/ha'

        output_ncfile = os.path.join(output_dir, f"{StudyArea}_{crop}_Res_NP_1997-2016.nc")
        result_ds.to_netcdf(output_ncfile)
        
        print(f"Saved result to {output_ncfile}")