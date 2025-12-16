# seven_day_forecast_console.py
import os, sys, math
import xarray as xr
import sys; print("RUNNING WITH:", sys.executable)
import numpy, xarray, cfgrib
print("OK numpy", numpy.__version__)
print("OK xarray", xarray.__version__)
print("OK cfgrib", cfgrib.__version__)
import earth2studio as e2s
print("OK earth2studio", e2s.__version__)



from earth2studio.models.px import DLWP
from earth2studio.data import GFS
from earth2studio.io import NetCDF4Backend
from earth2studio.run import deterministic

START_DATE = "2025-08-15"   # change if you want
DAYS       = 7
OUT_DIR    = "output"
OUT_NC     = os.path.join(OUT_DIR, "forecast_7day.nc")

ENGINES_TO_TRY = ["netcdf4", "h5netcdf", "zarr", "store"]  # supported by downloader

def init_gfs():
    last_err = None
    for eng in ENGINES_TO_TRY:
        try:
            print(f"Trying GFS(engine='{eng}') …")
            return GFS(engine=eng), eng
        except TypeError:
            # older builds might not accept engine kwarg at all
            print("  engine kw not supported; falling back to default GFS()")
            return GFS(), "default"
        except Exception as e:
            print(f"  failed with engine='{eng}': {e}")
            last_err = e
    raise RuntimeError(f"All GFS engines failed. Last error: {last_err}")

def main():
    print("RUNNING WITH:", sys.executable)
    os.makedirs(OUT_DIR, exist_ok=True)

    # Load model & dataset
    model = DLWP.load_model(DLWP.load_default_package())
    print("✅ DLWP model loaded.")
    gfs, used_engine = init_gfs()
    print(f"✅ GFS data source ready (engine={used_engine}).")

    # DLWP cadence is typically 6h → 4 steps/day
    step_hours = getattr(model, "step_hours", 6)
    steps = math.ceil(DAYS * 24 / step_hours)

    io = NetCDF4Backend(OUT_NC)
    print(f"➡️  Running forecast: start={START_DATE}, steps={steps} @ {step_hours}h/step")
    # IMPORTANT: 0.8.1 expects positional args: (start_times, steps, model, data, io)
    deterministic([START_DATE], steps, model, gfs, io)
    print(f"💾 Saved: {OUT_NC}")

    # Summarize
    ds = xr.open_dataset(OUT_NC)
    print("\n=== FORECAST SUMMARY ===")
    print("Vars:", list(ds.data_vars))
    print("Dims:", {k: int(v) for k, v in ds.dims.items()})
    for cand in ("time", "valid_time", "forecast_time", "step"):
        if (cand in ds.coords) or (cand in ds.dims):
            vals = ds[cand].values
            if len(vals):
                print("First:", str(vals[0]), "Last:", str(vals[-1]))
            break
    print("✅ Done.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n❗ Run failed:", e)
        print("Tips:")
        print(" - Ensure your Run config uses the conda env python:")
        print("   ~/miniconda3/envs/earth2/bin/python")
        print(" - If GFS download fails, try a different START_DATE or rerun (network hiccups).")
