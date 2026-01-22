"""
Phase 3A – Seq2Point Preprocessing (Memory-safe)
Dataset: REFIT – House 1 – Fridge (SINGLE HOUSE)
"""

import os
import numpy as np
from nilmtk import DataSet

# ==============================
# Configuration
# ==============================
DATASET_PATH = "data/processed/refit.h5"
OUTPUT_DIR = "data/phase3"

HOUSE_IDS = [1]              # ✅ SINGLE HOUSE ONLY
APPLIANCE_INDEX = 0          # fridge
WINDOW_LENGTH = 599
MAX_SAMPLES = 300_000        # memory safety

# Global normalization constants (REFIT)
MAINS_MAX = 24000.0
MAINS_MIN = 0.0
APPLIANCE_MAX = 1466.0

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# Helper functions
# ==============================
def create_windows(aggregate, target, window):
    half = window // 2
    X, y = [], []

    for i in range(half, len(aggregate) - half):
        X.append(aggregate[i - half : i + half + 1])
        y.append(target[i])

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

# ==============================
# Main preprocessing
# ==============================
def main():
    print("📂 Loading dataset...")
    ds = DataSet(DATASET_PATH)

    for house_id in HOUSE_IDS:
        print(f"\n🏠 Processing House {house_id}")
        elec = ds.buildings[house_id].elec

        print("🔌 Loading aggregate power...")
        agg = elec.mains().power_series_all_data().dropna().values

        print("🔍 Inspecting submeters...")
        meters = list(elec.submeters().meters)
        for i, m in enumerate(meters):
            print(f"Meter {i}: {m.appliances}")

        target = meters[APPLIANCE_INDEX].power_series_all_data().dropna().values

        # Limit size
        min_len = min(len(agg), len(target), MAX_SAMPLES)
        agg = agg[:min_len]
        target = target[:min_len]

        # ✅ Global min–max normalization
        agg = (agg - MAINS_MIN) / (MAINS_MAX - MAINS_MIN)
        target = target / APPLIANCE_MAX

        print("🪟 Creating Seq2Point windows...")
        X, y = create_windows(agg, target, WINDOW_LENGTH)

        print("X shape:", X.shape)
        print("y shape:", y.shape)

        out_path = f"{OUTPUT_DIR}/house1_fridge_seq2point.npz"
        np.savez_compressed(out_path, X=X, y=y)

        print(f"✅ Saved {out_path}")

    ds.store.close()
    print("\n🎉 Preprocessing COMPLETE (House 1 only)")

if __name__ == "__main__":
    main()

