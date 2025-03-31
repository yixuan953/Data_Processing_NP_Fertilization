# This code is used to: Calculate the annual N,P from residues [kg/ha harvested area] in study areas
# (output of wofost for past 30 years without water or nutrient limitations) 

import os
import pandas as pd
import xarray as xr
import numpy as np

StudyAreas = ["Yangtze"] # ["Rhine", "Yangtze", "LaPlata", "Indus"] 
crop_types = ["mainrice"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"] 
output_dir = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/NP_Fert_Res/"

for StudyArea in StudyAreas:
    for crop in crop_types:
        model_output = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-Nutrient/CaseStudy/{StudyArea}/Output/Annual_his_Yp/{StudyArea}_Yp_{crop}_Annual.csv"
        
        if not os.path.exists(model_output):
            print(f"File not found: {model_output}, skipping...")
            continue

        # Read CSV (pls be noticed that the "sep" of the header and values in output.c should be defined as the same)
        df = pd.read_csv(model_output)
        print(f"Processing {StudyArea} - {crop}")
        
        # Extract unique coordinate values
        lat = np.sort(df['Lat'].unique())
        lon = np.sort(df['Lon'].unique())
        years = np.sort(df['Year'].unique())
        print(f"Years range: {years.min()} to {years.max()}")
        print(f"Grid size: {len(lat)} latitudes × {len(lon)} longitudes")
        
        # Create empty arrays
        N_residue = np.full((len(years), len(lat), len(lon)), np.nan)
        P_residue = np.full((len(years), len(lat), len(lon)), np.nan)
        
        # Create dictionaries to map values to indices for faster lookup
        year_to_idx = {int(year): i for i, year in enumerate(years)}
        lat_to_idx = {value: i for i, value in enumerate(lat)}
        lon_to_idx = {value: i for i, value in enumerate(lon)}
        
        # Fill the arrays using the dictionaries for faster indexing
        for idx, row in df.iterrows():
            try:
                year_idx = year_to_idx[int(row['Year'])]
                lat_idx = lat_to_idx[row['Lat']]
                lon_idx = lon_to_idx[row['Lon']]
                
                N_residue[year_idx, lat_idx, lon_idx] = row['N_Residue']
                P_residue[year_idx, lat_idx, lon_idx] = row['P_Residue']
            except (KeyError, ValueError) as e:
                print(f"Warning at row {idx}: {e}")
                print(f"Row data: Year={row['Year']}, Lat={row['Lat']}, Lon={row['Lon']}")
        
        # Create an xarray Dataset
        ds = xr.Dataset(
            {
                'N_Residue': (['year', 'lat', 'lon'], N_residue),
                'P_Residue': (['year', 'lat', 'lon'], P_residue),
            },
            coords={
                'year': years,
                'lat': lat,
                'lon': lon,
            }
        )

        ds['N_Residue'].attrs['units'] = 'kg/ha'
        ds['P_Residue'].attrs['units'] = 'kg/ha'
        
        output_ncfile = os.path.join(output_dir, f"{StudyArea}_{crop}_Annual_his.nc")
        ds.to_netcdf(output_ncfile)
        print(f"{output_ncfile} has been created successfully!")