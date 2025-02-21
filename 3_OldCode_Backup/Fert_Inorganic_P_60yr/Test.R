options(repos = c(CRAN = "https://cloud.r-project.org/"))
Sys.setenv(GDAL_CONFIG = "/shared/legacyapps/gdal/gcc/64/3.4.1/bin/gdal-config")
Sys.setenv(GEOS_CONFIG = "/shared/legacyapps/geos/gcc/64/3.10.2/bin/geos-config")

install.packages("cshapes", lib = "/lustre/nobackup/WUR/ESG/zhou111/env/R/lib")
install.packages("terra", lib = "/lustre/nobackup/WUR/ESG/zhou111/env/R/lib")


library(sf, lib = "/lustre/nobackup/WUR/ESG/zhou111/env/R/lib")
library(cshapes, lib = "/lustre/nobackup/WUR/ESG/zhou111/env/R/lib")
df_national_bound_1 <- cshp(date = as.Date("1991-01-01"))
library(terra, lib.loc = "/lustre/nobackup/WUR/ESG/zhou111/env/R/lib")  


df_national_bound_1

# OR (if using sf package)
library(sf)
st_geometry(df_national_bound_1)  # View geometry information
plot(df_national_bound_1)
