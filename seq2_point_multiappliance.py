"""
Prepare Seq2Point Data (MULTI-APPLIANCE)
Kettle + Toaster + Laptop + Lamp
MULTI-HOUSE (1–21) + MEMORY-SAFE VERSION
"""

import numpy as np
from nilmtk import DataSet
import os

# -----------------------------
# Configuration
# -----------------------------
DATA_PATH = "data/processed/refit.h5"
OUTPUT_DIR = "data/phase3"

WINDOW_SIZE = 599
DOWNSAMPLE = "10s"
MAX_WINDOWS = 200000

AGG_MAX = 5000.0

# Appliance normalization
APP_CONFIG = {
    "kettle": 3000.0,
    "toaster": 2000.0,
    "computer": 500.0,   # laptop
    "lamp": 200.0        # lighting
}

# Name matching (REFIT is inconsistent)
TARGET_APPLIANCES = {
    "kettle": ["kettle"],
    "toaster": ["toaster"],
    "computer": ["computer", "laptop"],
    "lamp": ["lamp", "light", "lighting"]
}

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Load dataset
# -----------------------------
print("Loading dataset...")
ds = DataSet(DATA_PATH)

# -----------------------------
# Process houses 1–21
# -----------------------------
for BUILDING_ID in range(1, 22):   # includes house 21

    print(f"\nProcessing house {BUILDING_ID}...")

    try:
        elec = ds.buildings[BUILDING_ID].elec

        # -----------------------------
        # Aggregate (mains)
        # -----------------------------
        aggregate = elec.mains().power_series_all_data().dropna()
        aggregate = aggregate.resample(DOWNSAMPLE).mean().dropna()

        # -----------------------------
        # Loop appliances
        # -----------------------------
        for app_name, keywords in TARGET_APPLIANCES.items():

            print(f"\n➡ Searching for {app_name}...")

            target_meter = None

            # Find matching appliance
            for meter in elec.submeters().meters:
                for appliance_obj in meter.appliances:
                    label = str(appliance_obj.type).lower()

                    if any(k in label for k in keywords):
                        target_meter = meter
                        break
                if target_meter is not None:
                    break

            # Skip if not found
            if target_meter is None:
                print(f"{app_name} not found in house {BUILDING_ID}")
                continue

            print(f"✔ {app_name} found")

            # -----------------------------
            # Appliance data
            # -----------------------------
            appliance = target_meter.power_series_all_data().dropna()
            appliance = appliance.resample(DOWNSAMPLE).mean().dropna()

            # Align aggregate & appliance
            agg_aligned, app_aligned = aggregate.align(appliance, join="inner")

            # Skip if too short
            if len(agg_aligned) < WINDOW_SIZE:
                print(f"Not enough data for {app_name}")
                continue

            # -----------------------------
            # Windowing
            # -----------------------------
            half = WINDOW_SIZE // 2
            X, y = [], []

            for i in range(half, len(agg_aligned) - half):
                X.append(agg_aligned.iloc[i-half:i+half+1].values)
                y.append(app_aligned.iloc[i])

                if len(X) >= MAX_WINDOWS:
                    break

            if len(X) == 0:
                print(f" No samples for {app_name}")
                continue

            # -----------------------------
            # Normalization
            # -----------------------------
            X = np.array(X, dtype=np.float32) / AGG_MAX
            y = np.array(y, dtype=np.float32) / APP_CONFIG[app_name]

            # -----------------------------
            # Save NPZ
            # -----------------------------
            output_file = f"{OUTPUT_DIR}/house{BUILDING_ID}_{app_name}_seq2point.npz"
            np.savez_compressed(output_file, X=X, y=y)

            print(f"Saved {len(X)} samples → {output_file}")

    except Exception as e:
        print(f"Error in house {BUILDING_ID}: {e}")

# -----------------------------
# Close dataset
# -----------------------------
ds.store.close()

print("\n ALL houses (1–21) processed successfully!")
