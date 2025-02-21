# This code is used to: rename the .nc files

import shutil
import os

source_folder = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/N_Manure_Input'
destination_folder = 'C:/Users/zhou111/OneDrive - Wageningen University & Research/2_Data/NP_Input/Processed_data/Manure_NP_Input'

# Loop over all .nc files in the source folder
for nc_file in os.listdir(source_folder):
    
    if nc_file.endswith('.nc'):  # Check if the file has a .nc extension
        source_path = os.path.join(source_folder, nc_file)
        
        # Split the file name by underscores and get the part you want (assuming 'Barley' is between the underscores)
        file_parts = nc_file.split('_')
        
        # Modify the file name as needed (for example, add a prefix or suffix)
        new_file_name = 'Manure_NP_1961-2020_' + file_parts[3]
        destination_path = os.path.join(destination_folder, new_file_name)
        
        # Copy the file to the destination folder with the new name
        shutil.copy(source_path, destination_path)

        print(f"Copied and renamed {nc_file} to {new_file_name}")