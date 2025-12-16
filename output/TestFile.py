import sys
print("RUNNING WITH:", sys.executable)

import xarray as xr
import matplotlib.pyplot as plt

# Open the NetCDF file
ds = xr.open_dataset("weather_7day_forecast.nc")

# Print available variables (e.g., 't2m' for 2-meter temperature)
print(ds.data_vars)

# Access predicted temperature
t2m = ds["t2m"]  # '2 meter temperature'

# See dimensions
print(t2m.dims)  # Likely ('time', 'lat', 'lon')

# View data at time step 0 (initial forecast)
print(t2m[0])  # or t2m[0].values to see raw data






