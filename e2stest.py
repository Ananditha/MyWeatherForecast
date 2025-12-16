import xarray as xr
import numpy as np
import sys

# Get selected city from Flask (argument)
if len(sys.argv) < 2:
    print("No city provided!")
    sys.exit(1)

selected_city = sys.argv[1]

# Sample .nc file path
file_path = "weather_7day_forecast.nc"

# Load the NetCDF dataset
ds = xr.open_dataset(file_path)
temperature = ds["t2m"]
times = temperature.time.values

# Define Asian cities and their coordinates
asian_cities = {
    "tokyo": (35.6762, 139.6503),
    "bangkok": (13.7563, 100.5018),
    "jakarta": (-6.2088, 106.8456),
    "manila": (14.5995, 120.9842),
    "seoul": (37.5665, 126.9780),
    "india": (20.5937, 78.9629),
    "singapore": (1.3521, 103.8198),
    "japan": (36.2048, 138.2529)
}


if selected_city not in asian_cities:
    print(f"City '{selected_city}' not recognized!")
    sys.exit(1)

lat, lon = asian_cities[selected_city]

# Find nearest lat/lon in the dataset grid
nearest_lat = float(ds.sel(lat=lat, method="nearest").lat)
nearest_lon = float(ds.sel(lon=lon, method="nearest").lon)

# Select temperature forecast at the nearest grid point
forecast_temps = temperature.sel(lat=nearest_lat, lon=nearest_lon).values

print(f"<h3 style='text-align:center;'>{selected_city} 7-Day Forecast</h3>")
print("<div style='display: flex; justify-content: center; margin-top: 10px;'>")
print("<table style='text-align: center;'>")
print("<tr><th>Date</th><th>Description</th><th>Temperature (°C)</th></tr>")

for i in range(min(7, len(times))):
    date_str = str(np.datetime_as_string(times[i], unit='D'))
    try:
        temp_c = float(forecast_temps[i].item() - 273.15)
    except Exception:
        temp_c = float(forecast_temps[i].flatten()[0] - 273.15)

    if temp_c < 10:
        desc = "cold and possibly cloudy"
    elif temp_c < 20:
        desc = "mild and pleasant"
    elif temp_c < 30:
        desc = "warm and moderately sunny"
    else:
        desc = "hot and sunny"

    print(f"<tr><td>{date_str}</td><td>{desc}</td><td>{round(temp_c)}</td></tr>")

print("</table>")
print("</div>")


