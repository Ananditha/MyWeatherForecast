import xarray as xr
import numpy as np

# Create sample data
temperature = 15 + 8 * np.random.randn(2, 2)
lat = [45, 46]
lon = [7, 8]

# Create xarray dataset
ds = xr.Dataset(
    {
        "temperature": (["lat", "lon"], temperature)
    },
    coords={
        "lat": lat,
        "lon": lon
    }
)

# Save to NetCDF4 file
ds.to_netcdf("test_output.nc", engine="netcdf4")
print("✅ File written successfully.")

# Load it back
ds_loaded = xr.open_dataset("test_output.nc", engine="netcdf4")
print("📦 Dataset loaded from NetCDF file:")
print(ds_loaded)
