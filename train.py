import argparse
import yaml
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Import your model architecture
from src.models.seq2point import build_seq2point_model 
from nilmtk import DataSet 

# --- Data Loading Function ---
def load_and_preprocess_data(config):
    """
    Loads data directly from HDF5 file paths, applies normalization, 
    creates windows, and returns X_train_reshaped and y_train.
    """
    print("Loading and preprocessing data (Brute-Force Read)...")
    
    # --- Direct HDF5 Path Access (Bypassing problematic NILMTK objects) ---
    # NOTE: You found the correct paths: /building1/elec/meter1 and /building1/elec/meter2
    try:
        HDF_FILE = pd.HDFStore(config['data_path'])
        
        # 1. Load Mains (Aggregate) Data
        mains_path = '/building1/elec/meter1' # Correct path verified in terminal
        mains_power = HDF_FILE[mains_path].power['active'].rename('mains')
        
        # 2. Load Appliance (Fridge) Data
        fridge_path = '/building1/elec/meter2' # Correct path verified in terminal
        appliance_power = HDF_FILE[fridge_path].power['active'].rename('appliance')
        
        HDF_FILE.close() # Close the HDF5 file after reading!
        
    except Exception as e:
        print(f"FATAL ERROR: Could not read data from HDF5. {e}")
        return None, None
        
    # Align the timestamps, subset, and copy
    aligned_data = pd.concat([mains_power, appliance_power], axis=1, join='inner').head(500000).copy()
    aligned_data.columns = ['mains', 'appliance']

    # --- Apply Normalization ---
    MAINS_MAX = config['MAINS_MAX']
    MAINS_MIN = config['MAINS_MIN']
    APPLIANCE_MAX = config['APPLIANCE_MAX']
    
    aligned_data['mains_norm'] = (aligned_data['mains'] - MAINS_MIN) / (MAINS_MAX - MAINS_MIN)
    aligned_data['appliance_norm'] = aligned_data['appliance'] / APPLIANCE_MAX
    
    # --- Create Windows ---
    WINDOW_SIZE = config['window_size']
    num_samples = len(aligned_data) - WINDOW_SIZE
    
    X_train = np.zeros((num_samples, WINDOW_SIZE), dtype=np.float32)
    y_train = np.zeros(num_samples, dtype=np.float32)
    center_offset = WINDOW_SIZE // 2

    for i in range(num_samples):
        X_train[i, :] = aligned_data['mains_norm'].values[i : i + WINDOW_SIZE]
        y_train[i] = aligned_data['appliance_norm'].values[i + center_offset]
        
    X_train_reshaped = np.expand_dims(X_train, axis=-1)
    
    print(f"Data successfully loaded and windowed. X_train shape: {X_train_reshaped.shape}")
    return X_train_reshaped, y_train

# --- Main Training Function ---
def main(config):
    # --- STEP 1: Load and Preprocess Data ---
    X_train_reshaped, y_train = load_and_preprocess_data(config, mode="train")
    
    if X_train_reshaped is None:
        print("Training terminated due to data loading failure.")
        return
        
    # --- STEP 2: Build and Compile Model ---
    input_shape = (config['window_size'], 1)
    model = build_seq2point_model(input_shape)
    
    model.compile(
        optimizer='adam', 
        loss=config.get('loss_function', 'mean_absolute_error'),
        metrics=['mae']
    )
    print("Model built and compiled.")
    
    # --- STEP 3: Define Callbacks ---
    os.makedirs(config['checkpoint_dir'], exist_ok=True)
    checkpoint_callback = ModelCheckpoint(
        filepath=os.path.join(config['checkpoint_dir'], 'model.best.h5'), 
        save_best_only=True,
        monitor='val_mae',
        mode='min',
        verbose=1
    )
    early_stop = EarlyStopping(monitor='val_loss', patience=5)
    
    # --- STEP 4: Train Model ---
    print(f"Starting full training for {config['epochs']} epochs...")
    model.fit(
        X_train_reshaped,
        y_train,
        epochs=config['epochs'], 
        batch_size=config['batch_size'],
        validation_split=config['validation_split'],
        callbacks=[checkpoint_callback, early_stop],
        verbose=1
    )
    print("Training finished. Best weights saved.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train a NILM model.')
    parser.add_argument('--config', type=str, required=True, help='Path to YAML configuration file.')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # Run the main training function
    main(config)
