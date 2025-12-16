# Import the needed modules from Earth2Studio
import os, sys
import earth2studio
from earth2studio.models.px import DLWP
from earth2studio.data import GFS
from earth2studio.io import NetCDF4Backend
from earth2studio.run import deterministic as run
import xarray as xr


BASE_DIR = os.path.dirname(os.path.abspath(__file__))




print("RUNNING WITH:", sys.executable)
print(earth2studio.__version__)
print("BASE_DIR",BASE_DIR)
# Load the pre-trained DLWP model
model = DLWP.load_model(DLWP.load_default_package())

# Specify the input atmospheric data source (GFS is commonly used)
ds = GFS()

# Set up the output backend (NetCDF format)
io = NetCDF4Backend("weather_7day_forecast.nc",backend_kwargs={"mode": "w"})

# Pick your desired start date as a string in 'YYYY-MM-DD' format
start_date = "2025-09-24"

# Number of steps: DLWP predicts in 6-hour increments
# 7 days = 7 * 4 = 28 time steps of 6 hours each
nsteps = 28

# Run the inference
run([start_date], nsteps, model, ds, io)
ds = xr.open_dataset("weather_7day_forecast.nc")
print(ds)

print("7-day weather forecast completed! Results stored in 'weather_7day_forecast.nc'")
