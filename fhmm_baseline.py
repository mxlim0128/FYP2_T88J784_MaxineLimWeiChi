from nilmtk import DataSet
from nilmtk.disaggregate import FHMMDisaggregator
from sklearn.metrics import mean_absolute_error
import pandas as pd

DATA_PATH = "data/processed/refit.h5"
BUILDING_ID = 1

print("Loading dataset...")
ds = DataSet(DATA_PATH)
elec = ds.buildings[BUILDING_ID].elec

print("Loading aggregate power...")
mains = elec.mains()

print("Inspecting submeters...")
meters = list(elec.submeters().meters)
for i, m in enumerate(meters):
    print(f"Meter {i}: {m.appliances}")

# REFIT House 1 → fridge is Meter 0
fridge_meter = meters[0]

# ---------- Train FHMM ----------
print("Training FHMM...")
fhmm = FHMMDisaggregator()
fhmm.train(elec.submeters())

# ---------- Disaggregate ----------
print("Running FHMM disaggregation...")
pred = fhmm.disaggregate_chunk(mains.power_series_all_data())

# Extract fridge prediction
fridge_pred = pred.iloc[:, 0]
fridge_true = fridge_meter.power_series_all_data()

# Align timestamps
fridge_true, fridge_pred = fridge_true.align(fridge_pred, join="inner")

# ---------- Metric ----------
mae = mean_absolute_error(fridge_true, fridge_pred)

print(f"FHMM MAE (Fridge): {mae:.3f}")

# Save results
pd.Series({"FHMM_MAE": mae}).to_csv("results/phase3/fhmm_results.csv")

print("FHMM baseline completed.")
ds.store.close()

