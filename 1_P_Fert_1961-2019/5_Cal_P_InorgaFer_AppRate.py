import numpy as np
import os
import xarray as xr

crop_types = ["Rice", "Soybean", "Wheat", "Maize"] # The dataset also contains other crop types (in total 13 major crop groups)
fertilizer_types = ["P", "P2O5"]

Amount_path = '/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/P_Fert_Inorg_1961-2019/P_Inorg_Amount_05d'
HA_path = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/P_Fert_Inorg_1961-2019/HA_05d"
output_path = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/P_Fert_Inorg_1961-2019/P_Inorg_AppRate_05d"

for crop in crop_types:

    ha_nc = f"{HA_path}/{crop}_HA_05d_1961-2019.nc"
    ds_ha = xr.open_dataset(ha_nc)
    Harvest_area = ds_ha["HA"]
    years = ds_ha.coords["year"]
    lon = ds_ha.coords["lon"]
    lat = ds_ha.coords["lat"]

    for fert in fertilizer_types:

        fert_nc = f"{Amount_path}/{crop}_{fert}_1961-2019.nc"
        ds_fert = xr.open_dataset(fert_nc)
        if fert == "P":
            var_name = "P2O5"
        else:
            var_name = fert
        fert_amount = ds_fert[var_name]

        app_rate = fert_amount/Harvest_area
        # Residue fertilzer
        app_rate_dataset = xr.DataArray(
            app_rate,
            dims=("year", "lat", "lon"),
            coords={
                "year": years,
                "lon": lon,
                "lat": lat,
                    },
            name = f"{fert}_application_rate",
            attrs={
                   "units": "kg/ha harvest area"
                   }
                )  
        
        output_nc = os.path.join(output_path, f"{crop}_{fert}_AppRate_1961-2019.nc")
        app_rate_dataset.to_netcdf(output_nc)
        print (f"{fert} application rate for {crop} has been calculated and saved")