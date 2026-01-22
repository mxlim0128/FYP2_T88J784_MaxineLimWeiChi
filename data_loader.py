# file: src/data/data_loader.py
# FINAL shared data loading & preprocessing logic

import pandas as pd
import numpy as np


def load_and_preprocess_data(config, mode="train"):
    """
    Loads REFIT data from HDF5, applies normalization,
    creates sliding windows, and returns X, y.
    
    mode = "train" or "test"
    """

    print(f"Loading and preprocessing data (mode={mode})...")

    # --- Select buildings ---
    if mode == "train":
        buildings = config['train_buildings'] + [config['validation_building']]
    elif mode == "test":
        buildings = config['test_buildings']
    else:
        raise ValueError("mode must be 'train' or 'test'")

    # --- Open HDF5 ---
    HDF_FILE = pd.HDFStore(config['data_path'])

    all_X = []
    all_y = []

    for b in buildings:
        print(f"Processing building {b}")

        mains_path = f"/building{b}/elec/meter1"
        appliance_path = f"/building{b}/elec/meter2"

        mains_power = HDF_FILE[mains_path].power['active'].rename('mains')
        appliance_power = HDF_FILE[appliance_path].power['active'].rename('appliance')

        # Align timestamps
        data = pd.concat(
            [mains_power, appliance_power],
            axis=1,
            join="inner"
        ).dropna()

        # Optional downsampling for speed
        if config.get("max_samples"):
            data = data.head(config["max_samples"])

        # --- Normalization ---
        data['mains_norm'] = (
            data['mains'] - config['MAINS_MIN']
        ) / (config['MAINS_MAX'] - config['MAINS_MIN'])

        data['appliance_norm'] = (
            data['appliance'] / config['APPLIANCE_MAX']
        )

        # --- Windowing (Seq2Point) ---
        WINDOW_SIZE = config['window_size']
        center_offset = WINDOW_SIZE // 2
        num_samples = len(data) - WINDOW_SIZE

        X = np.zeros((num_samples, WINDOW_SIZE), dtype=np.float32)
        y = np.zeros(num_samples, dtype=np.float32)

        for i in range(num_samples):
            X[i, :] = data['mains_norm'].values[i:i + WINDOW_SIZE]
            y[i] = data['appliance_norm'].values[i + center_offset]

        X = np.expand_dims(X, axis=-1)

        all_X.append(X)
        all_y.append(y)

    HDF_FILE.close()

    X_final = np.concatenate(all_X, axis=0)
    y_final = np.concatenate(all_y, axis=0)

    print(f"Final dataset shape: X={X_final.shape}, y={y_final.shape}")
    return X_final, y_final

