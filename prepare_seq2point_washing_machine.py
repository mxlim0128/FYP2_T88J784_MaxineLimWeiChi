"""
Phase 3 – Prepare Seq2Point Data (Washing Machine)
MEMORY-SAFE VERSION
"""

import numpy as np
from nilmtk import DataSet

# -----------------------------
# Configuration
# -----------------------------
DATA_PATH = "data/processed/refit.h5"
OUTPUT_PATH = "data/phase3/house1_washing_machine_seq2point.npz"

BUILDING_ID = 1
TARGET_NAME = "washing machine"

WINDOW_SIZE = 599
DOWNSAMPLE = "10S"          # 10-second sampling
MAX_WINDOWS = 200000       # cap number of samples

AGG_MAX = 5000.0
APP_MAX = 2500.0

# -----------------------------
# Load dataset
# -----------------------------
print("Loading dataset...")
ds = DataSet(DATA_PATH)
elec = ds.buildings[BUILDING_ID].elec

# -----------------------------
# Load & downsample aggregate
# -----------------------------
print("Loading aggregate power...")
aggregate = elec.mains().power_series_all_data().dropna()
aggregate = aggregate.resample(DOWNSAMPLE).mean().dropna()

# -----------------------------
# Find washing machine submeter
# -----------------------------
print("Finding washing machine submeter...")
washing_machine_meter = None

for i, meter in enumerate(elec.submeters().meters):
    for appliance in meter.appliances:
        if TARGET_NAME in str(appliance.type).lower():
            washing_machine_meter = meter
            print(f"✔ Found washing machine at meter {i}")
            break
    if washing_machine_meter is not None:
        break

if washing_machine_meter is None:
    ds.store.close()
    raise RuntimeError("Washing machine not found!")

# -----------------------------
# Load & downsample appliance
# -----------------------------
print("Loading washing machine power...")
appliance = washing_machine_meter.power_series_all_data().dropna()
appliance = appliance.resample(DOWNSAMPLE).mean().dropna()

# -----------------------------
# Align timestamps
# -----------------------------
aggregate, appliance = aggregate.align(appliance, join="inner")

# -----------------------------
# Create sliding windows (LIMITED)
# -----------------------------
print("Creating sliding windows...")
half = WINDOW_SIZE // 2
X, y = [], []

for i in range(half, len(aggregate) - half):
    X.append(aggregate.iloc[i - half : i + half + 1].values)
    y.append(appliance.iloc[i])

    if len(X) >= MAX_WINDOWS:
        break

X = np.array(X, dtype=np.float32) / AGG_MAX
y = np.array(y, dtype=np.float32) / APP_MAX

# -----------------------------
# Save data
# -----------------------------
np.savez(OUTPUT_PATH, X=X, y=y)
print(f"Saved {len(X)} windows to:", OUTPUT_PATH)

ds.store.close()

