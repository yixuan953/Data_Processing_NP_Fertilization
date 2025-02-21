# This code is used to: Calculate the fertilization input amount at 5arcmin

import rasterio
import numpy as np
import glob
import os

# Path for the .tiff file with the area per pixel
area_file = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/General/pixel_area_ha_5arcmin.tiff'
# Open the first TIFF
with rasterio.open(area_file) as src1:
    area_5arcmin = src1.read(1)  # Read first band
    meta = src1.meta  # Copy metadata

# Path the intermediate data
process_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Fertilization'

# Path for the original fertilization data
input_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/Fertilization/P_Inorganic_1961-2019'

tiff_files = glob.glob(os.path.join(input_path, '*.tiff'))

for tiff_file in tiff_files:

    with rasterio.open(tiff_file) as src2:
         Org_value = src2.read(1)  # Read first band

         # Ensure the shapes match
         if Org_value.shape != area_5arcmin.shape:
            raise ValueError("Input TIFF files must have the same dimensions!")
    
         print(f"Processing {tiff_file}")
         result = area_5arcmin * Org_value

         # Update metadata for output
         meta.update(dtype=rasterio.float32)
    
    filename = os.path.basename(tiff_file).replace(".tiff", "")
    output_name = os.path.join(process_path, f"{filename}.tiff")
    
    with rasterio.open(output_name, "w", **meta) as dst:
         dst.write(result.astype(rasterio.float32), 1) 
         print(f"Calculated results saved as {output_name}")