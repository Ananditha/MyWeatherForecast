import xarray as xr
import numpy as np

# Load the NetCDF file
ds = xr.open_dataset("weather_7day_forecast.nc")

# Extract temperature and water vapor
temperature = ds["t2m"] - 273.15  # Convert from Kelvin to Celsius
water_vapor = ds["tcwv"]  # Water vapor
times = ds["time"].values

# Human-readable descriptions
def describe_temperature(temp_c):
    if temp_c >= 35:
        return "very hot"
    elif temp_c >= 30:
        return "hot"
    elif temp_c >= 20:
        return "warm"
    elif temp_c >= 10:
        return "cool"
    else:
        return "cold"

def describe_humidity(tcwv_val):
    if tcwv_val < 5:
        return "dry"
    elif tcwv_val < 20:
        return "moderate humidity"
    else:
        return "humid and possible clouds"

# Generate forecast summaries
print("\n📢 AI Weather Forecast Summary:\n" + "-" * 40)

for i in range(len(times)):
    time_str = np.datetime_as_string(times[i], unit='h')
    temp_c = float(temperature[i].mean().values)
    tcwv_val = float(water_vapor[i].mean().values)

    forecast = (
        f"{time_str}: {describe_temperature(temp_c)}, "
        f"{describe_humidity(tcwv_val)} (~{round(temp_c)}°C)"
    )
    print(forecast)
