# This code is used to: 
# 1. Calculate the average N,P from residues (output of wofost for past 30 years without water or nutrient limitations) [kg/ha harvested area]
# 2. Calculate the initial residual input (N, P from residues * return ratio)

import os
import pandas as pd
import xarray as xr
import numpy as np

StudyAreas = ["Rhine", "Yangtze", "LaPlata", "Indus"] # ["Rhine", "Yangtze", "LaPlata", "Indus"] 
crop_types = ["maize","mainrice","secondrice","soybean","winterwheat"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"] 
output_dir = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/NP_Fert_Res_wofost"

for StudyArea in StudyAreas:
    for crop in crop_types:
        # Read the output .csv file
        model_output = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-Nutrient/CaseStudy/{StudyArea}/Output/Annual_his_Yp/{StudyArea}_Yp_{crop}_Annual.csv"

        if not os.path.exists(model_output):
            print(f"File not found: {model_output}, skipping...")
        continue

    df = pd.read_csv(model_output)

    # Calculate the average N, P 
    avg_residue = df.groupby(['Lat', 'Lon'])['N_Residue', 'P_Residue'].mean().reset_index()

    lat = np.unique(avg_residue['Lat'])
    lon = np.unique(avg_residue['Lon'])

    # Create empty arrays for the variables we want to save
    N_Residue = np.full((len(lat), len(lon)), np.nan)
    P_Residue = np.full((len(lat), len(lon)), np.nan)

    for idx, row in avg_residue.iterrows():
        lat_idx = np.where(lat == row['Lat'])[0][0]
        lon_idx = np.where(lon == row['Lon'])[0][0]
            
        N_Residue[lat_idx, lon_idx] = row['N_Residue']
        P_Residue[lat_idx, lon_idx] = row['P_Residue']

        # Create an xarray Dataset
        ds = xr.Dataset(
            {
                'N_Residue': (['lat', 'lon'], N_Residue),
                'P_Residue': (['lat', 'lon'], P_Residue),
            },
            coords={
                'lat': lat,
                'lon': lon,
            }
        )

        ds['N_Residue'].attrs['units'] = 'kg/ha'
        ds['P_Residue'].attrs['units'] = 'kg/ha'
    
        output_ncfile = os.path.join(output_dir, f"{StudyArea}_{crop}_NPinRes_his.nc")
        # Save the Dataset to a NetCDF file
        ds.to_netcdf(output_ncfile)

        print(f"{output_ncfile} has been created")
    